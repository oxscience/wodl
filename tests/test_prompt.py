"""Tests für wodl/prompt.py — Systemprompt, Rückmeldung und Antwort-Auszug für lokale KI."""

from wodl import parse
from wodl.prompt import extract, feedback, system_prompt
from wodl.registry import EXERCISES


def test_system_prompt_lists_every_exercise_and_the_syntax():
    p = system_prompt()
    assert all(meta["de"] in p for meta in EXERCISES.values())
    assert "@plan" in p and "---[Tag A]" in p and "```wodl" in p


def test_feedback_suggests_known_names():
    plan = parse("---[A] Mo\nKurzhantel-Überkopfdrücken 3x10\n")
    text = feedback(plan.warnings)
    assert "Kurzhantel-Überkopfdrücken" in text and "Meintest du: " in text and "Kurzhantel-Schulterdrücken" in text


def test_extract_strips_thinking_and_fences():
    answer = "<think>erst überlegen</think>Hier:\n```wodl\n@plan \"X\"\n---[A] Mo\nKniebeuge 3x5\n```\nViel Erfolg!"
    assert extract(answer) == '@plan "X"\n---[A] Mo\nKniebeuge 3x5'
