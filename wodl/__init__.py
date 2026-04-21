"""WODL — Workout Definition Language.

A minimalist DSL for writing structured training plans in code blocks.

Usage:
    from wodl import parse, to_json, to_markdown

    plan = parse('''
    @plan "My Plan"
    ---[Push] Mo
    Bench Press  4x8  @RPE8
    ''')

    print(to_json(plan))
    print(to_markdown(plan))
"""

from wodl.parser import (
    parse,
    to_dict,
    to_json,
    to_markdown,
    to_cycle_matrix,
    Plan,
    Session,
    ExerciseLine,
    ExerciseGroup,
    CycleWeek,
)
from wodl.registry import resolve, resolve_fuzzy, list_exercises, get_muscles, EXERCISES

__version__ = "0.1.0"

__all__ = [
    "parse",
    "to_dict",
    "to_json",
    "to_markdown",
    "to_cycle_matrix",
    "Plan",
    "Session",
    "ExerciseLine",
    "ExerciseGroup",
    "CycleWeek",
    "resolve",
    "resolve_fuzzy",
    "list_exercises",
    "get_muscles",
    "EXERCISES",
]
