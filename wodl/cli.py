"""WODL CLI — parse .wodl files from the command line.

Usage:
    wodl plan.wodl              # validate and show summary
    wodl plan.wodl --json       # output as JSON
    wodl plan.wodl --markdown   # output as Markdown table
    wodl --list                # list all known exercises
    wodl --list compound       # list compound exercises only
"""

from __future__ import annotations

import argparse
import sys

from wodl.parser import parse, to_json, to_markdown
from wodl.registry import list_exercises


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(
        prog="wodl",
        description="WODL — Workout Definition Language parser",
    )
    p.add_argument("file", nargs="?", help="Path to a .wodl file")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.add_argument("--markdown", "--md", action="store_true", help="Output as Markdown")
    p.add_argument(
        "--list",
        nargs="?",
        const="all",
        metavar="CATEGORY",
        help="List known exercises (optionally filter: compound, isolation, cardio)",
    )
    args = p.parse_args(argv)

    # List exercises mode
    if args.list:
        category = None if args.list == "all" else args.list
        exercises = list_exercises(category)
        for name in exercises:
            print(name)
        return

    # Parse mode
    if not args.file:
        p.print_help()
        sys.exit(1)

    with open(args.file) as f:
        text = f.read()

    plan = parse(text)

    if args.json:
        print(to_json(plan))
    elif args.markdown:
        print(to_markdown(plan))
    else:
        # Summary view
        print(f"Plan:      {plan.name or '(unbenannt)'}")
        print(f"Frequenz:  {plan.frequency or '-'}")
        print(f"Zyklus:    {plan.cycle_length or '-'}")
        print(f"Gewicht:   {plan.unit}")
        print(f"Einheiten: {len(plan.sessions)}")
        print()
        for session in plan.sessions:
            days = " ".join(session.days) if session.days else ""
            ex_count = 0
            for item in session.items:
                if hasattr(item, "exercises"):
                    ex_count += len(item.exercises)
                else:
                    ex_count += 1
            print(f"  [{session.name}] {days} — {ex_count} Übungen")

        if plan.warnings:
            print()
            print("Hinweise:")
            for w in plan.warnings:
                print(f"  - {w}")


if __name__ == "__main__":
    main()
