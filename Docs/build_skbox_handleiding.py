from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Handleiding_SK-Box_instellingen.docx"
LOGO = ROOT / "Logos" / "ScoreKrijt Logo.png"

BLUE = "214F6B"
LIGHT_BLUE = "E8F1F6"
PALE = "F4F6F8"
GOLD = "C7942E"
INK = RGBColor(33, 39, 43)
MUTED = RGBColor(95, 105, 112)


def set_cell_fill(cell, color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), color)


def set_cell_margins(cell, top=90, start=120, bottom=90, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for tag, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{tag}"))
        if node is None:
            node = OxmlElement(f"w:{tag}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_run(run, size=10.5, bold=False, color=INK, italic=False):
    run.font.name = "Aptos"
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Aptos")
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Aptos")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    set_run(p.add_run(text))
    return p


def add_step(doc, title, text):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(f"{title}. ")
    set_run(r, bold=True)
    set_run(p.add_run(text))


def add_note(doc, label, text, color=LIGHT_BLUE):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.25)
    cell = table.cell(0, 0)
    set_cell_fill(cell, color)
    set_cell_margins(cell, top=130, bottom=130, start=180, end=180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    set_run(p.add_run(f"{label}: "), bold=True, color=RGBColor.from_string(BLUE))
    set_run(p.add_run(text))
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_settings_table(doc, rows):
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    widths = (Inches(2.45), Inches(1.05), Inches(2.75))
    headers = ("Instelling", "Waarde", "Betekenis")
    for idx, (cell, text, width) in enumerate(zip(table.rows[0].cells, headers, widths)):
        cell.width = width
        set_cell_fill(cell, BLUE)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_run(p.add_run(text), bold=True, color=RGBColor(255, 255, 255))
    set_repeat_table_header(table.rows[0])
    for name, value, meaning in rows:
        cells = table.add_row().cells
        for cell, text, width in zip(cells, (name, value, meaning), widths):
            cell.width = width
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_run(cell.paragraphs[0].add_run(text), size=9.5)
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

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Aptos"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
normal.font.size = Pt(10.5)
normal.font.color.rgb = INK
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15

for style_name, size, before, after in (
    ("Heading 1", 16, 16, 8),
    ("Heading 2", 13, 12, 6),
    ("Heading 3", 11.5, 9, 4),
):
    style = styles[style_name]
    style.font.name = "Aptos Display"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Aptos Display")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos Display")
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor.from_string(BLUE)
    style.paragraph_format.space_before = Pt(before)
    style.paragraph_format.space_after = Pt(after)
    style.paragraph_format.keep_with_next = True

header = section.header
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
set_run(hp.add_run("ScoreKrijt  |  SK-Box"), size=8.5, bold=True, color=MUTED)
footer = section.footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(fp.add_run("Beheerhandleiding - instellingen en werking"), size=8, color=MUTED)

# Editorial-cover opening.
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
set_run(p.add_run("HANDLEIDING"), size=10, bold=True, color=RGBColor.from_string(GOLD))
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
set_run(p.add_run("Instellingen van de SK-Box"), size=28, bold=True, color=RGBColor.from_string(BLUE))
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(30)
set_run(p.add_run("ScoreKrijt groot-scherm, kioskstart en Bluetooth-bediening"), size=13, color=MUTED)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Gebaseerd op de projectconfiguratie van 30 juli 2026"), size=9.5, italic=True, color=MUTED)

doc.add_page_break()

doc.add_heading("1. Doel van deze handleiding", level=1)
doc.add_paragraph(
    "Deze handleiding beschrijft de instellingen die in het ScoreKrijt-project voor de "
    "SK-Box zijn vastgelegd. De SK-Box is bedoeld als zelfstandig scorebord: na het "
    "opstarten verschijnt ScoreKrijt op het grote scherm en kan een Android-apparaat de "
    "wedstrijd via Bluetooth bedienen."
)
add_note(
    doc,
    "Afbakening",
    "De applicatie-instellingen en communicatieparameters zijn uit de projectbestanden "
    "overgenomen. Exacte Raspberry Pi OS-instellingen zoals hostnaam, wifi, gekoppelde "
    "Bluetooth-MAC-adressen en het gebruikte autostartbestand zijn niet in deze map "
    "vastgelegd en worden daarom niet als toegepaste waarden gepresenteerd.",
)

doc.add_heading("2. Werking bij het opstarten", level=1)
add_step(doc, "Start de SK-Box", "Zet de box en het aangesloten scherm aan.")
add_step(
    doc,
    "Kiosklauncher",
    "De launcher start ScoreKrijt vanuit zijn eigen programmamap en schrijft meldingen "
    "naar scorekrijt-autostart.log.",
)
add_step(
    doc,
    "Opstartscherm",
    "Gedurende 5 seconden wordt een zwart, beeldvullend ScoreKrijt-scherm getoond. "
    "De muiscursor is daarbij verborgen.",
)
add_step(
    doc,
    "Groot scherm",
    "ScoreKrijt opent het grote scorebord. Wanneer fullscreen actief is, wordt het "
    "normale bedieningsvenster verborgen.",
)
add_step(
    doc,
    "Bluetooth",
    "Als BlueTooth Mode aan staat, start de communicatie ongeveer een halve seconde "
    "na het openen van de applicatie. Bij een verbroken verbinding probeert de service "
    "na 2 seconden opnieuw te verbinden.",
)

doc.add_heading("3. Toegepaste hoofdinstellingen", level=1)
add_settings_table(
    doc,
    [
        ("Lettertype", "Bodoni", "Lettertype van de scoreweergave."),
        ("Groot scherm", "Aan", "Het externe scorebord wordt direct geopend."),
        ("Groot scherm fullscreen", "Aan", "Het scorebord vult het volledige scherm."),
        ("Startkleur", "Geel", "Eerste ingestelde speelkleur."),
        ("Geschiedenis tonen", "Aan", "De laatste beurten blijven zichtbaar."),
        ("Wedstrijdvorm", "Vaste beurten", "Standaard wedstrijdtype."),
        ("Aantal beurten", "30", "Standaard aantal vaste beurten."),
        ("Wedstrijdoverzicht", "Uit", "Geen lokaal eindoverzicht op de SK-Box."),
        ("Vragen om te mailen", "Uit", "Geen lokale e-mailvraag na de wedstrijd."),
        ("Automatisch nieuwe wedstrijd", "Uit", "De Android-app bepaalt de volgende start."),
        ("Open wedstrijden controleren", "Uit", "Geen controleprompt bij het opstarten."),
        ("Oude wedstrijden opruimen", "Aan", "Automatische opschoning is actief."),
        ("Bewaartermijn", "5 jaar", "Wedstrijden ouder dan deze termijn worden verwijderd."),
    ],
)
add_note(
    doc,
    "Belangrijk",
    "In het aanwezige ScoreKrijtSettings.json staat BlueTooth Mode op Uit. Voor gebruik "
    "als SK-Box met de Android-app moet deze optie op Aan staan en daarna moet ScoreKrijt "
    "opnieuw worden gestart. De programmasturing zet dan automatisch Groot scherm en "
    "Fullscreen aan en schakelt lokale eindacties uit.",
    color="FFF4D6",
)

doc.add_heading("4. Groot-scherminstellingen", level=1)
add_settings_table(
    doc,
    [
        ("Middenkolom-deler", "5", "Verhouding voor de middenkolom."),
        ("Beurt - label", "70 pt", "Tekstgrootte van het beurtlabel."),
        ("Beurt - waarde", "100 pt", "Tekstgrootte van het actuele beurtnummer."),
        ("Huidige caramboles - label", "50 pt", "Tekstgrootte van de omschrijving."),
        ("Huidige caramboles - waarde", "60 pt", "Tekstgrootte van de actuele invoer."),
        ("Aantal historieregels", "3", "Aantal zichtbare eerdere beurten."),
        ("Historie - label", "30 pt", "Tekstgrootte in het historieblok."),
        ("Historie - waarde", "30 pt", "Waardeweergave in het historieblok."),
        ("Carambole-informatie - label", "50 pt", "Tekstgrootte van het informatielabel."),
        ("Carambole-informatie - waarde", "200 pt", "Grote centrale scoreweergave."),
        ("Statistieken - label", "30 pt", "Tekstgrootte van statistieklabels."),
        ("Statistieken - waarde", "50 pt", "Tekstgrootte van statistiekwaarden."),
    ],
)

doc.add_heading("5. Grenzen voor wedstrijdinvoer", level=1)
add_settings_table(
    doc,
    [
        ("Minimale TMC", "6", "Laagste toegestane TMC-waarde."),
        ("Maximale TMC", "999", "Hoogste toegestane TMC-waarde."),
        ("Minimum aantal beurten", "10", "Ondergrens in de instellingen."),
        ("Spelernaam", "Max. 14 tekens", "Langere ontvangen namen worden begrensd."),
    ],
)

doc.add_heading("6. Bluetooth-configuratie", level=1)
add_settings_table(
    doc,
    [
        ("Techniek", "Bluetooth Classic SPP", "Seriële Bluetooth-verbinding."),
        ("Linux-poort", "/dev/rfcomm0", "Virtuele seriële poort van de koppeling."),
        ("Baudrate", "9600", "Communicatiesnelheid."),
        ("Leestime-out", "1 seconde", "Wachttijd per leesactie."),
        ("Automatisch herstellen", "Aan", "Opnieuw proberen na verbindingsverlies."),
        ("Herstelinterval", "2 seconden", "Pauze vóór een nieuwe verbindingspoging."),
        ("Berichtformaat", "JSON + nieuwe regel", "Ieder commando staat op één regel."),
    ],
)
doc.add_heading("Ondersteunde bediening", level=2)
for text in (
    "verbinding testen en status opvragen;",
    "een nieuwe wedstrijd starten of een bestaande wedstrijd bijwerken;",
    "score verhogen en verlagen;",
    "de beurt vastleggen en doorgaan naar de volgende speler;",
    "de vorige actie of beurt terugnemen;",
    "de wedstrijd afsluiten en de scorebordweergave terugzetten.",
):
    add_bullet(doc, text)

doc.add_heading("7. Instellingen controleren of wijzigen", level=1)
add_step(doc, "Open het menu", "Ga in ScoreKrijt naar Weergave.")
add_step(
    doc,
    "Controleer de kioskopties",
    "Zet Groot scherm, Open Groot scherm in full screen en Geschiedenis aan.",
)
add_step(
    doc,
    "Activeer Bluetooth",
    "Zet BlueTooth Mode aan wanneer de Android-app de SK-Box moet bedienen.",
)
add_step(
    doc,
    "Open Instellingen",
    "Controleer de groot-schermwaarden en pas alleen aan wanneer de tekst op het "
    "aangesloten scherm niet goed leesbaar is.",
)
add_step(
    doc,
    "Herstart ScoreKrijt",
    "Na het wijzigen van de Bluetooth-modus is een herstart de veiligste manier om de "
    "communicatieservice en de kioskweergave met de nieuwe waarden te laden.",
)

doc.add_heading("8. Snelle controle na onderhoud", level=1)
for text in (
    "Het zwarte ScoreKrijt-opstartscherm verschijnt ongeveer 5 seconden.",
    "Het scorebord opent automatisch en beeldvullend.",
    "Er is geen bureaublad of muiscursor zichtbaar tijdens het opstartscherm.",
    "De Android-app kan de SK-Box vinden en verbinden.",
    "Plus, min, Noteer en Return veranderen telefoon en scorebord tegelijk.",
    "Bij wedstrijdafsluiting worden beurt en huidige caramboles op 0 gezet.",
    "Beide spelers krijgen na afsluiting weer hun normale speelkleuren.",
):
    add_bullet(doc, text)

doc.add_heading("9. Storingen oplossen", level=1)
add_settings_table(
    doc,
    [
        (
            "Applicatie start niet",
            "Bekijk scorekrijt-autostart.log",
            "De launcher schrijft standaarduitvoer en fouten naar dit bestand.",
        ),
        (
            "Geen Bluetooth",
            "Controleer BlueTooth Mode",
            "Deze moet Aan staan; start ScoreKrijt daarna opnieuw.",
        ),
        (
            "Poort ontbreekt",
            "Controleer /dev/rfcomm0",
            "De gekoppelde Bluetooth-verbinding moet deze seriële poort aanbieden.",
        ),
        (
            "Fout over pyserial",
            "Installeer/controleer pyserial",
            "De Bluetooth-service kan zonder deze Python-module niet starten.",
        ),
        (
            "Verbinding valt weg",
            "Wacht enkele seconden",
            "De service probeert automatisch iedere 2 seconden te herstellen.",
        ),
        (
            "Scorebord niet fullscreen",
            "Controleer beide schermopties",
            "Groot scherm en fullscreen moeten beide ingeschakeld zijn.",
        ),
    ],
)

doc.add_heading("10. Beheer- en veiligheidsnotities", level=1)
for text in (
    "Bewaar e-mailwachtwoorden of app-wachtwoorden niet in een gedeelde handleiding.",
    "Maak vóór grotere wijzigingen een kopie van ScoreKrijtSettings.json.",
    "Wijzig Bluetooth-poort en baudrate alleen wanneer ook de Raspberry Pi-koppeling wordt aangepast.",
    "Voer na iedere update de snelle controle uit hoofdstuk 8 uit.",
):
    add_bullet(doc, text)

add_note(
    doc,
    "Bronnen binnen het project",
    "ScoreKrijtSettings.json, scorekrijt_launcher.py, bluetooth_service.py, "
    "bluetooth_protocol.py, application.py, menu.py en CHANGELOG.md. Gevoelige "
    "e-mailgegevens uit het configuratiebestand zijn bewust niet overgenomen.",
)

doc.save(OUT)
print(OUT)
