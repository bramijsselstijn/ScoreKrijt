# Biljart ScoreKrijt teller

Scoreteller voor biljart: een Android-app voor op de telefoon en de SK-Box (Python, Raspberry Pi) voor het grootscherm. Telefoon en SK-Box communiceren via Bluetooth.

Huidige versie: **2.8.8**.

## Gemaakt met behulp van AI

ScoreKrijt (de Android-app, de SK-Box-software, de hulpscripts en de handleidingen) is gemaakt met behulp van AI (Claude van Anthropic). De wensen, de keuzes en het testen op een echte telefoon en SK-Box komen van de maker.

*ScoreKrijt (the Android app, the SK-Box software, the helper scripts and the manuals) was made with the help of AI (Claude by Anthropic). The requirements, the decisions and the testing on a real phone and SK-Box come from the author.*

## Inhoud

- `Android/ScoreKrijtApp/` – broncode van de Android-app
- `Phyton/V2.8.7/` – broncode van de SK-Box (huidige versie)
- `Phyton/SK-Box_scripts/` – hulpscripts voor de SK-Box: `sk-update.sh` (bijwerken via USB-stick, zonder internet) en `sk-stille-opstart.sh` (stille opstart met het ScoreKrijt-logo, taakbalk uit, wifi uit)
- `Docs/` – handleidingen (SK-Box installeren, SK-Box bijwerken, Instellingen van de SK-Box) en het script waarmee ze worden gebouwd (`build_skbox_handleidingen.ps1`, vereist Microsoft Word)
- [`CHANGELOG.md`](CHANGELOG.md) – wat er per versie is veranderd
- [`ROADMAP.md`](ROADMAP.md) – geplande versies

## Versies

Elke versie krijgt een tag (bijvoorbeeld `v2.8.7`). Gecompileerde APK's staan niet in de repository; die horen bij een GitHub Release.

## De SK-Box installeren en bijwerken

Zie de handleidingen in `Docs/`. De SK-Box heeft geen internet nodig: een nieuwe versie van ScoreKrijt wordt met een USB-stick en het script `sk-update.sh` geïnstalleerd.
