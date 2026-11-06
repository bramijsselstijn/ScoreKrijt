#!/usr/bin/env bash
# sk-update.sh - ScoreKrijt op de SK-Box bijwerken vanaf een USB-stick, zonder internet.
#
# Gebruik (als gewone gebruiker, dus niet met sudo):
#   bash sk-update.sh                    zoekt de USB-stick en werkt het programma bij
#   bash sk-update.sh /pad/naar/map      gebruikt die map als bron in plaats van de USB-stick
#   bash sk-update.sh --terug            zet de vorige versie terug
#   bash sk-update.sh --bluetooth        alleen opnieuw koppelen toestaan (zonder USB-stick)
# Opties:
#   --ja               geen bevestiging vragen
#   --geen-herstart    de SK-Box niet opnieuw opstarten
#   --help             deze uitleg tonen
#
# De USB-stick moet een map "ScoreKrijt_update" hebben met daarin:
#   ScoreKrijt (map), ScoreKrijt.py en scorekrijt_launcher.py
# Instellingen (ScoreKrijtSettings.json) en wedstrijden (map matches) blijven behouden.
# De vorige versie blijft bewaard als ScoreKrijt_vorige_<nummer>_<datum>.
# Bij een update zet het script ook Bluetooth zo dat de SK-Box een telefoon opnieuw
# accepteert nadat de SK-Box op de telefoon is vergeten (JustWorksRepairing = always in
# /etc/bluetooth/main.conf). Een kopie van het origineel blijft bewaard als main.conf.sk-origineel.

set -u

PROGRAMMA="${SK_PROGRAMMA:-$HOME/ScoreKrijt}"
STICKMAP="ScoreKrijt_update"
MOUNTPUNT="/mnt/sk-usb"
NIEUW="${PROGRAMMA}_nieuw"

MODUS="update"
BRON_ARG=""
JA=0
HERSTART=1
STICK_DOEL=""
STICK_ZELF_GEMOUNT=0

info()  { printf '%s\n' "$*"; }
stap()  { printf '\n==> %s\n' "$*"; }
fout()  { printf '\nFOUT: %s\n' "$*" >&2; exit 1; }

uitleg() { sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'; }

for arg in "$@"; do
  case "$arg" in
    --terug)         MODUS="terug" ;;
    --bluetooth)     MODUS="bluetooth" ;;
    --ja)            JA=1 ;;
    --geen-herstart) HERSTART=0 ;;
    --help|-h)       uitleg; exit 0 ;;
    -*)              fout "Onbekende optie: $arg (zie --help)" ;;
    *)               BRON_ARG="$arg" ;;
  esac
done

[ "$(id -u)" -eq 0 ] && fout "Voer dit script uit als gewone gebruiker, niet met sudo. Het vraagt zelf om sudo waar dat nodig is."

PY=""
for kandidaat in python3 python; do
  if command -v "$kandidaat" >/dev/null 2>&1 && "$kandidaat" -c 'import ast' >/dev/null 2>&1; then
    PY="$kandidaat"
    break
  fi
done

ja_nee() {
  [ "$JA" -eq 1 ] && return 0
  local antw
  read -r -p "$1 [j/N] " antw || return 1
  case "$antw" in j|J|y|Y|ja|Ja|JA) return 0 ;; *) return 1 ;; esac
}

stop_scorekrijt() {
  if command -v pkill >/dev/null 2>&1; then
    pkill -f scorekrijt_launcher.py 2>/dev/null
    pkill -f 'ScoreKrijt\.py' 2>/dev/null
    sleep 1
  fi
}

# Maakt de USB-stick los (als die door dit script of een automount is gekoppeld).
maak_stick_los() {
  [ -n "$STICK_DOEL" ] || return 0
  cd / || true
  sync
  if sudo umount "$STICK_DOEL" 2>/dev/null; then
    info "USB-stick is losgekoppeld. Je kunt hem nu veilig verwijderen."
  else
    info "Let op: de USB-stick kon niet worden losgekoppeld. Wacht even en verwijder hem pas na 'sudo umount $STICK_DOEL'."
  fi
  STICK_DOEL=""
}

ruim_op() {
  if [ "$STICK_ZELF_GEMOUNT" -eq 1 ] && [ -n "$STICK_DOEL" ]; then
    cd / || true
    sync
    sudo umount "$STICK_DOEL" 2>/dev/null
  fi
}
trap ruim_op EXIT

versie_van() {
  local f="$1/ScoreKrijt/constants.py"
  if [ -f "$f" ]; then
    sed -n 's/^APP_VERSION *= *["'\'']\([^"'\'']*\)["'\''].*/\1/p' "$f" | head -n1
  fi
}

# Geeft de map met de nieuwe versie terug als $1 of $1/ScoreKrijt_update die bevat.
zoek_bron() {
  local m
  for m in "$1/$STICKMAP" "$1"; do
    if [ -f "$m/ScoreKrijt.py" ] && [ -f "$m/scorekrijt_launcher.py" ] && [ -d "$m/ScoreKrijt" ]; then
      printf '%s\n' "$m"
      return 0
    fi
  done
  return 1
}

# Geeft de apparaten van aangesloten USB-opslag, behalve de schijf waar het systeem op staat.
usb_apparaten() {
  local rootbron rootschijf schijf naam delen d
  rootbron="$(findmnt -n -o SOURCE / 2>/dev/null)"
  rootschijf="$(lsblk -no PKNAME "$rootbron" 2>/dev/null | head -n1)"
  for schijf in /sys/block/sd*; do
    [ -e "$schijf" ] || continue
    naam="$(basename "$schijf")"
    readlink -f "$schijf" | grep -q '/usb' || continue
    [ "$naam" = "$rootschijf" ] && continue
    delen="$(ls -d /dev/"${naam}"[0-9]* 2>/dev/null)"
    [ -z "$delen" ] && delen="/dev/$naam"
    for d in $delen; do printf '%s\n' "$d"; done
  done
}

# Zet BRON en STICK_DOEL.
vind_bron() {
  BRON=""
  if [ -n "$BRON_ARG" ]; then
    BRON="$(zoek_bron "$BRON_ARG")" || fout "In '$BRON_ARG' staan niet de bestanden ScoreKrijt, ScoreKrijt.py en scorekrijt_launcher.py."
    return 0
  fi

  local dev doel gemount gevonden=0
  for dev in $(usb_apparaten); do
    gevonden=1
    gemount=0
    doel="$(findmnt -n -o TARGET --source "$dev" 2>/dev/null | head -n1)"
    if [ -z "$doel" ]; then
      sudo mkdir -p "$MOUNTPUNT" || continue
      if sudo mount -o ro "$dev" "$MOUNTPUNT" 2>/dev/null; then
        doel="$MOUNTPUNT"
        gemount=1
      else
        continue
      fi
    fi
    if BRON="$(zoek_bron "$doel")"; then
      STICK_DOEL="$doel"
      STICK_ZELF_GEMOUNT="$gemount"
      info "USB-stick gevonden: $dev (gekoppeld op $doel)"
      return 0
    fi
    [ "$gemount" -eq 1 ] && sudo umount "$doel" 2>/dev/null
  done

  if [ "$gevonden" -eq 0 ]; then
    fout "Geen USB-stick gevonden. Steek de stick in, wacht enkele seconden en probeer opnieuw."
  fi
  fout "Op de USB-stick staat geen map '$STICKMAP' met ScoreKrijt, ScoreKrijt.py en scorekrijt_launcher.py."
}

volgend_nummer() {
  local hoogste=0 n d
  for d in "${PROGRAMMA}"_vorige_*; do
    [ -d "$d" ] || continue
    n="${d##*_vorige_}"
    n="${n%%_*}"
    case "$n" in ''|*[!0-9]*) continue ;; esac
    n=$((10#$n))
    [ "$n" -gt "$hoogste" ] && hoogste="$n"
  done
  printf '%03d' $((hoogste + 1))
}

hoogste_vorige() {
  local best="" bestnr=-1 n d
  for d in "${PROGRAMMA}"_vorige_*; do
    [ -d "$d" ] || continue
    n="${d##*_vorige_}"
    n="${n%%_*}"
    case "$n" in ''|*[!0-9]*) continue ;; esac
    n=$((10#$n))
    if [ "$n" -gt "$bestnr" ]; then bestnr="$n"; best="$d"; fi
  done
  [ -n "$best" ] && printf '%s\n' "$best"
}

herstart() {
  if [ "$HERSTART" -eq 1 ]; then
    info ""
    info "De SK-Box start over 10 seconden opnieuw op. Druk op Ctrl+C om dat te annuleren."
    sleep 10
    sudo reboot
  else
    info ""
    info "Klaar. Start de SK-Box opnieuw op met 'sudo reboot' om de nieuwe versie te gebruiken."
  fi
}

installeer_scripts() {
  local naam
  for naam in sk-update.sh sk-stille-opstart.sh; do
    if [ -f "$1/$naam" ] && ! cmp -s "$1/$naam" "$HOME/$naam" 2>/dev/null; then
      if cp "$1/$naam" "$HOME/.$naam.nieuw" && chmod +x "$HOME/.$naam.nieuw" && mv -f "$HOME/.$naam.nieuw" "$HOME/$naam"; then
        info "Hulpscript bijgewerkt: ~/$naam"
      fi
    fi
  done
}

# Zorgt dat de SK-Box een telefoon opnieuw accepteert na "Vergeet" in de Bluetooth-instellingen
# van de telefoon. BlueZ weigert dat standaard (JustWorksRepairing = never).
# $1 = 1: Bluetooth meteen opnieuw starten (anders gebeurt dat bij de herstart).
BT_CONF="/etc/bluetooth/main.conf"
herstel_bluetooth() {
  local herstart_bt="${1:-0}" gewijzigd=0
  if [ ! -f "$BT_CONF" ]; then
    info "Bluetooth-configuratie niet gevonden ($BT_CONF); overgeslagen."
    return 0
  fi
  if grep -qE '^[[:space:]]*JustWorksRepairing[[:space:]]*=[[:space:]]*always' "$BT_CONF"; then
    info "Opnieuw koppelen stond al aan."
  else
    [ -f "$BT_CONF.sk-origineel" ] || sudo cp -p "$BT_CONF" "$BT_CONF.sk-origineel"
    if grep -qE '^[#[:space:]]*JustWorksRepairing' "$BT_CONF"; then
      sudo sed -i -E 's/^[#[:space:]]*JustWorksRepairing.*/JustWorksRepairing = always/' "$BT_CONF"
    else
      sudo sed -i '/^\[General\]/a JustWorksRepairing = always' "$BT_CONF"
    fi
    if grep -qE '^[[:space:]]*JustWorksRepairing[[:space:]]*=[[:space:]]*always' "$BT_CONF"; then
      info "Opnieuw koppelen toegestaan (JustWorksRepairing = always)."
      gewijzigd=1
    else
      info "Let op: de instelling kon niet worden gezet. Voeg 'JustWorksRepairing = always' met de hand toe onder [General] in $BT_CONF."
      return 0
    fi
  fi
  if [ "$herstart_bt" -eq 1 ] && [ "$gewijzigd" -eq 1 ]; then
    sudo systemctl restart bluetooth && info "Bluetooth is opnieuw gestart."
  fi
  return 0
}

doe_update() {
  [ -f "$PROGRAMMA/ScoreKrijt.py" ] || fout "Geen bestaande installatie gevonden in $PROGRAMMA. Voor een eerste installatie: zie de installatiehandleiding."

  stap "Nieuwe versie zoeken"
  vind_bron
  local huidige nieuwe
  huidige="$(versie_van "$PROGRAMMA")"; huidige="${huidige:-onbekend (ouder dan 2.8.5)}"
  nieuwe="$(versie_van "$BRON")";       nieuwe="${nieuwe:-onbekend}"
  info "Bron:                $BRON"
  info "Huidige versie:      $huidige"
  info "Nieuwe versie:       $nieuwe"
  if [ "$huidige" = "$nieuwe" ]; then
    info "De nieuwe versie is gelijk aan de huidige versie."
  fi
  ja_nee "Doorgaan met bijwerken? ScoreKrijt wordt gestopt en de SK-Box start opnieuw op." || { info "Afgebroken. Er is niets gewijzigd."; exit 0; }

  stap "Bestanden kopiëren naar een tijdelijke map"
  rm -rf "$NIEUW"
  mkdir -p "$NIEUW" || fout "Kan $NIEUW niet maken."
  cp -R "$BRON/ScoreKrijt" "$BRON/ScoreKrijt.py" "$BRON/scorekrijt_launcher.py" "$NIEUW/" || { rm -rf "$NIEUW"; fout "Kopiëren is mislukt. De huidige versie is niet gewijzigd."; }
  find "$NIEUW" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null
  chmod -R u+rwX,go+rX "$NIEUW"

  stap "Nieuwe bestanden controleren"
  if [ -n "$PY" ]; then
    local f
    while IFS= read -r f; do
      "$PY" -c 'import ast,sys; ast.parse(open(sys.argv[1], "rb").read())' "$f" 2>/dev/null \
        || { rm -rf "$NIEUW"; fout "Het bestand $f is beschadigd of bevat een fout. De huidige versie is niet gewijzigd."; }
    done < <(find "$NIEUW" -name '*.py')
    info "Alle Python-bestanden zijn leesbaar."
  else
    info "Python niet gevonden; controle overgeslagen."
  fi

  stap "Instellingen en wedstrijden overnemen"
  if [ -f "$PROGRAMMA/ScoreKrijtSettings.json" ]; then
    cp "$PROGRAMMA/ScoreKrijtSettings.json" "$NIEUW/" || fout "Instellingen kopiëren is mislukt."
    info "Instellingen overgenomen."
  else
    info "Let op: geen ScoreKrijtSettings.json gevonden; de standaardinstellingen worden gebruikt."
  fi
  if [ -d "$PROGRAMMA/matches" ]; then
    cp -a "$PROGRAMMA/matches" "$NIEUW/" || fout "Wedstrijden kopiëren is mislukt."
    info "Wedstrijdbestanden overgenomen."
  fi

  stap "ScoreKrijt stoppen en nieuwe versie activeren"
  stop_scorekrijt
  local nr datum vorige
  nr="$(volgend_nummer)"
  datum="$(date +%Y-%m-%d)"
  vorige="${PROGRAMMA}_vorige_${nr}_${datum}"
  mv "$PROGRAMMA" "$vorige" || fout "De huidige map kon niet worden hernoemd."
  if ! mv "$NIEUW" "$PROGRAMMA"; then
    mv "$vorige" "$PROGRAMMA"
    fout "De nieuwe map kon niet worden geactiveerd. De oude versie is teruggezet."
  fi
  info "Vorige versie bewaard als: $vorige"

  installeer_scripts "$BRON"

  stap "Bluetooth: opnieuw koppelen toestaan"
  herstel_bluetooth "$((1 - HERSTART))"

  stap "USB-stick losmaken"
  maak_stick_los

  info ""
  info "Bijgewerkt van $huidige naar $nieuwe."
  info "Werkt het niet goed? Zet de vorige versie terug met: bash ~/sk-update.sh --terug"
  herstart
}

doe_terug() {
  local vorige mislukt
  vorige="$(hoogste_vorige || true)"
  [ -n "${vorige:-}" ] || fout "Geen vorige versie gevonden (ScoreKrijt_vorige_<nummer>_<datum>)."
  info "Teruggaan naar: $vorige"
  info "Versie daarin:  $(versie_van "$vorige")"
  ja_nee "Deze versie terugzetten?" || { info "Afgebroken. Er is niets gewijzigd."; exit 0; }

  stop_scorekrijt
  mislukt="${PROGRAMMA}_mislukt_$(date +%Y-%m-%d_%H%M%S)"
  mv "$PROGRAMMA" "$mislukt" || fout "De huidige map kon niet worden hernoemd."
  if ! mv "$vorige" "$PROGRAMMA"; then
    mv "$mislukt" "$PROGRAMMA"
    fout "De vorige versie kon niet worden teruggezet. De huidige versie is behouden."
  fi
  if [ -d "$mislukt/matches" ]; then
    mkdir -p "$PROGRAMMA/matches"
    cp -an "$mislukt/matches/." "$PROGRAMMA/matches/" 2>/dev/null
    info "Wedstrijden die na de update zijn gespeeld zijn meegenomen."
  fi
  info "Teruggezet. De mislukte versie staat in: $mislukt"
  herstart
}

case "$MODUS" in
  terug)      doe_terug ;;
  bluetooth)  stap "Bluetooth: opnieuw koppelen toestaan"; herstel_bluetooth 1 ;;
  *)      doe_update ;;
esac
