# WODL in eigene Apps einbauen

WODL ist Open Source (MIT) und läuft komplett bei dir. Für die meisten Fälle reicht die Python-Bibliothek, für andere Sprachen die Kommandozeile, und wer die Web-App selbst betreiben will, startet sie als Docker-Container.

## Python

Installieren:

```bash
pip install git+https://github.com/oxscience/wodl
```

Einen Plan lesen und weitergeben:

```python
from wodl import parse, to_json, to_markdown

plan = parse(open("plan.wodl", encoding="utf-8").read())

for w in plan.warnings:          # unbekannte Übungen, kaputte Zeilen
    print("Hinweis:", w)

print(to_json(plan))             # Struktur für Apps, siehe JSON-Format
print(to_markdown(plan))         # Tabellen für Doku oder E-Mail
```

Für eigene Datenstrukturen gibt es `to_dict(plan)`, das dasselbe wie das JSON als Python-Dictionary liefert.

Phasen und Blöcke stehen an jeder Einheit in `phase` (`"Phase 3"`, `"Block 1"`, sonst `None`). So holst du dir wie die Phasen-Auswahl der App nur die aktuelle Phase, dazu Einheiten ohne Phase wie ein Gehprogramm:

```python
aktuell = [s for s in plan.sessions if s.phase in (None, "Phase 3")]
```

## Progression aus Python

Dieselbe Engine wie im Reiter Progression, Woche für Woche als gültiges WODL:

```python
from wodl import parse
from wodl.progression import ProgressionConfig, progress_plan

plan = parse(open("plan.wodl", encoding="utf-8").read())
config = ProgressionConfig(weeks=6, goal="ausdauer", deload_rhythm="last")

for week in progress_plan(plan, config):
    print(week.label)
    print(week.text)             # wieder WODL, also auch wieder parsebar
```

Als Ziel gibt es `hypertrophie`, `kraft` und `ausdauer`, die übrigen Stellschrauben stehen in `ProgressionConfig`.

## Kommandozeile

Nach der Installation steht das Kommando `wodl` bereit:

```bash
wodl plan.wodl              # prüfen und Zusammenfassung zeigen
wodl plan.wodl --json       # JSON ausgeben
wodl plan.wodl --markdown   # Tabellen ausgeben
wodl --list                 # alle bekannten Übungen
```

## Andere Sprachen

Wer nicht in Python arbeitet, ruft die Kommandozeile auf und liest das JSON, zum Beispiel in Node:

```js
const { execFileSync } = require("node:child_process");
const plan = JSON.parse(execFileSync("wodl", ["plan.wodl", "--json"], { encoding: "utf8" }));
console.log(plan.sessions.map((s) => s.name));
```

Brauchst du WODL als HTTP-Dienst in deinem eigenen Netz, reichen ein paar Zeilen Flask:

```python
from flask import Flask, jsonify, request
from wodl import parse, to_dict

app = Flask(__name__)

@app.post("/wodl")
def wodl_json():
    return jsonify(to_dict(parse(request.get_data(as_text=True))))
```

## Die Web-App selbst betreiben

```bash
git clone https://github.com/oxscience/wodl
cd wodl
docker build -t wodl .
docker run -p 5051:5051 wodl
```

Danach läuft WODL Progressions unter http://localhost:5051, mit Bibliothek, Progression und Teilen-Links, nur eben auf deinem Rechner oder Server.

## Was es bewusst nicht gibt

Eine öffentliche API auf wodl.outoftheb-ox.de gibt es nicht, da sie Wartung und Verfügbarkeit verspräche, die ein kleines Open-Source-Projekt nicht halten kann. Die Bibliothek, die Kommandozeile oder die eigene Installation liefern dieselben Ergebnisse und laufen dort, wo deine Daten ohnehin liegen.
