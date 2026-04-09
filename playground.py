"""WODL Playground — Try the Workout Definition Language in your browser."""

from flask import Flask, request, jsonify, render_template_string
from wodl import parse, to_json, to_markdown

app = Flask(__name__)

SAMPLE_WOD = """\
@plan "Full Body Basics"
@freq 3x/week
@cycle 4w: w1-3 progress, w4 deload

---[Day A] Mo

Kniebeugen           3x5   @RPE8  r180s  +2.5kg/w
Bankdrücken          3x8   @RPE7  r120s
LH Rudern            3x8   @RPE7  r120s

---[Day B] Mi

Kreuzheben           3x5   @RPE8  r180s  +2.5kg/w
Schulterdrücken      3x8   @RPE7  r120s
Klimmzüge            3x8   @BW    r120s

---[Day C] Fr

Kniebeugen           3x5   @RPE8  r180s
KH Bankdrücken       3x8   @RPE7  r120s
KH Rudern            3x10  @RPE7  r90s

> Perfekt fuer Anfaenger und Wiedereinsteiger
"""

HTML = """\
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WODL Playground</title>
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
<style>
  :root {
    --bg: #0f1117;
    --bg2: #1a1d27;
    --bg3: #242836;
    --border: #2e3348;
    --text: #e2e4ed;
    --text2: #9298b0;
    --accent: #6c8cff;
    --accent2: #4a6adf;
    --green: #4ade80;
    --orange: #f59e0b;
    --red: #ef4444;
    --font: 'SF Mono', 'Fira Code', 'JetBrains Mono', monospace;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
  }

  header {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  }

  header h1 {
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  header h1 span {
    color: var(--accent);
  }

  .subtitle {
    color: var(--text2);
    font-size: 0.85rem;
  }

  .links {
    display: flex;
    gap: 1rem;
    font-size: 0.85rem;
  }

  .links a {
    color: var(--accent);
    text-decoration: none;
  }

  .links a:hover { text-decoration: underline; }

  main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    height: calc(100vh - 72px);
  }

  .panel {
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .panel-header {
    padding: 0.75rem 1.25rem;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text2);
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .panel:first-child { border-right: 1px solid var(--border); }

  textarea {
    flex: 1;
    background: var(--bg2);
    color: var(--text);
    border: none;
    padding: 1.25rem;
    font-family: var(--font);
    font-size: 0.9rem;
    line-height: 1.6;
    resize: none;
    outline: none;
    tab-size: 2;
  }

  textarea::placeholder { color: var(--text2); }

  #output {
    flex: 1;
    overflow-y: auto;
    padding: 1.25rem;
    background: var(--bg2);
    font-family: var(--font);
    font-size: 0.85rem;
    line-height: 1.6;
  }

  .tabs {
    display: flex;
    gap: 0;
  }

  .tab {
    padding: 0.4rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 500;
    background: transparent;
    color: var(--text2);
    border: 1px solid var(--border);
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    margin-left: 0.4rem;
  }

  .tab:hover { color: var(--text); background: var(--bg3); }
  .tab.active { color: var(--accent); border-color: var(--accent); background: var(--bg3); }

  /* Markdown output styling */
  #output h1 { font-size: 1.2rem; margin-bottom: 0.5rem; color: var(--accent); }
  #output h2 { font-size: 1rem; margin: 1.2rem 0 0.5rem; color: var(--green); }
  #output h3 { font-size: 0.9rem; margin: 1rem 0 0.3rem; color: var(--orange); }

  #output table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.5rem 0;
    font-size: 0.8rem;
  }

  #output th, #output td {
    padding: 0.4rem 0.6rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
  }

  #output th {
    color: var(--text2);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }

  #output td { color: var(--text); }

  #output blockquote {
    border-left: 3px solid var(--accent);
    padding-left: 0.8rem;
    color: var(--text2);
    margin: 0.5rem 0;
    font-style: italic;
  }

  #output strong { color: var(--text); }

  #output pre {
    background: var(--bg);
    padding: 1rem;
    border-radius: 6px;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .warning {
    color: var(--orange);
    font-size: 0.8rem;
    margin-top: 0.3rem;
  }

  .error-msg {
    color: var(--red);
    font-size: 0.85rem;
    padding: 1rem;
  }

  .stats {
    font-size: 0.75rem;
    color: var(--text2);
    padding: 0.5rem 1.25rem;
    border-top: 1px solid var(--border);
    background: var(--bg);
    display: flex;
    gap: 1.5rem;
  }

  .stats span strong { color: var(--text); }

  @media (max-width: 768px) {
    main {
      grid-template-columns: 1fr;
      grid-template-rows: 1fr 1fr;
    }
    .panel:first-child { border-right: none; border-bottom: 1px solid var(--border); }
  }
</style>
</head>
<body>

<header>
  <div>
    <h1><span>WODL</span> Playground</h1>
    <div class="subtitle">Workout Definition Language — schreib links, sieh rechts</div>
  </div>
  <div class="links">
    <a href="https://github.com/oxscience/wodl" target="_blank">GitHub</a>
    <a href="https://github.com/oxscience/wodl#syntax" target="_blank">Syntax</a>
  </div>
</header>

<main>
  <div class="panel">
    <div class="panel-header">
      <span>Editor</span>
      <button class="tab" onclick="loadSample()">Beispiel laden</button>
    </div>
    <textarea
      id="editor"
      placeholder="Trainingsplan hier eingeben..."
      name="wod"
    ></textarea>
  </div>

  <div class="panel">
    <div class="panel-header">
      <span>Output</span>
      <div class="tabs">
        <button class="tab active" onclick="setFormat('markdown', this)">Tabelle</button>
        <button class="tab" onclick="setFormat('json', this)">JSON</button>
        <button class="tab" onclick="setFormat('summary', this)">Summary</button>
      </div>
    </div>
    <div id="output">{{ initial_output | safe }}</div>
    <div class="stats" id="stats"></div>
  </div>
</main>

<input type="hidden" name="format" id="format-input" value="markdown">

<script>
  const editor = document.getElementById('editor');
  const output = document.getElementById('output');
  const sample = {{ sample_json | safe }};
  let currentFormat = 'markdown';
  let debounceTimer = null;

  function parseAndRender() {
    const body = new URLSearchParams({ wod: editor.value, format: currentFormat });
    fetch('/parse', { method: 'POST', body })
      .then(r => r.text())
      .then(html => { output.innerHTML = html; });
  }

  function setFormat(fmt, btn) {
    currentFormat = fmt;
    document.querySelectorAll('.tabs .tab').forEach(t => t.classList.remove('active'));
    if (btn) btn.classList.add('active');
    parseAndRender();
  }

  function loadSample() {
    editor.value = sample;
    parseAndRender();
  }

  // Live-update on typing with debounce
  editor.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(parseAndRender, 300);
  });

  // Load sample on start
  editor.value = sample;
  parseAndRender();
</script>

</body>
</html>
"""


def _md_to_html(md: str) -> str:
    """Minimal Markdown to HTML for the playground output."""
    import re

    lines = md.split("\n")
    html_lines = []
    in_table = False
    header_done = False

    for line in lines:
        stripped = line.strip()

        # Headings
        if stripped.startswith("### "):
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
                header_done = False
            html_lines.append(f"<h3>{stripped[4:]}</h3>")
            continue
        if stripped.startswith("## "):
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
                header_done = False
            html_lines.append(f"<h2>{stripped[3:]}</h2>")
            continue
        if stripped.startswith("# "):
            html_lines.append(f"<h1>{stripped[2:]}</h1>")
            continue

        # Bold inline **text**
        if "**" in stripped:
            stripped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            html_lines.append(f"<p>{stripped}</p>")
            continue

        # Blockquotes
        if stripped.startswith("> "):
            html_lines.append(f"<blockquote>{stripped[2:]}</blockquote>")
            continue

        # Table separator row — skip
        if stripped.startswith("|") and set(stripped.replace("|", "").strip()) <= {"-", " "}:
            continue

        # Table rows
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if not in_table:
                in_table = True
                header_done = False
                html_lines.append("<table>")

            if not header_done:
                html_lines.append(
                    "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr></thead><tbody>"
                )
                header_done = True
            else:
                html_lines.append(
                    "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
                )
            continue

        # Close table if open
        if in_table and not stripped.startswith("|"):
            html_lines.append("</tbody></table>")
            in_table = False
            header_done = False

        # List items
        if stripped.startswith("- "):
            html_lines.append(f"<div class='warning'>{stripped}</div>")
            continue

        # Empty line
        if not stripped:
            continue

    if in_table:
        html_lines.append("</tbody></table>")

    return "\n".join(html_lines)


@app.route("/")
def index():
    import json

    plan = parse(SAMPLE_WOD)
    initial_html = _md_to_html(to_markdown(plan))
    return render_template_string(
        HTML,
        sample=SAMPLE_WOD,
        sample_json=json.dumps(SAMPLE_WOD),
        initial_output=initial_html,
    )


@app.route("/parse", methods=["POST"])
def parse_wod():
    wod_text = request.form.get("wod", "")
    fmt = request.form.get("format", "markdown")

    if not wod_text.strip():
        return "<p style='color: var(--text2)'>Trainingsplan eingeben...</p>"

    try:
        plan = parse(wod_text)
    except Exception as e:
        return f"<div class='error-msg'>Parser-Fehler: {e}</div>"

    if fmt == "json":
        return f"<pre>{to_json(plan)}</pre>"

    if fmt == "summary":
        lines = []
        lines.append(f"<strong>Plan:</strong> {plan.name or '(unnamed)'}<br>")
        lines.append(f"<strong>Frequenz:</strong> {plan.frequency or '-'}<br>")
        lines.append(f"<strong>Zyklus:</strong> {plan.cycle_length or '-'}<br>")
        lines.append(f"<strong>Einheit:</strong> {plan.unit}<br>")
        lines.append(f"<strong>Sessions:</strong> {len(plan.sessions)}<br><br>")
        for session in plan.sessions:
            days = " ".join(session.days) if session.days else ""
            ex_count = sum(
                len(item.exercises) if hasattr(item, "exercises") else 1
                for item in session.items
            )
            lines.append(f"<strong>[{session.name}]</strong> {days} — {ex_count} Uebungen<br>")
        if plan.warnings:
            lines.append("<br><strong style='color: var(--orange)'>Warnings:</strong><br>")
            for w in plan.warnings:
                lines.append(f"<div class='warning'>- {w}</div>")
        return "".join(lines)

    # Default: markdown as HTML
    md = to_markdown(plan)
    return _md_to_html(md)


if __name__ == "__main__":
    app.run(debug=True, port=5051)
