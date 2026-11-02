# Screenshotlijst voor de SK-Box-handleidingen

Zet elk bestand in deze map (`Docs\Screenshots`), met **precies** de bestandsnaam uit de lijst, als `.png` (of `.jpg` voor foto's).
De bouwscripts (`build_skbox_handleidingen.ps1`) nemen een afbeelding automatisch mee zodra het bestand bestaat. Ontbreekt een bestand, dan wordt het overgeslagen en gemeld aan het eind van de build.

**★** = belangrijk, **○** = leuk als het lukt. Eén bestand mag in meerdere handleidingen worden gebruikt.

## Afspraken

- **Geen SSH voor de opnamen.** Alles wordt op de SK-Box zelf opgenomen, met een toetsenbord aan de SK-Box. Wifi staat alleen tijdens de installatie aan (updates en software) en gaat daarna uit (hoofdstuk 14). Er komen geen opnamen van SSH in de handleidingen en de tekst daarover blijft ongewijzigd.
- **Opnamen op de SK-Box:** open een Terminal op de Desktop, of gebruik Ctrl+Alt+F2 voor een tekstscherm. Probeer eerst of het commando `grim` (schermopname op de Raspberry Pi) werkt. Zo niet, maak dan een telefoonfoto van het scherm. Zet de bestanden met een USB-stick over naar de pc.
- **Telefoon:** aan/uit-knop + volume omlaag. Zet de schermen via Google Drive of USB op de pc.
- **Windows-opnamen:** Win+Shift+S en sleep een kader om alleen het venster.
- **Foto's van het HDMI-scherm:** houd de telefoon liggend, recht voor het scherm, zonder flits en zonder spiegeling.
- **Privacy:** geen wifi-naam of wachtwoord, geen e-mailadres of mailwachtwoord, geen persoonlijke namen van spelers in beeld. Gebruik testnamen (bijvoorbeeld "Speler A" en "Speler B").
- **Pijlen:** genummerde blauwe pijlen (1, 2, 3) bij de plekken waar de gebruiker moet klikken, zoals bij de GitHub-opnamen. In de handleidingtekst verwijzen we er met "pijl 1" naar.
- **Opmaak:** liefst allemaal in dezelfde stijl. Liever iets te klein uitknippen dan het hele scherm.

## Sessie A: Windows-pc (Verkenner)

| Nr | Bestandsnaam | Wat moet erop staan | Handleiding |
|----|--------------|---------------------|-------------|
| A0a ★ | `install-2.1-github-download` | Browser: de GitHub-pagina `github.com/bramijsselstijn/ScoreKrijt` met het menu van de groene knop **Code** open en **Download ZIP** zichtbaar | Installatie 2.1 |
| A0b ★ | `install-2.1-uitpakken` | Verkenner: het gedownloade ZIP-bestand met het rechtermuismenu en **Alles uitpakken** | Installatie 2.1 |
| A1 ★ | `install-6.2-kopieren` | **Klaar.** Selectie van de vijf onderdelen en het menu Kopiëren (pijl 4 en 5) | Installatie 6.2 |
| A1b ★ | `install-6.2-usbstick` | **Klaar.** De USB-stick met de map `ScoreKrijt_update` | Installatie 6.2 |
| A1c ★ | `install-6.2-plakken` | **Klaar.** Plakken in de lege map (pijl 6 en 7) | Installatie 6.2 |
| A1d ★ | `install-6.2-scripts` | **Klaar.** De USB-stick (hoofdmap) met de mappen `ScoreKrijt_update` en `SK-Box_scripts`. Haal losse overbodige bestanden, zoals `sk-update.sh` in de hoofdmap, eerst van de stick | Installatie 6.2 |
| A2 ★ | `update-2.1-usbstick-map` | Verkenner: de USB-stick met de map `ScoreKrijt_update` open, met de vijf onderdelen erin | Bijwerken 2.1 |

## Sessie B: de SK-Box zelf

### Terminal en tekstscherm

| Nr | Bestandsnaam | Wat moet erop staan | Handleiding |
|----|--------------|---------------------|-------------|
| B1 ★ | `install-3.2-raspi-config` | Hoofdmenu van `sudo raspi-config` | Installatie 3.2 |
| B2 ○ | `install-3.2-autologin` | raspi-config: System Options > Boot / Auto Login > keuze Desktop Autologin | Installatie 3.2 |
| B3 ○ | `install-5-controle` | De controleopdrachten uit hoofdstuk 5 met "Tkinter OK", "Pillow OK", "pyserial OK" | Installatie 5 |
| B4 ○ | `install-6.2-controle` | Uitvoer van `ls -la` met de regels "ScoreKrijt.py OK", "launcher OK", "instellingen OK", "icons OK" | Installatie 6.2 |
| B5 ★ | `install-8.2-nano-service` | nano met het servicebestand `scorekrijt-pairing.service` ingevuld | Installatie 8.2 |
| B6 ★ | `install-8.2-bluetoothctl-show` | `bluetoothctl show` met Powered, Discoverable en Pairable op `yes` | Installatie 8.2 |
| B7 ○ | `install-8.2-paired` | `bluetoothctl devices Paired` met de telefoon in de lijst (na het koppelen) | Installatie 8.2 |
| B8 ○ | `install-9.2-rfcomm-status` | `systemctl status scorekrijt-rfcomm.service` met "active (running)" | Installatie 9.2 |
| B9 ○ | `install-11.1-autostart` | `cat ~/.config/autostart/scorekrijt.desktop` | Installatie 11.1 |
| B10 ★ | `install-13.2-script` | `bash ~/sk-stille-opstart.sh` met de lijst van wijzigingen en de bevestigingsvraag | Installatie 13.2 |
| B11 ○ | `install-15-controle` | `systemctl is-active bluetooth` en `systemctl is-enabled scorekrijt-pairing.service scorekrijt-rfcomm.service` | Installatie 15 |
| B12 ★ | `update-3.1-sk-update` | `bash ~/sk-update.sh` met de huidige en de nieuwe versie en de vraag om te bevestigen | Bijwerken 3.1 |
| B13 ○ | `update-3.1-sk-update-klaar` | Slotmelding van het script dat de stick veilig kan worden verwijderd | Bijwerken 3.1 |
| B14 ★ | `update-3.4-versie` | `grep APP_VERSION ~/ScoreKrijt/ScoreKrijt/constants.py` met de versie in de uitvoer | Bijwerken 3.4 |

### Het welkomstscherm (foto's, alleen met een verse SD-kaart)

Het welkomstscherm verschijnt alleen bij de eerste start van een nieuwe SD-kaart zonder voorinstellingen. Zonder kaart die je opnieuw wilt beschrijven, kun je deze opnamen overslaan; de tekst blijft dan zonder afbeelding.

| Nr | Bestandsnaam | Wat moet erop staan | Handleiding |
|----|--------------|---------------------|-------------|
| B26 ★ | `install-3.1-welkom` | Het scherm **Welcome to the Raspberry Pi Desktop** | Installatie 3.1 |
| B27 ★ | `install-3.1-land` | Het scherm met Country, Language en Timezone ingevuld op Netherlands, Dutch en Amsterdam | Installatie 3.1 |
| B28 ★ | `install-3.1-gebruiker` | Het scherm waar de gebruikersnaam `user` en het wachtwoord worden ingevuld (verberg het wachtwoord met **Hide characters**) | Installatie 3.1 |
| B29 ○ | `install-3.1-wifi` | Het scherm met de wifi-keuze. Let op: de lijst toont namen van netwerken in de buurt. Maak die onherkenbaar of sla deze opname over | Installatie 3.1 |

### Het scherm

| Nr | Bestandsnaam | Wat moet erop staan | Handleiding |
|----|--------------|---------------------|-------------|
| B15 ★ | `install-7-hoofdvenster` | Het gewone ScoreKrijt-hoofdvenster op de Desktop | Installatie 7 |
| B16 ★ | `install-7-opstartscherm` | Opstartscherm met logo en "SK-Box wordt gestart" | Installatie 7, Instellingen 2 |
| B17 ★ | `install-11.2-scorebord` | Het grote scorebord schermvullend, tijdens een testwedstrijd | Installatie 11.2, Instellingen 2 |
| B18 ★ | `install-12-weergave` | Het venster met het onderdeel **Weergave** (BlueTooth Mode, Groot scherm, enz.) | Installatie 12 |
| B19 ★ | `install-13.1-opstartlogo` | Foto van het scherm tijdens het opstarten met het ScoreKrijt-logo | Installatie 13.1, Instellingen 2 |
| B20 ★ | `install-13.1-bureaublad` | Het zwarte bureaublad met het ScoreKrijt-logo, zonder taakbalk | Installatie 13.1, Instellingen 2 |
| B21 ○ | `install-13.3-bureaubladvoorkeuren` | Het venster Bureaubladvoorkeuren met logo, modus Centreren, kleur zwart | Installatie 13.3 |
| B22 ★ | `install-13.5-taakbalk` | **Klaar.** Scorebord met de taakbalk zichtbaar na F12 | Installatie 13.5, Instellingen 6 |
| B23 ★ | `install-14.3-tekstscherm` | Tekstscherm met inlogprompt na Ctrl+Alt+F2 | Installatie 14.3, Bijwerken 3.1 |

### De geprinte behuizing (foto's)

| Nr | Bestandsnaam | Wat moet erop staan | Handleiding |
|----|--------------|---------------------|-------------|
| B24 ★ | `install-2.2-schroeven` | De geprinte SK-Box met de vier schroeven goed zichtbaar, bij voorkeur met de inbussleutel erbij | Installatie 2.2 |
| B25 ★ | `install-2.2-uitkantelen` | De Raspberry Pi aan de voedingskant opgetild, half uit de behuizing gekanteld | Installatie 2.2 |

## Sessie C: scorebord (telefoonschermen vervallen)

Besluit: er komen **geen schermopnamen van de telefoon** in de handleidingen. Vervallen zijn C1 t/m C6, C8 en C12 (Bluetooth koppelen, app-schermen en de APK-update). Alleen de opnamen van het scorebord blijven over:

| Nr | Bestandsnaam | Wat moet erop staan | Handleiding |
|----|--------------|---------------------|-------------|
| C7 ○ | `instellingen-4-live` | Foto van het scorebord na het verschuiven van een regelaar | Instellingen 4 |
| C9 ★ | `instellingen-5.1-aanvang-scorebord` | Scorebord met namen en TMC en de witte vakken | Instellingen 5.1 |
| C10 ★ | `instellingen-5.2-vaste-beurten` | Scorebord bij vaste beurten: kolommen **Punten** en **Car. tot punt** | Instellingen 5.2 |
| C11 ★ | `instellingen-5.2-uit-is-uit` | Scorebord bij Uit is uit: kolommen **Procent** en **Car. tot uit** | Instellingen 5.2 |

Extra opnamen die jij zelf hebt gemaakt en die in de handleiding zijn verwerkt (klaar): `install-3.2-raspi-config` (= B1), `install-3.2-controlecentrum-menu`, `install-3.2-controlecentrum`, `install-3.2-schermblanking`, `install-3.2-systeem`, `install-6.2-sk-usb-melding`, `install-6.4-scripts-plakken`, `install-13.2-script` (= B10), `install-13.2-script-klaar`, `install-13.5-terminal`. Ook klaar: `install-5-controle`, `install-6.2-controle`, `install-8.2-nano-service`, `install-8.2-bluetoothctl-show`, `update-3.1-sk-update` (bijgesneden, zonder de eerdere foutmelding; het origineel staat in `update-3.1-sk-update-origineel.png`). Bewust overgeslagen als overbodig: `install-8.2-paired`, `install-9.2-rfcomm-status`, `install-11.1-autostart`, `install-15-controle`, `update-3.4-versie`. Nog niet gebruikt: `install-3.2-raspi-config-start` en `install-13.2-script-commando` (het getypte commando staat al in de tekst).

Vervallen: Hardware veilig verwijderen, de SD-kaart (bootfs) en alle telefoonschermen.
