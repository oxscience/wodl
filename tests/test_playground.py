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
