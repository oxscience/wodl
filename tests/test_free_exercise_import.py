"""Tests fuer den free-exercise-db Import (data/review/*, tools/*).

Deckt Abschnitt 8 des Imports ab:
  - Testfaelle aus Abschnitt 5 landen im erwarteten Bucket
  - neue Aliase loesen ueber resolve() korrekt auf
  - Regression: alle bestehenden Aliase loesen unveraendert auf
  - kein Alias zeigt auf zwei verschiedene kanonische Namen
  - resolve_fuzzy() wird durch die neuen Aliase nicht schlechter
  - alle muscles/category/equipment-Werte liegen im erlaubten Vokabular
"""

import ast
import csv
import subprocess
import sys
from pathlib import Path
from typing import ClassVar

import pytest

from wodl import EXERCISES, resolve, resolve_fuzzy

REPO_ROOT = Path(__file__).resolve().parent.parent
REVIEW_DIR = REPO_ROOT / "data" / "review"

# Commit unmittelbar VOR dem free-exercise-db-Import (189 Uebungen, 584
# Aliase). Bewusst eine feste SHA statt "HEAD": HEAD zeigt nach dem Commit
# des Imports selbst auf den NEUEN Stand, ein Vergleich dagegen waere
# wirkungslos.
PRE_IMPORT_COMMIT = "682eb75f3eb3513e90b3812c6de77d6f25e15f39"

sys.path.insert(0, str(REPO_ROOT))
from tools.match_exercises import match_one


def _read_csv_flex(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    first_line = text.split("\n", 1)[0]
    delim = ";" if first_line.count(";") > first_line.count(",") else ","
    return list(csv.DictReader(text.splitlines(), delimiter=delim))


@pytest.fixture(scope="module")
def orig_exercises():
    """EXERCISES-Stand vor dem Import (PRE_IMPORT_COMMIT) - fuer die
    Regressionspruefung. ast.literal_eval statt exec(): das EXERCISES-Dict
    besteht nur aus Literalen (Strings/Listen/Dicts), Codeausfuehrung ist
    dafuer nie noetig."""
    try:
        # Fixed argument list with a hardcoded SHA; no external input.
        orig_src = subprocess.check_output(  # noqa: S603, S607
            ["git", "show", f"{PRE_IMPORT_COMMIT}:wodl/registry.py"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
        ).decode()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip(
            f"Commit {PRE_IMPORT_COMMIT} nicht verfuegbar "
            "(flacher Clone? fetch-depth: 0 setzen)."
        )
    tree = ast.parse(orig_src, filename="orig_registry.py")
    for node in ast.walk(tree):
        # registry.py deklariert "EXERCISES: dict[str, dict] = {...}" -
        # das ist ein AnnAssign (annotierte Zuweisung), kein Assign.
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "EXERCISES" for t in node.targets
        ):
            return ast.literal_eval(node.value)
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == "EXERCISES"
            and node.value is not None
        ):
            return ast.literal_eval(node.value)
    raise RuntimeError(f"EXERCISES nicht gefunden in wodl/registry.py @ {PRE_IMPORT_COMMIT}")


# ===================================================================
# Abschnitt 5: die 7 dokumentierten Fehlzuordnungen
# ===================================================================


class TestKnownPitfalls:
    """Diese sieben Beispiele sind vorab bekannte Fehlzuordnungen (Abschnitt 5
    des Imports) und dienen als Regressionsanker fuer die beiden Waechter."""

    def test_antonym_guard_catches_decline_incline(self):
        r1 = match_one("Decline Dumbbell Flyes")
        assert r1.discarded_reason == "antonym"
        r2 = match_one("Decline Dumbbell Bench Press")
        assert r2.discarded_reason == "antonym"

    @pytest.mark.parametrize(
        "source_name,wrong_canonical",
        [
            ("Pin Presses", "Leg Press"),
            ("Split Squats", "Bulgarian Split Squat"),
            ("Reverse Hyperextension", "Back Extension"),
            ("Barbell Shoulder Press", "Dumbbell OHP"),
            ("Car Deadlift", "Deadlift"),
        ],
    )
    def test_flagged_matches_never_silently_auto_accepted(self, source_name, wrong_canonical):
        """Diese Treffer sind matcher-seitig plausibel, aber falsch bzw.
        strittig - sie duerfen nicht in aliases_auto.csv gelandet sein."""
        auto_rows = _read_csv_flex(REVIEW_DIR / "aliases_auto.csv")
        auto_sources = {row["source_name"] for row in auto_rows}
        assert source_name not in auto_sources
        assert resolve(source_name) != wrong_canonical

    @pytest.mark.parametrize(
        "source_name",
        [
            "Pullups", "Pushups", "Leg Extensions", "Standing Calf Raises",
            "Seated Cable Rows", "Triceps Pushdown", "Lying Leg Curls",
        ],
    )
    def test_clean_plural_variants_are_auto_accepted(self, source_name):
        auto_rows = _read_csv_flex(REVIEW_DIR / "aliases_auto.csv")
        auto_sources = {row["source_name"] for row in auto_rows}
        assert source_name in auto_sources


# ===================================================================
# Alias-Kollisionen und Vokabular
# ===================================================================


class TestRegistryConsistency:
    VALID_CATEGORIES: ClassVar[set[str]] = {
        "cardio", "compound", "isolation", "isometric", "mobility", "plyometric", "rehab",
    }
    VALID_EQUIPMENT: ClassVar[set[str]] = {
        "band", "barbell", "bodyweight", "box", "cable", "dumbbell", "kettlebell", "machine", "other",
    }

    def test_no_alias_maps_to_two_canonicals(self):
        seen: dict[str, str] = {}
        for canonical, meta in EXERCISES.items():
            names = [canonical.lower()] + [a.lower() for a in meta["aliases"]]
            for name in names:
                if name in seen and seen[name] != canonical:
                    pytest.fail(f"Alias {name!r} zeigt auf {seen[name]!r} UND {canonical!r}")
                seen[name] = canonical

    def test_all_categories_in_vocabulary(self):
        bad = {c: m["category"] for c, m in EXERCISES.items() if m["category"] not in self.VALID_CATEGORIES}
        assert not bad, f"ungueltige category-Werte: {bad}"

    def test_all_equipment_in_vocabulary(self):
        bad = {c: m["equipment"] for c, m in EXERCISES.items() if m["equipment"] not in self.VALID_EQUIPMENT}
        assert not bad, f"ungueltige equipment-Werte: {bad}"

    def test_all_muscles_in_original_vocabulary(self, orig_exercises):
        """Neue Eintraege duerfen nur bestehende Muskel-Tokens verwenden,
        kein neues Vokabular einfuehren."""
        orig_muscles = {m for meta in orig_exercises.values() for m in meta["muscles"]}
        new_muscles = {m for meta in EXERCISES.values() for m in meta["muscles"]}
        assert new_muscles <= orig_muscles, f"neue, nicht abgesprochene Muskel-Tokens: {new_muscles - orig_muscles}"


# ===================================================================
# Regression: bestehende 189 Uebungen / 584 Aliase unveraendert
# ===================================================================


class TestRegressionExisting:
    def test_all_original_canonicals_still_resolve(self, orig_exercises):
        for canonical in orig_exercises:
            assert resolve(canonical) == canonical

    def test_all_original_aliases_still_resolve(self, orig_exercises):
        for canonical, meta in orig_exercises.items():
            for alias in meta["aliases"]:
                assert resolve(alias) == canonical, f"{alias!r} loeste vorher auf {canonical!r} auf"

    def test_original_exercise_count_unchanged_within_import(self, orig_exercises):
        assert len(orig_exercises) == 189

    @pytest.mark.parametrize(
        "typo,expected",
        [
            ("Squatt", "Squat"),
            ("Benchpress", "Bench Press"),
            ("Klimmzuge", "Pull-up"),
            ("Face Puls", "Face Pull"),
        ],
    )
    def test_existing_fuzzy_cases_still_pass(self, typo, expected):
        """resolve_fuzzy() darf durch die neuen Aliase nicht schlechter werden."""
        assert resolve_fuzzy(typo) == expected

    def test_wand_external_rotation_guard_still_holds(self):
        assert resolve_fuzzy("Xand External Rotation") is None
        assert resolve_fuzzy("Wand External Rotation") != "Band External Rotation"


# ===================================================================
# Neue Aliase (aliases_auto.csv + akzeptierte DECISIONS.csv-Zeilen)
# ===================================================================


class TestNewAliasesResolve:
    def test_auto_aliases_resolve_to_expected_canonical(self):
        rows = _read_csv_flex(REVIEW_DIR / "aliases_auto.csv")
        assert rows, "aliases_auto.csv ist leer - Matcher-Lauf pruefen"
        for row in rows:
            assert resolve(row["source_name"]) == row["canonical_name"], (
                f"{row['source_name']!r} sollte auf {row['canonical_name']!r} zeigen"
            )

    def test_accepted_decision_aliases_resolve_to_expected_canonical(self):
        decisions_path = REVIEW_DIR / "DECISIONS.csv"
        if not decisions_path.exists():
            pytest.skip("DECISIONS.csv noch nicht befuellt")
        rows = _read_csv_flex(decisions_path)
        accepted = [r for r in rows if r.get("type") == "alias" and r.get("decision", "").strip().lower() == "accept"]
        assert accepted, "keine akzeptierten Alias-Entscheidungen gefunden"
        for row in accepted:
            target = row.get("override_canonical", "").strip() or row["proposed_canonical"]
            assert resolve(row["source_name"]) == target


# ===================================================================
# Neue kanonische Uebungen (Abschnitt 7)
# ===================================================================


class TestNewCanonicalExercises:
    NEW_CANONICALS: ClassVar[list[str]] = [
        "Hang Clean", "Arnold Press", "Good Morning", "Walking Lunge",
        "Glute-Ham Raise", "Pistol Squat", "Snatch", "Concentration Curl",
        "Renegade Row", "Ab Rollout", "Russian Twist", "Farmer's Walk",
        "Windmill", "Cable Pull Through", "Sissy Squat", "Zercher Squat",
        "Push Jerk", "Turkish Get-up", "Landmine Press", "Reverse Hyper",
        "Chest Supported Row", "Pendlay Row",
    ]

    def test_new_canonicals_present(self):
        for name in self.NEW_CANONICALS:
            assert name in EXERCISES, f"{name!r} fehlt in der Registry"

    def test_new_canonicals_resolve_to_themselves(self):
        for name in self.NEW_CANONICALS:
            assert resolve(name) == name

    def test_new_canonicals_aliases_resolve(self):
        for name in self.NEW_CANONICALS:
            for alias in EXERCISES[name]["aliases"]:
                assert resolve(alias) == name, f"{alias!r} sollte auf {name!r} zeigen"

    def test_ab_rollout_does_not_collide_with_ab_wheel_rollout(self):
        """'Ab Rollout' (Langhantel, neu) und 'Ab Wheel Rollout' (Geraet,
        bestehend) sind unterschiedliche Uebungen - beide muessen getrennt
        aufloesen."""
        assert resolve("Ab Rollout") == "Ab Rollout"
        assert resolve("Rollout") == "Ab Wheel Rollout"

    def test_nordic_hamstring_is_alias_not_new_exercise(self):
        """Laut Auftrag (Abschnitt 7) nur als Alias auf die bestehende
        'Nordic Hamstring Curl' - keine eigene kanonische Uebung."""
        assert resolve("Nordic Hamstring") == "Nordic Hamstring Curl"
        assert "Nordic Hamstring" not in EXERCISES

    def test_kettlebell_equipment_used(self):
        assert EXERCISES["Windmill"]["equipment"] == "kettlebell"
