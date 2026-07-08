"""Tests for the WODL parser and exercise registry."""

import glob
from pathlib import Path

from wodl import parse, to_json, to_markdown, resolve, resolve_fuzzy
from wodl import list_exercises, get_muscles, ExerciseLine, ExerciseGroup

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_FILES = sorted(
    glob.glob(str(REPO_ROOT / "catalog" / "*.wodl"))
    + glob.glob(str(REPO_ROOT / "examples" / "*.wodl"))
)


def _distinct_exercises(plan):
    names = set()
    for session in plan.sessions:
        for item in session.items:
            if isinstance(item, ExerciseGroup):
                names.update(e.raw_name for e in item.exercises)
            else:
                names.add(item.raw_name)
    return names


# ===================================================================
# Exercise Registry
# ===================================================================


class TestExerciseRegistry:
    def test_resolve_canonical(self):
        assert resolve("Bench Press") == "Bench Press"
        assert resolve("Squat") == "Squat"
        assert resolve("OHP") == "OHP"

    def test_resolve_german_alias(self):
        assert resolve("Bankdrücken") == "Bench Press"
        assert resolve("Kniebeugen") == "Squat"
        assert resolve("Kreuzheben") == "Deadlift"
        assert resolve("Klimmzüge") == "Pull-up"
        assert resolve("Seitheben") == "Lateral Raise"
        assert resolve("Liegestütz") == "Push-up"

    def test_resolve_abbreviation(self):
        assert resolve("KH Rudern") == "Dumbbell Row"
        assert resolve("LH Rudern") == "Barbell Row"
        assert resolve("BB Bench") == "Bench Press"
        assert resolve("DB Bench") == "Dumbbell Bench Press"

    def test_resolve_case_insensitive(self):
        assert resolve("bench press") == "Bench Press"
        assert resolve("SQUAT") == "Squat"

    def test_resolve_unknown(self):
        assert resolve("Unicorn Fly") is None

    def test_resolve_fuzzy(self):
        assert resolve_fuzzy("Benchpress") == "Bench Press"

    def test_get_muscles(self):
        muscles = get_muscles("Bench Press")
        assert "chest" in muscles
        assert "triceps" in muscles

    def test_list_exercises(self):
        all_ex = list_exercises()
        assert len(all_ex) > 30
        assert "Squat" in all_ex

    def test_list_by_category(self):
        compounds = list_exercises("compound")
        assert "Bench Press" in compounds
        assert "Lateral Raise" not in compounds


# ===================================================================
# Parser — metadata
# ===================================================================


class TestMetadata:
    def test_plan_name(self):
        plan = parse('@plan "Push Pull Legs"')
        assert plan.name == "Push Pull Legs"

    def test_frequency(self):
        plan = parse("@freq 4x/week")
        assert plan.frequency == "4x/week"

    def test_unit(self):
        plan = parse("@unit lb")
        assert plan.unit == "lb"

    def test_cycle(self):
        plan = parse("@cycle 4w: w1-3 progress, w4 deload")
        assert plan.cycle_length == "4w"
        assert len(plan.cycle_phases) == 2
        assert plan.cycle_phases[0].phase == "progress"
        assert plan.cycle_phases[1].phase == "deload"


# ===================================================================
# Parser — sessions
# ===================================================================


class TestSessions:
    def test_session_with_days(self):
        plan = parse("---[Push] Mo Do")
        assert plan.sessions[0].name == "Push"
        assert plan.sessions[0].days == ["Mo", "Do"]

    def test_german_days(self):
        plan = parse("---[Test] Montag Mittwoch Freitag")
        assert plan.sessions[0].days == ["Mo", "Mi", "Fr"]

    def test_multiple_sessions(self):
        plan = parse("---[A] Mo\n---[B] Di\n---[C] Mi")
        assert len(plan.sessions) == 3


# ===================================================================
# Parser — exercises
# ===================================================================


class TestExercises:
    def test_basic(self):
        plan = parse("---[T]\nBench Press  4x8")
        ex = plan.sessions[0].items[0]
        assert ex.canonical_name == "Bench Press"
        assert ex.sets == 4
        assert ex.reps == "8"

    def test_rep_range(self):
        plan = parse("---[T]\nSquat  3x8-12")
        assert plan.sessions[0].items[0].reps == "8-12"

    def test_intensity_rpe(self):
        plan = parse("---[T]\nBench Press  4x8  @RPE8")
        assert plan.sessions[0].items[0].intensity == "@RPE8"

    def test_intensity_percent(self):
        plan = parse("---[T]\nSquat  5x5  @85%")
        assert plan.sessions[0].items[0].intensity == "@85%"

    def test_intensity_absolute(self):
        plan = parse("---[T]\nBench Press  3x3  @100kg")
        assert plan.sessions[0].items[0].intensity == "@100kg"

    def test_intensity_bodyweight(self):
        plan = parse("---[T]\nPull-up  4x8  @BW+10kg")
        assert plan.sessions[0].items[0].intensity == "@BW+10kg"

    def test_rest(self):
        plan = parse("---[T]\nBench Press  4x8  r120s")
        assert plan.sessions[0].items[0].rest == "120s"

    def test_tempo(self):
        plan = parse("---[T]\nSquat  4x8  t3010")
        assert plan.sessions[0].items[0].tempo == "3010"

    def test_progression(self):
        plan = parse("---[T]\nSquat  4x6  +2.5kg/w")
        assert plan.sessions[0].items[0].progression == "+2.5kg/w"

    def test_modifier(self):
        plan = parse("---[T]\nLateral Raise  3x12  drop")
        assert "drop" in plan.sessions[0].items[0].modifiers

    def test_all_params(self):
        plan = parse("---[T]\nSquat  4x6  @RPE8  r180s  t3010  +2.5kg/w")
        ex = plan.sessions[0].items[0]
        assert ex.sets == 4
        assert ex.reps == "6"
        assert ex.intensity == "@RPE8"
        assert ex.rest == "180s"
        assert ex.tempo == "3010"
        assert ex.progression == "+2.5kg/w"

    def test_time_based(self):
        plan = parse("---[T]\nPlank  3x30s")
        ex = plan.sessions[0].items[0]
        assert ex.sets == 3
        assert ex.reps == "30s"

    def test_inline_comment(self):
        plan = parse("---[T]\nBench Press  4x8  # go deep")
        assert plan.sessions[0].items[0].comment == "go deep"

    def test_german_alias(self):
        plan = parse("---[T]\nBankdrücken  4x8\nKniebeugen  5x5")
        assert plan.sessions[0].items[0].canonical_name == "Bench Press"
        assert plan.sessions[0].items[1].canonical_name == "Squat"


# ===================================================================
# Parser — groups
# ===================================================================


class TestGroups:
    def test_superset(self):
        plan = parse("---[T]\nss {\n  Lateral Raise  3x15\n  Face Pull  3x15\n}")
        group = plan.sessions[0].items[0]
        assert isinstance(group, ExerciseGroup)
        assert group.kind == "superset"
        assert len(group.exercises) == 2

    def test_circuit(self):
        plan = parse("---[T]\ncircuit {\n  Push-up  x20\n  Plank  60s\n}")
        assert plan.sessions[0].items[0].kind == "circuit"

    def test_giant(self):
        plan = parse("---[T]\ngiant {\n  OHP  3x10\n  Lateral Raise  3x15\n  Face Pull  3x15\n  Shrug  3x12\n}")
        group = plan.sessions[0].items[0]
        assert group.kind == "giant"
        assert len(group.exercises) == 4

    def test_mixed(self):
        wod = "---[T]\nBench Press  4x8\nss {\n  A  3x12\n  B  3x12\n}\nLateral Raise  4x15"
        plan = parse(wod)
        items = plan.sessions[0].items
        assert isinstance(items[0], ExerciseLine)
        assert isinstance(items[1], ExerciseGroup)
        assert isinstance(items[2], ExerciseLine)


# ===================================================================
# Notes and warnings
# ===================================================================


class TestNotesWarnings:
    def test_notes(self):
        plan = parse("---[T]\nBench Press  4x8\n> Warm up first")
        assert "Warm up first" in plan.sessions[0].notes[0]

    def test_unknown_exercise_warning(self):
        plan = parse("---[T]\nUnicorn Press  4x8")
        assert len(plan.warnings) == 1
        assert "Unicorn Press" in plan.warnings[0]


# ===================================================================
# Regressions — Name-Tokenizer (drop-Modifier, Ziffern im Namen)
# ===================================================================


class TestNameTokenizerRegressions:
    """'drop' & Co. duerfen nur NACH dem Sets/Reps-Block Modifier sein."""

    def test_unknown_name_ending_in_drop_stays_intact(self):
        plan = parse("---[T]\nSeated Eccentric Heel Drop  3x15")
        ex = plan.sessions[0].items[0]
        assert ex.raw_name == "Seated Eccentric Heel Drop"
        assert ex.modifiers == []
        assert ex.canonical_name is None  # ehrliche Warning statt Verstuemmelung
        assert len(plan.warnings) == 1

    def test_known_name_ending_in_drop_resolves_exactly(self):
        plan = parse("---[T]\nEccentric Heel Drop  3x15  @BW+10kg  r60s")
        ex = plan.sessions[0].items[0]
        assert ex.raw_name == "Eccentric Heel Drop"
        assert ex.canonical_name == "Eccentric Heel Drop"
        assert ex.modifiers == []

    def test_drop_modifier_after_sets_reps_still_works(self):
        plan = parse("---[T]\nLateral Raise  3x12  r60s  drop")
        ex = plan.sessions[0].items[0]
        assert ex.modifiers == ["drop"]
        assert ex.raw_name == "Lateral Raise"

    def test_alias_containing_modifier_word(self):
        # "Drop Jump" ist ein Alias von Depth Jump — kein drop-Modifier
        plan = parse("---[T]\nDrop Jump  3x5  r120s")
        ex = plan.sessions[0].items[0]
        assert ex.canonical_name == "Depth Jump"
        assert ex.modifiers == []

    def test_digit_in_name_before_sets_reps(self):
        plan = parse("---[T]\nAbduction to 90  3x10")
        ex = plan.sessions[0].items[0]
        assert ex.raw_name == "Abduction to 90"
        assert ex.sets == 3
        assert ex.reps == "10"

    def test_figure_8_walk_keeps_digit_and_resolves(self):
        plan = parse("---[T]\nFigure 8 Walk  3x30s")
        ex = plan.sessions[0].items[0]
        assert ex.raw_name == "Figure 8 Walk"
        assert ex.canonical_name == "Figure-Eight Walk"
        assert ex.sets == 3
        assert ex.reps == "30s"

    def test_bare_number_reps_still_parse(self):
        # Ohne expliziten Sets/Reps-Block bleibt eine nachgestellte Zahl Reps
        plan = parse("---[T]\nSit-up  15")
        ex = plan.sessions[0].items[0]
        assert ex.raw_name == "Sit-up"
        assert ex.sets == 1
        assert ex.reps == "15"

    def test_bare_number_reps_followed_by_params(self):
        plan = parse("---[T]\nSit-up  20  @BW  r60s")
        ex = plan.sessions[0].items[0]
        assert ex.raw_name == "Sit-up"
        assert ex.reps == "20"
        assert ex.intensity == "@BW"
        assert ex.rest == "60s"


# ===================================================================
# Regressions — Fuzzy-Matching (Schwelle & Wort-Guards)
# ===================================================================


class TestFuzzyRegressions:
    """Fuzzy ist ein Tippfehler-Korrektor, kein Synonym-Finder."""

    def test_no_match_across_first_word(self):
        # 1 Buchstabe Unterschied, aber anderes Wort = andere Uebung
        assert resolve_fuzzy("Xand External Rotation") is None

    def test_wand_external_rotation_is_own_exercise(self):
        assert resolve("Wand External Rotation") == "Wand External Rotation"
        assert resolve_fuzzy("Wand External Rotation") != "Band External Rotation"

    def test_no_match_to_longer_qualified_name(self):
        # Kuerzerer Name darf nicht auf laengeren qualifizierten Namen matchen
        assert resolve_fuzzy("Nordic Curl Hold") is None

    def test_d2_extension_not_leg_extension(self):
        assert resolve_fuzzy("D2 Extension") == "PNF D2 Extension"

    def test_knee_extension_not_terminal(self):
        assert resolve_fuzzy("Knee Extension") == "Leg Extension"

    def test_typos_still_corrected(self):
        assert resolve_fuzzy("Squatt") == "Squat"
        assert resolve_fuzzy("Benchpress") == "Bench Press"
        assert resolve_fuzzy("Klimmzuge") == "Pull-up"
        assert resolve_fuzzy("Face Puls") == "Face Pull"


# ===================================================================
# Registry-Ausbau & Integritaet
# ===================================================================


class TestRegistryExpansion:
    def test_catalog_staples_resolve(self):
        assert resolve("Nordic Hamstring Curl") == "Nordic Hamstring Curl"
        assert resolve("Copenhagen Adduction") == "Copenhagen Adduction"
        assert resolve("Extender") == "Extender"
        assert resolve("Diver") == "Diver"
        assert resolve("Glider") == "Glider"
        assert resolve("Wobble Board") == "Wobble Board Balance"
        assert resolve("Lateral Band Walk") == "Lateral Band Walk"
        assert resolve("Power Clean") == "Power Clean"

    def test_german_aliases_resolve(self):
        assert resolve("Umsetzen") == "Power Clean"
        assert resolve("Wackelbrett") == "Wobble Board Balance"
        assert resolve("Kopenhagen-Adduktion") == "Copenhagen Adduction"
        assert resolve("Kniestreckung mit Band") == "Band Knee Extension"

    def test_no_duplicate_aliases(self):
        # Doppelte Aliases wuerden sich still gegenseitig ueberschreiben
        from wodl.registry import EXERCISES

        seen: dict[str, str] = {}
        for canonical, meta in EXERCISES.items():
            for key in [canonical, *meta.get("aliases", [])]:
                key = key.lower().strip()
                assert key not in seen or seen[key] == canonical, (
                    f"Alias '{key}' zeigt auf '{seen[key]}' UND '{canonical}'"
                )
                seen[key] = canonical

    def test_fifa_and_reha_exercises_resolve(self):
        # Ehemalige Unknowns aus den Praeventions-/Reha-Protokollen
        for name in [
            "Running Straight Ahead", "Plant and Cut",
            "Jumping with Shoulder Contact", "Isometric Neck Flexion",
            "Wrist Extensor Stretch", "External Rotation at Shoulder Level",
            "Folding Knife Sit-up", "Table Slide", "Walking",
            "Box Landing Drill",
        ]:
            assert resolve(name) == name, f"{name!r} loest nicht exakt auf"


# ===================================================================
# Katalog-Integritaet — kein File mit Unknowns oder nur einer Uebung
# ===================================================================


class TestCatalogIntegrity:
    def test_catalog_files_present(self):
        assert len(CATALOG_FILES) == 37

    def test_no_unknown_exercises_in_catalog(self):
        offenders = {}
        for path in CATALOG_FILES:
            plan = parse(Path(path).read_text(encoding="utf-8"))
            if plan.warnings:
                offenders[Path(path).name] = plan.warnings
        assert not offenders, f"Unknown-Uebungen im Katalog: {offenders}"

    def test_no_single_exercise_plans(self):
        # Ein-Uebungs-Plaene sind albern (Pat 2026-07-08) — jeder Plan
        # muss mindestens zwei verschiedene Uebungen haben.
        offenders = {}
        for path in CATALOG_FILES:
            plan = parse(Path(path).read_text(encoding="utf-8"))
            distinct = _distinct_exercises(plan)
            if len(distinct) <= 1:
                offenders[Path(path).name] = distinct
        assert not offenders, f"Ein-Uebungs-Plaene: {offenders}"


# ===================================================================
# Serialization
# ===================================================================


class TestSerialization:
    SAMPLE = '@plan "PPL"\n---[Push] Mo\nBench Press  4x8  @RPE8'

    def test_json(self):
        plan = parse(self.SAMPLE)
        j = to_json(plan)
        assert '"PPL"' in j
        assert '"Bench Press"' in j

    def test_markdown(self):
        plan = parse(self.SAMPLE)
        md = to_markdown(plan)
        assert "# PPL" in md
        assert "## Push" in md
        assert "Bench Press" in md


# ===================================================================
# Full integration
# ===================================================================


class TestFullPlan:
    def test_complete_ppl(self):
        wod = """\
@plan "Push Pull Legs"
@freq 6x/week
@cycle 4w: w1-3 progress, w4 deload

---[Push] Mo Do

Bench Press          4x8  @RPE8  r120s
OHP                  3x10 @70%   r90s
ss {
  Incline DB Fly     3x12
  Tricep Pushdown    3x12
}
Lateral Raise        4x15 r60s

---[Pull] Di Fr

Deadlift             3x5  @RPE9  r180s
Barbell Row          4x8  @RPE8  r120s
ss {
  Lat Pulldown       3x10
  Face Pull          3x15
}
Hammer Curl          3x12 r60s

---[Legs] Mi Sa

Squat                4x6  @RPE8  r180s  +2.5kg/w
RDL                  3x10 @RPE7  r120s
ss {
  Leg Press          3x12
  Leg Curl           3x12
}
Calf Raise           4x15 r60s
"""
        plan = parse(wod)
        assert plan.name == "Push Pull Legs"
        assert len(plan.sessions) == 3
        assert len(plan.warnings) == 0

        # All exercises resolved
        for session in plan.sessions:
            for item in session.items:
                if isinstance(item, ExerciseLine):
                    assert item.canonical_name is not None, f"Unresolved: {item.raw_name}"
                elif isinstance(item, ExerciseGroup):
                    for ex in item.exercises:
                        assert ex.canonical_name is not None, f"Unresolved: {ex.raw_name}"
