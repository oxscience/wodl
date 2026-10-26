# WODL kurz erklärt

WODL ist eine kleine Sprache für Trainingspläne, und WODL Progressions ist die Web-App dazu. Ein Plan ist dabei einfach Text mit einer Zeile pro Übung, den Menschen lesen und Programme verarbeiten können, ohne dass dafür eine Datenbank oder ein Konto nötig ist.

## Ein Plan, drei Formen

- **Text (WODL):** Das schreibst du im Editor, und genau dieser Text steckt auch im geteilten Link.
- **Tabelle:** die Vorschau rechts, die auch im PDF und im Link für Klient:innen landet.
- **JSON:** dieselben Daten als Struktur für Programme, im Reiter JSON der Vorschau.

Alle drei entstehen aus demselben Text. Du pflegst also nur den Text, und Tabelle, JSON und Progression folgen daraus.

## Phasen, Blöcke und Wochen

Ein Plan ist in WODL der Makrozyklus, also zum Beispiel eine ganze Reha oder eine Saison. Beginnt der Name einer Einheit mit Phase, Stufe, Block oder Pre-OP, erkennt WODL darin einen Mesozyklus, und alles vor dem Doppelpunkt gehört zusammen, sodass `---[Block 1: Aufbau] Mo` und `---[Block 1: Tag B] Do` ein Block mit zwei Trainingstagen sind. Die Wochen, die der Reiter Progression daraus baut, sind die Mikrozyklen.

Hat ein Plan mindestens zwei solcher Phasen, wählst du oben in der Vorschau aus, in welcher Phase deine Klientin gerade ist. Tabelle, Progression, PDF und der Link für Klient:innen zeigen dann nur diese Phase, dazu Einheiten ohne Phase wie ein Gehprogramm für alle Stufen. Im Editor bleibt der ganze Plan stehen, und für die nächste Phase stellst du die Auswahl einfach um.

## Was gespeichert wird

Die Web-App speichert deine Pläne nur in deinem Browser. Ein geteilter Link trägt den Plan im Teil hinter dem `#`, und dieser Teil geht nie an den Server, sodass dort weder Pläne noch Namen von Klient:innen liegen. Wenn du Branding nutzt, stehen Praxisname, Logo-Adresse und Farbe im vorderen Teil des Links und damit wie jede Adresse im Zugriffsprotokoll des Servers.

## Wie es weitergeht

- [WODL in eigene Apps einbauen](eigene-apps.md): Python, Kommandozeile und eigene Installation
- [Das JSON-Format](json-format.md): welches Feld was bedeutet
- [Lokale KI schreibt Pläne](ki-plaene-schreiben.md): Ollama oder LM Studio, geprüft durch den Parser
- [Lokale KI liest Pläne](ki-plaene-lesen.md): Pläne erklären, übersetzen oder gegen die Ausstattung prüfen lassen

Die Syntax im Detail steht in der [README auf GitHub](https://github.com/oxscience/wodl#syntax-auf-einen-blick). Die Tour und das How-to-Video findest du oben in der App.
