# Biljart ScoreKrijt teller

Scoreteller voor biljart: een Android-app voor op de telefoon en de SK-Box (Python, Raspberry Pi) voor het grootscherm. Telefoon en SK-Box communiceren via Bluetooth.

Huidige versie: **2.8.9**.

## Gemaakt met behulp van AI

ScoreKrijt (de Android-app, de SK-Box-software, de hulpscripts en de handleidingen) is gemaakt met behulp van AI (Claude van Anthropic). De wensen, de keuzes en het testen op een echte telefoon en SK-Box komen van de maker.

*ScoreKrijt (the Android app, the SK-Box software, the helper scripts and the manuals) was made with the help of AI (Claude by Anthropic). The requirements, the decisions and the testing on a real phone and SK-Box come from the author.*

## Inhoud

- `Phyton/V2.8.7/` – broncode van de SK-Box (huidige versie)
- `Phyton/SK-Box_scripts/` – hulpscripts voor de SK-Box: `sk-update.sh` (bijwerken via USB-stick, zonder internet) en `sk-stille-opstart.sh` (stille opstart met het ScoreKrijt-logo, taakbalk uit, wifi uit)
- `Docs/` – handleidingen als pdf (SK-Box installeren, SK-Box bijwerken, Instellingen van de SK-Box). Daarnaast `Docs/Play-Store-checklist.md` en `Docs/Release-teksten-v2.8.7.md` voor de publicatie in de Google Play Store. Daarnaast `Docs/Play-Store-checklist.md` en `Docs/Release-teksten-v2.8.7.md` voor de publicatie in de Google Play Store
- [`CHANGELOG.md`](CHANGELOG.md) – wat er per versie is veranderd
- [`ROADMAP.md`](ROADMAP.md) – geplande versies
- [`PRIVACY.md`](PRIVACY.md) – privacybeleid van de app (Nederlands en Engels)

## Versies

Elke versie krijgt een tag (bijvoorbeeld `v2.8.7`). De APK van de Android-app staat niet in de repository.

## De SK-Box installeren en bijwerken

Zie de handleidingen in `Docs/`. De SK-Box heeft geen internet nodig: een nieuwe versie van ScoreKrijt wordt met een USB-stick en het script `sk-update.sh` geïnstalleerd.

## Licentie

ScoreKrijt is vrije software onder de [GNU General Public License versie 3](LICENSE) (GPL-3.0). Je mag het gebruiken, aanpassen en delen, maar een aangepaste versie die je verspreidt moet je onder dezelfde licentie met de broncode delen.
