from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Handleiding_SK-Box_installatie_Raspberry_Pi.docx"
LOGO = ROOT / "Logos" / "ScoreKrijt Logo.png"

BLUE = "214F6B"
LIGHT_BLUE = "E8F1F6"
PALE = "F4F6F8"
YELLOW = "FFF4D6"
RED = "FCE8E6"
GOLD = "C7942E"
INK = RGBColor(33, 39, 43)
MUTED = RGBColor(95, 105, 112)


def set_run(run, size=10.5, bold=False, color=INK, italic=False, font="Aptos"):
    run.font.name = font
    rpr = run._element.get_or_add_rPr()
    rpr.rFonts.set(qn("w:ascii"), font)
    rpr.rFonts.set(qn("w:hAnsi"), font)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def cell_fill(cell, color):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = tcpr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcpr.append(shd)
    shd.set(qn("w:fill"), color)


def cell_margins(cell, top=90, start=120, bottom=90, end=120):
    tcpr = cell._tc.get_or_add_tcPr()
    mar = tcpr.first_child_found_in("w:tcMar")
    if mar is None:
        mar = OxmlElement("w:tcMar")
        tcpr.append(mar)
    for name, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = mar.find(qn(f"w:{name}"))
        if node is None:
            node = OxmlElement(f"w:{name}")
            mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def keep_table_header(row):
    trpr = row._tr.get_or_add_trPr()
    node = OxmlElement("w:tblHeader")
    node.set(qn("w:val"), "true")
    trpr.append(node)


def add_note(doc, label, text, fill=LIGHT_BLUE):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.25)
    cell_fill(cell, fill)
    cell_margins(cell, top=135, bottom=135, start=180, end=180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    set_run(p.add_run(f"{label}: "), bold=True, color=RGBColor.from_string(BLUE))
    set_run(p.add_run(text))
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(0)


def add_code(doc, code):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.25)
    cell_fill(cell, "20262B")
    cell_margins(cell, top=115, bottom=115, start=150, end=150)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    lines = code.strip("\n").splitlines()
    for idx, line in enumerate(lines):
        r = p.add_run(line)
        set_run(r, size=8.6, color=RGBColor(245, 247, 249), font="Consolas")
        if idx < len(lines) - 1:
            r.add_break()
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(0)


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    set_run(p.add_run(text))


def add_step(doc, title, text):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.space_after = Pt(5)
    set_run(p.add_run(f"{title}. "), bold=True)
    set_run(p.add_run(text))


def add_table(doc, headers, rows, widths):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for cell, text, width in zip(table.rows[0].cells, headers, widths):
        cell.width = width
        cell_fill(cell, BLUE)
        cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_run(cell.paragraphs[0].add_run(text), size=9.5, bold=True, color=RGBColor(255, 255, 255))
    keep_table_header(table.rows[0])
    for row in rows:
        cells = table.add_row().cells
        for cell, text, width in zip(cells, row, widths):
            cell.width = width
            cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_run(cell.paragraphs[0].add_run(text), size=9.2)
    return table


doc = Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Inches(0.8)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(1)
section.right_margin = Inches(1)
section.header_distance = Inches(0.35)
section.footer_distance = Inches(0.35)

normal = doc.styles["Normal"]
normal.font.name = "Aptos"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
normal.font.size = Pt(10.5)
normal.font.color.rgb = INK
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15

for style_name, size, before, after in (
    ("Heading 1", 16, 18, 10),
    ("Heading 2", 13, 14, 7),
    ("Heading 3", 12, 10, 5),
):
    style = doc.styles[style_name]
    style.font.name = "Aptos Display"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Aptos Display")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos Display")
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor.from_string(BLUE if style_name != "Heading 3" else "1F4D78")
    style.paragraph_format.space_before = Pt(before)
    style.paragraph_format.space_after = Pt(after)
    style.paragraph_format.keep_with_next = True

header = section.header.paragraphs[0]
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
set_run(header.add_run("ScoreKrijt  |  Installatie SK-Box"), size=8.5, bold=True, color=MUTED)
footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(footer.add_run("Raspberry Pi installatie- en beheerhandleiding"), size=8, color=MUTED)

# Cover
for _ in range(3):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(18)
if LOGO.exists():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(LOGO), width=Inches(1.45))
    p.paragraph_format.space_after = Pt(14)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
set_run(p.add_run("INSTALLATIEHANDLEIDING"), size=10, bold=True, color=RGBColor.from_string(GOLD))
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
set_run(p.add_run("ScoreKrijt op de SK-Box"), size=28, bold=True, color=RGBColor.from_string(BLUE))
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(28)
set_run(p.add_run("Raspberry Pi OS, programma-installatie, Bluetooth en automatisch opstarten"), size=13, color=MUTED)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Terminalgerichte werkwijze - versie 30 juli 2026"), size=9.5, italic=True, color=MUTED)
doc.add_page_break()

doc.add_heading("1. Uitgangspunt", level=1)
doc.add_paragraph(
    "Deze handleiding richt een Raspberry Pi in als SK-Box: een zelfstandig ScoreKrijt-"
    "scorebord dat op een aangesloten HDMI-scherm draait en via Bluetooth door de Android-"
    "app wordt bediend. De stappen gaan uit van Raspberry Pi OS met Desktop, omdat "
    "ScoreKrijt Tkinter en een grafische fullscreenweergave gebruikt."
)
add_note(
    doc,
    "Belangrijk vÃ³Ã³r de start",
    "Maak een back-up van een bestaande SK-Box. Vervang in alle voorbeelden de tekst "
    "<gebruikersnaam>, <IP-adres> en <ANDROID-MAC> door de waarden van de eigen installatie. "
    "Typ de punthaken niet mee.",
    fill=YELLOW,
)

doc.add_heading("2. Benodigdheden", level=1)
for item in (
    "Raspberry Pi met Bluetooth en HDMI, geschikte voeding en microSD-kaart of SSD;",
    "Raspberry Pi OS met Desktop (64-bit aanbevolen voor recente Pi-modellen);",
    "HDMI-scherm voor het scorebord;",
    "toetsenbord en netwerkverbinding voor de eerste installatie;",
    "de volledige inhoud van de projectmap Phyton/V3 Bleutooth;",
    "een Android-apparaat met de ScoreKrijt-app.",
):
    add_bullet(doc, item)

doc.add_heading("3. Raspberry Pi OS voorbereiden", level=1)
doc.add_heading("3.1 Basisconfiguratie", level=2)
doc.add_paragraph("Open een Terminal op de Raspberry Pi en start:")
add_code(doc, "sudo raspi-config")
doc.add_paragraph("Stel in het menu minimaal het volgende in:")
add_table(
    doc,
    ("Onderdeel", "Aanbevolen waarde", "Waarom"),
    (
        ("System Options > Hostname", "sk-box", "Herkenbare netwerknaam."),
        ("System Options > Auto Login", "Desktop autologin: Ja", "Nodig voor grafische autostart."),
        ("Localisation > Locale", "nl_NL.UTF-8", "Nederlandse tekens en notatie."),
        ("Localisation > Timezone", "Europe/Amsterdam", "Juiste tijden in wedstrijdbestanden."),
        ("Localisation > WLAN Country", "NL", "Correcte wifi-kanalen en zendregels."),
        ("Interface Options > SSH", "Aan", "Beheer via een andere computer."),
        ("Display Options > Screen Blanking", "Uit", "Scorebord blijft zichtbaar."),
    ),
    (Inches(2.15), Inches(1.65), Inches(2.45)),
)
doc.add_paragraph("Herstart nadat raspi-config daarom vraagt:")
add_code(doc, "sudo reboot")

doc.add_heading("3.2 Systeem bijwerken", level=2)
add_code(
    doc,
    """sudo apt update
sudo apt full-upgrade -y
sudo reboot""",
)
add_note(
    doc,
    "Waarom Desktop-autologin",
    "Een systeemdienst zonder grafische sessie kan een Tkinter-venster niet betrouwbaar op "
    "het HDMI-scherm openen. Daarom start ScoreKrijt via de autostart van de ingelogde "
    "desktopgebruiker.",
)

doc.add_heading("4. Netwerk en beheer controleren", level=1)
doc.add_heading("4.1 Hostnaam en IP-adres", level=2)
add_code(
    doc,
    """hostname
hostname -I
timedatectl
nmcli radio wifi""",
)
doc.add_paragraph("Wanneer wifi nog niet verbonden is:")
add_code(
    doc,
    """nmcli device wifi list
nmcli device wifi connect "NAAM-VAN-WIFI" password "WIFI-WACHTWOORD" """,
)
add_note(
    doc,
    "Wachtwoorden",
    "Zet wifi- en beheerwachtwoorden niet in deze handleiding of in het project. Het "
    "nmcli-commando komt in de shellgeschiedenis; gebruik bij voorkeur Raspberry Pi Imager "
    "of wis alleen het betreffende geschiedenisitem na de installatie.",
    fill=YELLOW,
)

doc.add_heading("4.2 Verbinden via SSH", level=2)
doc.add_paragraph("Vanaf Windows PowerShell of een andere computer:")
add_code(doc, "ssh <gebruikersnaam>@sk-box.local")
doc.add_paragraph("Als mDNS niet werkt, gebruik dan het IP-adres:")
add_code(doc, "ssh <gebruikersnaam>@<IP-adres>")

doc.add_heading("5. Benodigde software installeren", level=1)
add_code(
    doc,
    """sudo apt update
sudo apt install -y python3 python3-tk python3-pil python3-pil.imagetk
sudo apt install -y python3-serial bluez rfkill""",
)
doc.add_paragraph("Controleer Python, Tkinter, Pillow en pyserial:")
add_code(
    doc,
    """python3 --version
python3 -c "import tkinter; print('Tkinter OK')"
python3 -c "from PIL import Image, ImageTk; print('Pillow OK')"
python3 -c "import serial; print('pyserial OK')"
bluetoothctl --version""",
)

doc.add_heading("6. Programmabestanden op de SK-Box zetten", level=1)
doc.add_heading("6.1 Doelmap maken", level=2)
doc.add_paragraph("Voer op de Raspberry Pi uit:")
add_code(
    doc,
    """mkdir -p "$HOME/ScoreKrijt"
chmod 755 "$HOME/ScoreKrijt" """,
)
doc.add_heading("6.2 KopiÃ«ren via USB", level=2)
doc.add_paragraph(
    "Kopieer de volledige inhoud van Phyton/V3 Bleutooth naar de map ScoreKrijt. "
    "Controleer daarna of de volgende bestanden bestaan:"
)
add_code(
    doc,
    """cd "$HOME/ScoreKrijt"
ls -la
test -f ScoreKrijt.py && echo "ScoreKrijt.py OK"
test -f scorekrijt_launcher.py && echo "launcher OK"
test -f ScoreKrijtSettings.json && echo "instellingen OK"
test -d ScoreKrijt/icons && echo "icons OK" """,
)
doc.add_heading("6.3 Alternatief: kopiÃ«ren via SCP", level=2)
doc.add_paragraph(
    "Open PowerShell in Windows in de map Phyton\\V3 Bleutooth en voer uit:"
)
add_code(doc, 'scp -r ./* <gebruikersnaam>@sk-box.local:/home/<gebruikersnaam>/ScoreKrijt/')
add_note(
    doc,
    "Mapstructuur",
    "Kopieer de inhoud van V3 Bleutooth, niet alleen ScoreKrijt.py. De submap ScoreKrijt, "
    "de icons en ScoreKrijtSettings.json zijn eveneens nodig.",
)

doc.add_heading("7. Eerste lokale test", level=1)
add_code(
    doc,
    """cd "$HOME/ScoreKrijt"
python3 ScoreKrijt.py""",
)
doc.add_paragraph(
    "Controleer of het hoofdvenster en het grote scorebord openen. Sluit de toepassing "
    "daarna normaal af. Test vervolgens de kiosklauncher:"
)
add_code(
    doc,
    """cd "$HOME/ScoreKrijt"
python3 scorekrijt_launcher.py""",
)
doc.add_paragraph(
    "De launcher toont vijf seconden een zwart fullscreen opstartscherm, start ScoreKrijt "
    "en schrijft fouten naar scorekrijt-autostart.log."
)

doc.add_heading("8. Bluetooth voorbereiden", level=1)
doc.add_heading("8.1 Bluetooth inschakelen", level=2)
add_code(
    doc,
    """sudo systemctl enable --now bluetooth
sudo rfkill unblock bluetooth
systemctl is-active bluetooth
bluetoothctl show""",
)

doc.add_heading("8.2 Android-apparaat koppelen", level=2)
doc.add_paragraph("Start de interactieve Bluetooth-shell:")
add_code(doc, "bluetoothctl")
doc.add_paragraph("Voer daarin regel voor regel uit:")
add_code(
    doc,
    """power on
agent on
default-agent
pairable on
discoverable on
scan on""",
)
doc.add_paragraph(
    "Wacht tot het Android-apparaat verschijnt en noteer het MAC-adres. Vervang daarna "
    "<ANDROID-MAC> en voer uit:"
)
add_code(
    doc,
    """scan off
pair <ANDROID-MAC>
trust <ANDROID-MAC>
info <ANDROID-MAC>
quit""",
)
add_note(
    doc,
    "Bevestiging",
    "Vergelijk de getoonde koppelcode op beide apparaten. Accepteer uitsluitend het "
    "bedoelde Android-apparaat.",
    fill=YELLOW,
)

doc.add_heading("9. RFCOMM-poort /dev/rfcomm0 maken", level=1)
doc.add_heading("9.1 Aanbevolen: SK-Box luistert op kanaal 1", level=2)
doc.add_paragraph(
    "Deze route past bij de huidige Android-bediening: de telefoon maakt verbinding en de "
    "SK-Box luistert. Test eerst handmatig:"
)
add_code(doc, "sudo rfcomm watch /dev/rfcomm0 1")
doc.add_paragraph(
    "Laat dit Terminalvenster open en maak vanuit de Android-app verbinding. Controleer "
    "in een tweede Terminal:"
)
add_code(
    doc,
    """ls -l /dev/rfcomm0
sudo rfcomm show /dev/rfcomm0""",
)
doc.add_paragraph("Stop de handmatige test met Ctrl+C.")

doc.add_heading("9.2 Automatisch RFCOMM luisteren met systemd", level=2)
doc.add_paragraph("Maak het servicebestand:")
add_code(doc, "sudo nano /etc/systemd/system/scorekrijt-rfcomm.service")
doc.add_paragraph("Plak de volgende inhoud:")
add_code(
    doc,
    """[Unit]
Description=ScoreKrijt Bluetooth RFCOMM listener
After=bluetooth.service
Requires=bluetooth.service

[Service]
Type=simple
ExecStart=/usr/bin/rfcomm watch /dev/rfcomm0 1
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target""",
)
doc.add_paragraph("Opslaan in nano: Ctrl+O, Enter; afsluiten: Ctrl+X. Activeer daarna:")
add_code(
    doc,
    """sudo systemctl daemon-reload
sudo systemctl enable --now scorekrijt-rfcomm.service
systemctl status scorekrijt-rfcomm.service --no-pager""",
)
add_note(
    doc,
    "Poort verschijnt pas bij verbinding",
    "Bij rfcomm watch kan /dev/rfcomm0 pas zichtbaar worden wanneer de Android-app "
    "daadwerkelijk verbindt. De ScoreKrijt-service probeert zelf iedere twee seconden "
    "opnieuw, dus de startvolgorde is niet kritisch.",
)

doc.add_heading("9.3 Alleen indien nodig: binden naar een vast apparaat", level=2)
doc.add_paragraph(
    "Gebruik deze alternatiefroute alleen als de Raspberry Pi zÃ©lf de verbinding naar een "
    "vast Bluetooth-apparaat moet openen. Dit is niet de normale Android-clientroute:"
)
add_code(
    doc,
    """sudo rfcomm bind /dev/rfcomm0 <ANDROID-MAC> 1
sudo rfcomm show /dev/rfcomm0""",
)
doc.add_paragraph("Binding verwijderen:")
add_code(doc, "sudo rfcomm release /dev/rfcomm0")

doc.add_heading("10. Toegang tot /dev/rfcomm0", level=1)
doc.add_paragraph("Controleer eigenaar en groep nadat de poort bestaat:")
add_code(doc, "ls -l /dev/rfcomm0")
doc.add_paragraph(
    "Wanneer de poort tot de groep dialout behoort, voeg de desktopgebruiker eenmalig toe:"
)
add_code(
    doc,
    """sudo usermod -aG dialout "$USER"
sudo reboot""",
)
add_note(
    doc,
    "Geen chmod 777",
    "Maak de Bluetooth-poort niet wereldwijd schrijfbaar. Gebruik groepsrechten via "
    "dialout; dat is veiliger en blijft beter beheerbaar.",
    fill=YELLOW,
)

doc.add_heading("11. ScoreKrijt automatisch starten", level=1)
doc.add_heading("11.1 XDG-autostartbestand maken", level=2)
add_code(
    doc,
    """mkdir -p "$HOME/.config/autostart"
nano "$HOME/.config/autostart/scorekrijt.desktop" """,
)
doc.add_paragraph(
    "Plak onderstaande inhoud. Vervang <gebruikersnaam> door de werkelijke Linux-gebruiker:"
)
add_code(
    doc,
    """[Desktop Entry]
Type=Application
Name=ScoreKrijt SK-Box
Comment=Start ScoreKrijt in kioskmodus
Exec=/usr/bin/python3 /home/<gebruikersnaam>/ScoreKrijt/scorekrijt_launcher.py
Path=/home/<gebruikersnaam>/ScoreKrijt
Terminal=false
X-GNOME-Autostart-enabled=true""",
)
doc.add_paragraph("Controleer het bestand:")
add_code(
    doc,
    """desktop-file-validate "$HOME/.config/autostart/scorekrijt.desktop" 2>/dev/null || true
cat "$HOME/.config/autostart/scorekrijt.desktop" """,
)
doc.add_heading("11.2 Autostart testen", level=2)
add_code(doc, "sudo reboot")
doc.add_paragraph(
    "Na de automatische desktopaanmelding moet het zwarte opstartscherm verschijnen, gevolgd "
    "door het grote ScoreKrijt-scherm."
)

doc.add_heading("12. ScoreKrijt-instellingen voor de SK-Box", level=1)
doc.add_paragraph(
    "Open zo nodig het normale venster en ga naar Weergave. De aanbevolen SK-Box-waarden zijn:"
)
add_table(
    doc,
    ("Instelling", "Waarde", "Opmerking"),
    (
        ("BlueTooth Mode", "Aan", "Start Bluetooth-service in ScoreKrijt."),
        ("Groot scherm", "Aan", "Open het externe scorebord."),
        ("Open groot scherm fullscreen", "Aan", "Verberg normale venster en vul HDMI-scherm."),
        ("Geschiedenis", "Aan", "Toon drie recente regels."),
        ("Wedstrijdoverzicht", "Uit", "Android-app handelt het einde af."),
        ("Wedstrijd mailen", "Uit", "Geen lokale e-mailactie."),
        ("Nieuwe wedstrijd automatisch", "Uit", "Android-app bepaalt de volgende start."),
    ),
    (Inches(2.4), Inches(0.9), Inches(2.95)),
)
add_note(
    doc,
    "Configuratiebestand",
    "De projectkopie van ScoreKrijtSettings.json heeft BlueTooth Mode momenteel op false "
    "staan. Zet de optie in de toepassing aan en sluit ScoreKrijt normaal af zodat de "
    "instelling wordt opgeslagen.",
    fill=YELLOW,
)

doc.add_heading("13. Eindcontrole", level=1)
for item in (
    "De Pi meldt automatisch aan op de desktop.",
    "Het beeldscherm wordt niet zwart bij inactiviteit.",
    "Het ScoreKrijt-opstartscherm verschijnt circa vijf seconden.",
    "Het grote scorebord opent fullscreen.",
    "Bluetooth en scorekrijt-rfcomm.service zijn actief.",
    "De Android-app kan koppelen en verbinden.",
    "Plus, min, Noteer en Return werken op telefoon en SK-Box tegelijk.",
    "Na een herstart werkt alles zonder toetsenbord of muis.",
):
    add_bullet(doc, item)
add_code(
    doc,
    """systemctl is-active bluetooth
systemctl is-enabled scorekrijt-rfcomm.service
journalctl -u scorekrijt-rfcomm.service -n 30 --no-pager
tail -n 50 "$HOME/ScoreKrijt/scorekrijt-autostart.log" """,
)

doc.add_heading("14. Storingen oplossen", level=1)
add_table(
    doc,
    ("Probleem", "Controle", "Oplossing"),
    (
        ("Geen fullscreen", "Autologin en .desktop", "Test launcher handmatig vanuit de desktop."),
        ("Scherm wordt zwart", "Screen Blanking", "Schakel dit uit via raspi-config."),
        ("Geen /dev/rfcomm0", "RFCOMM-service en verbinding", "Controleer journalctl en verbind Android."),
        ("Permission denied", "Groep van de poort", "Voeg gebruiker toe aan dialout en herstart."),
        ("Bluetooth niet zichtbaar", "pairable/discoverable", "Zet deze tijdelijk aan in bluetoothctl."),
        ("Tkinter ontbreekt", "python3-tk", "Installeer het pakket met apt."),
        ("Pillow-fout", "python3-pil.imagetk", "Installeer beide Pillow-pakketten."),
        ("pyserial-fout", "python3-serial", "Installeer het pakket met apt."),
        ("App start niet", "autostartlog", "Lees scorekrijt-autostart.log."),
        ("Verkeerd lettertype", "Bodoni beschikbaar?", "Installeer een gelicentieerd font of kies aanwezig font."),
    ),
    (Inches(1.65), Inches(1.75), Inches(2.85)),
)

doc.add_heading("15. Programma bijwerken", level=1)
add_step(doc, "Stop ScoreKrijt", "Sluit de toepassing normaal af.")
add_step(
    doc,
    "Maak een back-up",
    "Kopieer minimaal ScoreKrijtSettings.json en de map matches naar een veilige locatie.",
)
add_step(
    doc,
    "Vervang programmabestanden",
    "Kopieer de nieuwe versie over de bestaande map, maar controleer vÃ³Ã³r overschrijven "
    "of het instellingenformaat is gewijzigd.",
)
add_step(doc, "Test handmatig", "Start python3 ScoreKrijt.py en controleer Bluetooth.")
add_step(doc, "Herstart", "Voer sudo reboot uit en doorloop de eindcontrole.")

doc.add_heading("16. Bronnen en versie-opmerking", level=1)
doc.add_paragraph(
    "De applicatiespecifieke waarden zijn gebaseerd op de projectbestanden "
    "scorekrijt_launcher.py, bluetooth_service.py, bluetooth_protocol.py, application.py "
    "en ScoreKrijtSettings.json. De systeemstappen zijn gecontroleerd tegen:"
)
for source in (
    "Raspberry Pi Documentation - Configuration: https://www.raspberrypi.com/documentation/computers/configuration.html",
    "Raspberry Pi Documentation - Remote access/SSH: https://www.raspberrypi.com/documentation/remote-access/ssh.html",
    "Debian Bookworm manpage bluetoothctl: https://manpages.debian.org/bookworm/bluez/bluetoothctl.1.en.html",
    "Debian Bookworm manpage rfcomm: https://manpages.debian.org/bookworm/bluez/rfcomm.1.en.html",
):
    add_bullet(doc, source)
add_note(
    doc,
    "Versies",
    "Menunamen in raspi-config en desktop-autostartgedrag kunnen bij toekomstige Raspberry "
    "Pi OS-versies wijzigen. Controleer bij een nieuw OS-image altijd eerst de actuele "
    "Raspberry Pi-documentatie.",
)

doc.save(OUT)
print(OUT)


