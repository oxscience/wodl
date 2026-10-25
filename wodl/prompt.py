"""Systemprompt und Rückmeldung für lokale KI-Modelle, die WODL schreiben (Ollama, LM Studio …).

Erprobt mit qwen3:8b über Ollama: Mit der Übungsliste im Prompt und „Meintest du …?“-Vorschlägen
in der Rückmeldung kam nach zwei Runden ein Plan ohne Parser-Hinweise heraus. Ob der Plan
fachlich passt, prüft der Parser nicht.
"""

from __future__ import annotations

import re

from wodl.registry import EXERCISES, suggest

SYNTAX = """\
@plan "Name"                  Planname
@freq 2x/Woche                Häufigkeit
---[Tag A] Mo Do              neue Einheit mit Wochentagen
Kniebeuge  3x8  @RPE7  r90s   eine Zeile = eine Übung: Name, Sätze x Wdh., Intensität (@12kg, @RPE7, @BW), Pause (r90s)
Ausfallschritt  3x10  je Seite
Plank  3x30s                  Zeit statt Wiederholungen
ss {                          Supersatz: Klammer auf eigener Zeile, darunter die Übungen
}                             Klammer zu auf eigener Zeile
> Hinweis                     Notiz für Klient:innen
# Kommentar                   wird nicht angezeigt"""


def system_prompt() -> str:
    """Systemprompt: Antwortformat, Syntax-Spickzettel und alle bekannten Übungsnamen (deutsch)."""
    names = ", ".join(sorted(meta["de"] for meta in EXERCISES.values()))
    return (
        "Du schreibst Trainingspläne in WODL. Antworte nur mit dem Plan in einem Codeblock "
        "(```wodl … ```), ohne Erklärung.\n"
        f"Syntax:\n{SYNTAX}\n"
        f"Verwende nur Übungsnamen aus dieser Liste: {names}"
    )


def feedback(warnings: list[str]) -> str:
    """Rückmeldung an das Modell: Parser-Hinweise plus Namensvorschläge für unbekannte Übungen."""
    lines = []
    for w in warnings:
        m = re.search(r"'(.+?)'", w)
        hint = f" (Meintest du: {', '.join(suggest(m.group(1)))}?)" if m and suggest(m.group(1)) else ""
        lines.append(f"- {w}{hint}")
    return (
        "Der WODL-Parser meldet:\n" + "\n".join(lines)
        + "\nErsetze diese Zeilen durch Übungen aus der Liste und gib den ganzen Plan erneut aus."
    )


def extract(answer: str) -> str:
    """WODL aus einer Modellantwort holen (Codeblock, <think>-Abschnitte von Reasoning-Modellen raus)."""
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.S)
    m = re.search(r"```[^\n]*\n(.*?)```", answer, re.S)
    return (m.group(1) if m else answer).strip()
