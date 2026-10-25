# Das JSON-Format

Das JSON im Reiter JSON, aus `wodl plan.wodl --json` und aus `to_json(plan)` ist immer dasselbe. Es übernimmt die Werte so, wie sie im Plan stehen, und ergänzt, was WODL beim Lesen erkannt hat, also vor allem den Namen der Übung im Wörterbuch.

## Ein Beispiel

Aus diesem Plan:

```wodl
@plan "Demo"
@freq 2x/Woche
@cycle 4w: w1-3 Aufbau, w4 Deload
---[Tag A] Mo Do
> Aufwärmen 5 min
Kniebeuge  4x6-8  @80kg  r180s  t3010  +2.5kg/w   # sauber tief
circuit {
  Ausfallschritt  3x10/Seite
  Plank  3x30s
}
```

wird (gekürzt):

```json
{
  "name": "Demo",
  "frequency": "2x/Woche",
  "cycle_length": "4w",
  "cycle_phases": [{"weeks": "w1-3", "phase": "Aufbau"}, {"weeks": "w4", "phase": "Deload"}],
  "unit": "kg",
  "sessions": [{
    "name": "Tag A",
    "days": ["Mo", "Do"],
    "notes": ["Aufwärmen 5 min"],
    "items": [
      {"raw_name": "Kniebeuge", "canonical_name": "Squat", "display_name": "Kniebeuge",
       "sets": 4, "reps": "6-8", "intensity": "@80kg", "rest": "180s", "tempo": "3010",
       "progression": "+2.5kg/w", "modifiers": [], "comment": "sauber tief", "line": 6},
      {"kind": "circuit", "exercises": [
        {"display_name": "Ausfallschritt", "sets": 3, "reps": "10", "modifiers": ["je Seite"], "...": "..."},
        {"display_name": "Unterarmstütz", "sets": 3, "reps": "30s", "...": "..."}]}
    ]
  }],
  "warnings": []
}
```

## Der Plan

- `name`, `frequency`: aus `@plan` und `@freq`, sonst `null`
- `cycle_length`, `cycle_phases`: aus `@cycle`, die Phasen mit Wochen und Bezeichnung
- `unit`: `kg` oder `lb` aus `@unit`, Standard ist `kg`
- `sessions`: die Einheiten in der Reihenfolge des Plans
- `warnings`: Hinweise des Parsers, etwa „Unbekannte Übung …“. Eine leere Liste heißt, dass jede Zeile verstanden wurde.

## Eine Einheit

- `name`, `days`: aus `---[Name] Mo Do`
- `notes`: Zeilen mit `>` als Text für Klient:innen
- `items`: Übungen und Gruppen in Reihenfolge. Eine Gruppe erkennst du an `kind` (`superset`, `circuit` oder `giant`) und an ihrer Liste `exercises`.

## Eine Übung

- `raw_name`: so, wie es im Plan steht, auch mit Tippfehler
- `canonical_name`: der englische Schlüssel im Wörterbuch (`Squat`), `null` bei unbekannten Übungen. Für eigene Apps ist das der stabile Wert zum Verknüpfen, etwa mit Videos oder Muskelgruppen.
- `display_name`: der deutsche Anzeigename (`Kniebeuge`)
- `sets`: Zahl der Sätze
- `reps`: als Text, da es viele Formen gibt: `"8"`, `"6-8"`, `"30s"`, `"20min"`, `"10,8,6"` (Pyramide) oder `"AMRAP"`
- `intensity`: wie geschrieben, zum Beispiel `"@80kg"`, `"@RPE8"`, `"@70%"` oder `"@BW"`
- `rest`, `tempo`: Pause und Tempo, `null` wenn nicht angegeben
- `progression`: ein Steigerungs-Token wie `"+2.5kg/w"`, das die Progression berücksichtigt
- `modifiers`: Zusätze wie `"je Seite"`, `"drop"` oder `"pause-rep"`
- `comment`: Text hinter `#` in derselben Zeile
- `line`: Zeilennummer im Plan, praktisch für Fehlermeldungen in deiner App

## Stabilität

WODL steht bei Version 0.x. Felder können dazukommen, bestehende sollen bleiben, und wenn sich doch eines ändert, steht das unter „Was ist neu“ an der Versionsnummer der App. Die Version steht auch in `wodl.__version__`.
