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
    assert "Ganzkörper Basics</h1>" not in html  # kein Beispielplan-Flackern
    assert "Ganzkörper Basics</h1>" in client.get("/").get_data(as_text=True)


def test_freetext_gets_convert_offer_and_stays_escaped(client):
    html = client.post("/parse", data={"wodl": "Montag\n<b>Kniebeugen</b> 3x10 60kg</textarea><script>x</script>",
                                       "format": "markdown"}).get_data(as_text=True)
    assert 'id="convert-btn"' in html
    assert "<script" not in html and "<b>" not in html and html.count("</textarea>") == 1


def test_unknown_names_logged_only_when_enabled(client, tmp_path, monkeypatch):
    import playground

    log = tmp_path / "miss.tsv"
    plan = "---[A]\nMeine Übung 3x10\nNoch eine Übung\nKniebeuge 3x5\nKunde 0171 1234567 3x5"
    client.post("/parse", data={"wodl": plan, "format": "markdown"})
    assert not log.exists()  # aus ohne WODL_MISS_LOG

    monkeypatch.setattr(playground, "MISS_LOG", str(log))
    monkeypatch.setattr(playground, "_miss_seen", set())
    html = client.post("/parse", data={"wodl": plan, "format": "markdown"}).get_data(as_text=True)
    client.post("/parse", data={"wodl": plan, "format": "markdown"})  # gleiches nochmal: kein Duplikat
    lines = log.read_text(encoding="utf-8").splitlines()
    assert [ln.split("\t")[1] for ln in lines] == ["Meine Übung"]  # ohne Sätze/mit Ziffern: nicht geloggt
    assert "anonym" in html


def test_progress_client_format_renders_week_tabs(client):
    plan = '@plan "Block"\n---[A] Mo\nKniebeuge 3x8 @60kg\nBankdrücken 3x8-10 @50kg'
    html = client.post("/progress", data={"wodl": plan, "weeks": "4", "deload_rhythm": "last",
                                          "format": "client"}).get_data(as_text=True)
    assert html.count('<button type="button" class="wk-tab') == 4 and html.count('class="wk-pane') == 4
    assert "Woche 4 · Deload" in html
    assert "<h1>Block</h1>" in html and html.count("<h1>") == 1  # Titel nur einmal oben
    assert "Block kopieren" not in html  # keine Werkzeuge für Klient:innen


def test_footer_shows_version(client):
    from wodl import __version__
    html = client.get("/").get_data(as_text=True)
    assert f"WODL {__version__}" in html and 'class="app-footer"' in html


def test_footer_changelog_newest_first(client):
    from playground import CHANGELOG
    html = client.get("/").get_data(as_text=True)
    assert "Was ist neu" in html and CHANGELOG[0][1] in html
    days = [d for d, _ in CHANGELOG]
    assert len(days) == len(set(days))  # ein Eintrag pro Tag


def test_doku_pages_render(client):
    from playground import DOCS
    assert client.get("/doku").status_code == 302
    for slug in DOCS:
        html = client.get(f"/doku/{slug}").get_data(as_text=True)
        assert "<h1>" in html and 'aria-current="page"' in html, slug
        assert ".md\"" not in html, slug  # Artikel-Verweise zeigen auf /doku/…, nicht auf Dateien
    assert client.get("/doku/gibt-es-nicht").status_code == 404


def test_doku_markdown_escapes_and_keeps_code():
    from playground import _doc_to_html
    html = _doc_to_html("# T\n\nText mit <b>x</b> und `a<b>`\n\n```js\nif (a < b) {}\n```\n- [Mehr](json-format.md)\n")
    assert "<b>x</b>" not in html and "&lt;b&gt;x&lt;/b&gt;" in html
    assert "<code>a&lt;b&gt;</code>" in html and "if (a &lt; b) {}" in html
    assert '<a href="/doku/json-format">Mehr</a>' in html


def test_json_tab_offers_ai_prompt(client):
    html = client.post("/parse", data={"wodl": "---[A] Mo\nKniebeuge 3x5", "format": "json"}).get_data(as_text=True)
    assert "Prompt für KI kopieren" in html and "JSON kopieren" in html
    page = client.get("/").get_data(as_text=True)
    assert "const AI_PROMPT" in page and "Kurzhantel-Rudern" in page


@pytest.mark.parametrize("route", ["/parse", "/progress"])
def test_overlong_plan_is_rejected(client, route):
    html = client.post(route, data={"wodl": "Kniebeuge " + "1" * 20_001}).get_data(as_text=True)
    assert "Plan zu lang" in html


def test_cycle_matrix_is_capped(client):
    html = client.post("/parse", data={"wodl": "@cycle 100000w\n---[A]\nKniebeuge 3x5 @100kg",
                                       "format": "cycle"}).get_data(as_text=True)
    assert "Zyklus zu lang" in html


def test_long_digit_runs_stay_fast():
    # Früher quadratisch: 4.000 Ziffern brauchten in /progress ~20 s
    import time
    from wodl.convert import freetext_to_wodl
    from wodl.progression import ProgressionConfig, progress_auto
    txt = "Kniebeuge " + "1" * 20_000
    start = time.perf_counter()
    freetext_to_wodl(txt)
    progress_auto(txt, ProgressionConfig(weeks=12))
    assert time.perf_counter() - start < 2
