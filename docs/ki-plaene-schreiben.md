# Lokale KI schreibt Pläne

Ein Sprachmodell auf deinem eigenen Rechner kann Pläne in WODL schreiben, und der Parser prüft danach, ob jede Zeile stimmt. Da Modell und Parser lokal laufen, verlässt dabei nichts den Rechner, auch keine Angaben zu Klient:innen.

## Warum WODL und nicht JSON

Für die Ausgabe eines Modells ist WODL besser geeignet als JSON. Der Text ist kurz, du kannst ihn ohne Werkzeug lesen und korrigieren, und der Parser sagt genau, welche Zeile er nicht versteht. JSON brauchst du erst danach, wenn der Plan in eine App soll.

## Was du brauchst

- [Ollama](https://ollama.com) oder [LM Studio](https://lmstudio.ai) mit einem Modell, zum Beispiel `ollama pull qwen3:8b`
- den Prompt für das Modell: In der App unter Vorschau, Reiter JSON, kopiert ihn der Knopf **Prompt für KI kopieren**. In Python liefert ihn `wodl.prompt.system_prompt()`.

Der Prompt enthält die Syntax als Spickzettel und alle Übungsnamen, die WODL kennt. Ohne diese Liste erfinden kleine Modelle gern Namen wie „Kurzhantel-Hocken“, die der Parser dann nicht zuordnen kann.

## Ohne Programmieren

Setz den kopierten Prompt in LM Studio als Systemprompt (bei Ollama-Oberflächen heißt das Feld oft „System“), beschreib den Plan in normaler Sprache und kopier die Antwort in den Editor von WODL. Was die Vorschau als unbekannt markiert, gibst du mit den „Meintest du …?“-Vorschlägen an das Modell zurück oder korrigierst es direkt.

## Mit einem kleinen Skript

Das Skript schickt die Anfrage an Ollama, prüft die Antwort mit dem Parser und gibt die Hinweise samt Namensvorschlägen so lange zurück, bis alles stimmt (höchstens drei Runden). Es liegt als [docs/ki_plan.py](https://github.com/oxscience/wodl/blob/main/docs/ki_plan.py) im Repository.

```python
import json, sys, urllib.request
from wodl import parse
from wodl.prompt import extract, feedback, system_prompt

MODEL = "qwen3:8b"

def chat(messages):
    body = {"model": MODEL, "messages": messages, "stream": False, "options": {"temperature": 0.2}}
    req = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["message"]["content"]

messages = [{"role": "system", "content": system_prompt()}, {"role": "user", "content": sys.argv[1]}]
for _ in range(3):
    answer = chat(messages)
    plan = parse(extract(answer))
    if not plan.warnings:
        break
    messages += [{"role": "assistant", "content": answer}, {"role": "user", "content": feedback(plan.warnings)}]

print(extract(answer))
```

Aufruf: `python ki_plan.py "Ganzkörperplan für Anfänger, 2x pro Woche, 45 Minuten"`. LM Studio bietet eine OpenAI-kompatible Schnittstelle unter `http://localhost:1234/v1/chat/completions`. Dafür änderst du Adresse und Modellnamen, setzt `temperature` direkt in den Body und liest die Antwort aus `choices[0].message.content`.

## Was dabei herauskommt

Im Test mit qwen3:8b über Ollama kam nach zwei Runden und rund einer Minute ein Plan heraus, den der Parser ohne Hinweis angenommen hat. Inhaltlich passte er trotzdem nicht ganz, denn bei der Vorgabe „nur Kurzhanteln“ standen Face Pulls am Kabelzug im Plan. Der Parser prüft eben die Form und nicht, ob ein Plan zur Person, zur Ausstattung oder zur Diagnose passt. Diese Prüfung bleibt bei dir. Größere Modelle dürften hier bessere Vorschläge machen als ein 8B-Modell, getestet ist das aber noch nicht.
