# Provenance: data/raw/free-exercise-db/exercises.json

## Quelle
- Repository: https://github.com/yuhonas/free-exercise-db
- Datei: `dist/exercises.json` (Bulk-Export, 873 Einträge)
- Abgerufen von: https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json
- Commit-SHA (main, zum Abrufzeitpunkt): `b0eed061e1c832b3ed815fbaa4b45b3cdc14df49`
- Commit-Datum: 2026-05-24T03:09:39Z
- Abrufdatum: 2026-08-02

## Lizenz
The Unlicense (Public Domain Dedication), bestätigt über die GitHub-Repo-API
(`license.spdx_id == "Unlicense"`). Keine Namensnennungspflicht; Quelle wird
hier und im Header der generierten Review-Dateien dennoch dokumentiert.

## Übernommene Felder
Nur strukturelle Metadaten:
- `name`
- `mechanic`
- `equipment`
- `primaryMuscles`
- `secondaryMuscles`
- `level`
- `category`

## Explizit NICHT übernommen
- `instructions` — Textbeschreibungen, deren Herkunft auf einen Scrape einer
  kommerziellen Fitness-Seite zurückgeht; die Unlicense-Widmung des
  free-exercise-db-Repos deckt das vermutlich nicht ab.
- `images` — dieselbe Herkunftsproblematik.

## Datei-Integrität
- SHA-256 (`exercises.json`): `d68a817484964095e6af0be2cdcbcc2c2504168d1d190c7d5c725ce52f3ae1f4`

Die Datei `exercises.json` in diesem Verzeichnis ist unverändert wie
abgerufen (keine Nachbearbeitung, kein Reformat). Alle Transformationen
(Matching, Mapping, Filterung) passieren als Code in `tools/` und werden
nicht in die Rohdatei zurückgeschrieben. Ein erneuter Abruf überschreibt
diese Datei und PROVENANCE.md; manuelle Entscheidungen liegen separat in
`data/review/DECISIONS.csv` und werden davon nicht berührt.
