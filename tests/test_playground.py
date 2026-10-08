"""Playground-Endpunkte: Ausgabe ist HTML-escaped (Pläne kommen auch über geteilte Links)."""

import pytest

from playground import app

EVIL = '@plan "<script>alert(1)</script>"\n---[<img src=x onerror=alert(1)>] Mo\n<b>x</b> 3x5 # <i>c</i>\n> <svg onload=alert(1)>'


@pytest.fixture
def client():
    return app.test_client()


@pytest.mark.parametrize("fmt", ["markdown", "summary", "json", "cycle"])
def test_parse_output_is_escaped(client, fmt):
    html = client.post("/parse", data={"wodl": EVIL, "format": fmt}).get_data(as_text=True)
    for tag in ("<script", "<img", "<b>", "<i>", "<svg"):
        assert tag not in html, f"{fmt}: {tag} unescaped"
    assert "&lt;" in html  # Inhalt ist da, nur escaped


def test_progress_output_is_escaped(client):
    html = client.post("/progress", data={"wodl": EVIL, "weeks": "4"}).get_data(as_text=True)
    for tag in ("<script", "<img", "<b>", "<i>", "<svg"):
        assert tag not in html, f"progress: {tag} unescaped"
    assert "&lt;" in html


def test_unknown_exercise_gets_suggestion_buttons(client):
    html = client.post("/parse", data={"wodl": "---[A] Mo\nKniebeuge mit Pause 3x8\nMeine Übung 3x10",
                                       "format": "markdown"}).get_data(as_text=True)
    assert 'data-from="Kniebeuge mit Pause" data-to="Kniebeuge"' in html
    assert "Meine Übung" in html and "zählt aber nicht im Volumen" in html
    assert html.count("Hinweise") == 1  # Markdown-Warnliste ersetzt, nicht doppelt


def test_table_rows_map_to_source_lines(client):
    html = client.post("/parse", data={"wodl": "---[A] Mo\nKniebeuge 3x5\nss {\n  Seitheben 3x15\n}",
                                       "format": "markdown"}).get_data(as_text=True)
    assert 'data-lines="2,4"' in html


def test_client_view_has_no_sample_and_marks_body(client):
    html = client.get("/?view=1").get_data(as_text=True)
    assert 'class="client-view"' in html
    assert "Full Body Basics</h1>" not in html  # kein Beispielplan-Flackern
    assert "Full Body Basics</h1>" in client.get("/").get_data(as_text=True)


def test_freetext_gets_convert_offer_and_stays_escaped(client):
    html = client.post("/parse", data={"wodl": "Montag\n<b>Kniebeugen</b> 3x10 60kg</textarea><script>x</script>",
                                       "format": "markdown"}).get_data(as_text=True)
    assert 'id="convert-btn"' in html
    assert "<script" not in html and "<b>" not in html and html.count("</textarea>") == 1
