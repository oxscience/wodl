# WODL - Trainingspläne als Code

Trainingspläne leben als Excel, als PDF, als Screenshot in WhatsApp. Jeder Coach hat sein eigenes Format, und keine App kann irgendwas davon lesen.

Ich habe eine kleine Sprache gebaut, die das löst: **WODL** (Workout Definition Language).

### 1. Wie sieht das aus?

```
@plan "Full Body Basics"
@freq 3x/week
@cycle 4w: w1-3 progress, w4 deload

---[Day A] Mo

Kniebeugen           3x5   @RPE8  r180s  +2.5kg/w
Bankdrücken          3x8   @RPE7  r120s
LH Rudern            3x8   @RPE7  r120s

---[Day B] Mi

Kreuzheben           3x5   @RPE8  r180s  +2.5kg/w
Schulterdrücken      3x8   @RPE7  r120s
Klimmzüge            3x8   @BW    r120s

> Perfekt für Anfänger und Wiedereinsteiger
```

Eine Zeile ist eine Übung. Sätze, Reps, Intensität, Pause und Progression stehen auf einen Blick da, und ein Programm kann daraus die komplette Wochen-Matrix rechnen: Woche 1 bis 4 inklusive Deload, ohne dass jemand eine Tabelle pflegt.

### 2. Was kann die Sprache?

- **Volumen:** `4x8`, `3x8-12`, `3x30s`, Reverse Pyramid `10,8,6`
- **Intensität:** `@RPE8`, `@85%`, `@BW+10kg`, `@ISO`
- **Pausen:** `r90s`, `r2m`
- **Tempo:** `t3010` (exzentrisch, Pause, konzentrisch, Pause)
- **Progression:** `+2.5kg/w`, `+1rep/w`
- **Supersets, Circuits, Giant Sets:** `ss { ... }`
- **Deutsche Namen:** `Bankdrücken` erkennt der Parser genauso wie `Bench Press`. Die Übungsbibliothek kennt 162 Übungen mit deutschen Aliases, Tippfehler werden automatisch korrigiert.

### 3. Der Katalog: 40 fertige Pläne aus der Forschung

Der eigentliche Anlass für diesen Post: WODL hat jetzt einen kuratierten Katalog mit 40 Plänen. 11 Trainings-Beispiele und 29 Protokolle, deren Parameter direkt aus der Studienlage kommen. Ein Ausschnitt:

- **Reha:** VKB nach dem Melbourne ACL Guide, Achillessehne (Alfredson und Silbernagel), Patellasehne (Heavy Slow Resistance), Hamstring (Askling L-Protokoll), Leiste (Hölmich), Sprunggelenk, Plantarfasziitis, Tennisarm, Frozen Shoulder, Thrower's Ten, HWS-Tiefenflexoren
- **Prävention:** Nordic Hamstring über 10 Wochen, Copenhagen Adduction, FIFA 11+
- **Kraft-Klassiker:** Anfänger-LP, 5/3/1, Texas Method, GZCLP
- **Hypertrophie:** Novize und Intermediate nach den Prinzipien der Helms-Pyramide
- **Spezial:** Otago-Sturzprävention, HiRIT für Knochendichte, In-Season-Erhalt und Off-Season-Block für Teamsport

Jede Datei nennt ihre Quellen als Kommentar im Kopf, alle DOIs sind gegen Crossref und PubMed geprüft. Wo ein Protokoll Lasten offenlässt oder wir vom Original abweichen, steht das als Kommentar direkt an der Übung.

Wichtig: Die Reha-Protokolle sind Referenzen für Fachpersonal, kein Ersatz für Diagnostik oder individuelle Betreuung.

### 4. Ausprobieren

Der Playground läuft im Browser, ohne Anmeldung: **[wodl.outoftheb-ox.de](https://wodl.outoftheb-ox.de)**. Links WODL eingeben, rechts kommt die Tabelle raus, wahlweise als Wochen-Matrix oder JSON. PDF-Export mit eigenem Logo ist eingebaut.

Code und Katalog sind Open Source (MIT): [github.com/oxscience/wodl](https://github.com/oxscience/wodl)

### 5. Feedback

Fehlt eine Übung? Stimmt eine Dosierung nicht? Schreibt mir hier per Nachricht oder macht ein Issue auf GitHub auf.
