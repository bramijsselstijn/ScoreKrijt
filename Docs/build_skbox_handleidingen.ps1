# Bouwt de SK-Box-handleidingen (installatie en bijwerken) als .docx en .pdf.
# Uitvoeren in PowerShell:  powershell -ExecutionPolicy Bypass -File .\build_skbox_handleidingen.ps1
# Vereist Microsoft Word (voor de inhoudsopgave en de pdf-export).

$ErrorActionPreference = 'Stop'
$Docs = $PSScriptRoot
. (Join-Path $Docs 'skbox_docgen.ps1')

$Logo = Join-Path $Docs 'Logos\ScoreKrijt Logo.png'
$Versie = '2.8.7'
$Datum = '27 oktober 2026'
$Map = 'Phyton\V2.8.7'
$MapC = '`' + $Map + '`'

# ---------------------------------------------------------------------------
# 1. Installatiehandleiding
# ---------------------------------------------------------------------------
Start-Doc
Cover 'INSTALLATIEHANDLEIDING' 'SK-Box installeren' 'Een Raspberry Pi instellen als ScoreKrijt-scorebord met Bluetooth-bediening' "SK-Box software $Versie   |   $Datum" $Logo
TocPage

H1 '1. Over deze handleiding'
Para 'Met deze handleiding richt je een Raspberry Pi in als **SK-Box**: een zelfstandig ScoreKrijt-scorebord. De SK-Box toont de stand op een aangesloten HDMI-scherm en wordt met Bluetooth bediend vanuit de Android-app.'
Para 'De stappen gaan uit van **Raspberry Pi OS met Desktop**. ScoreKrijt gebruikt Tkinter en een grafisch scherm; zonder Desktop kan het scorebord niet worden getoond.'
H2 '1.1 Zo gebruik je deze handleiding'
Bullet 'Werk de hoofdstukken in volgorde af. Elk hoofdstuk bouwt voort op het vorige.'
Bullet 'Tekst in een donker blok is een opdracht. Typ of plak die in een Terminal op de Raspberry Pi, tenzij er staat dat het in PowerShell op je pc moet.'
Bullet 'Tekst tussen punthaken, zoals `<IP-adres>`, vervang je door je eigen waarde. Typ de punthaken niet mee.'
Spacer
Tbl @('Vervang', 'Door', 'Hoe vind je dit?') @(
    @('`<IP-adres>`', 'Het IP-adres van de SK-Box', 'Typ `hostname -I` op de Pi (zie hoofdstuk 4).')
) @(2400, 3400, 3838)
Callout 'info' 'Inloggegevens van de SK-Box' 'In deze handleiding heeft de SK-Box de gebruikersnaam `user` en het wachtwoord `user`. Stel ze zo in bij de eerste start van Raspberry Pi OS (hoofdstuk 3.1) of in Raspberry Pi Imager; je hebt ze nodig bij SSH en bij inloggen op de SK-Box zelf.'
Callout 'warn' 'Eenvoudig wachtwoord' 'Het wachtwoord `user` is makkelijk te raden. Dat is acceptabel zolang de SK-Box nooit met internet of een openbaar netwerk is verbonden (zie hoofdstuk 14). Sluit je de SK-Box wel op een netwerk aan, kies dan een sterker wachtwoord.'
Callout 'warn' 'Heb je al een werkende SK-Box?' 'Wil je alleen een nieuwe versie van het programma installeren, volg dan de handleiding **SK-Box bijwerken**. Een nieuwe installatie is daarvoor niet nodig.'

H1 '2. Benodigdheden'
Bullet 'Raspberry Pi met Bluetooth en HDMI, een geschikte voeding en een microSD-kaart of SSD.'
Bullet 'Raspberry Pi OS met Desktop (64-bit wordt aanbevolen voor recente Pi-modellen).'
Bullet 'Een HDMI-scherm voor het scorebord.'
Bullet 'Een toetsenbord en een netwerkverbinding voor de eerste installatie. Daarna is internet niet meer nodig (hoofdstuk 14).'
Bullet 'Een USB-stick om bestanden en later updates naar de SK-Box te brengen.'
Bullet ('De programmamap ' + $MapC + ' uit het ScoreKrijt-project, op je pc. Die haal je eerst op van GitHub (zie hoofdstuk 2.1).')
Bullet 'Een pc met Windows om de bestanden te kopiëren (via USB-stick of via het netwerk).'
Bullet 'Een Android-telefoon met de ScoreKrijt-app.'
Bullet 'Alleen bij de geprinte SK-Box: een inbussleutel van 2 mm om de Raspberry Pi uit de behuizing te halen (zie hoofdstuk 2.2).'

H2 '2.1 De ScoreKrijt-bestanden van GitHub ophalen'
Para 'Alle bestanden van ScoreKrijt staan op GitHub. Haal ze eerst op je pc op; daarna kopieer je ze naar de SK-Box (hoofdstuk 6). Dit doe je op een pc met internet. De SK-Box zelf heeft geen internet nodig.'
$s = New-StepList
Step $s '**Open de projectpagina** in je browser: `https://github.com/bramijsselstijn/ScoreKrijt`'
Step $s '**Klik op de groene knop Code** (pijl 1) en kies **Download ZIP** (pijl 2). Je krijgt het bestand `ScoreKrijt-main.zip`.'
Shot 'install-2.1-github-download' 'De projectpagina op GitHub: eerst de groene knop Code (1), daarna Download ZIP (2).'
Step $s '**Pak het ZIP-bestand uit.** Zoek `ScoreKrijt-main.zip` in je map Downloads, klik er met de rechtermuisknop op en kies **Alles uitpakken** (pijl 3). Kies een map die je terugvindt, bijvoorbeeld Documenten.'
Shot 'install-2.1-uitpakken' 'Het ZIP-bestand uitpakken met Alles uitpakken (3).'
Step $s ('**Controleer de inhoud.** In de uitgepakte map staat de map `Phyton`. De programmamap ' + $MapC + ' daarin gebruik je in de rest van deze handleiding. De map `Phyton\SK-Box_scripts` bevat de twee hulpscripts. De APK van de telefoonapp staat niet in deze download.')
Callout 'info' 'Liever met Git?' 'Heb je Git op je pc, dan kan het ook met `git clone https://github.com/bramijsselstijn/ScoreKrijt.git`. Voor de SK-Box is de ZIP-download voldoende.'

H2 '2.2 De Raspberry Pi uit de geprinte SK-Box halen'
Para 'Gebruik je de geprinte SK-Box, dan zit de Raspberry Pi vast in de behuizing. Haal hem er zo uit. De microSD-kaart blijft in de Raspberry Pi zitten:'
$s = New-StepList
Step $s '**Schakel de SK-Box uit** en haal de voeding eruit.'
Step $s '**Draai de vier schroeven los** met een inbussleutel van 2 mm.'
Shot 'install-2.2-schroeven' 'De vier schroeven van de SK-Box, los te draaien met een inbussleutel van 2 mm.'
Step $s '**Til de Raspberry Pi aan de kant van de voeding als eerste op** en kantel hem zo uit de behuizing.'
Shot 'install-2.2-uitkantelen' 'De Raspberry Pi aan de voedingskant optillen en uit de behuizing kantelen.'
Callout 'info' 'Terugplaatsen' 'Plaats de Raspberry Pi in omgekeerde volgorde terug en draai de vier schroeven weer vast. Draai ze niet te hard aan; de behuizing is geprint.'

H1 '3. Raspberry Pi OS voorbereiden'
H2 '3.1 Het welkomstscherm bij de eerste start'
Para 'Start je een nieuwe SD-kaart voor het eerst op, dan verschijnt het scherm **Welcome to the Raspberry Pi Desktop**. Dat is de installatiewizard van Raspberry Pi OS. Je doorloopt hem één keer. Kies deze waarden:'
$s = New-StepList
Step $s '**Klik op Next** op het welkomstscherm.'
Shot 'install-3.1-welkom' 'Het welkomstscherm van Raspberry Pi OS.'
Step $s '**Land, taal en tijdzone.** Kies bij **Country** de waarde **Netherlands**, bij **Language** **Dutch** en bij **Timezone** **Amsterdam**. Laat **Use English language** uit, zodat de SK-Box Nederlands wordt. Vink **Use US keyboard** alleen aan als je toetsenbord een Amerikaanse indeling heeft. Klik op **Next**.'
Shot 'install-3.1-land' 'Land, taal en tijdzone instellen.'
Step $s '**Gebruiker aanmaken.** Vul als gebruikersnaam `user` in en als wachtwoord ook `user` (bij het wachtwoord twee keer). Klik op **Next**.'
Shot 'install-3.1-gebruiker' 'De gebruiker `user` met het wachtwoord `user` aanmaken.'
Step $s '**Internet verbinden.** Kies bij de vraag om een wifi-netwerk je eigen netwerk en vul het wachtwoord in. Sluit je liever een netwerkkabel aan, klik dan op **Skip**. Je hebt internet nodig om het systeem bij te werken (hoofdstuk 3.3) en om de benodigde software te installeren (hoofdstuk 5).'
Shot 'install-3.1-wifi' 'De keuze van een wifi-netwerk tijdens de eerste start.'
Step $s '**Software bijwerken overslaan.** Verschijnt de vraag om software bij te werken, klik dan op **Skip**. Het systeem werk je straks bij in hoofdstuk 3.3.'
Step $s '**Afronden.** Klik op **Restart** (of **Done**). De Raspberry Pi start opnieuw op. Ga daarna verder met hoofdstuk 3.2.'
Callout 'info' 'Gebruikersnaam en wachtwoord' 'Gebruik hier altijd `user` en `user`. Die gegevens heb je later nodig om in te loggen op de SK-Box (hoofdstuk 14.3) en om bij te werken. Zie hoofdstuk 1.1 voor de opmerking over dit eenvoudige wachtwoord.'
Callout 'warn' 'Wifi alleen tijdelijk' 'Wifi of een netwerkkabel is alleen nodig tijdens de installatie (updates en software). Zet wifi na de eindcontrole weer uit, zoals beschreven in hoofdstuk 14. De SK-Box werkt daarna zonder internet.'
Callout 'info' 'Geen welkomstscherm?' 'Zie je het welkomstscherm niet, bijvoorbeeld omdat de gebruiker al in Raspberry Pi Imager is ingesteld, ga dan door naar hoofdstuk 3.2. Controleer wel dat de gebruikersnaam `user` en het wachtwoord `user` zijn. De teksten en de volgorde van de wizard kunnen per versie van Raspberry Pi OS iets verschillen.'

H2 '3.2 Basisconfiguratie'
Para 'Open een Terminal op de Raspberry Pi en start het configuratieprogramma:'
CodeBlock 'sudo raspi-config'
Shot 'install-3.2-raspi-config' 'Het hoofdmenu van raspi-config. Kies met de pijltjestoetsen en Enter.'
Para 'Stel de onderstaande onderdelen in:'
Tbl @('Onderdeel', 'Waarde', 'Waarom') @(
    @('System Options > Hostname', 'SK-Box', 'Herkenbare netwerknaam.'),
    @('System Options > Auto Login', 'Desktop autologin: Ja', 'Nodig voor het grafische opstarten.'),
    @('Localisation > Locale', 'nl_NL.UTF-8', 'Nederlandse tekens en notatie.'),
    @('Localisation > Timezone', 'Europe/Amsterdam', 'Juiste tijden in de wedstrijdbestanden.'),
    @('Localisation > WLAN Country', 'NL', 'Correcte wifi-kanalen en zendregels.'),
    @('Interface Options > SSH', 'Aan', 'Beheer vanaf een andere computer.'),
    @('Display Options > Screen Blanking', 'Uit', 'Het scorebord blijft zichtbaar.')
) @(3000, 2400, 4238)
Para 'Herstart de Raspberry Pi wanneer raspi-config daarom vraagt:'
CodeBlock 'sudo reboot'
Para 'Liever met de muis? Het schermblanking en het automatisch inloggen stel je ook grafisch in met het **Control Centre**:'
$s = New-StepList
Step $s '**Open het Control Centre.** Klik op het framboospictogram linksboven, kies **Preferences** en dan **Control Centre** (pijl 8).'
Shot 'install-3.2-controlecentrum-menu' 'Het menu Preferences met het Control Centre (8).'
Shot 'install-3.2-controlecentrum' 'Het Control Centre met links de onderdelen. Scroll in de lijst om de overige onderdelen te zien.'
Step $s '**Schermblanking uit.** Kies links **Display** en zet **Screen Blanking** uit (de schakelaar staat dan links, in het grijs).'
Shot 'install-3.2-schermblanking' 'Display: Screen Blanking staat uit.'
Step $s '**Autologin aan.** Kies links **System**. Zet **Boot** op **To Desktop** en zet **Desktop auto login** aan. Via **Change Hostname...** in dit scherm geef je de Raspberry Pi ook zijn herkenbare naam.'
Shot 'install-3.2-systeem' 'System: Boot staat op To Desktop en Desktop auto login staat aan.'

H2 '3.3 Systeem bijwerken'
CodeBlock @'
sudo apt update
sudo apt full-upgrade -y
sudo reboot
'@
Callout 'info' 'Waarom Desktop-autologin?' 'Een systeemdienst zonder grafische sessie kan een Tkinter-venster niet betrouwbaar op het HDMI-scherm openen. ScoreKrijt start daarom via de autostart van de ingelogde desktopgebruiker.'

H2 '3.4 Schermresolutie vastzetten op 1080p'
Para 'Raspberry Pi OS kiest zelf de hoogste resolutie die het scherm doorgeeft. Bij een scherm van 2K of 4K kost dat veel geheugen en verschijnen er meldingen als **High display resolution is using large amounts of memory**. Het scorebord heeft genoeg aan 1080p (1920 x 1080). Leg die resolutie daarom vast, zodat de Raspberry Pi hem niet meer automatisch verhoogt. Op een Raspberry Pi met weinig werkgeheugen scheelt dit merkbaar.'
$s = New-StepList
Step $s '**Maak een kopie** van het opstartbestand. Op Raspberry Pi OS Bookworm of nieuwer staat het in `/boot/firmware`; bij oudere versies in `/boot`.'
CodeBlock 'sudo cp /boot/firmware/cmdline.txt /boot/firmware/cmdline.txt.bak'
Step $s '**Open `cmdline.txt`:**'
CodeBlock 'sudo nano /boot/firmware/cmdline.txt'
Step $s '**Voeg de resolutie toe.** Het bestand bevat **één regel**; maak er geen tweede regel van. Ga naar het einde van die regel en voeg, na een spatie, toe:'
CodeBlock 'video=HDMI-A-1:1920x1080@60 video=HDMI-A-2:1920x1080@60'
Step $s 'Sla op met **Ctrl+O** en Enter en sluit af met **Ctrl+X**. Start daarna opnieuw op:'
CodeBlock 'sudo reboot'
Step $s '**Controleer de resolutie.** Na de herstart moet dit `1920,1080` tonen:'
CodeBlock 'cat /sys/class/graphics/fb0/virtual_size'
Callout 'info' 'Welke HDMI-poort?' '`HDMI-A-1` is de eerste HDMI-poort van de Raspberry Pi (bij een Pi 4 en Pi 5 de poort naast de voedingsaansluiting), `HDMI-A-2` de tweede. Een poort die je niet gebruikt of die niet bestaat, wordt genegeerd. Je mag beide regels dus altijd laten staan.'
Callout 'info' 'Kent je scherm geen 1080p?' 'Heeft je scherm geen 1920 x 1080-stand, bijvoorbeeld een oud 4:3-scherm, vervang dan `1920x1080` door een resolutie die het scherm wel ondersteunt, zoals `1280x1024`.'
Callout 'info' 'Terugdraaien of nu al op een hoge resolutie?' 'Haal de woorden `video=HDMI-A-...` uit `cmdline.txt` weg om de automatische keuze terug te krijgen, of zet de kopie `cmdline.txt.bak` terug. Staat de SK-Box nu al op een te hoge resolutie, dan gelden dezelfde stappen. Het script `sk-stille-opstart.sh` (hoofdstuk 13) zet dezelfde instelling, dus heb je dat al uitgevoerd, dan is dit hoofdstuk niet meer nodig.'

H1 '4. Netwerk en toegang op afstand'
Para 'Met SSH bedien je de Raspberry Pi vanaf je pc. Je hebt dit nodig voor het kopiëren van bestanden (hoofdstuk 6), het instellen van Bluetooth (hoofdstuk 8) en voor onderhoud zolang de SK-Box met een netwerk is verbonden. Updates installeer je later met een USB-stick.'
H2 '4.1 Hostnaam en IP-adres controleren'
CodeBlock @'
hostname
hostname -I
timedatectl
nmcli radio wifi
'@
H2 '4.2 Wifi verbinden'
Para 'Is de Raspberry Pi nog niet met wifi verbonden, gebruik dan:'
CodeBlock @'
nmcli device wifi list
nmcli device wifi connect "NAAM-VAN-WIFI" password "WIFI-WACHTWOORD"
'@
Callout 'warn' 'Wachtwoorden' 'Zet wifi-wachtwoorden niet in deze handleiding of in het project. Het nmcli-commando blijft in de shellgeschiedenis staan; stel wifi bij voorkeur in met Raspberry Pi Imager.'
H2 '4.3 Verbinden via SSH'
Para 'Open PowerShell op je pc en maak verbinding:'
CodeBlock 'ssh user@SK-Box.local'
Para 'Werkt de naam `SK-Box.local` niet, gebruik dan het IP-adres:'
CodeBlock 'ssh user@<IP-adres>'

H1 '5. Benodigde software installeren'
CodeBlock @'
sudo apt update
sudo apt install -y python3 python3-tk python3-pil python3-pil.imagetk
sudo apt install -y python3-serial bluez bluez-tools rfkill
'@
Para 'Controleer of alles is geïnstalleerd:'
CodeBlock @'
python3 --version
python3 -c "import tkinter; print('Tkinter OK')"
python3 -c "from PIL import Image, ImageTk; print('Pillow OK')"
python3 -c "import serial; print('pyserial OK')"
bluetoothctl --version
'@
Shot 'install-5-controle' 'De controleopdrachten: Tkinter OK, Pillow OK en pyserial OK.'

H1 '6. Programmabestanden op de SK-Box zetten'
H2 '6.1 Doelmap maken'
Para 'Voer op de Raspberry Pi uit:'
CodeBlock @'
mkdir -p "$HOME/ScoreKrijt"
chmod 755 "$HOME/ScoreKrijt"
'@
H2 '6.2 Kopiëren via USB'
Para 'Breng de programmabestanden met een USB-stick van je pc naar de SK-Box. Eerst zet je ze op de stick:'
$s = New-StepList
Step $s ('**Kopieer de bestanden.** Open op je pc de map ' + $MapC + ' in de uitgepakte download (hoofdstuk 2.1) en selecteer alle onderdelen (pijl 4): `ScoreKrijt`, `ScoreKrijt.py`, `ScoreKrijt.spec`, `scorekrijt_launcher.py` en `ScoreKrijtSettings.json`. Klik met de rechtermuisknop op de selectie en kies **Kopiëren** (pijl 5).')
Shot 'install-6.2-kopieren' 'Alle onderdelen van de programmamap selecteren (4) en kopiëren (5).'
Step $s '**Open de USB-stick** en daarin de map `ScoreKrijt_update`. Bestaat die map nog niet, maak hem dan aan.'
Shot 'install-6.2-usbstick' 'De USB-stick met de map `ScoreKrijt_update`.'
Step $s '**Plak de bestanden.** Klik met de rechtermuisknop in de lege map (pijl 6) en kies **Plakken** (pijl 7).'
Shot 'install-6.2-plakken' 'Met de rechtermuisknop in de map (6) en Plakken (7) komen de bestanden op de stick.'
Step $s '**Zet ook de hulpscripts op de stick.** Kopieer op dezelfde manier de hele map `SK-Box_scripts` uit de map `Phyton` van de download naar de hoofdmap van de stick, naast `ScoreKrijt_update`. De twee scripts daarin heb je later nodig (hoofdstuk 6.4). Gebruik daarna **Hardware veilig verwijderen** in Windows voordat je de stick uit de pc haalt.'
Shot 'install-6.2-scripts' 'De USB-stick met de mappen `ScoreKrijt_update` en `SK-Box_scripts`.'
Step $s '**Zet de bestanden op de SK-Box.** Steek de stick in de SK-Box. Er verschijnt de melding **Removable medium is inserted**; klik op **OK** (pijl 11) om de bestandsbeheerder te openen. Kopieer daarin de volledige inhoud van de map `ScoreKrijt_update` naar de map `ScoreKrijt` in de thuismap. De scripts uit `SK-Box_scripts` zet je daarna neer zoals in hoofdstuk 6.4. Draait ScoreKrijt al op de SK-Box en zie je geen taakbalk, druk dan op **F12** om de taakbalk te tonen (zie hoofdstuk 13.5).'
Shot 'install-6.2-sk-usb-melding' 'De melding bij het insteken van de stick: klik op OK (11).'
Para 'Controleer daarna op de SK-Box of de volgende bestanden bestaan:'
CodeBlock @'
cd "$HOME/ScoreKrijt"
ls -la
test -f ScoreKrijt.py && echo "ScoreKrijt.py OK"
test -f scorekrijt_launcher.py && echo "launcher OK"
test -f ScoreKrijtSettings.json && echo "instellingen OK"
test -d ScoreKrijt/icons && echo "icons OK"
'@
Shot 'install-6.2-controle' 'De inhoud van de map ScoreKrijt met de eerste controle (ScoreKrijt.py OK).'
H2 '6.3 Alternatief: kopiëren via SCP'
Para ('Open PowerShell op je pc, ga naar de map ' + $MapC + ' en voer uit:')
CodeBlock @'
$box = "user@SK-Box.local"
scp -r ScoreKrijt ScoreKrijt.py scorekrijt_launcher.py ScoreKrijtSettings.json "${box}:ScoreKrijt/"
'@
Callout 'info' 'Mapstructuur' 'Kopieer de hele inhoud van de programmamap, niet alleen `ScoreKrijt.py`. De submap `ScoreKrijt` (met de iconen), de launcher en `ScoreKrijtSettings.json` zijn allemaal nodig.'
H2 '6.4 Hulpscripts op de SK-Box zetten'
Para 'In de map `Phyton\SK-Box_scripts` staan twee hulpscripts. Je hebt ze in hoofdstuk 6.2 al op de USB-stick gezet. Zet ze nu alvast op de SK-Box, want je hebt ze later nodig zonder internet:'
Tbl @('Script', 'Doel', 'Beschreven in') @(
    @('`sk-stille-opstart.sh`', 'Verbergt de Raspberry Pi-logo''s en opstarttekst en zet wifi uit.', 'Hoofdstuk 13 en 14'),
    @('`sk-update.sh`', 'Werkt ScoreKrijt bij vanaf een USB-stick.', 'Handleiding SK-Box bijwerken')
) @(2900, 4538, 2200)
Shot 'install-6.4-scripts-plakken' 'De scripts plakken in de thuismap met Paste (12).'
Para 'Kopieer beide bestanden met de bestandsbeheerder van de stick naar de thuismap van de SK-Box, of via SCP vanaf je pc. Open met de stick in de SK-Box de map `SK-Box_scripts`, selecteer de twee scripts en kopieer ze. Open daarna de thuismap, klik met de rechtermuisknop in een lege plek en kies **Paste** (pijl 12). Start ze daarna altijd met `bash` ervoor, zoals in deze handleiding. Bestanden die via een USB-stick of Windows zijn gekopieerd, hebben vaak geen uitvoerrecht en geven dan foutcode 126 (Permission denied). Het uitvoerrecht zet je zo alsnog:'
CodeBlock @'
chmod +x ~/sk-update.sh ~/sk-stille-opstart.sh
ls -l ~/sk-*.sh
'@

H1 '7. Eerste test'
Para 'Start ScoreKrijt handmatig op de Raspberry Pi, vanuit een Terminal op de Desktop:'
CodeBlock @'
cd "$HOME/ScoreKrijt"
python3 ScoreKrijt.py
'@
Para 'Controleer of het hoofdvenster en het grote scorebord openen. Sluit de toepassing daarna normaal af en test de kiosklauncher:'
CodeBlock @'
cd "$HOME/ScoreKrijt"
python3 scorekrijt_launcher.py
'@
Para 'De launcher toont een zwart opstartscherm met het logo en de melding "SK-Box wordt gestart" met bewegende puntjes. Het scherm blijft staan tot ScoreKrijt klaar is (minimaal 3 en hoogstens 90 seconden), start ScoreKrijt en schrijft eventuele fouten naar `scorekrijt-autostart.log`.'

H1 '8. Bluetooth instellen'
H2 '8.1 Bluetooth inschakelen'
CodeBlock @'
sudo systemctl enable --now bluetooth
sudo rfkill unblock bluetooth
systemctl is-active bluetooth
bluetoothctl show
'@
H2 '8.2 Automatisch koppelen zonder bevestigingsvenster'
Para 'De SK-Box heeft tijdens normaal gebruik geen muis of toetsenbord nodig. Met onderstaande service wordt Bluetooth bij iedere start automatisch ingeschakeld, zichtbaar en koppelbaar gemaakt. Voer deze stappen eenmalig uit via SSH.'
$s = New-StepList
Step $s '**Controleer de Bluetooth-agent.** Het pakket `bluez-tools` is in hoofdstuk 5 al geïnstalleerd. Doe je dit niet, installeer het dan alsnog:'
CodeBlock 'sudo apt install -y bluez-tools'
Step $s '**Maak de service aan:**'
CodeBlock 'sudo nano /etc/systemd/system/scorekrijt-pairing.service'
Step $s '**Plak de volgende inhoud** en sla op met Ctrl+O, Enter. Sluit nano af met Ctrl+X.'
CodeBlock @'
[Unit]
Description=Automatische Bluetooth-koppeling voor ScoreKrijt
Requires=bluetooth.service
After=bluetooth.service display-manager.service

[Service]
Type=simple
ExecStartPre=/bin/sleep 10
ExecStartPre=/usr/bin/bluetoothctl power on
ExecStartPre=/usr/bin/bluetoothctl pairable on
ExecStartPre=/usr/bin/bluetoothctl discoverable-timeout 0
ExecStartPre=/usr/bin/bluetoothctl discoverable on
ExecStart=/usr/bin/bt-agent -c NoInputNoOutput
Restart=always
RestartSec=2

[Install]
WantedBy=graphical.target
'@
Shot 'install-8.2-nano-service' 'Het servicebestand in nano. Sla op met Ctrl+O en Enter en sluit af met Ctrl+X.'
Step $s '**Activeer de service** en start de Raspberry Pi opnieuw op:'
CodeBlock @'
sudo systemctl daemon-reload
sudo systemctl enable --now scorekrijt-pairing.service
sudo reboot
'@
Step $s '**Controleer na het opstarten** via SSH:'
CodeBlock @'
systemctl status scorekrijt-pairing.service --no-pager
bluetoothctl show
'@
Step $s 'Bij `bluetoothctl show` moeten **Powered**, **Discoverable** en **Pairable** op `yes` staan.'
Shot 'install-8.2-bluetoothctl-show' 'De uitvoer van bluetoothctl show met Powered, Discoverable en Pairable op yes.'
Step $s '**Koppel de telefoon.** Open op de telefoon de Bluetooth-instellingen en kies de SK-Box. Op de SK-Box verschijnt geen bevestigingsvenster; op de telefoon kan wel een koppelingsmelding verschijnen.'
Step $s '**Controleer of de koppeling is opgeslagen.** Voer na het koppelen uit op de SK-Box. De telefoon moet in de lijst staan:'
CodeBlock 'bluetoothctl devices Paired'
Callout 'info' 'Meerdere telefoons' 'Er kunnen meerdere telefoons met de SK-Box zijn gekoppeld, maar er kan steeds maar één telefoon tegelijk met het scoreprogramma verbonden zijn. Verbreek eerst de verbinding op de ene telefoon voordat een andere verbindt.'
Callout 'warn' 'Veiligheid' 'De SK-Box blijft continu zichtbaar en koppelbaar. Gebruik deze instelling alleen in een vertrouwde omgeving.'

H1 '9. RFCOMM-poort maken'
Para 'De Android-app verbindt via Bluetooth Classic (SPP). De SK-Box luistert daarbij op kanaal 1 en maakt de seriële poort `/dev/rfcomm0` beschikbaar voor ScoreKrijt.'
H2 '9.1 Handmatig testen'
CodeBlock 'sudo rfcomm watch /dev/rfcomm0 1'
Para 'Laat dit Terminalvenster open en maak vanuit de Android-app verbinding. Controleer in een tweede Terminal:'
CodeBlock @'
ls -l /dev/rfcomm0
sudo rfcomm show /dev/rfcomm0
'@
Para 'Stop de handmatige test met Ctrl+C.'
H2 '9.2 Automatisch luisteren met systemd'
$s = New-StepList
Step $s '**Maak het servicebestand:**'
CodeBlock 'sudo nano /etc/systemd/system/scorekrijt-rfcomm.service'
Step $s '**Plak de volgende inhoud** en sla op met Ctrl+O, Enter. Sluit nano af met Ctrl+X.'
CodeBlock @'
[Unit]
Description=ScoreKrijt Bluetooth RFCOMM listener
After=bluetooth.service
Requires=bluetooth.service

[Service]
Type=simple
ExecStart=/usr/bin/rfcomm watch /dev/rfcomm0 1
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
'@
Step $s '**Activeer de service:**'
CodeBlock @'
sudo systemctl daemon-reload
sudo systemctl enable --now scorekrijt-rfcomm.service
systemctl status scorekrijt-rfcomm.service --no-pager
'@
Callout 'info' 'De poort verschijnt pas bij verbinding' 'Bij `rfcomm watch` wordt `/dev/rfcomm0` pas zichtbaar wanneer de Android-app daadwerkelijk verbindt. ScoreKrijt probeert zelf iedere twee seconden opnieuw, dus de opstartvolgorde is niet kritisch.'

H1 '10. Toegang tot /dev/rfcomm0'
Para 'Controleer eigenaar en groep zodra de poort bestaat (verbind daarvoor eerst vanuit de app):'
CodeBlock 'ls -l /dev/rfcomm0'
Para 'Behoort de poort tot de groep `dialout`, voeg dan eenmalig de desktopgebruiker aan die groep toe:'
CodeBlock @'
sudo usermod -aG dialout "$USER"
sudo reboot
'@
Callout 'warn' 'Geen chmod 777' 'Maak de Bluetooth-poort niet voor iedereen schrijfbaar. Gebruik groepsrechten via `dialout`; dat is veiliger en beter te beheren.'

H1 '11. ScoreKrijt automatisch starten'
H2 '11.1 Autostartbestand maken'
$s = New-StepList
Step $s '**Maak het bestand aan:**'
CodeBlock @'
mkdir -p "$HOME/.config/autostart"
nano "$HOME/.config/autostart/scorekrijt.desktop"
'@
Step $s '**Plak de volgende inhoud.** De gebruikersnaam is `user`; heeft jouw SK-Box een andere gebruiker, vervang `user` dan door die naam:'
CodeBlock @'
[Desktop Entry]
Type=Application
Name=ScoreKrijt SK-Box
Comment=Start ScoreKrijt in kioskmodus
Exec=/usr/bin/python3 /home/user/ScoreKrijt/scorekrijt_launcher.py
Path=/home/user/ScoreKrijt
Terminal=false
X-GNOME-Autostart-enabled=true
'@
Step $s '**Controleer het bestand:**'
CodeBlock @'
desktop-file-validate "$HOME/.config/autostart/scorekrijt.desktop" 2>/dev/null || true
cat "$HOME/.config/autostart/scorekrijt.desktop"
'@
H2 '11.2 Autostart testen'
CodeBlock 'sudo reboot'
Para 'Na de automatische aanmelding op de Desktop verschijnt eerst het ScoreKrijt-opstartscherm met de melding dat de SK-Box opstart, gevolgd door het grote ScoreKrijt-scherm.'

H1 '12. ScoreKrijt-instellingen voor de SK-Box'
Para 'Open zo nodig het normale ScoreKrijt-venster en ga naar **Weergave**. Dit zijn de aanbevolen waarden voor de SK-Box:'
Tbl @('Instelling', 'Waarde', 'Opmerking') @(
    @('BlueTooth Mode', 'Aan', 'Start de Bluetooth-service in ScoreKrijt.'),
    @('Groot scherm', 'Aan', 'Opent het externe scorebord.'),
    @('Open groot scherm fullscreen', 'Aan', 'Verbergt het normale venster en vult het HDMI-scherm.'),
    @('Geschiedenis', 'Aan', 'Toont de recente beurten op het scorebord.'),
    @('Wedstrijdoverzicht', 'Uit', 'De Android-app handelt het einde van de wedstrijd af.'),
    @('Wedstrijd mailen', 'Uit', 'Geen e-mailactie op de SK-Box.'),
    @('Nieuwe wedstrijd automatisch', 'Uit', 'De Android-app bepaalt de volgende start.')
) @(3300, 1300, 5038)
Callout 'warn' 'Configuratiebestand' 'In de projectmap staat `BlueTooth Mode` op uit. Zet de optie in de toepassing aan en sluit ScoreKrijt normaal af, zodat de instelling wordt opgeslagen.'
Callout 'info' 'Lettergroottes instellen' 'De lettergrootte van het scorebord, het geschiedenisvak en het aantal getoonde beurten pas je daarna aan met de ScoreKrijt-app op de telefoon, via de knop **SK-Box-instellingen**.'

H1 '13. Stille opstart zonder Raspberry Pi-logo''s'
Para 'Standaard toont een Raspberry Pi tijdens het opstarten een regenboogscherm, vier framboosjes, een stroom opstarttekst, het Raspberry Pi-opstartlogo en daarna het bureaublad met taakbalk. Voor een scorebord in een café of clubhuis wil je dat niet zien. Met onderstaande aanpassingen blijft het scherm zwart totdat het bureaublad klaar is. Daarna zie je het ScoreKrijt-logo, gevolgd door het ScoreKrijt-opstartscherm en het scorebord.'
Callout 'warn' 'Doe dit pas als alles werkt' 'Voer dit hoofdstuk en hoofdstuk 14 pas uit na de eindcontrole van hoofdstuk 15. Zodra de opstarttekst weg is, zie je geen foutmeldingen meer tijdens het opstarten, en voor de installatie van pakketten (hoofdstuk 3 en 5) is internet nodig.'
H2 '13.1 Wat verandert er?'
Tbl @('Wat je ziet', 'Zonder aanpassing', 'Na de aanpassing') @(
    @('Regenboogscherm van de firmware', 'Zichtbaar', 'Weg (`disable_splash=1`)'),
    @('Vier framboosjes linksboven', 'Zichtbaar', 'Weg (`logo.nologo`)'),
    @('Opstarttekst van Linux', 'Zichtbaar', 'Weg (`quiet`, `loglevel=3`, `console=tty3`)'),
    @('Raspberry Pi-opstartlogo met balk', 'Zichtbaar', 'Vervangen door het ScoreKrijt-logo (`splash`); zonder logo weg (`plymouth.enable=0`)'),
    @('Knipperende cursor', 'Zichtbaar', 'Weg (`vt.global_cursor_default=0`)'),
    @('Schermresolutie', 'Hoogste resolutie die het scherm opgeeft', 'Vast op 1080p (`video=HDMI-A-1:1920x1080@60`, zie hoofdstuk 3.4)'),
    @('Taakbalk', 'Kort zichtbaar voor ScoreKrijt start', 'Weg uit `/etc/xdg/labwc/autostart`'),
    @('Bureaubladachtergrond', 'Raspberry Pi-achtergrond met pictogrammen', 'Zwart met het ScoreKrijt-logo, zonder pictogrammen')
) @(3300, 2900, 3438)
H2 '13.2 Automatisch doorvoeren (aanbevolen)'
Para 'Het script `sk-stille-opstart.sh` voert alle wijzigingen door en bewaart van elk bestand een kopie met de extensie `.sk-origineel`. Voer uit op de SK-Box, als gewone gebruiker (dus zonder `sudo`):'
CodeBlock 'bash ~/sk-stille-opstart.sh'
Para 'Wil je meteen ook wifi uitzetten (zie hoofdstuk 14), gebruik dan:'
CodeBlock 'bash ~/sk-stille-opstart.sh --wifi-uit'
Para 'Wil je het opstarten ongeveer drie seconden korter maken, voeg dan `--sneller` toe. Het script zet dan `cloud-init` uit, het installatieprogramma voor de allereerste start van de Pi. Dat is optioneel; met `--terugdraaien` staat het weer aan.'
Para 'Het script zet ook de schermresolutie vast op 1080p (zie hoofdstuk 3.4). Heeft je scherm een andere resolutie nodig, geef die dan mee met bijvoorbeeld `--resolutie=1280x720`. Wil je de resolutie niet laten vastzetten, gebruik dan `--geen-resolutie`.'
Para 'Het script laat zien wat het gaat wijzigen en vraagt eerst om bevestiging. Typ **j** en druk op Enter om door te gaan; met alleen Enter breekt het script af en blijft alles zoals het was.'
Shot 'install-13.2-script' 'De bevestigingsvraag van het script, hier beantwoord met j.'
Para 'Aan het eind meldt het script wat het heeft gewijzigd en hoe je het terugdraait. Start daarna opnieuw op:'
Shot 'install-13.2-script-klaar' 'Het slot van het script, met de aanwijzing om opnieuw op te starten.'
CodeBlock 'sudo reboot'
Callout 'warn' 'SSH via wifi stopt met werken' 'Met `--wifi-uit` kun je de SK-Box niet meer via wifi bereiken. Controleer eerst of ScoreKrijt en Bluetooth goed werken en zorg dat je een toetsenbord hebt aangesloten voor het geval je iets wilt aanpassen (zie hoofdstuk 14.3).'
H2 '13.3 Handmatig doorvoeren'
Para 'Liever zelf doen, of werkt het script niet? Maak eerst een kopie van de twee opstartbestanden. Op Raspberry Pi OS Bookworm of nieuwer staan ze in `/boot/firmware`; bij oudere versies in `/boot`.'
CodeBlock @'
sudo cp /boot/firmware/cmdline.txt /boot/firmware/cmdline.txt.sk-origineel
sudo cp /boot/firmware/config.txt /boot/firmware/config.txt.sk-origineel
'@
$s = New-StepList
Step $s '**Open `cmdline.txt`:**'
CodeBlock 'sudo nano /boot/firmware/cmdline.txt'
Step $s '**Pas de regel aan.** Het bestand bevat **één regel**; maak er geen tweede regel van. Vervang `console=tty1` door `console=tty3`, haal bestaande woorden `quiet`, `splash` en `loglevel=...` weg en voeg achteraan, na een spatie, toe:'
CodeBlock 'quiet loglevel=3 logo.nologo vt.global_cursor_default=0 video=HDMI-A-1:1920x1080@60 video=HDMI-A-2:1920x1080@60 splash'
Para 'Wil je tijdens het opstarten geen logo maar een zwart scherm, laat dan `splash` weg en voeg `plymouth.enable=0` toe. Voor het ScoreKrijt-logo vervang je het bestand `/usr/share/plymouth/themes/pix/splash.png` door een verkleind logo (het logo `ScoreKrijt Logo.png`, verkleind tot 480 x 480 pixels) en voer je daarna `sudo update-initramfs -u` uit als er een bestand `initramfs` in `/boot/firmware` staat. Het script doet dit allemaal voor je.'
Step $s '**Open `config.txt`** en voeg onderaan toe:'
CodeBlock @'
sudo nano /boot/firmware/config.txt
'@
CodeBlock @'
[all]
disable_splash=1
boot_delay=0
'@
Step $s '**Taakbalk verbergen (alleen bij `labwc`).** Maak een kopie van het systeembestand en zet in het origineel voor de regel met `wf-panel-pi` een `#`. Laat de regel met `pcmanfm-pi` staan; die zorgt voor de achtergrond:'
CodeBlock @'
sudo cp /etc/xdg/labwc/autostart /etc/xdg/labwc/autostart.sk-origineel
sudo nano /etc/xdg/labwc/autostart
'@
Step $s 'Laat de regel met `lxsession-xdg-autostart` staan. Die start het ScoreKrijt-autostartbestand uit hoofdstuk 11.'
Callout 'warn' 'Maak geen eigen kopie in `~/.config/labwc`' 'Raspberry Pi OS voert het systeembestand ook uit als er een eigen `autostart` in je thuismap staat. Een kopie daar laat de taakbalk dus gewoon draaien en start alles dubbel, waaronder ScoreKrijt. Staat er al zo''n kopie van een eerdere versie van het script, verwijder die dan met `rm ~/.config/labwc/autostart`, maar alleen als je er zelf niets in hebt gezet.'
Step $s '**Achtergrond met logo.** Doe dit op de SK-Box zolang de taakbalk nog zichtbaar is: klik met de rechtermuisknop op het bureaublad en kies **Bureaubladvoorkeuren**. Kies als afbeelding `ScoreKrijt/ScoreKrijt/icons/ScoreKrijt Logo.png` in je thuismap, stel de modus in op **Centreren**, de kleur op zwart en zet de bureaubladpictogrammen uit.'
Step $s '**Start opnieuw op:**'
CodeBlock 'sudo reboot'
Callout 'info' 'Een ander bureaublad dan labwc' 'Gebruikt je Raspberry Pi OS het oudere Wayfire (`~/.config/wayfire.ini`, sectie `[autostart]`) of X11 (`~/.config/lxsession/LXDE-pi/autostart`), haal dan op dezelfde manier de regels weg die de taakbalk en de bureaubladachtergrond starten. Controleer met `echo $XDG_CURRENT_DESKTOP` welk bureaublad actief is.'
H2 '13.4 Terugdraaien'
Para 'Met het script zet je alles terug, ook het wifi-gebruik:'
CodeBlock 'bash ~/sk-stille-opstart.sh --terugdraaien'
Para 'Start de SK-Box na een foutieve aanpassing niet meer op, dan kun je de kopieën met de hand terugzetten:'
$s = New-StepList
Step $s 'Schakel de SK-Box uit en haal de microSD-kaart eruit. Bij de geprinte SK-Box haal je eerst de Raspberry Pi uit de behuizing (zie hoofdstuk 2.2). De kaart haal je alleen voor dit herstel uit de Raspberry Pi.'
Step $s 'Steek de kaart in een pc met Windows. Er verschijnt een schijf met de naam **bootfs** (of **boot**; de overige delen van de kaart kan Windows niet lezen; daar hoef je niets mee).'
Step $s 'Verwijder `cmdline.txt` en hernoem `cmdline.txt.sk-origineel` naar `cmdline.txt`. Doe hetzelfde voor `config.txt`.'
Step $s 'Zet de kaart terug in de SK-Box en start op.'
Callout 'info' 'Het ScoreKrijt-logo tijdens het opstarten' 'Het opstartscherm van Linux toont nu het ScoreKrijt-logo in plaats van het Raspberry Pi-logo. Alleen de allereerste seconden, tot Linux het scherm overneemt, blijft het zwart. Daarna volgen het bureaublad met het logo en het opstartscherm uit hoofdstuk 7 met "SK-Box wordt gestart", tot het scorebord klaar is. Lukt het opstartlogo niet (bijvoorbeeld door een ander Plymouth-thema), dan meldt het script dat en blijft het scherm tijdens het opstarten zwart.'
H2 '13.5 De taakbalk tijdelijk tonen (F12)'
Para 'Zonder taakbalk kom je niet makkelijk bij het bureaublad, bijvoorbeeld om een USB-stick te openen of een Terminal te starten. Met een toetsenbord aan de SK-Box doe je dat zo:'
$s = New-StepList
Step $s 'Druk op **F12** terwijl het scorebord in beeld is. Het scorebord verlaat het volledige scherm en de taakbalk verschijnt. Staat het grote scherm niet aan en zie je het gewone ScoreKrijt-venster, druk dan in dat venster op **F12**; de taakbalk verschijnt dan naast het venster.'
Shot 'install-13.5-taakbalk' 'Het scorebord met de taakbalk bovenaan na het drukken op F12, met onder meer de bestandsbeheerder en de Terminal.'
Step $s 'Werk met de taakbalk, bijvoorbeeld een Terminal of de bestandsbeheerder. Voor een Terminal klik je op het zwarte pictogram met de prompt (pijl 9); het Terminalvenster opent daarna (pijl 10).'
Shot 'install-13.5-terminal' 'Een Terminal starten vanaf de taakbalk (9); het venster opent in beeld (10).'
Step $s 'Druk opnieuw op **F12**. De taakbalk verdwijnt. Het scorebord vult weer het hele scherm, als het grote scherm aan staat.'
Callout 'info' 'Hulp als F12 niets doet' 'F12 werkt alleen als het scorebord of het gewone ScoreKrijt-venster het actieve venster is en de taakbalk op deze SK-Box is geïnstalleerd (`wf-panel-pi`). Lukt het niet, gebruik dan Ctrl+Alt+F2 voor een tekstscherm (hoofdstuk 14.3).'

H1 '14. Gebruik zonder internet'
Para 'De SK-Box heeft tijdens het spelen geen internet nodig: de bediening gaat via Bluetooth en alle bestanden staan op de SK-Box zelf. Het is daarom veilig en prima mogelijk om de SK-Box nooit met internet te verbinden. Updates installeer je dan met een USB-stick (zie de handleiding **SK-Box bijwerken**).'
H2 '14.1 Wifi en netwerk uitschakelen'
Para 'Zet wifi uit. Bluetooth blijft aan en is niet afhankelijk van wifi:'
CodeBlock @'
sudo nmcli radio wifi off
nmcli radio
'@
Para 'In de uitvoer moet bij `WIFI` de waarde `disabled` staan. Deze instelling blijft na een herstart behouden. Wil je wifi later weer gebruiken, bijvoorbeeld voor een nieuw OS-pakket:'
CodeBlock 'sudo nmcli radio wifi on'
Bullet 'Steek geen netwerkkabel in de SK-Box. Zonder kabel en zonder wifi kan er geen verbinding met internet ontstaan.'
Bullet 'De opgeslagen wifi-gegevens blijven bewaard en worden gebruikt zodra wifi weer aan staat. Mag de SK-Box nooit meer met wifi verbinden, verwijder ze dan met `nmcli connection show` en `sudo nmcli connection delete "<naam>"`.'
Callout 'info' 'Controleer dat er geen verbinding is' 'Met `hostname -I` zie je alle IP-adressen. Zonder netwerkverbinding blijft die uitvoer leeg of toont alleen een adres dat met `169.254` begint. Beide betekenen: geen internet.'
H2 '14.2 Datum en tijd'
Para 'Zonder internet kan de SK-Box de tijd niet meer van het netwerk halen. Een Raspberry Pi 4 of ouder heeft geen batterij voor de klok en begint na stroomuitval met de laatste opgeslagen tijd. Daardoor kunnen datums in bestanden en logboeken verkeerd zijn.'
Tbl @('Model', 'Klok bij stroomuitval', 'Aanbeveling') @(
    @('Raspberry Pi 5', 'Heeft een ingebouwde klok; die loopt door met een optionele batterij op de RTC-aansluiting.', 'Sluit de officiële RTC-batterij aan.'),
    @('Raspberry Pi 4 en ouder', 'Geen klok; de tijd loopt niet door.', 'Gebruik een RTC-module of stel de tijd handmatig in.')
) @(2500, 4138, 3000)
Para 'De tijd handmatig instellen doe je zo, met je eigen datum en tijd:'
CodeBlock @'
sudo timedatectl set-ntp false
sudo timedatectl set-time "2026-10-18 14:30:00"
timedatectl
'@
H2 '14.3 Bij de SK-Box komen zonder netwerk'
Para 'Zonder wifi werkt SSH via wifi niet. Sluit voor onderhoud een toetsenbord aan op de SK-Box en open een Terminal zo:'
$s = New-StepList
Step $s 'Druk op **Ctrl+Alt+F2**. Er verschijnt een tekstscherm met een inlogprompt.'
Step $s 'Meld je aan met gebruikersnaam `user` en wachtwoord `user`.'
Step $s 'Voer je opdrachten uit, bijvoorbeeld `bash ~/sk-update.sh`.'
Step $s 'Keer terug met **Ctrl+Alt+F1**, of start de SK-Box opnieuw op met `sudo reboot`.'
Callout 'info' 'Inloggegevens' 'De gebruikersnaam van de SK-Box is `user` en het wachtwoord is `user`. Verander je het wachtwoord, bewaar het dan op een veilige plek, bijvoorbeeld in de beheerdersmap van de club. Zonder die gegevens kun je de SK-Box niet meer bijwerken.'
H2 '14.4 Updates zonder internet'
Bullet '**ScoreKrijt zelf:** bijwerken met een USB-stick en het script `sk-update.sh`. Zie de handleiding **SK-Box bijwerken**.'
Bullet '**Raspberry Pi OS:** hoeft niet bijgewerkt te worden voor een gesloten scorebord. Wil je dat toch, zet dan tijdelijk wifi aan (`sudo nmcli radio wifi on`), voer hoofdstuk 3.3 uit en zet wifi daarna weer uit.'

H1 '15. Eindcontrole'
Para 'Loop onderstaande punten na. Alles moet werken zonder toetsenbord of muis.'
Check 'De Raspberry Pi meldt zichzelf automatisch aan op de Desktop.'
Check 'Het scherm wordt niet zwart bij inactiviteit.'
Check 'Het scherm staat op 1080p: `cat /sys/class/graphics/fb0/virtual_size` toont `1920,1080` (hoofdstuk 3.4).'
Check 'Het ScoreKrijt-opstartscherm met "SK-Box wordt gestart" blijft staan tot het scorebord klaar is.'
Check 'Het grote scorebord opent op het volledige scherm.'
Check 'De services `bluetooth`, `scorekrijt-pairing` en `scorekrijt-rfcomm` zijn actief.'
Check 'De telefoon kan koppelen en verbinden met de SK-Box.'
Check 'Plus, min, Noteer en Return werken op telefoon en SK-Box tegelijk.'
Check 'Na een herstart werkt alles opnieuw zonder ingrijpen.'
Para 'Voer deze punten pas uit als je hoofdstuk 13 en 14 hebt gedaan:'
Check 'Tijdens het opstarten zijn geen Raspberry Pi-logo''s, opstarttekst of taakbalk te zien.'
Check 'Wifi staat uit (`nmcli radio` toont `disabled`) en er zit geen netwerkkabel in.'
Check 'Ctrl+Alt+F2 geeft een inlogprompt en met `bash ~/sk-update.sh --help` verschijnt de uitleg.'
Check 'Datum en tijd zijn na een herstart nog bruikbaar (zie hoofdstuk 14.2).'
Spacer
Para 'Handige controleopdrachten:'
CodeBlock @'
systemctl is-active bluetooth
systemctl is-enabled scorekrijt-pairing.service scorekrijt-rfcomm.service
journalctl -u scorekrijt-rfcomm.service -n 30 --no-pager
tail -n 50 "$HOME/ScoreKrijt/scorekrijt-autostart.log"
'@

H1 '16. Storingen oplossen'
Tbl @('Probleem', 'Controle', 'Oplossing') @(
    @('Zwart scherm en ScoreKrijt start niet', 'Stille opstart actief', 'Druk op Ctrl+Alt+F2, log in en lees `tail -n 50 ~/ScoreKrijt/scorekrijt-autostart.log`. Draai zo nodig hoofdstuk 13.4 terug.'),
    @('SK-Box start niet meer op na hoofdstuk 13', '`cmdline.txt` beschadigd', 'Zet de kopieën `.sk-origineel` terug via een pc (hoofdstuk 13.4).'),
    @('Taakbalk of bureaublad blijft zichtbaar', 'Ander bureaublad dan `labwc`', 'Zie de opmerking onder hoofdstuk 13.3.'),
    @('Datum en tijd kloppen niet', 'Geen netwerktijd', 'Stel de tijd handmatig in (hoofdstuk 14.2).'),
    @('Geen volledig scherm', 'Autologin en `.desktop`-bestand', 'Test de launcher handmatig vanaf de Desktop.'),
    @('Scherm wordt zwart', 'Screen Blanking', 'Zet dit uit via `raspi-config`.'),
    @('Melding over veel geheugengebruik door de schermresolutie', 'Scherm staat hoger dan 1080p', 'Zet de resolutie vast op 1080p (hoofdstuk 3.4).'),
    @('Geen `/dev/rfcomm0`', 'RFCOMM-service en verbinding', 'Controleer `journalctl` en verbind vanuit de app.'),
    @('Permission denied', 'Groep van de poort', 'Voeg de gebruiker toe aan `dialout` en herstart.'),
    @('SK-Box niet zichtbaar op de telefoon', 'Koppelservice', 'Controleer met `systemctl status scorekrijt-pairing.service --no-pager` of de service draait en met `bluetoothctl show` of Powered, Discoverable en Pairable op `yes` staan.'),
    @('Verbinding valt elke 30 seconden weg', 'Telefoon is niet echt gekoppeld (BlueZ ruimt de tijdelijke koppeling na 30 seconden op)', 'Maak de koppeling opnieuw: vergeet de SK-Box op de telefoon, voer op de SK-Box `sudo rm -rf /var/lib/bluetooth/<adapter-adres>/<telefoon-adres>` en `sudo systemctl restart bluetooth` uit en koppel opnieuw (hoofdstuk 8.2). Zie het adres in `journalctl -u bluetooth`.'),
    @('Tkinter ontbreekt', 'Pakket `python3-tk`', 'Installeer het pakket met apt.'),
    @('Pillow-fout', 'Pakket `python3-pil.imagetk`', 'Installeer beide Pillow-pakketten.'),
    @('pyserial-fout', 'Pakket `python3-serial`', 'Installeer het pakket met apt.'),
    @('App start niet', 'Autostartlog', 'Lees `scorekrijt-autostart.log` in de programmamap.'),
    @('Verkeerd lettertype', 'Is Bodoni beschikbaar?', 'Installeer een gelicentieerd lettertype of kies een lettertype dat aanwezig is.')
) @(2500, 2700, 4438)

H1 '17. Programma later bijwerken'
Para 'Een nieuwe versie van ScoreKrijt installeer je niet opnieuw vanaf nul. Volg daarvoor de aparte handleiding **SK-Box bijwerken**. Die werkt met een USB-stick, dus zonder internet, behoudt je instellingen en wedstrijdbestanden en maakt terugdraaien mogelijk.'

H1 '18. Bronnen'
Para 'De systeemstappen zijn gecontroleerd tegen onderstaande bronnen. Menunamen in `raspi-config` en het autostartgedrag kunnen in nieuwe versies van Raspberry Pi OS veranderen; controleer dat bij een nieuw OS-image eerst in de actuele documentatie:'
Bullet 'Raspberry Pi Documentation, Configuration: https://www.raspberrypi.com/documentation/computers/configuration.html'
Bullet 'Raspberry Pi Documentation, SSH: https://www.raspberrypi.com/documentation/remote-access/ssh.html'
Bullet 'Debian Bookworm, handleiding bluetoothctl: https://manpages.debian.org/bookworm/bluez/bluetoothctl.1.en.html'
Bullet 'Debian Bookworm, handleiding rfcomm: https://manpages.debian.org/bookworm/bluez/rfcomm.1.en.html'

Callout 'info' 'Gemaakt met behulp van AI' 'ScoreKrijt (de Android-app, de SK-Box-software en de hulpscripts) en deze handleidingen zijn gemaakt met behulp van AI (Claude van Anthropic). Controleer opdrachten en instellingen altijd op je eigen SK-Box.'
$out1 = Join-Path $Docs 'Handleiding_SK-Box_installatie_Raspberry_Pi.docx'
Save-Doc -Path $out1 -HeaderText 'ScoreKrijt  |  SK-Box installeren' -FooterText 'Installatiehandleiding SK-Box' -LogoPath $Logo -Title 'SK-Box installeren'

# ---------------------------------------------------------------------------
# 2. Updatehandleiding
# ---------------------------------------------------------------------------
Start-Doc
Cover 'UPDATEHANDLEIDING' 'SK-Box bijwerken' 'Een nieuwe ScoreKrijt-versie op de Raspberry Pi installeren, met behoud van je instellingen en wedstrijden' "SK-Box software $Versie   |   $Datum" $Logo
TocPage

H1 '1. Voordat je begint'
Para 'Met deze handleiding installeer je een nieuwere versie van het ScoreKrijt-programma op een SK-Box die al werkt. Je vervangt alleen de programmabestanden. Je instellingen, wedstrijdbestanden, Bluetooth-koppeling en autostart blijven staan. De vorige versie blijft bewaard, zodat je altijd kunt terugdraaien.'
H2 '1.1 Wat verandert er en wat niet?'
Tbl @('Onderdeel', 'Bij een update') @(
    @('Programmabestanden (`ScoreKrijt.py`, map `ScoreKrijt`, launcher)', '**Wordt vervangen** door de nieuwe versie.'),
    @('`ScoreKrijtSettings.json` (instellingen)', '**Blijft behouden.** Wordt uit de vorige versie overgenomen.'),
    @('Map `matches` (wedstrijdbestanden)', '**Blijft behouden.** Wordt uit de vorige versie overgenomen.'),
    @('Bluetooth-koppeling en services', '**Blijft ongewijzigd.** Dit staat buiten de programmamap.'),
    @('Autostartbestand', '**Blijft ongewijzigd.** Wijst naar dezelfde map.')
) @(5100, 4538)
H2 '1.2 Wat heb je nodig?'
Bullet 'Een USB-stick (FAT32 of exFAT) en een pc met Windows om de update erop te zetten.'
Bullet 'Een toetsenbord om op de SK-Box aan te sluiten. Internet of wifi is niet nodig.'
Bullet 'De hulpscripts op de SK-Box (eenmalig geïnstalleerd, zie installatiehandleiding, hoofdstuk 6.4).'
Bullet ('De nieuwe programmamap op je pc, bijvoorbeeld ' + $MapC + '.')
Bullet 'Ongeveer 15 minuten, en geen wedstrijd die op dat moment bezig is.'
Callout 'warn' 'Update niet tijdens een wedstrijd' 'De SK-Box wordt tijdens de update herstart. Een wedstrijd die nog op de telefoon staat, kun je daarna weer hervatten. Wacht liever tot de wedstrijd is afgelopen.'
Callout 'info' 'Telefoonapp en SK-Box' 'Controleer in hoofdstuk 8 of ook de Android-app moet worden bijgewerkt. Zolang het Bluetooth-protocol hetzelfde blijft, hoeven telefoon en SK-Box niet tegelijk te worden bijgewerkt.'
Callout 'info' 'Drie manieren om bij te werken' 'Hoofdstuk 3: met een USB-stick en het updatescript (aanbevolen). Hoofdstuk 4: met een USB-stick zonder script, met de hand. Hoofdstuk 5: via het netwerk met SSH, alleen als de SK-Box tijdelijk met een netwerk is verbonden.'

H1 '2. De nieuwe versie klaarzetten op je pc'
Para ('Haal de nieuwe versie eerst op van GitHub, zoals beschreven in de installatiehandleiding, hoofdstuk 2.1. Gebruik daarna de map ' + $MapC + '. Je kopieert daaruit **alleen** de onderstaande onderdelen naar de SK-Box:')
Shot 'install-2.1-github-download' 'De nieuwste versie ophalen van GitHub: Code (1) en Download ZIP (2).'
Tbl @('Wel kopiëren', 'Niet kopiëren') @(
    @('`ScoreKrijt` (de map met het programma en de iconen)', '`ScoreKrijtSettings.json`'),
    @('`ScoreKrijt.py`', 'De mappen `matches`, `build` en `dist`'),
    @('`scorekrijt_launcher.py`', 'Mappen met de naam `__pycache__`')
) @(4819, 4819)
Callout 'warn' 'Kopieer nooit het instellingenbestand van je pc' 'Het bestand op je pc bevat andere waarden dan dat op de SK-Box, bijvoorbeeld `BlueTooth Mode` uit. Als je het overschrijft, start de SK-Box zonder Bluetooth en moet je alles opnieuw instellen. Het bestand kan bovendien gevoelige gegevens bevatten, zoals een e-mailwachtwoord.'
H2 '2.1 De USB-stick vullen'
Para 'Maak op de hoofdmap van de USB-stick een map met de naam `ScoreKrijt_update` en zet daarin de drie onderdelen uit de linkerkolom hierboven. De twee scripts uit `Phyton\SK-Box_scripts` mogen erbij, zodat ook het updatescript zichzelf kan vernieuwen:'
CodeBlock @'
USB-stick
  ScoreKrijt_update
    ScoreKrijt                (map)
    ScoreKrijt.py
    scorekrijt_launcher.py
    sk-update.sh              (optioneel, nieuwste versie)
    sk-stille-opstart.sh      (optioneel, nieuwste versie)
'@
Shot 'install-6.2-scripts' 'De hoofdmap van de USB-stick met de map `ScoreKrijt_update`.'
Para 'Kopieer de onderdelen in Verkenner, open de map `ScoreKrijt_update` op de stick en klik met de rechtermuisknop in de lege map (pijl 6). Kies daarna **Plakken** (pijl 7).'
Shot 'install-6.2-plakken' 'Met de rechtermuisknop in de map (6) en Plakken (7) komen de onderdelen op de stick.'
Para ('Of in PowerShell, vanuit de map ' + $MapC + ' (vervang `E:` door de stationsletter van je stick):')
CodeBlock @'
$stick = "E:\ScoreKrijt_update"
New-Item -ItemType Directory -Force $stick | Out-Null
Copy-Item -Recurse ScoreKrijt, ScoreKrijt.py, scorekrijt_launcher.py $stick
Copy-Item ..\SK-Box_scripts\sk-*.sh $stick
'@
Para 'Gebruik daarna **Hardware veilig verwijderen** in Windows voordat je de stick uit de pc haalt.'

H1 '3. De update uitvoeren met een USB-stick'
Para 'Dit is de aanbevolen manier. Het script `sk-update.sh` zoekt de stick zelf, controleert de bestanden, behoudt je instellingen en wedstrijden en bewaart de vorige versie. De stappen voer je uit op de SK-Box met een toetsenbord; een netwerk is niet nodig.'
H2 '3.1 Stappen'
$s = New-StepList
Step $s '**Steek de USB-stick in de SK-Box** en wacht ongeveer tien seconden. Staat de desktop in beeld, dan verschijnt de melding **Removable medium is inserted**. Sluit die af met **OK** (pijl 11) of laat hem open; het updatescript zoekt de stick zelf.'
Shot 'install-6.2-sk-usb-melding' 'De melding bij het insteken van de stick (11).'
Step $s '**Open een Terminal.** Druk op **Ctrl+Alt+F2** en meld je aan met gebruikersnaam `user` en wachtwoord `user`. Draait ScoreKrijt op de desktop, druk dan op **F12** om de taakbalk te tonen en klik op het Terminal-pictogram (pijl 9). Het Terminalvenster opent daarna (pijl 10), zie ook de installatiehandleiding, hoofdstuk 13.5.'
Shot 'install-13.5-terminal' 'Een Terminal starten vanaf de taakbalk (9); het venster opent in beeld (10).'
Step $s '**Start het updatescript** (zonder `sudo`):'
CodeBlock 'bash ~/sk-update.sh'
Step $s '**Controleer de versies.** Het script toont de huidige en de nieuwe versie. Bevestig met `j` en Enter.'
Shot 'update-3.1-sk-update' 'Het script vindt de stick, toont de huidige en de nieuwe versie en vraagt om bevestiging.'
Step $s '**Wacht tot het klaar is.** Het script meldt wanneer de stick veilig kan worden verwijderd en start de SK-Box daarna na tien seconden opnieuw op.'
Step $s '**Haal de USB-stick uit de SK-Box.** Na het opstarten verschijnt eerst het ScoreKrijt-opstartscherm en daarna het grote ScoreKrijt-scherm.'
Callout 'info' 'Het script staat er nog niet?' 'Het script moet eenmalig op de SK-Box zijn gezet (installatiehandleiding, hoofdstuk 6.4). Is dat niet gebeurd, gebruik dan hoofdstuk 4; daar kopieer je het script ook naar de SK-Box.'
H2 '3.2 Opties'
Tbl @('Opdracht', 'Wat het doet') @(
    @('`bash ~/sk-update.sh`', 'Zoekt de USB-stick en werkt bij na bevestiging.'),
    @('`bash ~/sk-update.sh --ja`', 'Werkt bij zonder bevestiging te vragen.'),
    @('`bash ~/sk-update.sh --geen-herstart`', 'Werkt bij maar start de SK-Box niet opnieuw op.'),
    @('`bash ~/sk-update.sh --terug`', 'Zet de vorige versie terug (hoofdstuk 6).'),
    @('`bash ~/sk-update.sh <map>`', 'Gebruikt een andere map als bron in plaats van de stick.')
) @(4300, 5338)
H2 '3.3 Wat het script doet'
Bullet 'Zoekt de USB-stick (nooit de schijf waarop het systeem staat) en koppelt hem alleen-lezen.'
Bullet 'Kopieert de nieuwe bestanden eerst naar een tijdelijke map en controleert of de Python-bestanden leesbaar zijn. Gaat daarbij iets mis, dan blijft de huidige versie ongewijzigd.'
Bullet 'Neemt `ScoreKrijtSettings.json` en de map `matches` over uit de huidige versie.'
Bullet 'Stopt ScoreKrijt en bewaart de huidige map als `ScoreKrijt_vorige_<nummer>_<datum>`.'
Bullet 'Koppelt de stick los en start opnieuw op.'
H2 '3.4 Controleren'
CodeBlock 'grep APP_VERSION "$HOME/ScoreKrijt/ScoreKrijt/constants.py"'
Check 'De versie in de uitvoer is de nieuwe versie.'
Check 'Het grote scorebord opent op het volledige scherm met je eigen lettergroottes.'
Check 'De telefoon verbindt met de SK-Box zonder melding over een niet-compatibele versie.'
Check 'Plus, min, Noteer en Return werken op telefoon en SK-Box tegelijk.'
Check 'Oude wedstrijden zijn nog te vinden in de map `matches`.'

H1 '4. Handmatig bijwerken met een USB-stick'
Para 'Gebruik dit hoofdstuk als het script nog niet op de SK-Box staat, of als je liever zelf elke stap uitvoert. Het resultaat is hetzelfde.'
$s = New-StepList
Step $s '**Open een Terminal.** Steek de stick in de SK-Box, druk op **Ctrl+Alt+F2** en meld je aan.'
Step $s '**Zoek de stick.** De stick staat in de lijst met `TRAN` = `usb`; de partitie heet meestal `sda1`:'
CodeBlock 'lsblk -o NAME,SIZE,TRAN,LABEL,MOUNTPOINT'
Step $s '**Koppel de stick** (vervang `sda1` zo nodig) en controleer de inhoud:'
CodeBlock @'
sudo mkdir -p /mnt/sk-usb
sudo mount -o ro /dev/sda1 /mnt/sk-usb
ls /mnt/sk-usb/ScoreKrijt_update
'@
Step $s '**Stop ScoreKrijt:**'
CodeBlock @'
pkill -f scorekrijt_launcher.py
pkill -f ScoreKrijt.py
pgrep -af ScoreKrijt
'@
Step $s '**Kopieer de nieuwe bestanden** naar een tijdelijke map:'
CodeBlock @'
mkdir -p ~/ScoreKrijt_nieuw
cp -R /mnt/sk-usb/ScoreKrijt_update/ScoreKrijt /mnt/sk-usb/ScoreKrijt_update/ScoreKrijt.py /mnt/sk-usb/ScoreKrijt_update/scorekrijt_launcher.py ~/ScoreKrijt_nieuw/
'@
Step $s '**Neem instellingen en wedstrijden over en activeer de nieuwe versie.** De oude map blijft bewaard met de datum in de naam:'
CodeBlock @'
cd ~
cp ScoreKrijt/ScoreKrijtSettings.json ScoreKrijt_nieuw/
[ -d ScoreKrijt/matches ] && cp -a ScoreKrijt/matches ScoreKrijt_nieuw/
mv ScoreKrijt "ScoreKrijt_vorige_$(date +%Y-%m-%d)"
mv ScoreKrijt_nieuw ScoreKrijt
ls ScoreKrijt
'@
Step $s '**Koppel de stick los en start opnieuw op:**'
CodeBlock @'
sudo umount /mnt/sk-usb
sudo reboot
'@
Callout 'info' 'Script alvast installeren' 'Staat `sk-update.sh` op de stick, kopieer het dan nu naar de SK-Box, zodat je de volgende keer hoofdstuk 3 kunt gebruiken. Doe dat voor `sudo umount`: `cp /mnt/sk-usb/ScoreKrijt_update/sk-update.sh ~/ && chmod +x ~/sk-update.sh`.'

H1 '5. Bijwerken via het netwerk (SSH)'
Para 'Gebruik deze manier alleen als de SK-Box tijdelijk met een netwerk is verbonden. De update bestaat uit acht stappen. Bij elke stap staat of je de opdrachten op de **SK-Box** (in een SSH-sessie of Terminal) of op je **pc** (in PowerShell) uitvoert.'
H2 '5.1 Verbinden met de SK-Box'
Para 'Open PowerShell op je pc en maak verbinding:'
CodeBlock 'ssh user@SK-Box.local'
Para 'Je ziet nu de opdrachtregel van de Raspberry Pi. De stappen 5.2 en 5.3 voer je in deze SSH-sessie uit. Laat het venster open staan.'
H2 '5.2 De huidige versie noteren'
Para 'Voer uit op de SK-Box:'
CodeBlock @'
grep APP_VERSION "$HOME/ScoreKrijt/ScoreKrijt/constants.py"
ls "$HOME/ScoreKrijt"
'@
Para 'Er verschijnt bijvoorbeeld `APP_VERSION = "2.8.7"`. Komt er geen regel, dan is de huidige versie ouder dan 2.8.5. Noteer de versie voor het geval je wilt terugdraaien.'
H2 '5.3 ScoreKrijt stoppen'
Para 'Voer uit op de SK-Box:'
CodeBlock @'
pkill -f scorekrijt_launcher.py
pkill -f ScoreKrijt.py
pgrep -af ScoreKrijt
'@
Para 'De laatste opdracht moet niets tonen. Het scherm van de SK-Box wordt leeg of toont de Desktop.'
H2 '5.4 Een back-up van de wedstrijden maken'
Para 'Dit is optioneel, maar aan te raden. Open een **tweede PowerShell-venster op je pc** en laat de SSH-sessie open staan. De variabele `$box` bewaart de verbindingsnaam, zodat de opdrachten kort blijven. Kopieer de wedstrijden en instellingen naar de huidige map op je pc:'
CodeBlock @'
$box = "user@SK-Box.local"
scp -r "${box}:ScoreKrijt/matches" ./matches-backup
scp "${box}:ScoreKrijt/ScoreKrijtSettings.json" ./instellingen-backup.json
'@
H2 '5.5 De nieuwe bestanden uploaden'
Para ('Voer uit in PowerShell op je pc. Ga eerst naar de nieuwe programmamap, bijvoorbeeld ' + $MapC + '. De bestanden gaan naar een tijdelijke map, zodat de huidige installatie intact blijft:')
CodeBlock @'
$box = "user@SK-Box.local"
ssh $box "mkdir -p ~/ScoreKrijt_nieuw"
scp -r ScoreKrijt ScoreKrijt.py scorekrijt_launcher.py "${box}:ScoreKrijt_nieuw/"
'@
Callout 'info' 'Alternatief met een USB-stick' 'Zet dezelfde drie onderdelen op een USB-stick en kopieer ze op de Raspberry Pi naar een nieuwe map `ScoreKrijt_nieuw` in de thuismap.'
H2 '5.6 De nieuwe versie activeren'
Para 'Ga terug naar de SSH-sessie op de SK-Box en voer uit. De instellingen en wedstrijden worden overgenomen en de oude map blijft bewaard met de datum in de naam:'
CodeBlock @'
cd ~
cp ScoreKrijt/ScoreKrijtSettings.json ScoreKrijt_nieuw/
[ -d ScoreKrijt/matches ] && cp -a ScoreKrijt/matches ScoreKrijt_nieuw/
mv ScoreKrijt "ScoreKrijt_vorige_$(date +%Y-%m-%d)"
mv ScoreKrijt_nieuw ScoreKrijt
ls ScoreKrijt
'@
Para 'In de lijst moeten `ScoreKrijt.py`, `scorekrijt_launcher.py`, `ScoreKrijtSettings.json`, `matches` en de map `ScoreKrijt` staan.'
H2 '5.7 Opnieuw opstarten'
CodeBlock 'sudo reboot'
Para 'Na het opstarten verschijnt eerst het ScoreKrijt-opstartscherm en daarna het grote ScoreKrijt-scherm, precies zoals voor de update.'
H2 '5.8 Controleren'
CodeBlock 'grep APP_VERSION "$HOME/ScoreKrijt/ScoreKrijt/constants.py"'
Check 'De versie in de uitvoer is de nieuwe versie.'
Check 'Het grote scorebord opent op het volledige scherm met je eigen lettergroottes.'
Check 'De telefoon verbindt met de SK-Box zonder melding over een niet-compatibele versie.'
Check 'Plus, min, Noteer en Return werken op telefoon en SK-Box tegelijk.'
Check 'Oude wedstrijden zijn nog te vinden in de map `matches`.'

H1 '6. Terugdraaien naar de vorige versie'
Para 'Werkt de nieuwe versie niet goed, dan zet je de vorige versie terug. Wedstrijden die na de update zijn gespeeld, worden meegenomen.'
H2 '6.1 Met het script'
Para 'Voer uit op de SK-Box (Ctrl+Alt+F2 en inloggen), zonder `sudo`:'
CodeBlock 'bash ~/sk-update.sh --terug'
Para 'Het script toont welke versie wordt teruggezet, vraagt om bevestiging en start daarna opnieuw op. De versie die niet werkte, blijft bewaard als `ScoreKrijt_mislukt_<datum>_<tijd>`.'
H2 '6.2 Met de hand'
Para 'Vervang `<naam>` door de exacte mapnaam, zoals `001_2026-10-18` of, na een handmatige update, de datum. Controleer de namen met `ls -d ~/ScoreKrijt_vorige_*`.'
CodeBlock @'
pkill -f scorekrijt_launcher.py
pkill -f ScoreKrijt.py
cd ~
mv ScoreKrijt ScoreKrijt_mislukt
mv ScoreKrijt_vorige_<naam> ScoreKrijt
sudo reboot
'@
Para 'Zijn er na de update wedstrijden gespeeld die je wilt behouden? Kopieer die dan terug, zonder bestaande bestanden te overschrijven:'
CodeBlock 'cp -an ~/ScoreKrijt_mislukt/matches/. ~/ScoreKrijt/matches/'

H1 '7. Opruimen'
Para 'Werkt de nieuwe versie na een paar dagen zonder problemen, dan kun je de oude mappen verwijderen. Bekijk eerst welke er zijn:'
CodeBlock 'ls -d ~/ScoreKrijt_*'
Para 'Verwijder daarna één map tegelijk, met de exacte naam uit de lijst:'
CodeBlock 'rm -rf ~/ScoreKrijt_vorige_<naam>'
Callout 'warn' 'Verwijderen kan niet ongedaan worden gemaakt' 'Controleer de mapnaam voordat je op Enter drukt. Verwijder nooit de map `ScoreKrijt` zelf.'

H1 '8. De telefoonapp bijwerken'
H2 '8.1 Moet de app ook worden bijgewerkt?'
Para 'Telefoon en SK-Box spreken met elkaar via een Bluetooth-protocol dat een versienummer heeft. Bij het verbinden vergelijken ze dat nummer.'
Tbl @('Programmaversie', 'Bluetooth-protocol', 'Opmerking') @(
    @('2.8', '2', 'Werkt samen met 2.8.5 tot en met 2.8.7.'),
    @('2.8.5 tot en met 2.8.7', '2', 'Werkt samen met 2.8 en met elkaar. De regelaar voor de middelste kolom en de hogere maxima werken alleen als telefoon en SK-Box allebei 2.8.6 of nieuwer zijn.'),
    @('Ouder dan 2.8', '1', 'Werkt niet samen met 2.8 of nieuwer.')
) @(3000, 2600, 4038)
Bullet '**Zelfde protocolnummer:** telefoon en SK-Box mogen een verschillende programmaversie hebben en kunnen in willekeurige volgorde worden bijgewerkt.'
Bullet '**Ander protocolnummer:** de app toont de melding **SK-Box-versie niet compatibel** en vermeldt welk onderdeel moet worden bijgewerkt. Werk dat onderdeel bij.'
H2 '8.2 De app installeren'
$s = New-StepList
Step $s 'Zet het nieuwe APK-bestand op de telefoon, bijvoorbeeld via USB of een gedeelde map.'
Step $s 'Open het bestand op de telefoon en kies **Installeren** of **Bijwerken**. Geef zo nodig eenmalig toestemming om apps uit deze bron te installeren.'
Step $s 'Start de app en verbind met de SK-Box. Je lopende wedstrijd en je gekoppelde SK-Box blijven behouden.'
Callout 'warn' 'Vanaf versie 2.8.9 een nieuwe pakketnaam' 'De app heeft sinds versie 2.8.9 de pakketnaam `io.github.bramijsselstijn.scorekrijt`. Android ziet dat als een andere app: de nieuwe APK installeert naast de oude en werkt die niet bij. Maak een lopende wedstrijd eerst af, want de opgeslagen gegevens van de oude app (zoals de laatste wedstrijd en het onthouden van de SK-Box) worden niet overgenomen. Geef de nieuwe app de Bluetooth-toestemming als daarom wordt gevraagd. De koppeling met de SK-Box in de Bluetooth-instellingen van de telefoon blijft bestaan. Verwijder de oude app nadat je de nieuwe hebt getest.'
Callout 'warn' 'Gebruik steeds hetzelfde soort APK''Android accepteert een update alleen als het nieuwe APK-bestand met dezelfde sleutel is ondertekend als de geïnstalleerde app. Geeft Android een melding dat de app niet kan worden geïnstalleerd, dan is dat meestal de oorzaak. Verwijderen en opnieuw installeren lost het op, maar wist ook de lokaal opgeslagen gegevens, zoals een lopende wedstrijd en het laatste wedstrijdoverzicht.'

H1 '9. Storingen bij het bijwerken'
Tbl @('Probleem', 'Mogelijke oorzaak', 'Oplossing') @(
    @('Script meldt: Geen USB-stick gevonden', 'Stick nog niet herkend of ander bestandssysteem', 'Wacht tien seconden na het insteken en probeer opnieuw. Controleer met `lsblk -o NAME,TRAN,FSTYPE` of de stick met `TRAN` = `usb` wordt getoond. Gebruik FAT32 of exFAT.'),
    @('Script meldt: geen map `ScoreKrijt_update`', 'Map ontbreekt of heet anders op de stick', 'Controleer op je pc de mapnaam en of daarin `ScoreKrijt`, `ScoreKrijt.py` en `scorekrijt_launcher.py` staan (hoofdstuk 2.1).'),
    @('Script meldt: bestand is beschadigd', 'Het kopiëren naar de stick is mislukt', 'Kopieer de update opnieuw naar de stick en gebruik Hardware veilig verwijderen. De huidige versie is dan niet gewijzigd.'),
    @('`bash ~/sk-update.sh`: No such file', 'Script is niet geïnstalleerd', 'Volg hoofdstuk 4; kopieer daarbij het script naar de SK-Box.'),
    @('`scp` meldt Permission denied of No such file', 'Verkeerde gebruikersnaam of map', 'Controleer de gebruikersnaam (`user`) en voer eerst `mkdir -p ~/ScoreKrijt_nieuw` uit.'),
    @('Scherm blijft leeg na de update', 'Programmafout of bestand ontbreekt', 'Lees `tail -n 50 ~/ScoreKrijt/scorekrijt-autostart.log`. Draai zo nodig terug (hoofdstuk 6).'),
    @('`ModuleNotFoundError` in het log', 'Een benodigd Python-pakket ontbreekt', 'Voer de installatieopdrachten uit hoofdstuk 5 van de installatiehandleiding opnieuw uit.'),
    @('Instellingen zijn weer standaard', '`ScoreKrijtSettings.json` is niet overgenomen', 'Kopieer het bestand uit `ScoreKrijt_vorige_<naam>` naar `ScoreKrijt` en herstart.'),
    @('Wedstrijdbestanden ontbreken', 'Map `matches` is niet overgenomen', 'Kopieer de map uit `ScoreKrijt_vorige_<naam>` naar `ScoreKrijt`.'),
    @('Telefoon meldt een niet-compatibele versie', 'Ander Bluetooth-protocol', 'Werk het genoemde onderdeel bij (hoofdstuk 8).'),
    @('Telefoon vindt de SK-Box niet meer', 'De koppelservice draait niet', 'Controleer `systemctl status scorekrijt-pairing.service --no-pager`. Een update van het programma wijzigt die service niet.')
) @(2800, 2700, 4138)

H1 '10. Snelle referentie'
Para 'Voor wie de stappen al kent.' '' '<w:keepNext/>'
Para '**Met een USB-stick (zonder netwerk):**' '' '<w:keepNext/>'
CodeBlock @'
Op de pc:   map ScoreKrijt_update op de stick met ScoreKrijt, ScoreKrijt.py, scorekrijt_launcher.py
Op de Box:  stick insteken, Ctrl+Alt+F2, inloggen
            bash ~/sk-update.sh
Terugdraaien:  bash ~/sk-update.sh --terug
'@
Para '**Via het netwerk.**' '' '<w:keepNext/>'
Para '**Op je pc (PowerShell, in de nieuwe programmamap):**'
CodeBlock @'
$box = "user@SK-Box.local"
ssh $box "mkdir -p ~/ScoreKrijt_nieuw"
scp -r ScoreKrijt ScoreKrijt.py scorekrijt_launcher.py "${box}:ScoreKrijt_nieuw/"
'@
Para '**Op de SK-Box (via SSH):**'
CodeBlock @'
pkill -f scorekrijt_launcher.py; pkill -f ScoreKrijt.py
cd ~
cp ScoreKrijt/ScoreKrijtSettings.json ScoreKrijt_nieuw/
[ -d ScoreKrijt/matches ] && cp -a ScoreKrijt/matches ScoreKrijt_nieuw/
mv ScoreKrijt "ScoreKrijt_vorige_$(date +%Y-%m-%d)"
mv ScoreKrijt_nieuw ScoreKrijt
sudo reboot
'@

Callout 'info' 'Gemaakt met behulp van AI' 'ScoreKrijt (de Android-app, de SK-Box-software en de hulpscripts) en deze handleidingen zijn gemaakt met behulp van AI (Claude van Anthropic). Controleer opdrachten en instellingen altijd op je eigen SK-Box.'
$out2 = Join-Path $Docs 'Handleiding_SK-Box_bijwerken.docx'
Save-Doc -Path $out2 -HeaderText 'ScoreKrijt  |  SK-Box bijwerken' -FooterText 'Updatehandleiding SK-Box' -LogoPath $Logo -Title 'SK-Box bijwerken'

# ---------------------------------------------------------------------------
# 3. Handleiding instellingen
# ---------------------------------------------------------------------------
Start-Doc
Cover 'HANDLEIDING' 'Instellingen van de SK-Box' 'Het grote scherm, het opstarten en de bediening via Bluetooth' "SK-Box software $Versie   |   $Datum" $Logo
TocPage

H1 '1. Over deze handleiding'
Para 'Deze handleiding beschrijft hoe de SK-Box is ingesteld, hoe je het grote scherm aanpast en wat je tijdens een wedstrijd ziet. De installatie staat in de handleiding **SK-Box installeren** en het bijwerken in de handleiding **SK-Box bijwerken**.'
Callout 'info' 'Wat is de SK-Box?' 'Een Raspberry Pi die op een HDMI-scherm de stand van de wedstrijd toont. De wedstrijd wordt bediend met de ScoreKrijt-app op een Android-telefoon, via Bluetooth. De SK-Box heeft geen internet nodig.'

H1 '2. Wat gebeurt er bij het opstarten?'
$s = New-StepList
Step $s '**Zet de SK-Box en het scherm aan.** Het scherm toont tijdens het opstarten het ScoreKrijt-logo in plaats van het Raspberry Pi-logo.'
Step $s '**Het bureaublad** is zwart met het ScoreKrijt-logo. Er is geen taakbalk en er zijn geen pictogrammen.'
Step $s '**Het opstartscherm van ScoreKrijt** toont het logo met de melding "SK-Box wordt gestart" en bewegende puntjes. Het blijft staan tot ScoreKrijt klaar is, minimaal 3 en hoogstens 90 seconden.'
Step $s '**Het grote scherm** opent schermvullend. Het gewone bedieningsvenster blijft verborgen.'
Step $s '**Bluetooth** start ongeveer een halve seconde na het openen van het programma. Bij een verbroken verbinding probeert de SK-Box na 2 seconden opnieuw te verbinden.'

H1 '3. Aanbevolen instellingen op de SK-Box'
Para 'De SK-Box werkt in **Bluetooth-modus**. Die schakelt een aantal instellingen automatisch goed, zodat de telefoon de wedstrijd bedient.'
Tbl @('Instelling', 'Waarde', 'Opmerking') @(
    @('BlueTooth Mode', 'Aan', 'Start de Bluetooth-service en zet de vijf onderstaande instellingen automatisch.'),
    @('Groot scherm', 'Aan', 'Automatisch door Bluetooth-modus.'),
    @('Open groot scherm in full screen', 'Aan', 'Automatisch. Het gewone venster blijft verborgen.'),
    @('Wedstrijdoverzicht', 'Uit', 'Automatisch. De app handelt het einde van de wedstrijd af.'),
    @('Wedstrijd mailen', 'Uit', 'Automatisch. Geen e-mailvraag op de SK-Box.'),
    @('Nieuwe wedstrijd automatisch', 'Uit', 'Automatisch. De app bepaalt de volgende start.'),
    @('Lettertype', 'Bodoni', 'Lettertype van het scorebord.'),
    @('Startkleur', 'Geel', 'Wordt per wedstrijd door de telefoon doorgegeven.'),
    @('Geschiedenis tonen', 'Aan', 'Standaard 3 regels; in te stellen met de app (hoofdstuk 4).'),
    @('Open wedstrijden controleren', 'Uit', 'Geen vraag over een onafgeronde wedstrijd bij het opstarten.'),
    @('Oude wedstrijden opruimen', 'Aan', 'Wedstrijdbestanden ouder dan 5 jaar worden verwijderd.')
) @(3300, 1500, 4838)
Callout 'info' 'Je instellingen blijven bewaard' 'De instellingen staan in `ScoreKrijtSettings.json`. Bij een update met `sk-update.sh` wordt dat bestand overgenomen, dus ook je lettergroottes blijven staan.'

H1 '4. Het grote scherm instellen met de app'
Para 'Je past de weergave van het grote scherm aan met de ScoreKrijt-app op de telefoon, terwijl je het resultaat op het scherm ziet.'
$s = New-StepList
Step $s '**Verbind de telefoon met de SK-Box** (zie de app, hoofdmenu).'
Step $s '**Open Instellingen SK-Box.** Dat kan vanuit het hoofdmenu en tijdens een wedstrijd, via Instellingen, de knop **Instellingen SK-Box**.'
Step $s '**Verschuif een regelaar.** Zodra je loslaat, verandert het grote scherm direct (live voorbeeld).'
Step $s '**Kies Permanent opslaan op SK-Box** om de waarden te bewaren. Zonder opslaan gaan ze na een herstart verloren.'
Step $s '**Standaardweergave herstellen** zet alle waarden terug naar de fabrieksinstellingen en slaat ze op.'
Tbl @('Onderdeel', 'Standaard', 'Bereik') @(
    @('Aantal getoonde beurten', '3', '1 - 10'),
    @('Breedte middelste kolom', '20 %', '10 - 60 %'),
    @('Spelersnamen', '70', '20 - 200'),
    @('Tekst caramboles / score', '50', '20 - 160'),
    @('Waarde caramboles / score', '200', '120 - 500'),
    @('Tekst beurt', '70', '50 - 160'),
    @('Waarde beurt', '100', '50 - 300'),
    @('Tekst huidige caramboles', '50', '20 - 160'),
    @('Waarde huidige caramboles', '60', '40 - 200'),
    @('Tekst TMC', '28', '10 - 120'),
    @('Waarde TMC', '42', '15 - 180'),
    @('Tekst punten', '30', '10 - 100'),
    @('Waarde punten', '50', '20 - 160'),
    @('Tekst statistieken', '30', '10 - 100'),
    @('Waarden statistieken', '50', '20 - 160'),
    @('Tekst geschiedenis', '30', '10 - 100'),
    @('Waarden geschiedenis', '30', '10 - 100')
) @(4200, 2400, 3038)
Callout 'info' 'Past een tekst niet in zijn vak?' 'Kies dan een kleinere lettergrootte, of maak de middelste kolom breder of smaller met **Breedte middelste kolom**. Sommige lettertypen zijn breder dan andere en hebben meer ruimte nodig.'
Callout 'warn' 'Telefoon en SK-Box moeten dezelfde versie hebben' 'De regelaar voor de breedte van de middelste kolom en de hoge maxima werken alleen als de app en de SK-Box allebei versie 2.8.6 of nieuwer zijn. Een oudere SK-Box weigert hogere waarden met een foutmelding.'

H1 '5. Wat je tijdens een wedstrijd ziet'
H2 '5.1 Voor de start'
Para 'Zodra je in de app op **Bepalen aanvang wedstrijd** komt, tonen de SK-Box de namen en de TMC van beide spelers. Alle bovenste vakken zijn dan wit, omdat nog niet bepaald is wie begint. Bij het starten van de wedstrijd komen de kleuren en de speler aan de beurt.'
Callout 'info' 'Een lopende wedstrijd blijft ongemoeid' 'Staat er op de SK-Box een wedstrijd, dan verandert dit scherm niet wanneer je in de app een nieuwe wedstrijd voorbereidt. Pas bij het starten van de nieuwe wedstrijd wordt de stand vervangen.'
H2 '5.2 Vaste beurten en Uit is uit'
Tbl @('Wedstrijdvorm', 'Kolommen per speler', 'Betekenis') @(
    @('Vaste beurten', '`Punten` en `Car. tot punt`', 'Punten volgens de TMC, en het aantal caramboles tot het volgende punt.'),
    @('Uit is uit', '`Procent` en `Car. tot uit`', 'Het percentage van het te maken aantal (naar beneden afgerond) en het aantal caramboles dat nog nodig is om uit te zijn.')
) @(2200, 3000, 4438)
Para 'Bij Uit is uit is 100 procent gelijk aan 10 punten. De wedstrijd eindigt dus op hetzelfde moment als eerder. Bij een verlenging rekent de SK-Box met de nieuwe, hogere TMC.'

H1 '6. Toetsen op de SK-Box'
Para 'Sluit een toetsenbord aan op de SK-Box. Het gewone ScoreKrijt-venster of het grote scherm moet daarbij het actieve venster zijn.'
Tbl @('Toets', 'Wat doet de toets?') @(
    @('F12', 'Toont of verbergt de taakbalk. Met het grote scherm open haalt F12 dat scherm even uit volledig scherm, zodat de taakbalk zichtbaar wordt.'),
    @('F11', 'Zet het grote scherm in of uit volledig scherm.'),
    @('Esc', 'Sluit het grote scherm en toont het gewone ScoreKrijt-venster.'),
    @('Ctrl+Alt+F2', 'Opent een tekstscherm met een inlogprompt, bijvoorbeeld om `sk-update.sh` te starten. Terug met Ctrl+Alt+F1 of met `sudo reboot`.')
) @(2200, 7438)
Para 'Het bijwerken van ScoreKrijt staat in de handleiding **SK-Box bijwerken**.'

H1 '7. Bluetooth'
Tbl @('Onderdeel', 'Waarde', 'Opmerking') @(
    @('Techniek', 'Bluetooth Classic SPP', 'Seriële Bluetooth-verbinding.'),
    @('Linux-poort', '`/dev/rfcomm0`', 'Virtuele seriële poort van de koppeling.'),
    @('Baudrate', '9600', 'Communicatiesnelheid.'),
    @('Leestime-out', '1 seconde', 'Wachttijd per leesactie.'),
    @('Automatisch herstellen', 'Aan', 'Opnieuw proberen na verbindingsverlies, iedere 2 seconden.'),
    @('Berichtformaat', 'JSON, een regel per bericht', 'Protocolversie 2.')
) @(3000, 2900, 3738)
H2 '7.1 Wat de telefoon kan bedienen'
Bullet 'de verbinding testen en de status opvragen;'
Bullet 'namen en TMC alvast tonen (vanaf versie 2.8.7) en een nieuwe wedstrijd starten of bijwerken;'
Bullet 'de score verhogen en verlagen en de beurt noteren;'
Bullet 'de vorige actie terugnemen;'
Bullet 'de wedstrijd afsluiten;'
Bullet 'de weergave van het grote scherm bekijken, aanpassen, opslaan en herstellen.'
Callout 'warn' 'Valt de verbinding steeds na 30 seconden weg?' 'Dan is de telefoon waarschijnlijk niet echt gekoppeld. Vergeet de SK-Box op de telefoon, verwijder de oude koppelgegevens op de SK-Box en koppel opnieuw. Zie de installatiehandleiding, hoofdstuk 8.2 en de storingstabel.'

H1 '8. Snelle controle na onderhoud'
Para 'Loop onderstaande punten na. Alles moet werken zonder muis.'
Check 'Tijdens het opstarten verschijnt het ScoreKrijt-logo, geen Raspberry Pi-logo en geen opstarttekst.'
Check 'Het opstartscherm toont "SK-Box wordt gestart" en gaat over in het scorebord.'
Check 'Het scorebord staat schermvullend, zonder taakbalk.'
Check 'F12 toont en verbergt de taakbalk.'
Check 'De telefoon kan de SK-Box vinden en verbinden en blijft verbonden.'
Check 'Plus, min en Noteer veranderen telefoon en scorebord tegelijk.'
Check 'Bij Bepalen aanvang wedstrijd staan de namen en TMC op het scorebord, met witte vakken.'
Check 'Bij Uit is uit staan `Procent` en `Car. tot uit` in beeld, bij vaste beurten `Punten`.'
Check 'Na het afsluiten van de wedstrijd staan beurt en huidige caramboles op 0.'

H1 '9. Storingen oplossen'
Tbl @('Probleem', 'Controle', 'Oplossing') @(
    @('ScoreKrijt start niet', '`scorekrijt-autostart.log`', 'Lees de laatste regels: `tail -n 50 ~/ScoreKrijt/scorekrijt-autostart.log`.'),
    @('Geen Bluetooth', 'BlueTooth Mode', 'Zet de instelling aan en start ScoreKrijt opnieuw.'),
    @('Poort `/dev/rfcomm0` ontbreekt', 'Koppeling en `scorekrijt-rfcomm.service`', 'De poort verschijnt pas als de telefoon verbindt. Controleer `journalctl -u scorekrijt-rfcomm.service`.'),
    @('Verbinding valt steeds weg', 'Koppeling met de telefoon', 'Koppel opnieuw (zie hoofdstuk 7). Het log toont de reden in `scorekrijt-autostart.log`.'),
    @('Scorebord niet schermvullend', 'Groot scherm en full screen', 'Beide moeten aan staan. Druk op F11 in het grote scherm.'),
    @('Taakbalk blijft zichtbaar of komt niet', 'Bureaublad en F12', 'Zie de installatiehandleiding, hoofdstuk 13.'),
    @('Procenten of namen vooraf ontbreken', 'Versie van app en SK-Box', 'Beide moeten 2.8.7 zijn. Controleer met `grep APP_VERSION ~/ScoreKrijt/ScoreKrijt/constants.py`.'),
    @('Tekst valt buiten zijn vak', 'Lettergroottes', 'Verklein de tekst of pas de breedte van de middelste kolom aan (hoofdstuk 4).')
) @(2800, 2500, 4338)

H1 '10. Beheer en veiligheid'
Bullet 'Bewaar wachtwoorden niet in een gedeelde handleiding. De inloggegevens van de SK-Box staan in de installatiehandleiding, hoofdstuk 1.'
Bullet 'Maak vóór grotere wijzigingen een kopie van `ScoreKrijtSettings.json`.'
Bullet 'Wijzig de Bluetooth-poort en de baudrate alleen als ook de koppeling op de Raspberry Pi wordt aangepast.'
Bullet 'Voer na iedere update de snelle controle uit hoofdstuk 8 uit.'
Callout 'info' 'Gemaakt met behulp van AI' 'ScoreKrijt (de Android-app, de SK-Box-software en de hulpscripts) en deze handleidingen zijn gemaakt met behulp van AI (Claude van Anthropic). Controleer instellingen en opdrachten altijd op je eigen SK-Box.'

$out3 = Join-Path $Docs 'Handleiding_SK-Box_instellingen.docx'
Save-Doc -Path $out3 -HeaderText 'ScoreKrijt  |  Instellingen van de SK-Box' -FooterText 'Handleiding instellingen SK-Box' -LogoPath $Logo -Title 'Instellingen van de SK-Box'

# ---------------------------------------------------------------------------
# Word: inhoudsopgave bijwerken en pdf maken
# ---------------------------------------------------------------------------
foreach ($d in @($out1, $out2, $out3)) {
    $pdf = [System.IO.Path]::ChangeExtension($d, '.pdf')
    $pages = Update-InWord -DocPath $d -PdfPath $pdf
    "{0}: {1} pagina's" -f (Split-Path $d -Leaf), $pages
}

$ontbreekt = @($script:missingShots | Sort-Object -Unique)
if ($ontbreekt.Count -gt 0) {
    "Nog te maken afbeeldingen in Screenshots ({0}): {1}" -f $ontbreekt.Count, ($ontbreekt -join ', ')
}
