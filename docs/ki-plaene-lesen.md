# Lokale KI liest Pläne

In die andere Richtung gibst du einem lokalen Modell einen fertigen Plan und lässt es damit arbeiten. Dafür eignet sich das JSON aus dem Reiter JSON, da jede Angabe dort ein eigenes Feld hat und das Modell nichts aus Abkürzungen erraten muss.

## So geht es

1. Plan in WODL öffnen, Vorschau auf JSON stellen und mit **JSON kopieren** in die Zwischenablage holen.
2. In LM Studio oder einer Ollama-Oberfläche das JSON einfügen und die Aufgabe dazuschreiben.

Klient:innen-Namen braucht das Modell dafür nicht, und im JSON stehen auch keine.

## Aufgaben, die gut funktionieren

- **Für Klient:innen erklären:** „Erkläre diesen Plan in einfacher Sprache für eine 60-jährige Klientin, ein Absatz pro Einheit, ohne Fachbegriffe.“
- **Übersetzen:** „Übersetze Übungsnamen und Notizen ins Englische, Zahlen und Struktur bleiben gleich.“
- **Gegen die Ausstattung prüfen:** „Welche Übungen brauchen Geräte außer Kurzhanteln und einer Matte? Schlag je eine Alternative vor.“
- **Fragen sammeln:** „Was sollte ich vor dem Start klären, etwa zu Schmerzen, Vorerfahrung oder Zeit?“

## Was du besser nicht der KI überlässt

Zählen und Rechnen machen die Werkzeuge in WODL zuverlässiger, da sie nicht raten. Die Sätze pro Muskelgruppe stehen im Reiter Volumen, die Wochen mit Steigerung und Deload im Reiter Progression. Ein Modell kann diese Zahlen gut erklären, aber es sollte sie nicht selbst ausrechnen.

## Datenschutz

Mit einem lokalen Modell bleiben Plan und Fragen auf deinem Rechner. Bei Cloud-Modellen gilt das nicht, und Gesundheitsdaten von Klient:innen gehören dort nicht hinein. Ein Plan ohne Namen und Diagnose ist meist unkritisch, die Entscheidung liegt aber bei dir und deiner Praxis.
