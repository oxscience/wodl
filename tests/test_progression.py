"""Tests für wodl/progression.py — semantischer Pfad, Freitext-Pfad, Weiche."""

import pytest

from wodl.parser import parse
from wodl.progression import (
    ProgressionConfig,
    block_as_text,
    looks_like_wodl,
    progress_auto,
    progress_plan,
    progress_text,
    transform_line,
    week_kinds,
)

WODL_HYP = """\
@plan "Test Hypertrophie"
@freq 2x/week

---[Ganzkörper] Mo Do

Bench Press          3x8-12  @40kg  r120s
Squat                4x10    @60kg
Lateral Raise        3x15    @RPE8
Plank                3x30s
"""

WODL_STRENGTH = """\
@plan "Test Kraft"

---[A] Mo

Deadlift             3x5  @100kg  r180s
OHP                  4x6  @RPE8
"""

FREETEXT = """\
Aufwärmen: 5min Rudern
Kniebeugen 3x10 20kg
Liegestütze 12x
Plank 45sek
Rudern 10 Wdh
"""


# ---------------------------------------------------------------------------
# Wochen-Schema
# ---------------------------------------------------------------------------


def test_week_kinds_default_last_deload():
    cfg = ProgressionConfig(weeks=4)
    assert week_kinds(cfg) == ["start", "build", "build", "deload"]


def test_week_kinds_none():
    cfg = ProgressionConfig(weeks=4, deload_rhythm="none")
    assert week_kinds(cfg) == ["start", "build", "build", "build"]


def test_week_kinds_every4_in_8_weeks():
    cfg = ProgressionConfig(weeks=8, deload_rhythm="every4")
    kinds = week_kinds(cfg)
    assert kinds[3] == "deload" and kinds[7] == "deload"
    assert kinds.count("deload") == 2


def test_week_kinds_auto_short_block_has_no_deload():
    cfg = ProgressionConfig(weeks=3)
    assert "deload" not in week_kinds(cfg)


def test_week_kinds_auto_respects_plan_cycle():
    plan = parse('@plan "X"\n@cycle 4w: w1-3 progress, w4 deload\n\n---[A] Mo\n\nSquat 3x5 @60kg\n')
    cfg = ProgressionConfig(weeks=4)
    assert week_kinds(cfg, plan) == ["start", "build", "build", "deload"]


# ---------------------------------------------------------------------------
# Semantischer Pfad: Doppelprogression (Hypertrophie)
# ---------------------------------------------------------------------------


def test_double_progression_within_range():
    plan = parse(WODL_HYP)
    cfg = ProgressionConfig(weeks=3, deload_rhythm="none", rep_increment=2)
    weeks = progress_plan(plan, cfg)
    # Woche 1 = Range-Boden, dann +2 pro Woche
    assert "3x8" in weeks[0].text
    assert "3x10" in weeks[1].text
    assert "3x12" in weeks[2].text
    # Last bleibt bis zur Schwelle stabil
    assert "@40kg" in weeks[2].text


def test_double_progression_bump_resets_reps_and_raises_load():
    plan = parse(WODL_HYP)
    # 8-12: Woche 4 würde 14 → Schwelle 12 überschritten → Bump
    cfg = ProgressionConfig(weeks=4, deload_rhythm="none", rep_increment=2)
    weeks = progress_plan(plan, cfg)
    assert "3x8" in weeks[3].text          # Reps zurück auf Range-Boden
    assert "@42.5kg" in weeks[3].text      # Last +2.5
    assert "zurück auf 8" in weeks[3].text  # Kommentar erklärt den Wechsel


def test_double_progression_fixed_reps_threshold_15():
    plan = parse('---[A] Mo\n\nSquat 3x14 @60kg\n')
    cfg = ProgressionConfig(weeks=3, deload_rhythm="none", rep_increment=1)
    weeks = progress_plan(plan, cfg)
    assert "3x15" in weeks[1].text         # 14 → 15 (Schwelle)
    assert "3x14" in weeks[2].text and "@62.5kg" in weeks[2].text  # Bump


def test_double_progression_custom_threshold_overrides_range_top():
    plan = parse('---[A] Mo\n\nCurl 3x8-12 @10kg\n')
    cfg = ProgressionConfig(weeks=4, deload_rhythm="none", rep_increment=2, rep_threshold=15)
    weeks = progress_plan(plan, cfg)
    # Schwelle 15 statt Range-Top 12: Woche 4 = 14, noch kein Bump
    assert "3x14" in weeks[3].text
    assert "@10kg" in weeks[3].text


def test_double_progression_without_kg_emits_instruction():
    plan = parse('---[A] Mo\n\nLateral Raise 3x12-15 @RPE8\n')
    cfg = ProgressionConfig(weeks=3, deload_rhythm="none", rep_increment=2)
    weeks = progress_plan(plan, cfg)
    # Woche 3: 12→14→16 > 15 → Anweisung statt Zahl
    assert "Last erhöhen" in weeks[2].text
    assert "3x12" in weeks[2].text


# ---------------------------------------------------------------------------
# Semantischer Pfad: Kraft & Ausdauer
# ---------------------------------------------------------------------------


def test_strength_progresses_load_keeps_reps():
    plan = parse(WODL_STRENGTH)
    cfg = ProgressionConfig(weeks=3, goal="kraft", deload_rhythm="none")
    weeks = progress_plan(plan, cfg)
    assert "3x5" in weeks[2].text and "@105kg" in weeks[2].text
    # RPE-Übung: Reps fix, Anweisung als Kommentar
    assert "4x6" in weeks[2].text
    assert "Last +2.5 kg" in weeks[2].text


def test_endurance_reps_rise_load_stays():
    plan = parse('---[A] Mo\n\nCalf Raise 3x15 @20kg\n')
    cfg = ProgressionConfig(weeks=3, goal="ausdauer", deload_rhythm="none", rep_increment=2)
    weeks = progress_plan(plan, cfg)
    assert "3x19" in weeks[2].text and "@20kg" in weeks[2].text


def test_time_based_progression():
    plan = parse(WODL_HYP)
    cfg = ProgressionConfig(weeks=3, deload_rhythm="none", time_increment=10)
    weeks = progress_plan(plan, cfg)
    assert "3x30s" in weeks[0].text
    assert "3x50s" in weeks[2].text


def test_explicit_token_overrides_preset():
    plan = parse('---[A] Mo\n\nBench Press 5x5 @80kg +2.5kg/w\n')
    cfg = ProgressionConfig(weeks=3, goal="ausdauer", deload_rhythm="none")
    weeks = progress_plan(plan, cfg)
    # Token gewinnt: Last steigt trotz Ausdauer-Preset, Reps bleiben
    assert "5x5" in weeks[2].text and "@85kg" in weeks[2].text


# ---------------------------------------------------------------------------
# Semantischer Pfad: Deload
# ---------------------------------------------------------------------------


def test_deload_halves_sets_keeps_load_by_default():
    plan = parse(WODL_HYP)
    cfg = ProgressionConfig(weeks=4, rep_increment=1)
    weeks = progress_plan(plan, cfg)
    deload = weeks[3]
    assert deload.kind == "deload"
    assert "2x10" in deload.text           # Squat 4→2 Sätze, Reps eingefroren
    assert "@60kg" in deload.text          # Last gehalten (Default)


def test_deload_load_factor_applies():
    plan = parse('---[A] Mo\n\nSquat 4x5 @100kg\n')
    cfg = ProgressionConfig(weeks=4, goal="kraft", deload_load_factor=0.85)
    weeks = progress_plan(plan, cfg)
    # 2 Aufbau-Schritte: 100 → 105; Deload: 105 × 0.85 = 89.25 → 89 (0.5er-Raster)
    assert "@89kg" in weeks[3].text
    assert "2x5" in weeks[3].text


def test_deload_does_not_advance_state():
    plan = parse('---[A] Mo\n\nSquat 3x8-12 @60kg\n')
    cfg = ProgressionConfig(weeks=5, deload_rhythm="every4", rep_increment=1)
    weeks = progress_plan(plan, cfg)
    # W1 8, W2 9, W3 10, W4 Deload (Reps eingefroren bei 10), W5 = 11
    assert "x10" in weeks[3].text
    assert "3x11" in weeks[4].text


# ---------------------------------------------------------------------------
# Round-Trip: emittiertes WODL muss wieder parsen
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("goal", ["hypertrophie", "kraft", "ausdauer"])
def test_emitted_wodl_reparses_cleanly(goal):
    plan = parse(WODL_HYP)
    cfg = ProgressionConfig(weeks=4, goal=goal)
    for week in progress_plan(plan, cfg):
        reparsed = parse(week.text)
        assert reparsed.sessions, week.text
        n_items = sum(len(s.items) for s in reparsed.sessions)
        assert n_items == 4, week.text
        assert not [w for w in reparsed.warnings if "Unknown" in w], week.text


def test_emit_preserves_groups_rest_tempo():
    src = ('---[Push] Mo\n\nss {\n  Dip 3x8 @BW\n  Face Pull 3x15\n}\n'
           'Bench Press 4x8 @60kg r120s t3010\n')
    plan = parse(src)
    cfg = ProgressionConfig(weeks=2, deload_rhythm="none")
    week2 = progress_plan(plan, cfg)[1]
    assert "ss {" in week2.text and "}" in week2.text
    assert "r120s" in week2.text and "t3010" in week2.text
    reparsed = parse(week2.text)
    assert len(reparsed.sessions[0].items) == 2  # Gruppe + Einzelübung


# ---------------------------------------------------------------------------
# Freitext-Pfad
# ---------------------------------------------------------------------------


def test_freetext_reps_rise_kg_protected():
    cfg = ProgressionConfig(weeks=4, rep_increment=2)
    weeks = progress_text(FREETEXT, cfg)
    w3 = weeks[2].text                      # 2 Aufbau-Schritte = +4
    assert "3x14 20kg" in w3                # Sätze fix, Reps hoch, kg unangetastet
    assert "15x" in w3                      # 12x → 15x (Default-Schwelle 15 cappt)
    assert "14 Wdh" in w3                   # 10 Wdh → 14 Wdh


def test_freetext_time_progresses_headline_untouched():
    cfg = ProgressionConfig(weeks=3, deload_rhythm="none", rep_increment=1, time_increment=10)
    weeks = progress_text("Plank 45sek\nCooldown dehnen", cfg)
    assert "65sek" in weeks[2].text
    assert "Cooldown dehnen" in weeks[2].text


def test_freetext_deload_scales_sets_not_reps():
    cfg = ProgressionConfig(weeks=4, rep_increment=1)
    weeks = progress_text("Kniebeugen 4x10 20kg", cfg)
    deload = weeks[3].text
    assert "2x" in deload                   # Sätze halbiert
    assert "20kg" in deload                 # Last gehalten (Default)


def test_freetext_deload_load_factor():
    cfg = ProgressionConfig(weeks=4, deload_load_factor=0.8)
    weeks = progress_text("Kniebeugen 3x10 20kg", cfg)
    assert "16kg" in weeks[3].text


def test_freetext_threshold_caps_reps():
    cfg = ProgressionConfig(weeks=6, deload_rhythm="none", rep_increment=2, rep_threshold=15)
    weeks = progress_text("Curls 3x12", cfg)
    assert "3x15" in weeks[5].text          # 12+10 wäre 22 → Schwelle 15


def test_freetext_range_chain_shifts():
    cfg = ProgressionConfig(weeks=2, deload_rhythm="none", rep_increment=2, rep_threshold=20)
    weeks = progress_text("Rudern 8+10+12\nMcGill 10-8-6", cfg)
    assert "10+12+14" in weeks[1].text
    assert "12-10-8" in weeks[1].text


# ---------------------------------------------------------------------------
# Weiche
# ---------------------------------------------------------------------------


def test_switch_detects_wodl():
    assert looks_like_wodl(WODL_HYP) is not None
    mode, weeks = progress_auto(WODL_HYP, ProgressionConfig(weeks=4))
    assert mode == "wodl" and len(weeks) == 4


def test_switch_falls_back_to_freetext():
    assert looks_like_wodl(FREETEXT) is None
    mode, weeks = progress_auto(FREETEXT, ProgressionConfig(weeks=4))
    assert mode == "freetext" and len(weeks) == 4


def test_block_as_text_contains_all_weeks():
    _, weeks = progress_auto(FREETEXT, ProgressionConfig(weeks=4))
    block = block_as_text(weeks)
    for w in range(1, 5):
        assert f"=== Woche {w}" in block
