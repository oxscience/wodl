"""Freitext → WODL."""

from wodl.convert import freetext_to_wodl
from wodl.parser import parse


def test_whatsapp_style_plan():
    text = (
        "Montag – Oberkörper\n"
        "1. Bankdrücken 3x10 60kg\n"
        "- KH Rudern 3 x 12, 20kg, Pause 90 Sek\n"
        "Seitheben 3 Sätze à 15 Wdh\n"
        "Plank 3x45 sek\n"
        "Achte auf saubere Technik!\n"
        "\n"
        "Mittwoch Beine\n"
        "Kniebeugen 4x8 @80kg RPE 8\n"
        "Ausfallschritte 3x10 pro Seite\n"
        "Laufen 20 min\n"
    )
    assert freetext_to_wodl(text) == (
        "---[Oberkörper] Mo\n"
        "Bankdrücken  3x10 @60kg\n"
        "KH Rudern  3x12 @20kg r90s\n"
        "Seitheben  3x15\n"
        "Plank  3x45s\n"
        "> Achte auf saubere Technik!\n"
        "\n"
        "---[Beine] Mi\n"
        "Kniebeugen  4x8 @80kg # RPE8\n"
        "Ausfallschritte  3x10 je Seite\n"
        "Laufen  1x20min\n"
    )


def test_result_parses_and_resolves():
    plan = parse(freetext_to_wodl("Tag 1\nKniebeugen 5x5 100kg\nKlimmzüge 3x max\nWandsitz 3x30 Sekunden, 2 min Pause"))
    names = [ex.display_name for ex in plan.sessions[0].items]
    assert names == ["Kniebeuge", "Klimmzug", "Wandsitz"]
    assert plan.sessions[0].items[2].rest == "2m"


def test_excel_columns_and_missing_header():
    out = freetext_to_wodl("Übung\tSätze\tWdh\tGewicht\nBankdrücken\t3\t10\t60\nKniebeuge\t4\t8-10\t80\tlangsam")
    assert out == "---[Training]\nBankdrücken  3x10 @60kg\nKniebeuge  4x8-10 @80kg # langsam\n"


def test_long_text_with_weekday_word_is_a_note_not_a_header():
    out = freetext_to_wodl("Tag A\nKniebeuge 3x5\nSo oft wie möglich sauber ausführen")
    assert out.endswith("> So oft wie möglich sauber ausführen\n")
