# ScoreKrijt-roadmap V2.8.8 t/m V3.1

**Status:** gepland

**Laatst bijgewerkt:** 29 oktober 2026

V2.8.7 is voltooid en praktisch getest. Deze roadmap verdeelt de volgende uitbreidingen over vijf afzonderlijke releases. Afgeronde onderdelen worden na implementatie en controle naar `CHANGELOG.md` verplaatst.

## Release-indeling

- **V2.8.8:** moyenne correct in het CSV-wedstrijdbestand en het laatst gespeelde spel onthouden in de telefoonapp.
- **V2.9:** uitsluitend de spelsoort `10 over rood`, inclusief bediening op telefoon en SK-Box.
- **V2.9.5:** de spelsoort `Honderden`, voortbouwend op de meerspelersbasis van V2.9.
- **V3.0:** competities instellen via de telefoon en blijvend opslaan en volgen op de SK-Box.
- **V3.1:** biljarttrainer voor libre, bandstoten en driebanden, inclusief stootadvies en fotoherkenning.

Een latere release wordt pas gestart wanneer de voorgaande release is geïmplementeerd, getest en in `CHANGELOG.md` als voltooid is genoteerd.

## Globale appflow

De aangeleverde flowschema's dienen als voorlopige navigatiereferentie voor de volledige app. Ze beschrijven de hoofdroute en competitieflow, maar zijn nog niet compleet en gelden daarom niet als definitieve schermspecificatie.

### Hoofdmenu

Vanuit het keuzemenu kan de gebruiker naar:

- `Enkel spel`;
- `10 over rood`;
- `Honderden`;
- `Biljarttrainer`.
- `SK-Box koppelen`;
- `Competities`, nadat een SK-Box is verbonden;


### Enkel spel

1. Spelersnamen invoeren of beschikbare spelersgegevens ophalen van de SK-Box.
2. TMC of gemiddelde per speler instellen.
3. Wedstrijdvorm instellen: aantal beurten of `Uit is uit`.
4. Bij vaste beurten het aantal beurten instellen.
5. Doorgaan naar `Aanvang wedstrijd`.
6. Startende speler en startkleur selecteren.
7. Wedstrijd starten.

### `10 over rood`

1. Spelers invoeren of beschikbare spelersgegevens ophalen van de SK-Box.
2. Spelers toevoegen en de volgorde van oud naar jong controleren.
3. De gezamenlijke speelbal kiezen.
4. Wedstrijd starten.

### `Honderden`

1. Spelers invoeren of beschikbare spelersgegevens ophalen van de SK-Box.
2. Spelers toevoegen en de volgorde van oud naar jong controleren.
3. Kleur van bal 4 en linker- of rechteracquit voor bal 3 kiezen.
4. De bijzondere acquitopstelling tonen.
5. Wedstrijd starten.

### SK-Box koppelen

1. Beschikbare gekoppelde Bluetooth-apparaten zoeken en tonen.
2. De gekozen SK-Box verbinden.
3. Communicatieprotocol en protocolversie controleren.
4. Na een geslaagde verbinding de SK-Box-instellingen en het competitiemenu beschikbaar maken.

### Competities

1. Competities ophalen van de verbonden SK-Box.
2. Een nieuwe competitie toevoegen of een bestaande competitie selecteren.
3. Bij een nieuwe competitie de competitieopzet invullen en op de SK-Box opslaan.
4. Bij een bestaande competitie een competitiesessie openen.
5. Spelersnamen en leeftijden ophalen van de SK-Box.
6. Aanwezige spelers selecteren, ontbrekende spelers toevoegen en afwezige spelers uitsluiten voor de sessie.
7. De geplande competitiewedstrijd kiezen en starten.
8. Na afloop de uitslag en voortgang op de SK-Box opslaan.

### Nog toe te voegen aan het definitieve flowschema

- biljarttrainer: handmatige invoer, fotoherkenning, berekening en stootadvies;
- SK-Box-instellingen en instellingen van het grote scherm;
- lopende wedstrijd hervatten en synchronisatieconflicten oplossen;
- spelers tijdens `10 over rood` en `Honderden` toevoegen of laten opgeven;
- laatste wedstrijd en wedstrijdverslag bekijken of delen;
- terug-, annuleer- en bevestigingsroutes;
- foutmeldingen, verbinding verbroken en opnieuw verbinden;
- einde wedstrijd, klassering en terugkeer naar het hoofdmenu.

## V2.8.8 – Moyenne in CSV en laatst gespeelde spel onthouden

**Van toepassing op:** SK-Box (CSV-wedstrijdbestand) en de Android-telefoonapp.

### Moyenne correct in het CSV-bestand

**Wat gaan we toepassen:**  
Het CSV-wedstrijdbestand krijgt de moyenne zo opgeslagen dat de waarde bij openen correct wordt weergegeven. Nu staat er bij een gespeelde moyenne van `0.333` in het bestand of na openen `333`; de decimale scheiding gaat dus verloren.

- de moyenne wordt per speler in het CSV-bestand opgenomen;
- de moyenne wordt altijd met drie decimalen geschreven, bijvoorbeeld `0,333`;
- de waarde wordt bij openen in een Nederlandstalig spreadsheetprogramma (zoals Excel) als getal `0,333` gelezen en niet als `333`;
- het scheidingsteken tussen kolommen botst niet met het decimale teken;
- hervatten van een wedstrijd vanuit het CSV-bestand blijft werken.

**Waarom:**  
Zo kloppen de moyennes wanneer wedstrijdverslagen worden bekeken of verder verwerkt, zonder handmatige correctie.

### Laatst gespeelde spel onthouden in de telefoonapp

**Wat gaan we toepassen:**  
De telefoonapp onthoudt het laatst gespeelde spel totdat er een nieuw spel wordt gestart. Ook na afloop van de wedstrijd, na het sluiten van de app of na het verbreken van de Bluetoothverbinding blijft deze wedstrijd beschikbaar.

- na afloop kan de laatst gespeelde wedstrijd vanuit de app opnieuw worden geopend;
- in de laatst gespeelde wedstrijd kunnen nog wijzigingen worden gemaakt, zoals een verkeerd ingevoerde beurt of score corrigeren;
- wijzigingen worden naar de SK-Box gestuurd, zodat het CSV-bestand en het grote scherm worden bijgewerkt;
- de onthouden wedstrijd wordt pas vervangen wanneer een nieuw spel wordt gestart;
- vóór het starten van een nieuw spel is duidelijk dat de vorige wedstrijd daarna niet meer via deze functie kan worden gewijzigd.

**Waarom:**  
Fouten die pas na afloop worden opgemerkt, kunnen zo nog worden hersteld zonder de wedstrijd opnieuw te spelen of het bestand handmatig aan te passen.

## V2.9 – Spelsoort `10 over rood`

**Van toepassing op:** SK-Box en, als deze spelsoort ook vanaf de telefoon wordt gestart, de Android-telefoonapp en Bluetooth-synchronisatie.

**Wat gaan we toepassen:**  
Voeg `10 over rood` toe als afzonderlijk selecteerbare spelsoort. De wedstrijdinstellingen, puntentelling, beurtverwerking en weergave op het grootscherm moeten deze spelsoort correct ondersteunen.

Tijdens de wedstrijd houdt de SK-Box de actuele score en beurtstand in het werkgeheugen bij. Het grote scherm toont deze gegevens direct en wordt na iedere score- of beurtwijziging bijgewerkt. Na het beëindigen van de wedstrijd worden de wedstrijdstand en historie niet blijvend opgeslagen en wordt geen wedstrijdverslag gemaakt.

### Vastgelegde spelregels

**Speelbal en geldige carambole**

- Er wordt gespeeld met uitsluitend de witte óf uitsluitend de gele bal als speelbal. De gekozen speelbal blijft tijdens de partij gelijk.
- Alle spelers gebruiken tijdens de volledige wedstrijd dezelfde gekozen speelbal.
- Voor een geldige carambole moet de speelbal via de rode bal uiteindelijk ook de derde bal raken.
- De speelbal mag eerst één of meer banden raken voordat de rode bal en daarna de derde bal worden geraakt.

**Spelers en startvolgorde**

- Een wedstrijd wordt gespeeld met minimaal twee spelers; het systeem legt geen vaste bovengrens op.
- De spelers worden op leeftijd gerangschikt: de oudste speler begint en de jongste speler speelt als laatste.
- Iedere speler begint de eerste keer vanuit de acquitpositie.
- Nadat de jongste speler zijn eerste beurt heeft gespeeld en mist, gaat het spel verder bij de oudste speler zonder de ballen opnieuw in de acquitpositie te leggen.
- Na iedere geldige carambole blijft dezelfde speler aan de beurt.
- De beurt gaat naar de volgende speler wanneer de speler mist, een fout maakt of alleen de rode bal raakt zonder daarna de derde bal te raken.

**Doel, uitgaan en eindstand**

- Het doel is tien caramboles behalen.
- Een speler die tien caramboles heeft bereikt, is uit en krijgt zijn eindpositie op basis van de volgorde waarin spelers uitgaan.
- De laatst overgebleven speler krijgt de laatste plaats.
- De SK-Box toont per speler de actuele score, status en behaalde eindpositie.

**Fouten en terugvallen naar nul**

Wanneer een speler minder dan acht caramboles heeft, wordt zijn score teruggezet naar nul bij:

- het niet raken van de rode bal;
- een touché of andere als touché geregistreerde speelfout;
- een bal die uit de tafel springt.

Vanaf acht caramboles staat de speler **vast**. Een speler die op acht of negen staat, kan door bovenstaande fouten niet meer terugvallen naar nul. De SK-Box toont bij deze speler duidelijk de status `Vast`.

**Punt negen en punt tien**

- Bij een losse-bandcarambole moet de speelbal eerst een band raken voordat een andere bal wordt geraakt.
- Om van acht naar negen te gaan, moet de speler een losse-bandcarambole of een driebandencarambole maken.
- Als een gemaakte carambole als meerdere soorten kan worden beoordeeld, vraagt de SK-Box welke soort is gemaakt.
- Om de tiende carambole te behalen, moet de speler het tegenovergestelde type maken van de carambole waarmee het negende punt is behaald.
- Is punt negen gemaakt met een losse-bandcarambole, dan is voor punt tien een driebandencarambole verplicht.
- Is punt negen gemaakt met een driebandencarambole, dan is voor punt tien een losse-bandcarambole verplicht.
- Een gewone carambole die bij punt negen of tien niet voldoet aan het vereiste type, telt als een misser: er komt geen punt bij en de volgende speler is aan de beurt.
- Bij zo'n ongeldige poging blijft de speler `Vast` en blijft de score van acht of negen behouden.
- De SK-Box bewaart per speler welk type voor punt tien vereist is en toont dit op het grote scherm.

### Spelers tijdens `10 over rood` toevoegen of laten opgeven

**Speler toevoegen:**

- tijdens een lopende wedstrijd kan een nieuwe speler worden toegevoegd;
- naam en leeftijd worden ingevoerd en de speler wordt op de juiste plek in de volgorde van oud naar jong geplaatst;
- de speler krijgt zijn eerste beurt zodra de actieve volgorde zijn positie bereikt;
- de speler begint vanuit de actuele balpositie en altijd met nul punten;
- de SK-Box werkt spelerslijst, beurtvolgorde en het grote scherm direct bij;
- toevoegen moet eerst worden bevestigd.

**Speler geeft op:**

- de speler krijgt de status `Opgegeven`, ontvangt geen beurten meer en kan niet opnieuw aan dezelfde wedstrijd deelnemen;
- score en historie blijven tijdens de lopende wedstrijd zichtbaar, maar worden na afloop niet blijvend opgeslagen;
- de eerste opgever krijgt de laatste plaats en iedere latere opgever komt direct vóór de eerdere opgevers;
- zodra nog maar één actieve speler overblijft, eindigt de wedstrijd automatisch;
- de laatste opgever krijgt de lagere nog beschikbare positie en de overblijvende speler de direct hogere positie;
- de SK-Box werkt beurtvolgorde, klassering en het grote scherm direct bij;
- opgeven moet eerst worden bevestigd.

**Waarom:**  
Hierdoor kan deze spelvorm volledig binnen ScoreKrijt worden gespeeld en geregistreerd zonder handmatige scoreberekening buiten het systeem.

## V2.9.5 – Spelsoort `Honderden`

**Van toepassing op:** SK-Box en, als deze spelsoort ook vanaf de telefoon wordt gestart, de Android-telefoonapp en Bluetooth-synchronisatie.

**Wat gaan we toepassen:**  
Voeg `Honderden` toe als afzonderlijk selecteerbare spelsoort. De wedstrijdinstellingen, puntentelling, beurtverwerking en weergave op het grootscherm moeten deze spelsoort correct ondersteunen.

Tijdens de wedstrijd houdt de SK-Box de actuele score en beurtstand in het werkgeheugen bij. Het grote scherm toont deze gegevens direct en wordt na iedere score- of beurtwijziging bijgewerkt. Na het beëindigen van de wedstrijd worden de wedstrijdstand en historie niet blijvend opgeslagen en wordt geen wedstrijdverslag gemaakt.

### Vastgelegde spelregels

**Ballen:**

- er wordt met vier ballen gespeeld;
- bal 1 is de gele stootbal;
- bal 2 is wit;
- bal 3 is rood;
- bal 4 is blauw of groen; de gebruiker kiest deze kleur bij het aanmaken van de wedstrijd.

De SK-Box en eventuele grafische weergave in de app moeten alle vier de ballen afzonderlijk kunnen herkennen en weergeven volgens hun rol en kleur.

**Puntentelling:**

- raakt de gele stootbal bal 2 en bal 3, dan krijgt de speler 2 punten;
- raakt de gele stootbal bal 2 en bal 4, dan krijgt de speler 2 punten;
- raakt de gele stootbal bal 3 en bal 4, dan krijgt de speler 4 punten;
- raakt de gele stootbal bal 2, bal 3 en bal 4, dan krijgt de speler 20 punten;
- de volgorde waarin de objectballen worden geraakt, heeft geen invloed op het aantal punten.

Na iedere geldige stoot blijft de speler aan de beurt en worden de behaalde punten binnen de actuele beurt opgeteld. Bij een misser of fout eindigt de beurt, wordt het puntentotaal van die beurt bij de eerder behaalde totaalscore van de speler opgeteld en gaat de beurt naar de volgende speler.

De SK-Box moet na iedere stoot laten kiezen of vastleggen welke ballen zijn geraakt, het juiste puntenaantal berekenen en de totaalscore en beurtinformatie direct op het grote scherm bijwerken.

**Doel en overschrijden van honderd:**

- de speler die als eerste precies 100 punten bereikt, wint en beëindigt de wedstrijd;
- komt de berekende totaalscore boven 100, dan wordt de score van die speler direct teruggezet naar 80;
- het overschrijden van 100 telt niet als een misser en beëindigt de beurt niet;
- de speler blijft aan de beurt en speelt verder met 80 als nieuwe totaalscore;
- daarna worden nieuwe punten weer vanaf 80 opgeteld.

Voorbeeld: een speler staat op 98 en maakt een stoot van 4 punten. De uitkomst 102 wordt vervangen door 80 en de speler blijft aan de beurt.

**Afwijkende acquitopstelling:**

`Honderden` begint vanuit een eigen acquitopstelling, die afwijkt van de normale acquitstoot:

- bal 1, de gele stootbal, ligt op het bovenacquit;
- bal 2, de witte bal, ligt op het middenacquit;
- de gebruiker kiest of bal 3, de rode bal, op het linker- of rechteracquit ligt;
- bal 4, de blauwe of groene bal, ligt op het benedenacquit.

De SK-Box toont deze beginopstelling vóór de start van de wedstrijd, zodat de ballen correct kunnen worden neergelegd.

**Spelers en startcyclus:**

- de spelers worden op leeftijd gerangschikt: de oudste speler begint en de jongste speler speelt als laatste;
- iedere speler begint zijn eerste beurt vanuit de hierboven beschreven acquitopstelling;
- nadat de jongste speler zijn eerste beurt heeft gespeeld en mist, gaat het spel verder bij de oudste speler zonder de ballen opnieuw in de acquitopstelling te leggen.

**Waarom:**  
Hierdoor kan ook deze spelvorm volledig vanuit ScoreKrijt worden gestart, gevolgd en opgeslagen.

### Spelers tijdens `Honderden` toevoegen of laten opgeven

**Speler toevoegen:**

- tijdens een lopende wedstrijd kan een nieuwe speler worden toegevoegd;
- naam en leeftijd van de nieuwe speler worden ingevoerd, zodat de speler op de juiste plek in de volgorde van oud naar jong kan worden geplaatst;
- de nieuwe speler wordt direct op basis van leeftijd in de actieve beurtvolgorde geplaatst en krijgt zijn eerste beurt zodra die volgorde zijn positie bereikt;
- de nieuwe speler begint vanuit de actuele balpositie; de ballen worden niet opnieuw in de acquitopstelling gelegd;
- een later toegevoegde speler begint altijd met nul punten;
- de SK-Box werkt de spelerslijst, beurtvolgorde en weergave op het grote scherm direct bij;
- toevoegen moet eerst worden bevestigd om een onbedoelde wijziging tijdens de wedstrijd te voorkomen.

**Speler geeft op:**

- een actieve speler kan tijdens een lopende wedstrijd opgeven;
- de speler krijgt de status `Opgegeven` en ontvangt daarna geen beurten meer;
- de tot dan behaalde score en gespeelde historie blijven tijdens de lopende wedstrijd zichtbaar, maar worden na afloop niet blijvend opgeslagen;
- de eerste speler die opgeeft, krijgt de laatste plaats;
- iedere speler die later opgeeft, wordt direct vóór de eerdere opgevers geplaatst: de tweede opgever wordt voorlaatste, de derde opgever één plaats daarvoor, enzovoort;
- een speler die heeft opgegeven, kan niet opnieuw aan dezelfde wedstrijd worden toegevoegd of actief worden gemaakt;
- zodra door opgeven nog maar één actieve speler overblijft, eindigt de wedstrijd automatisch;
- de laatste opgever krijgt de lagere nog beschikbare positie en de overblijvende actieve speler krijgt de direct hogere positie;
- voorbeeld: de opgever wordt laatste en de laatste actieve speler wordt voorlaatste wanneer dat de twee nog beschikbare posities zijn;
- de SK-Box verwijdert de speler uit de actieve beurtvolgorde en werkt het grote scherm direct bij;
- opgeven moet eerst worden bevestigd en vermeldt duidelijk dat de actie gevolgen heeft voor de verdere wedstrijd.

### Starten vanuit het hoofdmenu van de telefoonapp

Op het hoofdmenu van de Android-app komen twee afzonderlijke knoppen:

- `10 over rood`;
- `Honderden`.

Iedere knop opent een eigen scherm voor het aanmaken van een wedstrijd voor de gekozen spelsoort.

**Spelers invoeren:**

- voeg minimaal twee spelers toe;
- voer per speler de naam en leeftijd in;
- voeg extra spelers toe zonder vaste bovengrens;
- wijzig of verwijder een speler voordat de wedstrijd begint;
- toon vóór het starten de automatisch berekende volgorde van oud naar jong;
- blokkeer het starten zolang verplichte gegevens ontbreken of minder dan twee spelers zijn ingevoerd.

**Instellingen voor `10 over rood`:**

- kies de gezamenlijke speelbal: wit of geel;
- toon een korte samenvatting van de speciale regels voor punt negen en tien;
- start de wedstrijd en stuur spelers, volgorde en spelinstellingen naar de SK-Box.

**Instellingen voor `Honderden`:**

- kies voor bal 4 de kleur blauw of groen;
- kies voor bal 3 de linker- of rechteracquitpositie;
- toon vóór de start de afwijkende acquitopstelling;
- start de wedstrijd en stuur spelers, volgorde, balkeuzes en spelinstellingen naar de SK-Box.

Na het starten opent de bijbehorende wedstrijdweergave op de telefoon en toont de SK-Box dezelfde spelers, volgorde en instellingen op het grote scherm.

## V3.0 – Competities instellen via de telefoon en opslaan op de SK-Box

**Van toepassing op:** Android-telefoonapp als bedieningsscherm en de SK-Box als centrale en blijvende opslag.

**Wat gaan we toepassen:**  
Voeg in de telefoonapp een speciaal menu `Competities` toe. Dit menu is beschikbaar wanneer de telefoon met een SK-Box is verbonden. Vanuit dit menu kan de gebruiker:

- een nieuwe competitie kan aanmaken en benoemen;
- meerdere competities naast elkaar kan bewaren;
- spelers en wedstrijden aan een competitie kan toevoegen;
- een wedstrijd aan de juiste competitie kan koppelen;
- gespeelde en nog te spelen wedstrijden kan bekijken;
- uitslagen en voortgang automatisch kan laten bijhouden;
- een bestaande competitie kan openen en verder kan vervolgen;
- een competitie kan afronden en later opnieuw kan bekijken.

### Spelers in een competitie

Bij het toevoegen van een speler worden minimaal de volgende gegevens ingevoerd:

- naam;
- libre-TMC: het aantal te maken caramboles voor libre.

De TMC voor bandstoten en driebanden wordt niet afzonderlijk ingevoerd. De SK-Box berekent beide doelen automatisch volgens een vaste verhouding op basis van de ingestelde libre-TMC van de speler. De berekende waarden worden bij de speler opgeslagen en vóór een wedstrijd in de betreffende spelvorm getoond.

Aan het begin van iedere speelavond geeft de gebruiker via de telefoon aan welke competitiespelers aanwezig zijn. Alleen aanwezige spelers worden voor die avond ingepland. Afwezigheid verwijdert een speler niet uit de competitie en heeft geen invloed op reeds gespeelde wedstrijden of opgeslagen voortgang.

### Seizoen en sessies

- een competitieseizoen duurt ongeveer negen tot tien maanden;
- er wordt normaal eenmaal per week gespeeld;
- een speelavond duurt doorgaans van 19:30 tot 22:30;
- een seizoen bestaat uit minimaal drie sessies;
- iedere speler speelt tegen andere spelers in drie spelvormen: libre, bandstoten en driebanden;
- de planning houdt rekening met wisselende aanwezigheid per speelavond;
- niet gespeelde wedstrijden blijven openstaan voor een latere speelavond.

### Planning per speelavond

- een seizoen start met de spelvorm libre;
- zolang geschikte librewedstrijden tussen aanwezige spelers mogelijk zijn, plant de app eerst zoveel mogelijk librewedstrijden;
- pas daarna worden volgens de vastgelegde competitievolgorde wedstrijden bandstoten en driebanden ingepland;
- aan het begin van de avond wordt eerst geprobeerd iedere aanwezige speler minimaal één keer in te delen;
- spelers die minder wedstrijden hebben gespeeld dan de overige aanwezigen krijgen daarna voorrang bij een extra indeling;
- een speler met een wedstrijdachterstand mag daardoor meerdere keren op dezelfde avond spelen;
- de planning blijft binnen de beschikbare speeltijd, normaal 19:30 tot 22:30;
- de gebruiker ziet de voorgestelde indeling in de telefoonapp en kan deze vóór definitief opslaan controleren.

### Extra sessie toevoegen

Wanneer binnen de beschikbare speeltijd ruimte overblijft en een aanwezige speler alle op dat moment geplande wedstrijden heeft gespeeld, kan via de telefoon een extra sessie of wedstrijd worden toegevoegd. De SK-Box slaat deze extra sessie, deelnemers, spelvorm en uitslag op als onderdeel van de competitievoortgang.

De app toont vóór het toevoegen welke spelers beschikbaar zijn, welke onderlinge wedstrijden al zijn gespeeld en of de extra sessie meetelt voor de officiële rangschikking.

### Opslagstructuur op de SK-Box

Voor iedere competitie maakt de SK-Box een afzonderlijke competitiemap aan. De beoogde structuur is:

```text
Competities/
└── <competitienaam>/
    └── <jaar-of-seizoen>/
        ├── Wedstrijdenoverzicht
        ├── Seizoensinstellingen
        ├── Eindstand
        └── Wedstrijden/
            ├── <wedstrijd-1>
            ├── <wedstrijd-2>
            └── ...
```

- onder de competitiemap komt eerst een seizoensmap, bijvoorbeeld `2025` of `2025-2026`;
- bij het aanmaken van een seizoen voert of kiest de gebruiker deze jaaraanduiding via de telefoonapp;
- dezelfde competitie kan meerdere seizoensmappen bevatten, zonder dat oude seizoenen worden overschreven;
- de map `Wedstrijden` bevat een afzonderlijk bestand of verslag voor iedere gespeelde wedstrijd;
- `Wedstrijdenoverzicht` in de seizoensmap bevat zowel de gespeelde als de nog te spelen wedstrijden;
- het overzicht wordt na iedere gespeelde, toegevoegde of verplaatste wedstrijd bijgewerkt;
- `Seizoensinstellingen` bevat minimaal spelers, TMC's, spelvormen, planning en competitieregels;
- `Eindstand` wordt bij de seizoensafsluiting in de betreffende seizoensmap aangemaakt;
- alle mappen en documenten blijven uitsluitend op de SK-Box opgeslagen.

### Seizoen afsluiten en nieuw seizoen voorbereiden

Wanneer alle geplande wedstrijden zijn gespeeld, kan de gebruiker het seizoen via de telefoon afsluiten. De SK-Box:

- controleert dat geen verplichte wedstrijd meer openstaat;
- berekent de definitieve stand;
- slaat een einddocument met de stand, uitslagen en spelersprestaties op in de betreffende seizoensmap;
- markeert het seizoen als afgerond en voorkomt verdere wijzigingen zonder een bewuste heropenactie;
- berekent voor iedere speler een voorstel voor de nieuwe TMC van het volgende seizoen op basis van de oude TMC en de resultaten van het afgesloten seizoen;
- toont de berekende nieuwe TMC's in de telefoonapp voordat het volgende seizoen wordt aangemaakt;
- bewaart het afgesloten seizoen ongewijzigd en maakt voor het nieuwe seizoen onder dezelfde competitie een nieuwe seizoensmap aan.

De telefoon dient alleen voor invoer, bediening en weergave. Bij het openen van het competitiemenu vraagt de telefoon de actuele competities en voortgang op bij de verbonden SK-Box.

Alle competitiegegevens, wedstrijdindelingen, uitslagen, rangschikkingen en voortgang worden uitsluitend blijvend op de SK-Box opgeslagen. De telefoon bewaart hiervan geen zelfstandige permanente versie. Na opnieuw opstarten of verbinden met een andere telefoon worden de gegevens opnieuw vanaf de SK-Box geladen.

Iedere wijziging wordt via een apart Bluetooth-bericht naar de SK-Box gestuurd. De telefoon toont de wijziging pas als definitief opgeslagen nadat de SK-Box de ontvangst en opslag heeft bevestigd.

### Nog vast te leggen vóór implementatie

- de exacte omrekenverhouding en afrondingsregel van libre-TMC naar bandstoten-TMC;
- de exacte omrekenverhouding en afrondingsregel van libre-TMC naar driebanden-TMC;
- wat precies als één sessie geldt: een speelavond, een wedstrijd of een volledige ronde;
- hoe tegenstanders en spelvormen per speelavond worden ingepland;
- de puntentoekenning, rangschikking en regels bij gelijke stand;
- wanneer een extra sessie meetelt voor de officiële rangschikking.
- het bestandsformaat van wedstrijdenoverzicht en eindstand;
- de formule, minimum- en maximumwaarden en afrondingsregels voor de nieuwe TMC;
- het moment waarop van libre naar bandstoten en daarna naar driebanden wordt overgegaan.

**Waarom:**  
De telefoon biedt een gemakkelijker invoerscherm, terwijl de SK-Box de centrale bron van waarheid blijft. De competitievoortgang blijft bij het biljart en is daardoor niet afhankelijk van de gebruikte telefoon.

## V3.1 – Biljarttrainer

**Van toepassing op:** Android-telefoonapp. De trainer staat los van een lopende wedstrijd en is bedoeld voor oefenen en stootadvies.

**Ondersteunde spelsoorten:**

- libre;
- bandstoten, waarbij minimaal één band moet worden geraakt;
- driebanden, waarbij minimaal drie banden moeten worden geraakt.

**Invoer van de balpositie:**

De gebruiker kan op twee manieren een uitgangspositie invoeren:

1. De speelbal, mikbal en derde bal handmatig op een digitale biljarttafel plaatsen en corrigeren.
2. Een foto van de biljarttafel maken of kiezen, waarna de app de tafelranden en de posities van de drie ballen herkent en omzet naar de digitale tafel.

Na automatische herkenning moet de gebruiker de gevonden tafelranden en balposities kunnen controleren en handmatig verbeteren voordat de berekening begint.

**Berekening en keuze van een stoot:**

De app berekent meerdere geldige stootmogelijkheden en beoordeelt deze op:

- voldoen aan de regels van de gekozen spelsoort;
- moeilijkheidsgraad;
- foutmarge bij afwijkingen in richting, snelheid en balcontact;
- geschiktheid als verzamelstoot en de verwachte positie voor een volgende carambole.

De resultaten worden gerangschikt, zodat de speler bijvoorbeeld de eenvoudigste, veiligste of beste verzamelstoot kan kiezen. Het advies wordt als berekende inschatting getoond en niet als garantie, omdat tafel, laken, banden, ballen en uitvoering het werkelijke resultaat beïnvloeden.

**Invloed van techniek op de berekening:**

- de horizontale keuhoek en mikrichting bepalen de basisrichting van de speelbal;
- zijwaarts effect, ook Engels genoemd, verandert de uitgaande hoek na bal- en bandcontact;
- hoog in de speelbal raken geeft voorwaarts effect en beïnvloedt het vervolgtraject;
- laag in de speelbal raken geeft terugwaarts effect en kan een trekbal veroorzaken;
- de berekening combineert raakdikte, keuhoek, contactpunt, snelheid en effect in plaats van deze waarden los van elkaar te behandelen;
- de voorspelde lijnen worden opnieuw berekend zodra de gebruiker één van deze instellingen wijzigt.

**Moeilijkheid en foutmarge:**

De app berekent rondom de ideale stoot een toegestane afwijkingsmarge voor zowel het contactpunt op de speelbal als de raakdikte op de mikbal. Een kleine toegestane afwijking betekent dat de stoot nauwkeurig moet worden uitgevoerd en daarom als moeilijker wordt beoordeeld. Een grotere marge betekent een vergevingsgezindere stoot.

De foutmarge wordt behalve als score ook visueel getoond als een smalle of brede tolerantiezone rond het ideale mikpunt en de berekende baan.

**Stootadvies in de app:**

Voor iedere voorgestelde stoot toont de app minimaal:

- een getekende baan van de speelbal en de verwachte beweging van de andere ballen;
- de raakdikte op de mikbal;
- de plaats waar de keu de speelbal moet raken, inclusief links/rechts effect en hoog/laag contact;
- de richting en hoek van de keu ten opzichte van de tafel;
- een indicatie van de benodigde stootsnelheid;
- het geadviseerde stoottype: normaal, trekbal, snijbal, massé of piqué;
- de moeilijkheidsgraad en geschatte foutmarge;
- een uitleg waarom deze stoot wordt voorgesteld.

**Visuele weergave:**

- toon de biljarttafel van bovenaf, inclusief banden en diamantmarkeringen;
- gebruik afzonderlijke gekleurde lijnen voor de verwachte banen van de speelbal en objectballen;
- teken bandcontacten, balcontacten en de volgorde van de route duidelijk in;
- toon naast of onder de tafel een vergrote balweergave voor de raakdikte op de mikbal;
- geef in die vergroting de ideale overlap, raaklijn en toegestane afwijkingszone aan;
- toon een aparte speelbalweergave met een richtpunt voor hoog/laag en links/rechts effect;
- geef de keuhoek weer met een lijn, pijl of gradenboog ten opzichte van de tafel;
- laat de gebruiker effect, hoogte, snelheid en keuhoek aanpassen en werk de voorspelde baan direct bij;
- bied een duidelijke legenda waarmee kleuren, lijnen en foutzones worden uitgelegd.

**Nog vast te leggen vóór implementatie:**

- ondersteunde tafelafmetingen en hoe de gebruiker een tafelmaat kiest;
- de numerieke eenheden en schaal voor raakdikte, snelheid, effect en keuhoek;
- welke fysieke factoren in de eerste versie worden meegenomen;
- hoe moeilijkheid en foutmarge worden berekend en uitgelegd;
- of foto's uitsluitend op het toestel worden verwerkt en of ze na analyse worden bewaard.

**Waarom:**  
De trainer helpt spelers een positie beter te begrijpen, meerdere oplossingen te vergelijken en gericht te oefenen op techniek en positie­spel.

## Mijlpalen voor de ontwikkeling

Iedere mijlpaal levert een afzonderlijk werkende en testbare tussenversie op. Begin pas aan de volgende mijlpaal wanneer het controlepunt van de huidige stap is geslaagd.

### Mijlpaal 1 (V2.9) – Basis voor meerdere spelers

**Status:** gepland

- beschrijf eerst de benodigde gegevens voor spelers, beurten en klasseringen;
- maak een herbruikbare spelerslijst zonder vaste bovengrens;
- sorteer spelers op leeftijd van oud naar jong;
- houd actieve, uitgeschakelde en opgegeven spelers afzonderlijk bij;
- maak beurtvolgorde en eindklassering geschikt voor meer dan twee spelers;
- bewaar de actuele status alleen zolang de wedstrijd actief is.

**Controlepunt:** een testwedstrijd met meerdere spelers kan worden gestart, gespeeld en beëindigd zonder blijvende wedstrijdopslag en zonder de bestaande spelsoorten te wijzigen.

### Mijlpaal 2 (V2.9) – Basis van `10 over rood`

**Status:** gepland

- voeg de spelsoort en de keuze voor één gezamenlijke witte of gele speelbal toe;
- bouw de startcyclus van oudste naar jongste vanuit acquit;
- verwerk geldige caramboles, missers, alleen-rood en speelfouten;
- bouw de terugval naar nul onder acht punten en de status `Vast` vanaf acht.

**Controlepunt:** score en beurtvolgorde volgen de vastgelegde regels tot en met acht punten.

### Mijlpaal 3 (V2.9) – Uitgaan bij `10 over rood`

**Status:** gepland

- registreer voor punt negen een losse-band- of driebandencarambole;
- verplicht voor punt tien het tegenovergestelde type;
- behandel een verkeerd type als misser zonder verlies van de status `Vast`;
- verwerk uitgaan, eindposities en de laatst overgebleven speler.

**Controlepunt:** volledige partijen met verschillende routes naar punt negen en tien leveren altijd de juiste score en klassering op.

### Mijlpaal 4 (V2.9) – Spelers toevoegen en laten opgeven

**Status:** gepland

- voeg tijdens `10 over rood` een speler op leeftijd toe;
- start de nieuwe speler vanuit de actuele balpositie en met nul punten;
- laat een speler bevestigd opgeven en blokkeer opnieuw deelnemen;
- werk beurtvolgorde en de rangschikking van opgevers bij;
- beëindig de wedstrijd wanneer nog één actieve speler overblijft.

**Controlepunt:** toevoegen en opgeven op verschillende momenten beschadigt scores, historie, beurtvolgorde of klassering niet.

### Mijlpaal 5 (V2.9) – Telefoon, Bluetooth en grootscherm

**Status:** gepland

- leg vast welke tijdelijke wedstrijdgegevens op telefoon en SK-Box bestaan en via Bluetooth worden gedeeld;
- voeg alleen de knop, spelersinvoer en wedstrijdweergave voor `10 over rood` aan de telefoonapp toe;
- synchroniseer spelers, scores, beurten, statussen, historie en klassering tijdens de lopende wedstrijd;
- toon spelers, score, actieve speler, `Vast`, vereist type voor punt tien en klassering op het grote scherm;
- behoud protocolversiecontrole, ontvangstbevestiging en opnieuw synchroniseren na een tijdelijke verbindingsbreuk;
- wis de tijdelijke wedstrijdgegevens na het beëindigen van de wedstrijd.

**Controlepunt:** V2.9 bevat uitsluitend `10 over rood`; telefoon en SK-Box blijven gelijk en na afsluiten blijft geen opgeslagen wedstrijd of verslag achter.

### Mijlpaal 6 (V2.9.5) – Basis van `Honderden`

**Status:** gepland

- voeg de vier ballen en kleurkeuze voor bal 4 toe;
- toon de bijzondere acquitopstelling en laat links/rechts voor bal 3 kiezen;
- bouw de startcyclus van oudste naar jongste;
- verwerk de combinaties van 2, 4 en 20 punten onafhankelijk van raakvolgorde;
- tel punten binnen de beurt op en wissel bij een misser of fout.

**Controlepunt:** iedere mogelijke geldige balcombinatie geeft het juiste puntenaantal en een misser sluit de beurt correct af.

### Mijlpaal 7 (V2.9.5) – Winnen en weergeven bij `Honderden`

**Status:** gepland

- beëindig de wedstrijd wanneer een speler precies 100 bereikt;
- zet een score boven 100 direct terug naar 80 en laat de speler verder spelen;
- toon score, beurtpunten, totaalscore, actieve speler en balinformatie op het grote scherm;
- houd de partij alleen tijdens de lopende wedstrijd bij en wis de tijdelijke gegevens na afloop.

**Controlepunt:** grensgevallen rond 100, waaronder 98 + 4 en 90 + 20, worden correct verwerkt en weergegeven.

### Mijlpaal 8 (V2.9.5) – Spelers en telefoon uitbreiden voor `Honderden`

**Status:** gepland

- breid spelers toevoegen en opgeven uit voor `Honderden`;
- voeg de knop, spelersinvoer, balkeuzes en wedstrijdweergave voor `Honderden` aan de telefoonapp toe;
- breid de tijdelijke Bluetooth-synchronisatie uit met alle gegevens van `Honderden`;
- controleer opnieuw verbinden en opnieuw synchroniseren zolang de wedstrijd actief is.

**Controlepunt:** V2.9.5 voegt alleen `Honderden` toe en behoudt de volledige werking van V2.9.

### Mijlpaal 9 (V3.0) – Competities aanmaken en bewaren

**Status:** gepland

- leg vóór het bouwen het competitieformat, de betekenis van een sessie en de benodigde wedstrijd- en seizoensgegevens vast;
- voeg een speciaal menu `Competities` aan de telefoonapp toe;
- laad bij het openen alle competitiegegevens vanaf de verbonden SK-Box;
- beheer via de telefoon spelers met naam en libre-TMC en bereken daaruit automatisch de TMC voor bandstoten en driebanden;
- leg seizoen, sessies en de drie spelvormen libre, bandstoten en driebanden vast;
- beheer geplande wedstrijden en wekelijkse speelavonden;
- koppel iedere wedstrijd aan precies één competitie;
- stuur wijzigingen via Bluetooth en verwerk de opslagbevestiging;
- maak per competitie een hoofdmap en daarbinnen een afzonderlijke map per jaar of seizoen;
- bewaar seizoensinstellingen en wedstrijdenoverzicht in de juiste seizoensmap;
- maak daarbinnen een map `Wedstrijden` met alle gespeelde wedstrijdverslagen;
- sla competities uitsluitend op de SK-Box afzonderlijk en blijvend op.

**Controlepunt:** meerdere competities kunnen na opnieuw opstarten en vanaf een andere verbonden telefoon worden geladen zonder gegevens te verliezen of te vermengen.

### Mijlpaal 10 (V3.0) – Competitievoortgang en rangschikking

**Status:** gepland

- leg vóór de berekeningen de puntentoekenning, rangschikking en regels bij gelijke stand vast;
- registreer uitslagen en gespeelde wedstrijden;
- selecteer per speelavond de aanwezige spelers en plan alleen met deze spelers;
- laat niet gespeelde wedstrijden voor een latere speelavond openstaan;
- plan eerst zoveel mogelijk libre en ga daarna volgens de vastgelegde volgorde verder met bandstoten en driebanden;
- deel eerst iedere aanwezige speler in en geef daarna voorrang aan spelers met een wedstrijdachterstand;
- voeg bij beschikbare tijd extra wedstrijden of sessies toe;
- bereken voortgang, punten en rangschikking;
- toon gespeelde en nog te spelen wedstrijden in het competitiemenu van de telefoon;
- laat de SK-Box iedere uitslag en voortgang blijvend opslaan;
- ondersteun via de telefoon afronden en later terugkijken.

**Controlepunt:** een volledige proefcompetitie levert na iedere uitslag de verwachte voortgang en eindrangschikking op.

### Mijlpaal 11 (V3.0) – Seizoen afsluiten en nieuwe TMC bepalen

**Status:** gepland

- controleer dat alle verplichte wedstrijden zijn gespeeld;
- maak en bewaar het einddocument met de definitieve stand;
- sluit het seizoen af zonder oude resultaten te wijzigen;
- bereken nieuwe TMC-voorstellen uit oude TMC's en seizoensresultaten;
- maak vanuit de telefoon een nieuw seizoen met de berekende TMC's aan.

**Controlepunt:** een afgesloten proefseizoen blijft volledig terug te lezen en levert voor iedere speler een reproduceerbaar TMC-voorstel voor het volgende seizoen op.

### Mijlpaal 12 (V3.1) – Biljarttrainer met handmatige invoer

**Status:** gepland

- leg vóór het bouwen de open keuzes voor tafelmaat, eenheden, fysiek model, foutmarge en foto-opslag vast;
- teken een schaalbare biljarttafel in de Android-app;
- laat de drie ballen handmatig plaatsen en corrigeren;
- ondersteun libre, minimaal één band en driebanden;
- bereken en teken eerst één eenvoudige geldige baan.

**Controlepunt:** bekende oefenposities leveren reproduceerbare geldige basisbanen op.

### Mijlpaal 13 (V3.1) – Uitgebreid stootadvies

**Status:** gepland

- bereken meerdere mogelijke stoten;
- rangschik op moeilijkheid, foutmarge en verzamelpositie;
- verwerk de gezamenlijke invloed van raakdikte, contactpunt, keuhoek, snelheid en effect op bal- en bandhoeken;
- toon de tafelbanen, vergrote raakdikte, speelbalcontactpunt, keuhoek en tolerantiezones;
- laat aanpassingen aan effect en keuhoogte de voorspelde baan direct wijzigen;
- leg begrijpelijk uit waarom een stoot wordt voorgesteld.

**Controlepunt:** de speler kan oplossingen vergelijken, alle waarden terugvinden en visueel zien hoe zij-effect, hoog/laag raken en een kleine uitvoeringsfout de voorspelde baan veranderen.

### Mijlpaal 14 (V3.1) – Fotoherkenning en kalibratie

**Status:** gepland

- herken tafelranden en balposities uit een foto;
- corrigeer perspectief en schaal naar de digitale tafel;
- laat de gebruiker herkenning handmatig corrigeren;
- test met verschillende tafels, belichting en camerahoeken.

**Controlepunt:** een gecorrigeerde foto-invoer levert dezelfde berekening op als dezelfde positie die handmatig is ingevoerd.

### Mijlpaal 15 (iedere release) – Regressietest en vrijgave

**Status:** gepland

- voer deze mijlpaal afzonderlijk uit vóór vrijgave van V2.8.8, V2.9, V2.9.5, V3.0 en V3.1;
- test de functies van de betreffende release op de echte SK-Box en telefoon;
- controleer bestaande spelsoorten en alle V2.8-functies;
- controleer competitieopslag, bestaande hervatfuncties, Bluetooth en bestaande wedstrijdverslagen;
- werk helpteksten en changelog bij.

**Controlepunt:** alle algemene acceptatiecriteria zijn geslaagd en er zijn geen blokkerende fouten meer.

## Algemene acceptatiecriteria

- nieuwe spelsoorten kunnen zonder invloed op bestaande spelsoorten worden gebruikt;
- de SK-Box houdt voor `10 over rood` en `Honderden` de actuele score en beurtstand correct bij;
- beide spelsoorten kunnen vanuit een eigen knop en invoerscherm in het hoofdmenu van de telefoonapp worden gestart;
- de app controleert minimaal twee spelers en toont vóór de start de volgorde van oud naar jong;
- het grote scherm toont scorewijzigingen en beurtwisselingen direct;
- spelers kunnen tijdens `10 over rood` en `Honderden` veilig worden toegevoegd of als `Opgegeven` worden gemarkeerd;
- na toevoegen of opgeven blijven beurtvolgorde, spelersstatus, scores en historie correct;
- wedstrijden `10 over rood` en `Honderden` worden na afloop niet opgeslagen en maken geen wedstrijdverslag;
- competitiegegevens blijven volledig lokaal op de SK-Box;
- competities kunnen via een speciaal menu in de telefoonapp worden ingesteld en gevolgd;
- een andere telefoon kan na verbinden dezelfde actuele competitiegegevens vanaf de SK-Box laden;
- meerdere competities kunnen zonder onderlinge vermenging worden opgeslagen en gevolgd;
- iedere competitie heeft per jaar of seizoen een eigen submap met een wedstrijdenoverzicht en afzonderlijke map voor gespeelde wedstrijden;
- de speelavondplanning geeft spelers met een wedstrijdachterstand extra kansen zonder andere aanwezige spelers over te slaan;
- een afgesloten seizoen bevat een definitieve stand en reproduceerbare TMC-voorstellen voor het volgende seizoen;
- de biljarttrainer controleert voorgestelde stoten volgens de gekozen spelsoort;
- handmatig ingevoerde en uit foto's herkende balposities kunnen vóór berekening worden gecorrigeerd;
- ieder stootadvies toont baan, raakdikte, contactpunt, keuhoek, stoottype, moeilijkheid en foutmarge;
- zij-effect en hoog/laag raken hebben zichtbaar invloed op de berekende uitgaande bal- en bandhoeken;
- een kleinere tolerantie voor speelbalcontact of raakdikte resulteert in een hogere moeilijkheidsscore;
- bestaande V2.8-functionaliteit blijft werken.
