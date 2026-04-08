"""WOD CLI — parse .wod files from the command line.

Usage:
    wod plan.wod              # validate and show summary
    wod plan.wod --json       # output as JSON
    wod plan.wod --markdown   # output as Markdown table
    wod --list                # list all known exercises
    wod --list compound       # list compound exercises only
"""

from __future__ import annotations

import argparse
import sys

from wod.parser import parse, to_json, to_markdown
from wod.registry import list_exercises


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(
        prog="wod",
        description="WOD — Workout Definition Language parser",
    )
    p.add_argument("file", nargs="?", help="Path to a .wod file")
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
        print(f"Plan:      {plan.name or '(unnamed)'}")
        print(f"Frequency: {plan.frequency or '-'}")
        print(f"Cycle:     {plan.cycle_length or '-'}")
        print(f"Unit:      {plan.unit}")
        print(f"Sessions:  {len(plan.sessions)}")
        print()
        for session in plan.sessions:
            days = " ".join(session.days) if session.days else ""
            ex_count = 0
            for item in session.items:
                if hasattr(item, "exercises"):
                    ex_count += len(item.exercises)
                else:
                    ex_count += 1
            print(f"  [{session.name}] {days} — {ex_count} exercises")

        if plan.warnings:
            print()
            print("Warnings:")
            for w in plan.warnings:
                print(f"  - {w}")


if __name__ == "__main__":
    main()
