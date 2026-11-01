# ScoreKrijt changelog

## V2.8.8 – moyenne in het CSV-bestand en laatste wedstrijd heropenen

Alleen de Android-app is gewijzigd; de SK-Box blijft ongewijzigd (code 2.8.7) en het Bluetooth-protocol blijft versie 2. Nog niet op een telefoon getest.

### Android-app

- CSV-bestand: de moyenne staat nu als tekstformule (`="0,333"`) in het bestand. Een spreadsheet met een Engelse taalinstelling las `0,333` eerder als duizendtal en toonde `333`; nu staat er in elke taalinstelling `0,333`. Het tekstoverzicht is niet veranderd. Let op: de cel is tekst, geen getal.
- De app onthoudt de laatst gespeelde wedstrijd, ook na het afronden (`Verzenden & Sluiten`, `Alleen Sluiten`). In het hoofdmenu staat dan de knop `Laatste wedstrijd openen`. Die opent de wedstrijd op de laatste beurt (bijvoorbeeld beurt 30) met speler 2 aan de beurt en de score van die beurt nog open, zodat je die kunt aanpassen en opnieuw kunt noteren. Het totaal telt de open score niet dubbel.
- Is er een lopende wedstrijd, dan blijft de knop `Hervat Wedstrijd`. Het scherm voor het bepalen van de aanvang toont de knop voor een afgeronde wedstrijd niet en vraagt dan ook niet om bevestiging.
- Versienummer is `2.8.8` (app).

## V2.8.7 – kleine verbeteringen in de app

Voltooid en getest op 27 oktober 2026. Alle onderdelen hieronder zijn door de gebruiker op een telefoon en op de SK-Box getest. De Python-code is daarnaast gecontroleerd met Python 3.11 (Anaconda): een syntaxiscontrole van alle bestanden en een rooktest van de SK-Box met het grote scherm (namen en TMC vooraf, witte vakken, procenten, punten bij vaste beurten, negeren tijdens een lopende wedstrijd). Het Bluetooth-protocol blijft versie 2.

### Android-app

- Moyenne in het verzonden CSV-bestand (`<speler> moyenne`, onder het totaal aantal caramboles) en in het tekstoverzicht. Moyenne is het totaal aantal caramboles gedeeld door de gespeelde beurten van die speler, met drie decimalen en een komma. Een onthouden tussenstand na Undo telt niet als beurt. Bij het tijdelijke overzicht telt de lopende beurt mee.
- De lijst bij het verbinden heet `Selecteer SK-Box` (was `SK-Box verbinden`).
- Enkel spel, Uit is uit: onder `Gelijkspel aan` staat nu `(verlenging uit)` en onder `Gelijkspel uit` staat `(verlenging aan)`.
- Knoppen: licht afgeronde hoeken (6 dp) via het thema, in plaats van de volledig ronde zijkanten. Knoppen met een eigen hoekinstelling (zoals 0 dp in het wedstrijdscherm) blijven zoals ze waren.
- Instellingen tijdens een wedstrijd met verbonden SK-Box: de drie knoppen (Instellingen SK-Box, Synchroniseer naar en van SK-Box) zijn nu even hoog en hebben allemaal twee regels tekst.
- Wedstrijdscherm: tikken op de beurt (het middelste vak met `Beurt` en het nummer) opent het tijdelijke wedstrijdoverzicht, net als de knop in de instellingen.
- Alle drukknoppen hebben reliëf: een schaduw in rust die verdwijnt als je erop drukt, plus een dunne donkere rand (`Widget.ScoreKrijt.Button` in `themes.xml`; hoogte in `dimens.xml`). De tekstknoppen in dialogen (zoals Annuleren en Sluiten) blijven plat, maar hebben dezelfde hoeken (`ThemeOverlay.ScoreKrijt.AlertDialog`). De vier grote knoppen in het wedstrijdscherm liggen strak tegen elkaar en tegen de rand, waar een schaduw niet zichtbaar is; die hebben daarom een opgehoogde rand (lichte rand boven en links, donkere rand onder en rechts, ingedrukt omgekeerd) via `drawable/bevel_raised.xml`.
- Wedstrijdscherm: Help / spelregels, Instellingen en het vak met de beurt hebben ook een opgehoogde rand (`drawable/bevel_raised_small.xml`).
- Wedstrijdscherm: `Beurt` staat nu bovenin het middelste vak, even groot (14 sp) en op dezelfde hoogte als `Caramboles`.
- Uit is uit: het kopje `Punten` heet `Procent` en toont het percentage van het te maken aantal (naar beneden afgerond; 100 procent is gelijk aan 10 punten, dus de wedstrijd eindigt op hetzelfde moment). De tekst `En nog # tot volgend punt` is `En nog #` en telt het aantal caramboles dat nog nodig is om uit te zijn. Bij vaste beurten blijft alles zoals het was. Het CSV-bestand en het tekstoverzicht tonen nog punten.
- SK-Box, groot scherm: bij Uit is uit toont de kolom `Punten` ook procenten (kopje `Procent`, zonder %-teken in het vak) en de kolom `Car. tot punt` het aantal caramboles tot uit (kopje `Car. tot uit`). Dit wordt in `BSInfoFrame` (`widgets.py`) uitgerekend uit de bestaande waarden; de spellogica is niet gewijzigd. Het hoofdvenster van de SK-Box (verborgen in Bluetooth-modus) toont nog punten.
  (Vervolg: de herkenning van `Uit is uit` is hoofdletterongevoelig en onverwachte fouten in deze berekening komen met een traceback in `scorekrijt-autostart.log`.)
- Bepalen aanvang wedstrijd: als de SK-Box verbonden is, worden de namen en TMC alvast naar de SK-Box gestuurd (nieuw commando `prepare_match`), zodat ze op het grote scherm staan terwijl de telefoon de aanvang bepaalt. De app stuurt dit altijd als er verbinding is; de beveiliging zit aan de SK-Box-kant: die negeert het bericht als er een wedstrijd loopt (`Turn` groter dan 0). Een oudere SK-Box kent het commando niet en antwoordt met een melding die in dit scherm niet wordt getoond. De SK-Box start er geen wedstrijd mee (geen timer, geen wedstrijdbestand). Zolang nog niet bepaald is wie begint, zijn alle bovenste vakken op het grote scherm wit; de kleuren komen bij het starten van de wedstrijd. Het Bluetooth-protocol blijft versie 2.
- Handleidingen: de gebruikersnaam `user` en het wachtwoord `user` van de SK-Box staan nu in de handleiding (inclusief een opmerking dat het een eenvoudig wachtwoord is) en vervangen de plaatshouder `<gebruikersnaam>`.
- De map met de SK-Box-code is hernoemd van `Phyton/V2.8.5 Bleutooth` naar `Phyton/V2.8.7`. De bestanden en de updateroute (`ScoreKrijt_update` op de stick, `~/ScoreKrijt` op de SK-Box) zijn niet veranderd.
- SK-Box: F12 toont of verbergt de taakbalk nu ook in het gewone ScoreKrijt-venster, als het grote scherm niet aan staat (eerder alleen in het grote scherm).
- AI-vermelding: de app (Help / spelregels, `Over Score Krijt`), het About-venster van de SK-Box, de README en de handleidingen vermelden dat ScoreKrijt met behulp van AI is gemaakt.
- Handleidingen: `Handleiding_SK-Box_instellingen` is opnieuw gemaakt (nieuwe opstart, regelaars en bereiken, procenten, toetsen, Bluetooth) en wordt nu ook met `Docs/build_skbox_handleidingen.ps1` gebouwd. De oude Python-bouwscripts staan in `Docs/Archief`.
- Versienummer is `2.8.7` (app en SK-Box).

### Getest

- Door de gebruiker getest op 27 oktober 2026: de schermen en knoppen in de app, Uit is uit (procenten, `En nog #`), de SK-Box (procenten en punten, namen en TMC vooraf ook bij het eerste spel, witte vakken, F12 ook zonder groot scherm), de moyenne en een korte wedstrijd met de bugfixes uit 2.8.5.

## V2.8.6 – SK-Box zonder internet, instellingen groot scherm en opstartscherm

Laatst bijgewerkt: 27 oktober 2026. Het Bluetooth-protocol blijft versie 2. Op 27 oktober door de gebruiker op de SK-Box en de telefoon bekeken: het opstartscherm, F12 en de aanpassing van de middelste kolom werken, en de Bluetooth-verbinding blijft langdurig stabiel. De map met de SK-Box-code heet sinds 2.8.7 `V2.8.7` (eerder `V2.8.5 Bleutooth`).

### Android-app

- SK-Box-instellingen: nieuwe regelaar `Breedte middelste kolom` (10-60 procent, standaard 20).
- Ruimere bereiken voor alle lettergroottes, bijvoorbeeld waarde caramboles / score tot 500, spelersnamen tot 200, waarde beurt tot 300.
- Versienummer is `2.8.6` (versionName `2.8.6`, versionCode `286`, hello-bericht).
- Build: een taak in `app/build.gradle.kts` ruimt `desktop.ini`-bestanden van Google Drive op voordat de resources worden samengevoegd. Zonder die taak stopte Android Studio met "The file name must end with .xml or .png".

### SK-Box (Python, map `V2.8.5 Bleutooth`)

- Groot scherm: de breedte van de middelste kolom is een percentage (`BS Mid col. width percent`). De kolommen worden via gewichten verdeeld. Een oude instelling `BS Mid col. width divider` wordt omgerekend. De oude resize-functie is verwijderd; die reageerde ook op afmetingen van onderdelen in het venster.
- Dezelfde ruimere bereiken in `models.py`, ook voor het instellingenscherm op de SK-Box zelf.
- Het groot scherm vraagt volledig scherm na het opstarten nog een paar keer opnieuw aan, omdat het eerste verzoek op de SK-Box soms werd genegeerd.
- F12 op het groot scherm toont of verbergt de taakbalk (`toggle_taskbar`).
- `scorekrijt_launcher.py`: start ScoreKrijt niet een tweede keer als het al draait (`scorekrijt.lock`). Het opstartscherm blijft staan tot ScoreKrijt klaar is (`scorekrijt.ready`), met "SK-Box wordt gestart" en bewegende puntjes, minimaal 3 en hoogstens 90 seconden. Het toont `ScoreKrijt Logo.png` in plaats van `biljart.png`.
- `bluetooth_service.py`: fouten waardoor de poort sluit (en de verbinding wegvalt) komen met tijdstip in `scorekrijt-autostart.log`. Alleen diagnose.
- `APP_VERSION = "2.8.6"`.

Telefoon en SK-Box kunnen apart worden bijgewerkt, maar de regelaar voor de middelste kolom en de hogere maxima werken alleen als beide 2.8.6 zijn. Een oudere SK-Box weigert waarden boven het oude maximum met een foutmelding.

### Hulpscripts (`Phyton/SK-Box_scripts`)

- `sk-update.sh`: bijwerken vanaf een USB-stick, zonder internet. Controleert de bestanden, behoudt `ScoreKrijtSettings.json` en `matches`, bewaart de vorige versie als `ScoreKrijt_vorige_<nummer>_<datum>` en kan met `--terug` terugdraaien.
- `sk-stille-opstart.sh`: geen Raspberry Pi-logo's en opstarttekst, taakbalk uit `/etc/xdg/labwc/autostart` (een kopie in `~/.config/labwc` liet de taakbalk draaien en ScoreKrijt dubbel starten), ScoreKrijt-logo op de achtergrond en in het opstartscherm van Linux (Plymouth, thema pix; verkleinde kopie in `~/.local/share/scorekrijt/logo.png`). Opties `--wifi-uit`, `--sneller` (cloud-init uit, ongeveer 3 seconden) en `--terugdraaien`.

### Handleidingen

- Installatiehandleiding: hoofdstuk 13 (stille opstart), hoofdstuk 14 (gebruik zonder internet), hulpscripts in 6.4, controle van de Bluetooth-koppeling in 8.2 en nieuwe storingsregels.
- Updatehandleiding: USB-stick met script als eerste route, handmatig met USB als tweede, SSH als derde.
- Gebouwd met `Docs/build_skbox_handleidingen.ps1`.

### Getest

- Door de gebruiker getest op 27 oktober 2026: opstartscherm met logo, F12, breedte van de middelste kolom en een stabiele Bluetooth-verbinding.
- De handleiding van de instellingen is bijgewerkt in 2.8.7.

## V2.8.5 – bugfixes (Android-app en SK-Box, versienummers gelijkgetrokken)

Laatst bijgewerkt: 27 oktober 2026. Door de gebruiker getest op een echte telefoon en SK-Box (samen met 2.8.6 en 2.8.7). Het Bluetooth-protocol blijft versie 2, dus telefoon en SK-Box hoeven niet tegelijk te worden bijgewerkt.

### Android-app

- Undo telt een eerder genoteerde beurt niet langer dubbel mee in punten en `nog te maken`.
- Een beurt die na Undo opnieuw wordt genoteerd, verliest geen caramboles meer.
- Onthouden tussenstanden na Undo verschijnen niet meer als gespeelde beurt in het CSV-bestand, het wedstrijd-overzicht en de berichten naar de SK-Box.
- Een afgeronde wedstrijd verschijnt na `Verzenden & Sluiten` of `Alleen Sluiten` niet meer opnieuw als te hervatten wedstrijd.
- Na het annuleren van het eindscherm telt de speeltijd niet meer de tijd mee dat het scherm openstond.
- Versienummer van de app is `2.8.5` (versionName/versionCode en hello-bericht).

### SK-Box (Python, map `V2.8.5 Bleutooth`)

- Bij `Uit is uit` crasht het afronden van een wedstrijd op de SK-Box zelf niet meer (ontbrekende `player_is_out`).
- `APP_VERSION = "2.8.5"` toegevoegd en meegestuurd in `connection_match_status`.

## V2.8 – voltooid en getest

Laatst bijgewerkt: 3 september 2026.

### Gerealiseerd

- Instellingenknop voor de SK-Box toegevoegd aan het hoofdscherm van de Android-app; zichtbaar bij een actieve verbinding.
- Actuele Bluetooth-verbindingsstatus en naam van de verbonden SK-Box worden getoond.
- Basisscherm `SK-Box-instellingen` en de navigatie ernaartoe zijn toegevoegd.
- De lettergrootte van ieder ondersteund tekstonderdeel op het SK-Box-grootscherm kan afzonderlijk via de telefoon worden aangepast en direct als voorbeeld worden getoond.
- Het geschiedenisvak kan via de telefoon worden in- of uitgeschakeld; ook de lettergrootte en het aantal zichtbare beurten zijn instelbaar.
- Gewijzigde grootscherminstellingen kunnen permanent op de SK-Box worden opgeslagen of naar de standaardweergave worden hersteld.
- De TMC-instelling is volledig instelbaar, wordt direct toegepast en blijft na opnieuw opstarten behouden.
- Bij het verbinden controleert de telefoon of op de SK-Box al een wedstrijd actief is.
- Een actieve SK-Box-wedstrijd kan inclusief spelers, scores, beurt, actieve speler, wedstrijdinstellingen, tijden en beurtgeschiedenis op de telefoon worden hervat.
- De gebruiker krijgt vóór het overnemen van een SK-Box-wedstrijd een duidelijke keuze, zodat lokale wedstrijdgegevens niet stilzwijgend worden overschreven.
- Wedstrijdstatus en overige opdrachten gebruiken afzonderlijke Bluetooth-berichten met terugkoppeling van de SK-Box.
- Telefoonapp en SK-Box controleren bij het verbinden of hun Bluetooth-protocolversies overeenkomen en tonen bij een verschil welk onderdeel moet worden bijgewerkt.
- Na een onverwachte Bluetooth-onderbreking probeert de telefoonapp maximaal drie keer automatisch opnieuw te verbinden; daarna verschijnt een knop `Opnieuw verbinden`.
- Het helpgedeelte bevat uitleg over verbinden, opnieuw verbinden, synchroniseren, grootscherminstellingen en het controleren van Bluetooth-communicatie.

- De volledige V2.8-functionaliteit is praktisch getest met een echte telefoon en SK-Box.

Zie `ROADMAP.md` voor de geplande onderdelen van V2.9.

## V2.7

- Hoofdmenu uitgebreid met `Laatste wedstrijd overzicht`.
- Laatste afgeronde wedstrijd wordt opgeslagen als overzicht en kan later opnieuw bekeken worden.
- Laatste wedstrijd-overzicht kan opnieuw verzonden worden vanuit het hoofdmenu.
- Tijdens een lopende wedstrijd is via `Instellingen` een `Tijdelijk wedstrijd overzicht` beschikbaar.
- Tijdelijk wedstrijd-overzicht kan worden verzonden zonder de wedstrijd af te sluiten.
- `Verzenden & Sluiten` bij einde wedstrijd deelt weer het CSV-bestand via Android delen, bijvoorbeeld WhatsApp of e-mail.
- Na sluiten van het CSV-deelvenster keert de app terug naar het hoofdmenu.
- `Alleen Sluiten` keert direct terug naar het hoofdmenu.
- Wedstrijdvorm wordt onthouden voor volgende wedstrijden.
- Keuze `Gelijkspel aan/uit` wordt onthouden voor volgende wedstrijden.
- Aantal vaste beurten blijft standaard 30, maar wordt onthouden als dit wordt aangepast.

## V2.6

- Bij `Uit is uit` is een keuze toegevoegd voor gelijkspel:
  - `Gelijkspel aan`: als beide spelers tegelijk 10 punten halen, eindigt de wedstrijd als gelijkspel.
  - `Gelijkspel uit`: de bestaande verlenging blijft actief.
- Wedstrijd-overzicht na afloop uitgebreid met afsluitknoppen.
- Knoppen onder het wedstrijd-overzicht sturen terug naar het hoofdmenu.
- `Verzenden & Sluiten` bedoeld voor delen van het wedstrijdverslag.
- `Alleen Sluiten` sluit de wedstrijd zonder verzenden.

## V2.5

- Android app en SK-Box verder gesynchroniseerd via Bluetooth.
- Bij einde wedstrijd stuurt de app `match_finished` naar de SK-Box.
- SK-Box zet bij einde wedstrijd de beurt op `0`.
- SK-Box zet huidige caramboles terug naar `0`.
- SK-Box toont beide spelers weer in hun normale speelkleuren.
- SK-Box verwerkt `match_finished` als apart Bluetooth-commando.
- Namen zijn begrensd op maximaal 14 tekens in de Android app.
- SK-Box beperkt ontvangen namen ook tot maximaal 14 tekens.
- Python-bestanden voor de SK-Box aangepast zodat update-, start- en finish-commando's beter gescheiden worden verwerkt.

## V2.4

- Instellingen tijdens een lopende wedstrijd worden naar de SK-Box verzonden.
- Aanpassingen zoals spelernaam, TMC en startkleur worden via Bluetooth doorgestuurd.
- SK-Box verwerkt `update_match` vanuit de app.
- Puntentelling op de SK-Box aangepast zodat de actuele beurt alleen bij de actieve speler meetelt.

## V2.3

- Hervatten van een wedstrijd aangepast zodat de SK-Box dit niet meer als nieuwe wedstrijd interpreteert.
- Bij hervatten stuurt de app een update van de bestaande wedstrijdstatus in plaats van een nieuwe wedstrijdstart.
- Opgeslagen wedstrijdstatus bevat spelers, TMC, kleur, beurten, huidige caramboles en historie.

## V2.2

- Vorige-speler/undo gedrag aangepast.
- De app onthoudt nu gemaakte caramboles per speler en per beurt.
- Als je teruggaat naar een vorige speler en daarna weer vooruitgaat, wordt de eerder ingevulde score opnieuw getoond.
- App-gedrag is hiermee gelijkgetrokken met het SK-Box gedrag.

## V2.1

- Bluetooth-bediening tussen Android app en SK-Box uitgebreid.
- Knoppen `+`, `-`, `Noteer` en `Return` sturen acties naar de SK-Box.
- Caramboles worden op telefoon en SK-Box tegelijk bijgewerkt.
- Spelergegevens, startkleur en puntenberekening verder gecorrigeerd.

## V2.0

- `SK-Box verbinden` toegevoegd aan het hoofdmenu.
- Bluetooth-apparaten worden in een lijst getoond.
- Bluetooth-apparaatnaam en ID worden overzichtelijker weergegeven.
- Scrollbar toegevoegd voor langere Bluetooth-apparatenlijsten.
- Android Bluetooth-permissies uitgebreid voor nieuwere Android-versies.
- Verbinding met Raspberry Pi/SK-Box opgezet via Bluetooth.
