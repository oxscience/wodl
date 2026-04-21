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

Links `.wodl` schreiben, rechts live das Ergebnis sehen. Features:

- **Tabelle / JSON / Summary** — drei Ansichten im Live-Preview
- **Branding** — eigenes Logo, Praxis-/Coach-Name, Primärfarbe (6 Presets + Custom Hex)
- **Dark & Light Mode** — umschaltbar, persistiert in localStorage
- **PDF-Export** — via Browser-Print, mit Coach/Klient-Header und Datum
- **Share-Link** — URL enthält Branding und Plan (bei kurzen Plänen)

### Self-host (Railway / Docker)

```bash
# Lokal mit gunicorn
pip install -r requirements.txt && pip install -e .
gunicorn playground:app --bind 0.0.0.0:5051

# Docker
docker build -t wodl-playground .
docker run -p 5051:5051 wodl-playground

# Railway: railway.json ist vorhanden, `railway up` reicht
```

Health-Check: `GET /healthz` → `{"status": "ok"}`

### URL-Branding (für Coaches)

Coaches können ihre Klient:innen direkt zu einer gebrandeten Instanz linken:

```
https://your-wodl.app/?primary=%23ff4477&logo=https://.../logo.png&coach=Praxis%20M%C3%BCller
```

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
| Reverse Pyramid | `10,8,6` | Absteigende Reps pro Satz (z.B. McGill-Protokoll) |
| Intensitaet | `@RPE8`, `@RIR1`, `@ISO`, `@85%`, `@100kg`, `@BW+10kg`, `@low` | Belastung |
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

Im [`examples/`](examples/) Ordner — alle Pläne mit peer-reviewed Paper-Quellen direkt im File-Kommentar.

### Training

| Datei | Split | Frequenz | Evidenz |
|-------|-------|----------|---------|
| `beginner-full-body.wodl` | Full Body | 3x/Woche | Rhea et al. (2003), Med Sci Sports Exerc |
| `minimalist-3day.wodl` | Full Body | 3x/Woche | Schoenfeld et al. (2019), J Sports Sci |
| `home-minimal.wodl` | Full Body | 3x/Woche | Schoenfeld et al. (2017), J Strength Cond Res |
| `push-pull-4day.wodl` | Push/Pull | 4x/Woche | Schoenfeld et al. (2016), Sports Med |
| `upper-lower-strength.wodl` | Upper/Lower | 4x/Woche | Peterson et al. (2005), J Strength Cond Res |
| `ppl-hypertrophy.wodl` | Push/Pull/Legs | 6x/Woche | Schoenfeld et al. (2017), J Sports Sci |
| `powerbuilding-5day.wodl` | Upper/Lower + Arms | 5x/Woche | Schoenfeld et al. (2014), J Strength Cond Res |

### Rehabilitation (evidenzbasiert)

Diese Protokolle sind als **Referenz für Physiotherapeut:innen** gedacht, nicht als Ersatz für individuelle Betreuung. Jedes File enthält Phasen, Progressionskriterien und die Quellen-Papers als Kommentare.

| Datei | Indikation | Quellen |
|-------|-----------|---------|
| `rehab-acl-postop.wodl` | VKB-Rekonstruktion, 4 Phasen (0-24 Wo) | Wilk & Arrigo 2017, van Melick 2016 |
| `rehab-rotator-cuff.wodl` | Rotator Cuff / SAPS, konservativ | Ellenbecker 2010, Kuhn 2009, MOON |
| `rehab-lbp-mcgill.wodl` | Chronic Low Back Pain, McGill Big 3 | McGill 2016, Lee & McGill 2015 |
| `rehab-achilles-alfredson.wodl` | Achilles-Tendinopathie (midportion) | Alfredson 1998, Beyer 2015 |

## Was kann man damit bauen?

- **Plaene versionieren** — `.wodl` in Git, Aenderungen diffbar
- **Plaene exportieren** — JSON fuer Apps, Markdown fuer Docs
- **Plaene generieren** — LLMs koennen `.wodl` ausgeben statt Freitext
- **Plaene validieren** — Parser warnt bei unbekannten Uebungen
- **App-Integration** — Import in Fitness-Apps, Kalender-Export, Progression-Tracking

## License

MIT
