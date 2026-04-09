# WODL — Trainingsplaene als Code

Kennt ihr das? Trainingsplaene als Excel, als PDF, als Screenshot in WhatsApp. Jeder Coach hat sein eigenes Format, nichts davon ist standardisiert, nichts davon kann eine App lesen.

Ich hab eine kleine Sprache gebaut, die das loest: **WODL** (Workout Definition Language).

## Wie sieht das aus?

```
@plan "Full Body Basics"
@freq 3x/week
@cycle 4w: w1-3 progress, w4 deload

---[Day A] Mo

Kniebeugen           3x5   @RPE8  r180s  +2.5kg/w
Bankdruecken         3x8   @RPE7  r120s
LH Rudern            3x8   @RPE7  r120s

---[Day B] Mi

Kreuzheben           3x5   @RPE8  r180s  +2.5kg/w
Schulterdruecken     3x8   @RPE7  r120s
Klimmzuege           3x8   @BW    r120s

> Perfekt fuer Anfaenger und Wiedereinsteiger
```

**Eine Zeile = eine Uebung.** Saetze, Reps, Intensitaet, Pause, Progression — alles auf einen Blick.

## Was kann die Sprache?

- **Volumen:** `4x8`, `3x8-12`, `3x30s`
- **Intensitaet:** `@RPE8`, `@85%`, `@BW+10kg`
- **Pausen:** `r90s`, `r2m`
- **Tempo:** `t3010` (Exzentrisch-Pause-Konzentrisch-Pause)
- **Progression:** `+2.5kg/w`, `+1rep/w`
- **Supersets:** `ss { ... }`, Circuits, Giant Sets
- **Deutsche Namen:** `Bankdruecken` wird automatisch zu `Bench Press`, `Kniebeugen` zu `Squat`

## Warum nicht einfach eine Tabelle?

Tabellen sind **Darstellung**. WODL ist **Daten**. Aus einer WODL-Zeile kann ein Tool:

- die Progression berechnen
- die Muskelgruppe zuordnen
- den Plan in eine App importieren
- Woche 1 mit Woche 4 vergleichen

Aus einer Excel-Tabelle kann es das nicht.

## Ausprobieren

Das Ganze ist Open Source auf GitHub:
**[github.com/oxscience/wodl](https://github.com/oxscience/wodl)**

Es gibt einen **Playground** — WODL links eingeben, rechts live das Ergebnis sehen (Tabelle, JSON oder Summary).

Drei Beispiel-Plaene sind dabei:
- Push/Pull/Legs (6x/Woche)
- Upper/Lower Strength (4x/Woche)
- Minimalist Full Body (3x/Woche)

## Was denkt ihr?

Wuerde euch sowas helfen? Habt ihr Uebungen die fehlen, oder Features die ihr euch wuenschen wuerdet?

Feedback ist willkommen — das Projekt ist noch frueh und ich bin offen fuer Ideen.
