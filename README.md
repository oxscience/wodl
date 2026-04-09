# WODL — Workout Definition Language

Eine minimalistische Sprache fuer strukturierte Trainingsplaene.

**Schreib deinen Trainingsplan als Text — kompakt, lesbar, maschinenlesbar.**

```wodl
@plan "Push Pull Legs"
@freq 6x/week
@cycle 4w: w1-3 progress, w4 deload

---[Push] Mo Do

Bench Press          4x8  @RPE8  r120s  +2.5kg/w
OHP                  3x10 @70%   r90s
ss {
  Incline DB Fly     3x12
  Tricep Pushdown    3x12
}
Lateral Raise        4x15 r60s  drop

---[Pull] Di Fr

Deadlift             3x5  @RPE9  r180s
Barbell Row          4x8  @RPE8  r120s
Hammer Curl          3x12 r60s

---[Legs] Mi Sa

Squat                4x6  @RPE8  r180s  +2.5kg/w  t3010
RDL                  3x10 @RPE7  r120s
Calf Raise           4x15 r60s
```

## Warum?

Trainingsplaene leben in Excel-Tabellen, PDFs, Screenshots und WhatsApp-Nachrichten. Keins davon ist versionierbar, vergleichbar oder maschinenlesbar.

WODL ist beides: **fuer Menschen lesbar** (jeder Trainer versteht es sofort) und **fuer Maschinen parsbar** (ein Parser macht daraus strukturierte Daten).

## Playground

Direkt im Browser ausprobieren — ohne Installation:

```bash
python playground.py
# Oeffnet http://localhost:5051
```

Links `.wodl` schreiben, rechts live das Ergebnis sehen.

## Install

```bash
pip install -e .
```

## Usage

### CLI

```bash
wodl plan.wodl               # Zusammenfassung
wodl plan.wodl --json        # JSON-Output
wodl plan.wodl --markdown    # Markdown-Tabellen
wodl --list                 # Alle bekannten Uebungen
wodl --list compound        # Nur Compound-Movements
```

### Python

```python
from wodl import parse, to_json, to_markdown

plan = parse(open("plan.wodl").read())

print(to_json(plan))      # Strukturiertes JSON
print(to_markdown(plan))   # Lesbare Tabelle
```

## Syntax auf einen Blick

### Metadata

```wodl
@plan "Plan Name"
@freq 4x/week
@cycle 4w: w1-3 progress, w4 deload
@unit kg
```

### Sessions

```wodl
---[Session Name] Mo Mi Fr
```

Tage: `Mo Di Mi Do Fr Sa So` (oder Englisch: `Mon Tue Wed Thu Fri Sat Sun`)

### Uebungszeile

```
Name    SETSxREPS  @INTENSITY  rREST  MODIFIERS
```

| Token | Beispiel | Bedeutung |
|-------|----------|-----------|
| Saetze x Reps | `4x8`, `3x8-12`, `5x5`, `3x30s` | Volumen |
| Intensitaet | `@RPE8`, `@85%`, `@100kg`, `@BW+10kg` | Belastung |
| Pause | `r90s`, `r2m`, `r60-90s` | Satzpause |
| Tempo | `t3010` | Exzentrisch-Pause-Konzentrisch-Pause |
| Progression | `+2.5kg/w`, `+1rep/w` | Woechentliche Steigerung |
| Modifier | `drop`, `cluster`, `pause-rep` | Satzmethode |

### Gruppierungen

```wodl
ss {                    # Superset
  Lateral Raise  3x15
  Face Pull      3x15
}

circuit {               # Circuit
  Push-up         x20
  Plank           60s
}

giant {                 # Giant Set (4+)
  OHP             3x10
  Lateral Raise   3x15
  Face Pull       3x15
  Shrug           3x12
}
```

### Notizen & Kommentare

```wodl
# Das ist ein Kommentar (wird ignoriert)
> Das ist eine Notiz (gehoert zur Session)
Bench Press  4x8  # Inline-Kommentar
```

## Deutsche Uebungsnamen

45+ Uebungen mit kanonischen englischen Namen. Deutsche Aliases und Abkuerzungen werden automatisch aufgeloest:

```
Bankdruecken     -> Bench Press
Kniebeugen       -> Squat
Kreuzheben       -> Deadlift
Klimmzuege       -> Pull-up
KH Rudern        -> Dumbbell Row
LH Rudern        -> Barbell Row
Seitheben        -> Lateral Raise
Schulterdruecken -> OHP
Liegestuetz      -> Push-up
```

Unbekannte Uebungen werden trotzdem geparst — es gibt nur eine Warnung.

## Beispiel-Plaene

Im [`examples/`](examples/) Ordner:

| Datei | Split | Frequenz | Fokus |
|-------|-------|----------|-------|
| `ppl-hypertrophy.wodl` | Push/Pull/Legs | 6x/Woche | Hypertrophie, Supersets |
| `upper-lower-strength.wodl` | Upper/Lower | 4x/Woche | 5x5 Kraft + Volumen |
| `minimalist-3day.wodl` | Full Body | 3x/Woche | Nur Compounds, 45 min |

## Was kann man damit bauen?

- **Plaene versionieren** — `.wodl` in Git, Aenderungen diffbar
- **Plaene exportieren** — JSON fuer Apps, Markdown fuer Docs
- **Plaene generieren** — LLMs koennen `.wodl` ausgeben statt Freitext
- **Plaene validieren** — Parser warnt bei unbekannten Uebungen
- **App-Integration** — Import in Fitness-Apps, Kalender-Export, Progression-Tracking

## License

MIT
