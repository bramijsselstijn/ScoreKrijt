#!/usr/bin/env bash
# sk-stille-opstart.sh - maakt het opstarten van de SK-Box stil: geen Raspberry Pi-logo's,
# geen opstarttekst en (op labwc) geen taakbalk. Het ScoreKrijt-logo staat in het opstartscherm
# van Linux en op het bureaublad.
# Optioneel wordt wifi uitgezet, zodat de SK-Box nooit met internet verbonden is.
#
# Gebruik (als gewone gebruiker, dus niet met sudo):
#   bash sk-stille-opstart.sh                 doorvoeren (vraagt eerst om bevestiging)
#   bash sk-stille-opstart.sh --wifi-uit      ook wifi uitzetten (Bluetooth blijft aan)
#   bash sk-stille-opstart.sh --sneller       ook cloud-init uitzetten (ongeveer 3 seconden sneller)
#   bash sk-stille-opstart.sh --terugdraaien  alles terugzetten zoals het was
# Opties:
#   --resolutie=BREEDTExHOOGTE  schermresolutie vastzetten (standaard 1920x1080)
#   --geen-resolutie            de schermresolutie niet vastzetten
#   --ja     geen bevestigingen vragen
#   --help   deze uitleg tonen
#
# Wat dit script wijzigt (van alle bestanden wordt eenmalig een kopie bewaard
# met de extensie .sk-origineel):
#   <boot>/cmdline.txt            opstartparameters en schermresolutie (video=HDMI-A-1:...)
#   /usr/share/plymouth/themes/pix/splash.png  zet het ScoreKrijt-logo in het opstartscherm
#   <boot>/config.txt             schakelt het regenboogscherm van de firmware uit
#   /etc/cloud/cloud-init.disabled  alleen met --sneller: zet cloud-init uit
#   /etc/xdg/labwc/autostart      haalt de taakbalk uit de autostart
#   ~/.config/pcmanfm/*/desktop-items-0.conf  zet het logo als bureaubladachtergrond
# Het script is herhaalbaar: opnieuw uitvoeren geeft hetzelfde resultaat.

set -u

MODUS="doorvoeren"
WIFI_UIT=0
SNEL=0
JA=0
RESOLUTIE="1920x1080"
MARKER="# ScoreKrijt stille opstart"
LABWC_MARKER="# sk-stil: "

info() { printf '%s\n' "$*"; }
stap() { printf '\n==> %s\n' "$*"; }
fout() { printf '\nFOUT: %s\n' "$*" >&2; exit 1; }
uitleg() { sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'; }

for arg in "$@"; do
  case "$arg" in
    --terugdraaien) MODUS="terug" ;;
    --wifi-uit)     WIFI_UIT=1 ;;
    --sneller)      SNEL=1 ;;
    --ja)           JA=1 ;;
    --geen-resolutie) RESOLUTIE="" ;;
    --resolutie=*)  RESOLUTIE="${arg#--resolutie=}"
                    case "$RESOLUTIE" in
                      [0-9]*x[0-9]*) ;;
                      *) fout "Ongeldige resolutie: $RESOLUTIE (gebruik bijvoorbeeld --resolutie=1920x1080)" ;;
                    esac ;;
    --help|-h)      uitleg; exit 0 ;;
    *)              fout "Onbekende optie: $arg (zie --help)" ;;
  esac
done

[ "$(id -u)" -eq 0 ] && fout "Voer dit script uit als gewone gebruiker, niet met sudo. Het vraagt zelf om sudo waar dat nodig is."

BOOT="/boot/firmware"
[ -f "$BOOT/cmdline.txt" ] || BOOT="/boot"
CMD="$BOOT/cmdline.txt"
CFG="$BOOT/config.txt"
[ -f "$CMD" ] && [ -f "$CFG" ] || fout "cmdline.txt en config.txt niet gevonden in /boot/firmware of /boot. Is dit een Raspberry Pi?"

LABWC_SYS="/etc/xdg/labwc/autostart"
LABWC_USER="$HOME/.config/labwc/autostart"
LOGO_BRON="$HOME/ScoreKrijt/ScoreKrijt/icons/ScoreKrijt Logo.png"
LOGO="$HOME/.local/share/scorekrijt/logo.png"
PLY_IMG="/usr/share/plymouth/themes/pix/splash.png"
PLY_OK=0

ja_nee() {
  [ "$JA" -eq 1 ] && return 0
  local antw
  read -r -p "$1 [j/N] " antw || return 1
  case "$antw" in j|J|y|Y|ja|Ja|JA) return 0 ;; *) return 1 ;; esac
}

bewaar_origineel() {
  [ -f "$1.sk-origineel" ] || sudo cp -p "$1" "$1.sk-origineel"
}

# Zet het ScoreKrijt-logo op zwart als bureaubladachtergrond (pcmanfm-pi) en verberg
# de bureaubladpictogrammen. Zo is er geen leeg zwart scherm vlak voor ScoreKrijt start.
zet_achtergrond() {
  local dir conf
  if [ ! -f "$LOGO" ]; then
    info "Logo niet gevonden ($LOGO); achtergrond niet ingesteld."
    return 0
  fi
  for dir in "$HOME/.config/pcmanfm/default" "$HOME/.config/pcmanfm/LXDE-pi"; do
    conf="$dir/desktop-items-0.conf"
    mkdir -p "$dir"
    if [ -f "$conf" ] && [ ! -f "$conf.sk-origineel" ] && ! grep -qE "wallpaper=.*(/.local/share/scorekrijt/|/icons/biljart.png)" "$conf"; then
      cp -p "$conf" "$conf.sk-origineel"
    fi
    cat > "$conf" <<EOF
[*]
wallpaper_mode=center
wallpaper_common=1
wallpaper=$LOGO
desktop_bg=#000000
desktop_fg=#ffffff
desktop_shadow=#000000
show_documents=0
show_trash=0
show_mounts=0
EOF
  done
  info "Achtergrond ingesteld op $LOGO"
}

# Maakt een verkleinde kopie van het ScoreKrijt-logo (480 x 480 pixels, net zo groot als op
# het opstartscherm van de launcher). Die kopie wordt voor de achtergrond en voor het
# Plymouth-opstartscherm gebruikt. Hij staat buiten de programmamap, zodat een update
# hem niet verplaatst.
maak_logo() {
  if [ ! -f "$LOGO_BRON" ]; then
    info "Logo niet gevonden ($LOGO_BRON). Is ScoreKrijt geïnstalleerd?"
    return 1
  fi
  mkdir -p "$(dirname "$LOGO")"
  if ! python3 - "$LOGO_BRON" "$LOGO" <<'PY'
import sys
from PIL import Image
image = Image.open(sys.argv[1]).convert("RGBA")
image.thumbnail((480, 480))
image.save(sys.argv[2])
PY
  then
    info "Logo verkleinen is mislukt (is python3-pil geïnstalleerd?)."
    return 1
  fi
  info "Logo klaargezet: $LOGO"
}

# Zet het ScoreKrijt-logo in het opstartscherm van Linux (Plymouth, thema "pix") in
# plaats van het Raspberry Pi-logo. Geeft 0 terug als dat is gelukt; anders blijft
# het scherm tijdens het opstarten zwart (plymouth.enable=0).
zet_opstartlogo() {
  if [ ! -f "$LOGO" ] || [ ! -f "$PLY_IMG" ]; then
    info "Opstartlogo niet mogelijk (logo of Plymouth-thema 'pix' ontbreekt)."
    return 1
  fi
  bewaar_origineel "$PLY_IMG"
  if sudo cp "$LOGO" "$PLY_IMG"; then
    herbouw_initramfs
    info "Opstartlogo ingesteld ($PLY_IMG)."
    return 0
  fi
  return 1
}

# Het thema kan in de initramfs zitten; werk die dan bij zodat het nieuwe logo gebruikt wordt.
herbouw_initramfs() {
  if command -v update-initramfs >/dev/null 2>&1 && ls "$BOOT"/initramfs* >/dev/null 2>&1; then
    info "initramfs wordt bijgewerkt (dit kan even duren)..."
    sudo update-initramfs -u >/dev/null 2>&1 || info "Let op: update-initramfs gaf een foutmelding."
  fi
}

# cloud-init is een installatieprogramma voor de allereerste start van de Pi. Op een
# werkende SK-Box doet het niets meer, maar het kost ongeveer 3 seconden bij het opstarten.
CLOUD_UIT="/etc/cloud/cloud-init.disabled"
CLOUD_MARKER="/etc/cloud/.sk-cloud-init-uitgezet"
zet_cloud_init_uit() {
  if [ ! -d /etc/cloud ]; then
    info "cloud-init niet aanwezig; niets te doen."
    return 0
  fi
  if [ -e "$CLOUD_UIT" ]; then
    info "cloud-init stond al uit."
    return 0
  fi
  sudo touch "$CLOUD_UIT" "$CLOUD_MARKER" && info "cloud-init uitgezet (bespaart ongeveer 3 seconden bij het opstarten)."
}

# Een eerdere versie van dit script maakte een kopie van het systeembestand in
# ~/.config/labwc. Die kopie liet ScoreKrijt dubbel starten. Ruim hem op als hij
# niets bevat dat niet ook in het originele systeembestand stond.
ruim_gebruikerskopie_op() {
  [ -f "$LABWC_USER" ] && grep -qF "$LABWC_MARKER" "$LABWC_USER" || return 0
  sed -i "s/^${LABWC_MARKER}//" "$LABWC_USER"
  if cmp -s "$LABWC_USER" "$LABWC_SYS.sk-origineel"; then
    rm -f "$LABWC_USER" "$LABWC_USER.sk-origineel"
    info "Oude kopie $LABWC_USER verwijderd (die liet ScoreKrijt dubbel starten)."
  else
    info "Let op: $LABWC_USER bevat eigen regels en is bewaard. Controleer of er niets"
    info "in staat dat ook in $LABWC_SYS staat, want dan draait het twee keer."
  fi
}

# ---------------------------------------------------------------------------
doorvoeren() {
  info "Dit script past het opstarten van de SK-Box aan."
  info "  - opstartbestanden: $CMD en $CFG"
  info "  - bureaublad:       $LABWC_SYS (alleen als labwc wordt gebruikt)"
  [ -n "$RESOLUTIE" ] && info "  - schermresolutie:  wordt vastgezet op $RESOLUTIE (via $CMD)"
  [ "$WIFI_UIT" -eq 1 ] && info "  - wifi:             wordt uitgezet (SSH via wifi werkt daarna niet meer)"
  ja_nee "Doorgaan?" || { info "Afgebroken. Er is niets gewijzigd."; exit 0; }

  stap "Opstartlogo (tijdens het opstarten van Linux)"
  maak_logo
  zet_opstartlogo && PLY_OK=1

  stap "Opstartparameters (cmdline.txt)"
  bewaar_origineel "$CMD"
  local regel nieuw w extra
  regel="$(tr -d '\r\n' < "$CMD")"
  nieuw=""
  for w in $regel; do
    case "$w" in
      splash|loglevel=*|plymouth.enable=*) continue ;;
      video=HDMI-A-*) [ -n "$RESOLUTIE" ] && continue ;;
      console=tty1)                         w="console=tty3" ;;
    esac
    nieuw="$nieuw $w"
  done
  extra="quiet loglevel=3 logo.nologo vt.global_cursor_default=0"
  # Resolutie vastzetten, zodat de Pi bij een scherm van 2K of 4K niet zelf hoger kiest
  # (dat kost veel geheugen). Een poort die niet bestaat of niet gebruikt wordt, wordt genegeerd.
  [ -n "$RESOLUTIE" ] && extra="$extra video=HDMI-A-1:${RESOLUTIE}@60 video=HDMI-A-2:${RESOLUTIE}@60"
  if [ "$PLY_OK" -eq 1 ]; then extra="$extra splash"; else extra="$extra plymouth.enable=0"; fi
  for w in $extra; do
    case " $nieuw " in *" $w "*) ;; *) nieuw="$nieuw $w" ;; esac
  done
  nieuw="${nieuw# }"
  printf '%s\n' "$nieuw" | sudo tee "$CMD" >/dev/null || fout "Schrijven naar $CMD is mislukt."
  info "Nieuwe cmdline.txt:"
  info "  $nieuw"

  stap "Firmware-opstartscherm (config.txt)"
  bewaar_origineel "$CFG"
  if grep -qF "$MARKER" "$CFG"; then
    info "Staat er al in; niets gewijzigd."
  else
    printf '\n%s (toegevoegd door sk-stille-opstart.sh)\n[all]\ndisable_splash=1\nboot_delay=0\n' "$MARKER" \
      | sudo tee -a "$CFG" >/dev/null || fout "Schrijven naar $CFG is mislukt."
    info "disable_splash=1 en boot_delay=0 toegevoegd."
  fi

  stap "Bureaublad (taakbalk en achtergrond)"
  if [ -f "$LABWC_SYS" ]; then
    # Raspberry Pi OS voert het systeembestand ook uit als er een eigen bestand in
    # ~/.config/labwc staat. Daarom passen we het systeembestand zelf aan.
    bewaar_origineel "$LABWC_SYS"
    # Alleen de taakbalk gaat uit; pcmanfm-pi blijft draaien voor de achtergrond met logo.
    # Een eerdere versie van dit script zette pcmanfm ook uit: dat wordt hersteld.
    sudo sed -i -E -e "/^[[:space:]]*#/!{/wf-panel-pi/ s/^/${LABWC_MARKER}/}" \
                   -e "s/^${LABWC_MARKER}(.*pcmanfm.*)$/\1/" "$LABWC_SYS" \
      || fout "Aanpassen van $LABWC_SYS is mislukt."
    info "De taakbalk staat niet meer in de autostart. Inhoud van $LABWC_SYS:"
    sed 's/^/  /' "$LABWC_SYS"
    ruim_gebruikerskopie_op
    zet_achtergrond
  else
    info "Geen labwc-autostart gevonden. Dit bureaublad moet je handmatig aanpassen;"
    info "zie de installatiehandleiding, hoofdstuk 'Stille opstart'."
  fi

  if [ "$SNEL" -eq 1 ]; then
    stap "Sneller opstarten (cloud-init)"
    zet_cloud_init_uit
  fi

  stap "Wifi"
  if [ "$WIFI_UIT" -eq 1 ]; then
    if command -v nmcli >/dev/null 2>&1; then
      sudo nmcli radio wifi off && info "Wifi staat uit. Bluetooth is niet gewijzigd."
    else
      info "nmcli niet gevonden; wifi niet uitgezet. Gebruik: sudo rfkill block wifi"
    fi
  else
    info "Niet gevraagd; wifi blijft zoals het was. Gebruik --wifi-uit om het uit te zetten."
  fi

  info ""
  info "Klaar. Start de SK-Box opnieuw op om het resultaat te zien:  sudo reboot"
  info "Terugdraaien kan met:  bash ~/sk-stille-opstart.sh --terugdraaien"
}

# ---------------------------------------------------------------------------
terugdraaien() {
  ja_nee "Alle wijzigingen van dit script ongedaan maken en wifi weer aanzetten?" || { info "Afgebroken."; exit 0; }

  stap "Opstartbestanden terugzetten"
  local f
  for f in "$CMD" "$CFG"; do
    if [ -f "$f.sk-origineel" ]; then
      sudo cp -p "$f.sk-origineel" "$f" && info "Teruggezet: $f"
    else
      info "Geen kopie van $f gevonden; niets teruggezet."
    fi
  done

  stap "Opstartlogo terugzetten"
  if [ -f "$PLY_IMG.sk-origineel" ]; then
    sudo cp -p "$PLY_IMG.sk-origineel" "$PLY_IMG" && info "Teruggezet: $PLY_IMG"
    herbouw_initramfs
  else
    info "Geen kopie van het opstartlogo gevonden; niets teruggezet."
  fi

  stap "Bureaublad terugzetten"
  if [ -f "$LABWC_SYS.sk-origineel" ]; then
    sudo cp -p "$LABWC_SYS.sk-origineel" "$LABWC_SYS" && info "Teruggezet: $LABWC_SYS"
  else
    info "Geen kopie van $LABWC_SYS gevonden; niets teruggezet."
  fi
  [ -f "$LABWC_USER" ] && sed -i "s/^${LABWC_MARKER}//" "$LABWC_USER"
  local dir conf
  for dir in "$HOME/.config/pcmanfm/default" "$HOME/.config/pcmanfm/LXDE-pi"; do
    conf="$dir/desktop-items-0.conf"
    if [ -f "$conf.sk-origineel" ]; then
      cp -p "$conf.sk-origineel" "$conf" && info "Achtergrondinstellingen teruggezet: $conf"
    elif [ -f "$conf" ] && grep -qE "wallpaper=.*(/.local/share/scorekrijt/|/icons/biljart.png)" "$conf"; then
      rm -f "$conf" && info "Achtergrond met logo verwijderd: $conf"
    fi
  done

  stap "cloud-init weer aanzetten"
  if [ -e "$CLOUD_MARKER" ]; then
    sudo rm -f "$CLOUD_UIT" "$CLOUD_MARKER" && info "cloud-init staat weer aan."
  else
    info "Niets te herstellen."
  fi

  stap "Wifi aanzetten"
  if command -v nmcli >/dev/null 2>&1; then
    sudo nmcli radio wifi on && info "Wifi staat aan."
  fi

  info ""
  info "Klaar. Start de SK-Box opnieuw op:  sudo reboot"
}

case "$MODUS" in
  terug) terugdraaien ;;
  *)     doorvoeren ;;
esac
