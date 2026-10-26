"""Wochenvolumen: Sätze pro Muskelgruppe."""

from wodl.parser import parse
from wodl.volume import weekly_volume


def test_direct_full_indirect_half_times_days():
    # Bankdrücken: Brust direkt, Trizeps + Schulter vorne halb; 2 Tage/Woche
    cols, rows, unknown = weekly_volume(parse("---[A] Mo Do\nBankdrücken 4x8"))
    assert cols == ["pro Woche"]
    assert rows["Brust"] == [8]
    assert rows["Trizeps"] == [4]
    assert rows["Schulter vorne"] == [4]
    assert unknown == 0


def test_session_without_days_counts_once_and_groups_sum():
    plan = parse("---[A]\nKniebeuge 3x5\nss {\n  Beinstrecker 3x12\n  Beinbeuger 3x12\n}")
    _, rows, _ = weekly_volume(plan)
    assert rows["Quadrizeps"] == [6]
    assert rows["Hamstrings"] == [4.5]  # 3 direkt (Beinbeuger) + 1,5 indirekt (Kniebeuge)
    assert rows["Gesäß"] == [1.5]


def test_mobility_cardio_and_unknown_not_counted():
    _, rows, unknown = weekly_volume(parse("---[A]\nWadendehnung 3x30s\nRudergerät 1x600s\nMeine Übung 3x10"))
    assert rows == {}
    assert unknown == 1


def test_phase_plan_gets_one_column_per_phase():
    plan = parse("---[Phase 1: Akut (Woche 0-2)] Mo Mi Fr\nWandsitz 3x30s\n"
                 "---[Phase 2: Kraft] Mo Fr\nKniebeuge 3x8")
    cols, rows, _ = weekly_volume(plan)
    assert cols == ["Phase 1", "Phase 2"]
    assert rows["Quadrizeps"] == [9, 6]


BLOCKS = """@plan "Offseason"
---[Block 1: Aufbau] Mo
Kniebeuge  4x8
Bankdrücken  4x8
---[Block 1: Aufbau] Do
Kreuzheben  4x8
Bankdrücken  4x8
---[Block 2: Maximalkraft] Mo
Kniebeuge  5x3
---[Gehprogramm (alle Blöcke)] Sa
Ausfallschritt  2x10
"""


def test_block_with_two_days_is_one_column():
    columns, rows, _ = weekly_volume(parse(BLOCKS))
    assert columns == ["Block 1", "Block 2", "Gehprogramm"]
    assert rows["Brust"][:2] == [8.0, 0]          # Mo + Do addiert, nicht 4 | 4


def test_single_block_counts_per_week():
    # Nur Block 1 gewählt (wie die Phasen-Auswahl filtert): keine Phasen-Spalten, Wochensumme
    one = "---[Block 1: Aufbau] Mo\nBankdrücken  4x8\n---[Block 1: Aufbau] Do\nBankdrücken  4x8\n"
    columns, rows, _ = weekly_volume(parse(one))
    assert columns == ["pro Woche"] and rows["Brust"] == [8.0]
