"""Lokale KI schreibt einen WODL-Plan, der Parser prüft, das Modell bessert nach.

Voraussetzung: Ollama läuft lokal (http://127.0.0.1:11434) und das Modell ist geladen,
z. B. `ollama pull qwen3:8b`. Aufruf: python ki_plan.py "Ganzkörperplan für Anfänger, 2x pro Woche"
Nichts verlässt den Rechner.
"""
import json
import sys
import urllib.request

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
for w in plan.warnings:
    print("Noch offen:", w, file=sys.stderr)
