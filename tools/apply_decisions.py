"""
Schreibt wodl/registry.py anhand von data/review/DECISIONS.csv fort.

Zwei Arten von Aenderungen:
  1. Neue Aliase auf BESTEHENDE kanonische Uebungen
     - alle Zeilen aus data/review/aliases_auto.csv (bereits als sicher
       eingestuft)
     - Zeilen aus DECISIONS.csv mit type=alias, decision=accept
  2. Neue kanonische Uebungen (type=new_exercise, decision=accept in
     DECISIONS.csv). Die 16 hier hart codierten Eintraege sind die manuell
     kuratierten Ergaenzungen aus Abschnitt 7 des Auftrags; Metadaten wurden
     aus data/raw/free-exercise-db/exercises.json abgeleitet und dort, wo
     die Quelle laut Mapping-Tabelle (Abschnitt 6) "MANUELL" verlangte
     (Muskeln bei "shoulders", Kategorie bei mechanic=null), fachlich
     nachbewertet.

Macht textuelle, chirurgische Aenderungen an registry.py statt eines vollen
AST-Rewrites, um Kommentare/Formatierung der handkuratierten Datei zu
erhalten. Nach dem Schreiben wird die Datei neu importiert und die
bestehende Testsuite laeuft, um Regressionen sofort zu erkennen.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "wodl" / "registry.py"
REVIEW_DIR = ROOT / "data" / "review"

sys.path.insert(0, str(ROOT))
from wodl.registry import EXERCISES


def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


# ---------------------------------------------------------------------------
# 1. Neue Aliase fuer bestehende Uebungen einsammeln
# ---------------------------------------------------------------------------


def read_csv_flex(path: Path) -> list[dict]:
    """Liest CSV mit Komma- oder Semikolon-Trennzeichen (Tabellenkalkulationen
    speichern je nach Locale mit ';')."""
    text = path.read_text(encoding="utf-8")
    delim = ";" if text.split("\n", 1)[0].count(";") > text.split("\n", 1)[0].count(",") else ","
    return list(csv.DictReader(text.splitlines(), delimiter=delim))


def collect_new_aliases() -> dict[str, list[str]]:
    additions: dict[str, list[str]] = {}

    def add(canonical: str, source_name: str):
        if canonical not in EXERCISES:
            print(f"  WARNUNG: kanonische Uebung {canonical!r} existiert nicht, ueberspringe {source_name!r}")
            return
        existing_norms = {normalize(canonical)} | {normalize(a) for a in EXERCISES[canonical]["aliases"]}
        already_added = {normalize(a) for a in additions.get(canonical, [])}
        if normalize(source_name) in existing_norms or normalize(source_name) in already_added:
            return
        additions.setdefault(canonical, []).append(source_name)

    auto_rows = read_csv_flex(REVIEW_DIR / "aliases_auto.csv")
    for row in auto_rows:
        add(row["canonical_name"], row["source_name"])

    decisions = read_csv_flex(REVIEW_DIR / "DECISIONS.csv")
    for row in decisions:
        if row.get("type") != "alias" or row.get("decision", "").strip().lower() != "accept":
            continue
        target = row.get("override_canonical", "").strip() or row["proposed_canonical"]
        add(target, row["source_name"])

    return additions


# ---------------------------------------------------------------------------
# 2. Neue kanonische Uebungen (kuratiert, Abschnitt 7)
#    Muskeln/Kategorie/Equipment aus free-exercise-db abgeleitet + manuell
#    nachbewertet, wo die Quelle laut Abschnitt 6 "MANUELL" verlangte.
# ---------------------------------------------------------------------------

NEW_EXERCISES: dict[str, dict] = {
    "Hang Clean": {
        "muscles": ["quads", "hamstrings", "glutes", "traps", "front_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Hang Power Clean", "Alternating Hang Clean", "Kettlebell Hang Clean",
            "KB Hang Clean", "Smith Machine Hang Power Clean",
            "Double Kettlebell Alternating Hang Clean", "BB Hang Clean",
            "LH Hang Clean", "Hangumsetzen",
        ],
    },
    "Arnold Press": {
        "muscles": ["front_delt", "side_delt", "triceps"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Arnold Dumbbell Press", "Kettlebell Arnold Press", "KB Arnold Press",
            "DB Arnold Press", "KH Arnold Press",
        ],
    },
    "Good Morning": {
        "muscles": ["hamstrings", "lower_back", "glutes"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Good Mornings", "Band Good Morning", "Seated Good Morning",
            "Seated Good Mornings", "Stiff Leg Barbell Good Morning",
            "BB Good Morning", "LH Good Morning",
        ],
    },
    "Walking Lunge": {
        "muscles": ["quads", "glutes", "hamstrings"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Walking Lunges", "Barbell Walking Lunge", "Bodyweight Walking Lunge",
            "BB Walking Lunge", "LH Walking Lunge", "Gehender Ausfallschritt",
        ],
    },
    "Glute-Ham Raise": {
        "muscles": ["hamstrings", "glutes", "calves"],
        "category": "compound",
        "equipment": "machine",
        "aliases": [
            "GHR", "GHD Raise", "Glute Ham Raise", "Floor Glute-Ham Raise",
            "Natural Glute Ham Raise",
        ],
    },
    "Pistol Squat": {
        "muscles": ["quads", "glutes", "hamstrings"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": [
            "Pistol Squats", "Single Leg Squat", "One Leg Squat",
            "Kettlebell Pistol Squat", "KB Pistol Squat",
            "Smith Machine Pistol Squat", "Pistolenkniebeuge", "Einbeinkniebeuge",
        ],
    },
    "Snatch": {
        "muscles": ["quads", "hamstrings", "glutes", "traps", "front_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Snatches", "One-Arm Kettlebell Snatch", "KB Snatch",
            "Reißen", "Reissen",
        ],
    },
    "Concentration Curl": {
        "muscles": ["biceps", "forearms"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Concentration Curls", "Standing Concentration Curl",
            "Seated Close-Grip Concentration Barbell Curl",
            "DB Concentration Curl", "KH Concentration Curl", "Konzentrationscurl",
        ],
    },
    "Renegade Row": {
        "muscles": ["back", "core", "triceps"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Renegade Rows", "Alternating Renegade Row", "Kettlebell Renegade Row",
            "KB Renegade Row", "DB Renegade Row", "KH Renegade Row",
        ],
    },
    "Ab Rollout": {
        # Bewusst nicht "Rollout"/"Ab Roller"/"Ab Wheel" als Alias - das ist
        # das bestehende "Ab Wheel Rollout" (anderes Geraet, keine Kollision,
        # aber Verwechslungsgefahr vermeiden).
        "muscles": ["core", "lower_back", "front_delt"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": [
            "Barbell Ab Rollout", "Barbell Ab Rollout - On Knees",
            "BB Ab Rollout", "LH Ab Rollout",
        ],
    },
    "Russian Twist": {
        "muscles": ["obliques", "core"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": [
            "Russian Twists", "Cable Russian Twists", "Weighted Russian Twist",
            "Russische Drehung",
        ],
    },
    "Farmer's Walk": {
        "muscles": ["forearms", "traps", "core"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Farmers Walk", "Farmer's Carry", "Farmers Carry",
            "Kettlebell Farmer's Walk", "KB Farmer's Walk",
            "DB Farmer's Walk", "KH Farmer's Walk",
        ],
    },
    "Windmill": {
        "muscles": ["obliques", "side_delt", "hamstrings"],
        "category": "compound",
        "equipment": "kettlebell",
        "aliases": ["Windmills", "Kettlebell Windmill", "KB Windmill", "Turkish Windmill"],
    },
    "Cable Pull Through": {
        "muscles": ["glutes", "hamstrings", "lower_back"],
        "category": "compound",
        "equipment": "cable",
        "aliases": ["Pull Through", "Pull-Through", "Cable Pull-Through", "Rope Pull Through"],
    },
    "Sissy Squat": {
        "muscles": ["quads"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": ["Sissy Squats", "Weighted Sissy Squat", "BB Sissy Squat", "LH Sissy Squat"],
    },
    "Zercher Squat": {
        "muscles": ["quads", "glutes", "core"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Zercher Squats", "BB Zercher Squat", "LH Zercher Squat"],
    },

    # --- Abschnitt-7-Nachtrag: hatten keinen Matcher-Kandidaten in
    # candidates_new.csv (kein oder kein eindeutiger Rohdaten-Treffer),
    # daher direkt in DECISIONS.csv als section7_manual_no_matcher_candidate
    # erfasst statt ueber den Matcher-Review-Weg.
    "Push Jerk": {
        # Kein exakter Rohdaten-Treffer; "Power Jerk"/"Split Jerk" sind
        # technisch andere Fusstechniken und daher bewusst NICHT als Alias
        # verlinkt.
        "muscles": ["quads", "front_delt", "triceps"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Push-Jerk"],
    },
    "Turkish Get-up": {
        "muscles": ["front_delt", "core", "quads", "hamstrings"],
        "category": "compound",
        "equipment": "kettlebell",
        "aliases": [
            "Kettlebell Turkish Get-Up (Lunge style)",
            "Kettlebell Turkish Get-Up (Squat style)",
            "TGU", "KB Turkish Get-up",
        ],
    },
    "Landmine Press": {
        # Kein Rohdaten-Treffer; "Landmine 180's"/"Landmine Linear Jammer"
        # in free-exercise-db sind andere (rotatorische) Uebungen.
        "muscles": ["front_delt", "triceps", "core"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Landmine Shoulder Press", "Single Arm Landmine Press",
            "BB Landmine Press", "LH Landmine Press",
        ],
    },
    "Reverse Hyper": {
        # War zuvor ein equipment_conflict-Alias-Kandidat auf "Back
        # Extension" (in DECISIONS.csv abgelehnt) - zurecht, es ist eine
        # eigene Uebung mit anderer Equipment- und Kraftkurve.
        "muscles": ["hamstrings", "glutes", "erectors"],
        "category": "compound",
        "equipment": "machine",
        "aliases": ["Reverse Hyperextension", "Reverse Hyperextensions"],
    },
    "Chest Supported Row": {
        # Kein Rohdaten-Treffer, komplett manuell kuratiert.
        "muscles": ["back", "rear_delt", "biceps"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Chest-Supported Row", "Incline Chest Supported Row",
            "Machine Chest Supported Row", "DB Chest Supported Row",
            "KH Chest Supported Row",
        ],
    },
    "Pendlay Row": {
        # Kein Rohdaten-Treffer, komplett manuell kuratiert.
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Pendlay Rows", "Dead Stop Row", "BB Pendlay Row", "LH Pendlay Row"],
    },
}


def accepted_new_exercise_names() -> set[str]:
    decisions = read_csv_flex(REVIEW_DIR / "DECISIONS.csv")
    names = set()
    for row in decisions:
        if row.get("type") == "new_exercise" and row.get("decision", "").strip().lower() == "accept":
            names.add(row["proposed_canonical"])
    return names


# ---------------------------------------------------------------------------
# 3. Textuelle Chirurgie an registry.py
# ---------------------------------------------------------------------------


def insert_aliases_into_source(src: str, canonical: str, new_aliases: list[str]) -> str:
    start_marker = f'"{canonical}": {{'
    start = src.index(start_marker)
    entry_end = src.index("\n    },", start)  # Ende DIESES Eintrags, zur Absicherung
    a_start = src.index('"aliases": [', start)
    if a_start > entry_end:
        raise ValueError(f'"aliases" nicht innerhalb des Eintrags {canonical!r} gefunden')
    # Die Aliase sind eine flache Liste aus Strings ohne verschachtelte
    # Klammern - die naechste ']' nach '"aliases": [' ist IMMER die
    # richtige schliessende Klammer, egal ob ein- oder mehrzeilig formatiert.
    close = src.index("]", a_start)
    if close > entry_end:
        raise ValueError(f'schliessende "]" nicht innerhalb des Eintrags {canonical!r} gefunden')

    j = close - 1
    while src[j] in " \n\t":
        j -= 1
    insert_pos = j + 1
    trailing_comma = src[j] == ","

    quoted = ", ".join(f'"{a}"' for a in new_aliases)
    insertion = f" {quoted}," if trailing_comma else f", {quoted}"
    return src[:insert_pos] + insertion + src[insert_pos:]


def format_entry(canonical: str, meta: dict) -> str:
    muscles = ", ".join(f'"{m}"' for m in meta["muscles"])
    aliases_lines = ",\n            ".join(
        ", ".join(f'"{a}"' for a in meta["aliases"][i : i + 3])
        for i in range(0, len(meta["aliases"]), 3)
    )
    return (
        f'    "{canonical}": {{\n'
        f'        "muscles": [{muscles}],\n'
        f'        "category": "{meta["category"]}",\n'
        f'        "equipment": "{meta["equipment"]}",\n'
        f'        "aliases": [\n'
        f"            {aliases_lines},\n"
        f"        ],\n"
        f"    }},\n"
    )


def append_new_entries(src: str, entries: dict[str, dict]) -> str:
    # Idempotenz: bereits vorhandene kanonische Namen ueberspringen, damit
    # ein erneuter Lauf (z.B. nach einem Abschnitt-7-Nachtrag) den Eintrag
    # nicht doppelt anhaengt.
    entries = {name: meta for name, meta in entries.items() if name not in EXERCISES}
    if not entries:
        return src
    header = (
        "\n    # ========================================================================\n"
        "    # IMPORT: free-exercise-db (Unlicense) - kuratierte Ergaenzungen fehlender\n"
        "    # Grunduebungen. Quelle: data/raw/free-exercise-db/exercises.json,\n"
        "    # siehe data/raw/PROVENANCE.md. Entscheidungen: data/review/DECISIONS.csv.\n"
        "    # ========================================================================\n\n"
    )
    body = "".join(format_entry(name, meta) for name, meta in entries.items())
    marker = "\n}\n"
    idx = src.rindex(marker)
    return src[:idx] + header + body + src[idx:]


def main():
    print("Sammle neue Aliase fuer bestehende Uebungen ...")
    alias_additions = collect_new_aliases()
    total_new_aliases = sum(len(v) for v in alias_additions.values())
    print(f"  {total_new_aliases} neue Aliase auf {len(alias_additions)} bestehende Uebungen")

    print("Sammle akzeptierte neue Uebungen ...")
    accepted = accepted_new_exercise_names()
    new_entries = {k: v for k, v in NEW_EXERCISES.items() if k in accepted}
    skipped = accepted - set(new_entries)
    if skipped:
        print(f"  WARNUNG: akzeptiert in DECISIONS.csv, aber nicht in NEW_EXERCISES hinterlegt: {skipped}")
    print(f"  {len(new_entries)} neue kanonische Uebungen: {sorted(new_entries)}")

    src = REGISTRY_PATH.read_text(encoding="utf-8")

    for canonical, aliases in alias_additions.items():
        src = insert_aliases_into_source(src, canonical, aliases)

    src = append_new_entries(src, new_entries)

    REGISTRY_PATH.write_text(src, encoding="utf-8")
    print(f"\n{REGISTRY_PATH} geschrieben.")


if __name__ == "__main__":
    main()
