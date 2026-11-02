# Checklist: ScoreKrijt in de Google Play Store zetten

*Opgesteld op 2 november 2026. De regels van Google Play veranderen regelmatig; controleer de details in de Play Console en in de officiële documentatie van Google. Dit is een werklijst, geen garantie dat Google de app goedkeurt.*

Wat ik (Claude) niet doe: de APK of het `.aab`-bestand bouwen of ondertekenen, en het Play Console-account aanmaken. Dat doe jij.

## 1. Besluiten vooraf

### 1.1 Pakketnaam (`applicationId`)

De app heet nu `com.example.scorekrijtapp`. Google Play weigert pakketnamen die met `com.example` beginnen. De pakketnaam staat na de eerste upload vast: je kunt hem later niet meer wijzigen.

**Voorstel: `io.github.bramijsselstijn.scorekrijt`**

- Het is de omgekeerde vorm van `bramijsselstijn.github.io`, het adres dat bij je GitHub-account hoort. Zo gebruiken veel open-sourceprojecten zonder eigen domein een pakketnaam.
- Alleen kleine letters, geen streepjes of spaties, en hij past bij de naam van het project.
- Je hoeft er geen domein voor te bezitten.

**Alternatief:** heb je een eigen domein, bijvoorbeeld `ijsselstijn.nl`, gebruik dan `nl.ijsselstijn.scorekrijt`. Gebruik geen domein dat je niet bezit.

**Wat er verandert als je dit doet:**
- Voor Android is het een andere app. Wie de APK van GitHub (`com.example.scorekrijtapp`) al heeft, kan er niet op bijwerken, en verliest de lokale gegevens als hij de oude app verwijdert.
- Alleen `applicationId` in `app/build.gradle.kts` verandert. De codepakketnaam (`namespace`) en de mappen met code mogen blijven.
- De deelfunctie gebruikt de pakketnaam automatisch (`${packageName}.fileprovider`), dus daar hoeft niets aan te veranderen.
- Meld de overstap in het changelog en in de uitleg bij de downloads.

- [ ] Pakketnaam gekozen: `______________________`
- [ ] `applicationId` aangepast en een testbouw geprobeerd op een telefoon

### 1.2 Overige keuzes

- [ ] **Soort account:** persoonlijk of organisatie. Voor een persoonlijk account dat na 13 november 2023 is aangemaakt, geldt volgens meerdere bronnen een verplichte gesloten test (zie 5). Organisatieaccounts zijn daarvan vrijgesteld, maar vragen om extra gegevens (bijvoorbeeld een D-U-N-S-nummer). Controleer dit in de Play Console.
- [ ] **Back-up door Android:** het manifest staat nu op `allowBackup="true"` met lege regels. Dat betekent dat Android alle app-gegevens (ook namen van spelers) in een back-up van het Google-account kan opnemen. Dat staat ook zo in het privacybeleid. Wil je dat niet, zet het dan op `false` of vul de regels in `backup_rules.xml` en `data_extraction_rules.xml` in.
- [ ] **Naam in de winkel:** `ScoreKrijt Biljart` (zie de releaseteksten). De naam onder het pictogram op de telefoon is nu `ScoreKrijtApp` (`app_name`); pas die aan als je dat wilt.

## 2. De app voorbereiden

- [x] `targetSdk` is 36 (Android 16). Google Play eist dit voor nieuwe apps en updates vanaf 31 augustus 2026. Controleer of de eis niet is gewijzigd.
- [x] Geen `INTERNET`-recht. Alleen Bluetooth-rechten (`BLUETOOTH_CONNECT`, `BLUETOOTH_SCAN` met `neverForLocation`).
- [x] AI-vermelding in de app (Help / spelregels, Over ScoreKrijt) en in de winkeltekst.
- [ ] `versionCode` en `versionName` kloppen voor deze versie (bij iedere nieuwe upload moet `versionCode` hoger zijn dan de vorige).
- [ ] App-pictogram: controleer dat het pictogram scherp is op alle formaten.

## 3. Ondertekenen en bouwen (door jou, in Android Studio)

- [ ] Een **upload-sleutel** (`.jks`) maken via Build, Generate Signed App Bundle. Bewaar het bestand en de wachtwoorden op een veilige plek, **buiten Git en niet in een gedeelde map**. Verlies je de sleutel, dan kun je geen updates meer uploaden zonder een procedure bij Google.
- [ ] **Play App Signing** gebruiken (Google beheert de uiteindelijke sleutel; jij houdt de upload-sleutel).
- [ ] Een **Android App Bundle** (`.aab`) bouwen met de release-variant. Controleer dat de bundel de nieuwe pakketnaam en het juiste `versionCode` heeft.

## 4. Play Console

- [ ] Ontwikkelaarsaccount aanmaken en betalen (eenmalige kosten; controleer het bedrag in de Play Console). Identiteit en contactgegevens bevestigen.
- [ ] Nieuwe app aanmaken: naam, taal (Nederlands), app of spel (app), gratis of betaald (gratis).
- [ ] **Privacybeleid:** gebruik als webadres `https://github.com/bramijsselstijn/ScoreKrijt/blob/main/PRIVACY.md`. Controleer dat de pagina openbaar te bekijken is.
- [ ] **Winkelvermelding:** titel, korte en volledige beschrijving en "wat is nieuw" uit `Docs/Release-teksten-v2.8.7.md` (NL en EN, de tekenlimieten zijn gecontroleerd). Werk de tekst bij voor de versie die je uploadt.
- [ ] **Beeldmateriaal:** pictogram van 512 x 512 pixels (het logo in `ScoreKrijt Logo.png` is 1024 x 1024), een afbeelding van 1024 x 500 en minstens twee schermafbeeldingen van de telefoon. Maak de schermafbeeldingen met de definitieve versie.
- [ ] **Categorie en contact:** categorie (bijvoorbeeld Sport), een e-mailadres dat in de winkel zichtbaar is. Gebruik daarvoor liever niet je privéadres als je dat niet wilt tonen.

### 4.1 Formulieren in "App-inhoud" (concept, controleer zelf)

Op dit moment, op basis van hoe de app werkt (gegevens blijven op het apparaat, geen internet):

| Formulier | Voorlopig antwoord | Opmerking |
|---|---|---|
| Privacybeleid | Webadres van `PRIVACY.md` | Zie boven. |
| Advertenties | Nee | Geen advertenties. |
| App-toegang | Geen beperking | Geen inlog nodig. |
| Gegevensbeveiliging (data safety) | Er worden geen gegevens verzameld of gedeeld | Deelfunctie is door de gebruiker gestart. Controleer hoe Google de automatische back-up van Android beoordeelt. |
| Inhoudsclassificatie | Geen geweld, geen gokken, geen gebruikersinhoud, geen echt geld | Vul de vragenlijst eerlijk in. |
| Doelgroep | Niet gericht op kinderen | Kies de leeftijdsgroepen die bij een biljartscoreteller passen. |
| Overige verklaringen | Geen nieuws-, financiële-, gezondheids- of overheidsapp | Controleer per onderdeel. |

## 5. Testen voordat de app openbaar kan

- [ ] **Interne test** met jezelf: controleer dat de bundel installeert en werkt.
- [ ] **Gesloten test:** bij een persoonlijk account (aangemaakt na 13 november 2023) volgens de huidige berichten minstens 12 testers die 14 dagen lang meedoen, voordat je productietoegang kunt aanvragen. Dit staat in de meeste bronnen, maar die zijn deels van partijen die testers verkopen. Controleer de eis in de Play Console zelf. Plan hier rekening mee: dit bepaalt de doorlooptijd.
- [ ] Testers kunnen leden van je biljartvereniging zijn. Ze hebben een Google-account en een Android-telefoon nodig.
- [ ] Productietoegang aanvragen en de vragen van Google beantwoorden.

## 6. Publiceren en daarna

- [ ] Productie-release maken met het `.aab`-bestand en de releasenotities.
- [ ] Controleer de vermelding op een telefoon (zoek op de naam of open de directe link).
- [ ] Zet de link naar de winkelpagina in de README en in de uitleg bij de downloads.
- [ ] Houd bij iedere volgende versie `versionCode` bij, test eerst en publiceer daarna.
- [ ] Vermeld in de README en op de winkelpagina dat de app met behulp van AI is gemaakt (staat al in de winkeltekst).

## Bronnen

- [Google Play: eisen voor doel-API](https://developer.android.com/google/play/requirements/target-sdk)
- [Overzicht van de 12-testersregel](https://www.choicely.com/blog/google-play-12-tester-rule) (bron van een derde partij)
- [Forum: "com.example is restricted"](https://ads.teamtreehouse.com/community/couldnt-upload-apk-because-comexample-is-restricted-what)
