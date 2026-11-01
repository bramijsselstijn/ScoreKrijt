# Release-teksten ScoreKrijt 2.8.7

Teksten voor de GitHub Release en de winkel (Google Play). Alle teksten vermelden dat ScoreKrijt met
behulp van AI is gemaakt. De tekenlimieten van de winkel zijn gecontroleerd.

## 1. GitHub Release

- **Tag:** `v2.8.7`
- **Titel:** `ScoreKrijt 2.8.7`
- **Bestanden om te uploaden** (staan klaar in `Release/v2.8.7/`, die map staat bewust niet in Git):
  `ScoreKrijt-2.8.7-debug.apk`, `ScoreKrijt-SK-Box-2.8.7.zip`, `SHA256SUMS.txt`

### Beschrijving (plakken in de release)

## ScoreKrijt 2.8.7

Scoreteller voor biljart: een Android-app en de SK-Box (Raspberry Pi) voor het grote scherm. De SK-Box werkt zonder internet.

### Nieuw in 2.8.7

**Android-app**
- Moyenne in het verzonden CSV-bestand en in het tekstoverzicht.
- Bij Uit is uit toont het wedstrijdscherm procenten en `En nog #` (caramboles die nog nodig zijn).
- Tik op de beurt in het wedstrijdscherm voor het tijdelijke wedstrijdoverzicht.
- Knoppen met reliëf en licht afgeronde hoeken; de vier grote knoppen hebben een opgehoogde rand.
- `Selecteer SK-Box` bij het verbinden; uitleg over verlenging bij Gelijkspel.
- Regelaar voor de breedte van de middelste kolom en ruimere lettergroottes in de SK-Box-instellingen.

**SK-Box**
- Opstarten zonder Raspberry Pi-logo's, met het ScoreKrijt-logo en een laadscherm.
- Namen en TMC verschijnen alvast zodra de aanvang van de wedstrijd wordt bepaald.
- Procenten en `Car. tot uit` bij Uit is uit; F12 toont of verbergt de taakbalk.
- Bijwerken zonder internet met een USB-stick (`sk-update.sh`).

Alle wijzigingen staan in [CHANGELOG.md](CHANGELOG.md).

### Downloaden

| Bestand | Waarvoor |
|---|---|
| `ScoreKrijt-2.8.7-debug.apk` | De Android-app (versie 2.8.7). Installeer hem op je telefoon. |
| `ScoreKrijt-SK-Box-2.8.7.zip` | De map `ScoreKrijt_update` voor de USB-stick: het SK-Box-programma en de twee hulpscripts. |
| `SHA256SUMS.txt` | Controlesommen van beide bestanden. |

De handleidingen (installeren, bijwerken en instellingen) staan in de map [`Docs`](Docs).

### Let op
- Zet telefoon en SK-Box allebei op 2.8.7 (minstens 2.8.6 voor de nieuwe regelaars).
- De APK is met de standaard-debugsleutel ondertekend. Heb je al een versie van een andere bron geïnstalleerd, dan kan Android weigeren hem bij te werken.
- Het wachtwoord in de handleiding (`user`) is eenvoudig; gebruik de SK-Box niet op een openbaar netwerk.

### Gemaakt met behulp van AI
ScoreKrijt (app, SK-Box-software, hulpscripts en handleidingen) is gemaakt met behulp van AI (Claude van Anthropic). De wensen, de keuzes en het testen op een echte telefoon en SK-Box komen van de maker.

---

## ScoreKrijt 2.8.7 (English)

Score counter for carom billiards: an Android app and the SK-Box (Raspberry Pi) for the big screen. The SK-Box works without internet.

### What is new in 2.8.7

**Android app**
- Moyenne (average per turn) in the CSV report and in the text overview.
- In Out-is-out games the match screen shows percentages and `And still #` (carambols still needed).
- Tap the turn on the match screen for the temporary match overview.
- Buttons with relief and slightly rounded corners; the four big buttons have a raised edge.
- `Selecteer SK-Box` when connecting; clearer explanation of extension next to Draw.
- Slider for the width of the middle column and larger font ranges in the SK-Box settings.

**SK-Box**
- Silent start-up without Raspberry Pi logos, with the ScoreKrijt logo and a loading screen.
- Names and targets appear in advance as soon as the start of the match is being decided.
- Percentages and `Car. tot uit` in Out-is-out games; F12 shows or hides the taskbar.
- Update without internet from a USB stick (`sk-update.sh`).

All changes are in [CHANGELOG.md](CHANGELOG.md) (Dutch).

### Downloads
- `ScoreKrijt-2.8.7-debug.apk` – the Android app (version 2.8.7).
- `ScoreKrijt-SK-Box-2.8.7.zip` – the `ScoreKrijt_update` folder for the USB stick: the SK-Box program and the two helper scripts.
- `SHA256SUMS.txt` – checksums of both files.

### Made with the help of AI
ScoreKrijt (app, SK-Box software, helper scripts and manuals) was made with the help of AI (Claude by Anthropic). The requirements, the decisions and the testing on a real phone and SK-Box come from the author.

## 2. Winkeltekst (Google Play)

### Nederlands

**Titel** (18/30): ScoreKrijt Biljart

**Korte beschrijving** (72/80): Scoreteller voor biljart, met Bluetooth-scorebord voor een groot scherm.

**Wat is nieuw** (289/500):

```
• Moyenne in het wedstrijdverslag
• Bij Uit is uit: procenten en "En nog #"
• Tik op de beurt voor het tijdelijke overzicht
• Knoppen met reliëf en minder ronde hoeken
• Duidelijke uitleg bij Gelijkspel en verlenging
• SK-Box: namen en TMC vooraf, breedte van de middelste kolom instelbaar
```

**Volledige beschrijving** (1057/4000):

```
ScoreKrijt is een scoreteller voor biljart. Noteer caramboles, beurten en punten tijdens een wedstrijd en laat de stand desgewenst zien op een groot scherm.

Functies
• Enkel spel met vaste beurten of Uit is uit, met of zonder gelijkspel en verlenging
• TMC per speler, punten of percentage, moyenne en hoogste serie
• Beurt noteren, score verhogen en verlagen en de vorige actie terugnemen
• Tijdelijk wedstrijdoverzicht en een wedstrijdverslag (CSV) delen
• Help en spelregels voor libre, bandstoten en driebanden
• Optioneel: verbinden met een SK-Box, een Raspberry Pi met scherm, via Bluetooth. De SK-Box toont de stand op een groot scherm en heeft geen internet nodig. De weergave stel je in met de app.

Privacy
De app heeft geen internetverbinding nodig en stuurt zelf geen gegevens naar een server. Wedstrijdgegevens blijven op je telefoon. Bluetooth wordt alleen gebruikt om met de SK-Box te verbinden.

Gemaakt met behulp van AI
ScoreKrijt is gemaakt met behulp van AI (Claude van Anthropic). De wensen, de keuzes en het testen komen van de maker.
```

### English

**Title** (20/30): ScoreKrijt Billiards

**Short description** (69/80): Billiards score counter with a Bluetooth scoreboard for a big screen.

**What is new** (309/500):

```
• Moyenne (average) in the match report
• In Out-is-out games: percentages and "And still #"
• Tap the turn for a temporary match overview
• Buttons with relief and less rounded corners
• Clearer explanation of Draw and extension
• SK-Box: names and TMC shown in advance, adjustable width of the middle column
```

**Full description** (1016/4000):

```
ScoreKrijt is a score counter for carom billiards. Note carambols, turns and points during a match and show the score on a big screen if you like.

Features
• Single game with fixed turns or Out-is-out, with or without a draw and extension
• Target per player, points or percentage, moyenne (average) and highest run
• Note the turn, raise or lower the score and undo the last action
• Share a temporary match overview and a match report (CSV)
• Help and rules for libre, one-cushion and three-cushion
• Optional: connect over Bluetooth to an SK-Box, a Raspberry Pi with a screen. The SK-Box shows the score on a big screen and needs no internet. You set up the display with the app.

Privacy
The app needs no internet connection and does not send any data to a server itself. Match data stays on your phone. Bluetooth is only used to connect to the SK-Box.

Made with the help of AI
ScoreKrijt was made with the help of AI (Claude by Anthropic). The requirements, the decisions and the testing come from the author.
```

## 3. Nog te regelen voor de winkel

Dit staat hier als checklist; controleer de actuele eisen van Google Play zelf, want die veranderen regelmatig.

- **Pakketnaam:** de app heet nu `com.example.scorekrijtapp`. Google Play accepteert geen pakketnamen die met
  `com.example` beginnen. Kies vóór de eerste upload een eigen naam (bijvoorbeeld op basis van een domein dat je beheert)
  en pas `applicationId` aan in `app/build.gradle.kts`. Een andere pakketnaam is voor Android een andere app: wie de
  huidige APK al heeft, kan er niet op bijwerken en verliest de lokale gegevens. Beslis dit dus voordat je de APK
  breed verspreidt.
- **Appnaam:** `app_name` is nu `ScoreKrijtApp`; de winkeltitel hierboven is `ScoreKrijt Biljart`.
- **Ondertekening:** een winkelversie moet met een eigen release-sleutel zijn ondertekend (bewaar de sleutel en het
  wachtwoord veilig en buiten Git). De huidige APK is een debug-bouw.
- **Bestandstype:** Google Play vraagt voor nieuwe apps normaal een Android App Bundle (`.aab`) in plaats van een APK.
- **Doel-API:** controleer welk `targetSdk` Google Play nu vereist (nu `36`).
- **Privacybeleid:** een webpagina met een korte privacyverklaring. De app heeft geen `INTERNET`-recht en gebruikt alleen
  Bluetooth (`BLUETOOTH_CONNECT`, `BLUETOOTH_SCAN` met `neverForLocation`).
- **Formulieren in de Play Console:** gegevensbeveiliging (data safety), inhoudsclassificatie en doelgroep.
- **Beeldmateriaal:** pictogram van 512 x 512 pixels (het ScoreKrijt-logo is 1024 x 1024), een afbeelding van 1024 x 500
  pixels en schermafbeeldingen van de telefoon.
- **Testregels:** controleer of voor een nieuw ontwikkelaarsaccount eerst een gesloten test met testers nodig is.
- **AI-vermelding:** staat in de beschrijving hierboven, in de app (Help / spelregels, Over Score Krijt) en op het
  About-venster van de SK-Box. Deze vermelding is vrijwillig; ScoreKrijt heeft geen AI-functies die inhoud genereren.
