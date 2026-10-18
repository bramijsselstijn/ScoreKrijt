# ScoreKrijt changelog

## V2.8.5 – bugfixes (Android-app en SK-Box, versienummers gelijkgetrokken)

Laatst bijgewerkt: 18 oktober 2026. Nog niet getest op een echte telefoon en SK-Box. Het Bluetooth-protocol blijft versie 2, dus telefoon en SK-Box hoeven niet tegelijk te worden bijgewerkt.

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
