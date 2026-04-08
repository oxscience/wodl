# WOD — Workout Definition Language

A minimalist DSL for writing structured training plans in code blocks.

```wod
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

## Install

```bash
pip install -e .
```

## Usage

### Python

```python
from wod import parse, to_json, to_markdown

plan = parse(open("plan.wod").read())

print(to_json(plan))      # structured JSON
print(to_markdown(plan))   # readable table
```

### CLI

```bash
wod plan.wod               # summary
wod plan.wod --json        # JSON output
wod plan.wod --markdown    # Markdown tables
wod --list                 # all known exercises
wod --list compound        # only compound movements
```

## Syntax

### Metadata

```wod
@plan "Plan Name"
@freq 4x/week
@cycle 4w: w1-3 progress, w4 deload
@unit kg
```

### Sessions

```wod
---[Session Name] Mo Mi Fr
```

Days: `Mo Di Mi Do Fr Sa So` (or English: `Mon Tue Wed Thu Fri Sat Sun`)

### Exercise Lines

```
Name    SETSxREPS  @INTENSITY  rREST  MODIFIERS
```

| Token | Examples | Meaning |
|-------|----------|---------|
| Sets x Reps | `4x8`, `3x8-12`, `5x5`, `3x30s` | Volume |
| Intensity | `@RPE8`, `@85%`, `@100kg`, `@BW+10kg` | Load |
| Rest | `r90s`, `r2m`, `r60-90s` | Pause between sets |
| Tempo | `t3010` | Eccentric-Pause-Concentric-Pause |
| Progression | `+2.5kg/w`, `+1rep/w` | Weekly increment |
| Modifiers | `drop`, `cluster`, `pause-rep` | Set type |

### Groupings

```wod
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

### Notes & Comments

```wod
# This is a comment (ignored by parser)
> This is a note (attached to the session)
Bench Press  4x8  # inline comment
```

## Exercise Registry

45+ exercises with canonical English names. German aliases and abbreviations are resolved automatically:

```
Bankdrücken     -> Bench Press
Kniebeugen      -> Squat
Kreuzheben      -> Deadlift
Klimmzüge       -> Pull-up
KH Rudern       -> Dumbbell Row
LH Rudern       -> Barbell Row
Seitheben       -> Lateral Raise
```

Unknown exercises trigger a warning but still parse.

## Examples

See the [`examples/`](examples/) directory:

- `ppl-hypertrophy.wod` — 6-day Push/Pull/Legs
- `upper-lower-strength.wod` — 4-day Upper/Lower
- `minimalist-3day.wod` — 3-day Full Body

## License

MIT
