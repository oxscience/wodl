"""WODL Playground — Try the Workout Definition Language in your browser.

Features:
  - Live parse & preview (Markdown / JSON / Summary)
  - Branding panel: theme presets, custom primary color, logo, coach/client name
  - localStorage persistence + shareable URL params
  - Print-optimized CSS for PDF export (browser print → PDF)
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from flask import Flask, abort, jsonify, request, render_template_string

from wodl import parse, to_json, to_markdown, to_cycle_matrix

app = Flask(__name__)

EXAMPLES_DIR = Path(__file__).parent / "examples"

# Bibliothek: Metadata für jedes Beispiel. Reihenfolge bestimmt UI-Reihenfolge.
EXAMPLE_LIBRARY: list[dict] = [
    # --- Training ---
    {
        "file": "beginner-full-body",
        "title": "Anfänger Full Body",
        "category": "training",
        "level": "Anfänger",
        "freq": "3x/Woche",
        "split": "Full Body",
        "desc": "Lineare Progression, nur Compounds, RPE 7, +2.5kg/Woche. Für Menschen im ersten Trainingsjahr.",
        "source": "Rhea et al. (2003), Med Sci Sports Exerc — untrainierte profitieren von niedrigen Volumina (~4 Sets/Muskel/Woche)",
    },
    {
        "file": "minimalist-3day",
        "title": "Minimalist 3-Day Full Body",
        "category": "training",
        "level": "Anfänger / Fortgeschritten",
        "freq": "3x/Woche",
        "split": "Full Body",
        "desc": "Nur Compounds, 45 Minuten pro Session. Für Menschen mit wenig Zeit oder Wiedereinsteiger.",
        "source": "Schoenfeld et al. (2019), J Sports Sci — Volumen-matched ist Frequenz für Hypertrophie nicht entscheidend",
    },
    {
        "file": "home-minimal",
        "title": "Home Minimal — Bodyweight & Bänder",
        "category": "training",
        "level": "Alle Stufen",
        "freq": "3x/Woche",
        "split": "Full Body",
        "desc": "Nur Bodyweight + Resistance-Bänder. Kein Gym nötig. Progression durch Reps, Tempo, Einbein-Varianten.",
        "source": "Schoenfeld et al. (2017), J Strength Cond Res — low-load (<60% 1RM) mit RIR 0-2 ergibt vergleichbare Hypertrophie",
    },
    {
        "file": "push-pull-4day",
        "title": "Push-Pull 4x/Woche",
        "category": "training",
        "level": "Fortgeschritten",
        "freq": "4x/Woche",
        "split": "Push / Pull",
        "desc": "Hypertrophie-Fokus ohne dedizierten Bein-Tag. Pro Muskelgruppe 2x pro Woche getroffen.",
        "source": "Schoenfeld et al. (2016), Sports Med — Meta-Analyse: ≥2x/Woche pro Muskelgruppe > 1x/Woche für Hypertrophie",
    },
    {
        "file": "upper-lower-strength",
        "title": "Upper / Lower Strength",
        "category": "training",
        "level": "Fortgeschritten",
        "freq": "4x/Woche",
        "split": "Upper / Lower",
        "desc": "5x5 Kraft-Fokus auf den großen Lifts, moderate Volumen-Arbeit drumherum.",
        "source": "Peterson et al. (2005), J Strength Cond Res — Meta-Analyse: 80-85% 1RM bei 2-3 Sets optimal für Kraftentwicklung",
    },
    {
        "file": "ppl-hypertrophy",
        "title": "Push / Pull / Legs Hypertrophy",
        "category": "training",
        "level": "Fortgeschritten",
        "freq": "6x/Woche",
        "split": "Push / Pull / Legs",
        "desc": "Hohes Volumen pro Muskelgruppe. 2x/Woche pro Muskel. Supersets für Isolation-Arbeit.",
        "source": "Schoenfeld et al. (2017), J Sports Sci — Dose-Response: ≥10 Sets/Muskel/Woche maximiert Hypertrophie",
    },
    {
        "file": "powerbuilding-5day",
        "title": "Powerbuilding 5x/Woche",
        "category": "training",
        "level": "Fortgeschritten / Advanced",
        "freq": "5x/Woche",
        "split": "Upper/Lower + Arms",
        "desc": "Hybrid Kraft + Hypertrophie. Heavy-Tage mit Primer-Lift, Volume-Tage pump-orientiert.",
        "source": "Schoenfeld et al. (2014), J Strength Cond Res — gemischte Rep-Ranges optimieren beide Adaptationen parallel",
    },

    # --- Rehabilitation ---
    {
        "file": "rehab-acl-postop",
        "title": "VKB-Rekonstruktion — Post-OP Reha",
        "category": "rehab",
        "level": "Klinisch",
        "freq": "täglich → 3-5x/Woche",
        "indication": "Nach VKB-Rekonstruktion (ACL Reconstruction)",
        "desc": "4 Phasen über 24+ Wochen: Akut → Early Strength → Kraft → Return to Sport. Mit Meilensteinen und LSI-Kriterien.",
        "source": "Wilk & Arrigo 2017 (JOSPT), van Melick 2016 (BJSM)",
    },
    {
        "file": "rehab-rotator-cuff",
        "title": "Rotator Cuff — Konservative Reha",
        "category": "rehab",
        "level": "Klinisch",
        "freq": "5x/Woche",
        "indication": "Rotator-Cuff-Tendinopathie / SAPS / Impingement",
        "desc": "4 Phasen: Akut → Isometrics → Strength → Function. Symptom-geleitet, nicht zeitbasiert.",
        "source": "Ellenbecker & Cools 2010, Kuhn 2009, MOON-Protokoll",
    },
    {
        "file": "rehab-lbp-mcgill",
        "title": "LBP — McGill Big 3",
        "category": "rehab",
        "level": "Klinisch",
        "freq": "täglich",
        "indication": "Chronische unspezifische Kreuzschmerzen (cLBP)",
        "desc": "Curl-up, Side Plank, Bird Dog mit Reverse-Pyramid 10-8-6. Neutrale Spine, keine Sit-ups.",
        "source": "McGill 2016, Lee & McGill 2015",
    },
    {
        "file": "rehab-achilles-alfredson",
        "title": "Achilles-Tendinopathie — Alfredson",
        "category": "rehab",
        "level": "Klinisch",
        "freq": "2x täglich, 7 Tage/Woche",
        "indication": "Chronische midportion Achilles-Tendinopathie",
        "desc": "Original-Protokoll: 3x15 exzentrische Heel Drops, straight-knee + bent-knee, 12 Wochen durchgehend.",
        "source": "Alfredson et al. 1998, Beyer 2015",
    },
]

SAMPLE_WODL = """\
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

> Perfekt für Anfänger und Wiedereinsteiger
"""

# Theme-Presets: Name -> Primärfarbe. Coaches wählen, Rest bleibt Dark.
THEMES: dict[str, dict] = {
    "OX Pink":      {"primary": "#ff4477", "accent2": "#c62f5a"},
    "Royal Blue":   {"primary": "#6c8cff", "accent2": "#4a6adf"},
    "Forest Green": {"primary": "#4ade80", "accent2": "#22c55e"},
    "Sunset":       {"primary": "#f59e0b", "accent2": "#d97706"},
    "Violet":       {"primary": "#a78bfa", "accent2": "#7c3aed"},
    "Crimson":      {"primary": "#ef4444", "accent2": "#b91c1c"},
}

HTML = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WODL Playground</title>
<link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32.png">
<link rel="icon" type="image/png" sizes="180x180" href="/static/favicon-180.png">
<link rel="apple-touch-icon" href="/static/favicon-180.png">
<meta name="theme-color" content="#0f1117">
<style>
  :root {
    --bg: #0f1117;
    --bg2: #1a1d27;
    --bg3: #242836;
    --border: #2e3348;
    --text: #e2e4ed;
    --text2: #9298b0;
    --primary: #6c8cff;
    --primary2: #4a6adf;
    --green: #4ade80;
    --orange: #f59e0b;
    --red: #ef4444;
    --font: 'SF Mono', 'Fira Code', 'JetBrains Mono', monospace;
  }

  [data-theme="light"] {
    --bg: #ffffff;
    --bg2: #f7f8fa;
    --bg3: #eef0f4;
    --border: #d8dce3;
    --text: #1a1d27;
    --text2: #5a6073;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
  }

  header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .brand img {
    height: 32px;
    max-width: 120px;
    object-fit: contain;
  }

  .brand h1 {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  .brand h1 span { color: var(--primary); }

  .subtitle {
    color: var(--text2);
    font-size: 0.8rem;
    margin-top: 0.1rem;
  }

  .header-actions {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    flex-wrap: wrap;
  }

  .btn {
    padding: 0.45rem 0.85rem;
    font-size: 0.8rem;
    font-weight: 500;
    background: transparent;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s;
  }

  .btn:hover { background: var(--bg3); border-color: var(--primary); }

  .btn.primary {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
  }

  .btn.primary:hover {
    background: var(--primary2);
    border-color: var(--primary2);
  }

  .theme-toggle {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.25rem;
    padding: 0.3rem 0.5rem;
    border-radius: 4px;
    color: var(--text2);
    transition: color 0.15s;
    line-height: 1;
    margin-left: 0.25rem;
  }
  .theme-toggle:hover { color: var(--text); }

  /* Mini-Logo invertieren im Light-Mode (für helle/weiße Logos die primär fürs Dark-Branding designed sind) */
  [data-theme="light"] .brand img { filter: invert(1) hue-rotate(180deg); }

  /* Harter Cut beim Theme-Wechsel — keine Transitionen während des Switches */
  html.no-transitions *,
  html.no-transitions *::before,
  html.no-transitions *::after {
    transition: none !important;
    animation: none !important;
  }

  /* Branding panel */
  .branding-panel {
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    padding: 1rem 1.5rem;
    display: none;
  }

  .branding-panel.open { display: block; }

  .branding-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    max-width: 1200px;
  }

  .field { display: flex; flex-direction: column; gap: 0.3rem; }
  .field label { font-size: 0.75rem; color: var(--text2); font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; }
  .field input[type="text"], .field input[type="url"] {
    padding: 0.45rem 0.7rem;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    font-family: inherit;
    font-size: 0.85rem;
  }
  .field input:focus { outline: none; border-color: var(--primary); }

  .theme-grid {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
  }

  .theme-swatch {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    cursor: pointer;
    border: 2px solid transparent;
    transition: transform 0.1s;
  }
  .theme-swatch:hover { transform: scale(1.1); }
  .theme-swatch.active { border-color: var(--text); }

  .color-row {
    display: flex;
    gap: 0.4rem;
    align-items: center;
  }
  .color-row input[type="color"] {
    width: 36px;
    height: 36px;
    padding: 0;
    border: 1px solid var(--border);
    border-radius: 6px;
    cursor: pointer;
    background: transparent;
  }
  .color-row input[type="text"] { flex: 1; }

  main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    height: calc(100vh - 72px);
  }

  body.has-branding main { height: calc(100vh - 72px - var(--branding-height, 0px)); }

  .panel {
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .panel-header {
    padding: 0.7rem 1.25rem;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text2);
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
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

  .tabs { display: flex; gap: 0; }

  .tab {
    padding: 0.35rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 500;
    background: transparent;
    color: var(--text2);
    border: 1px solid var(--border);
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    margin-left: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }

  .tab:hover { color: var(--text); background: var(--bg3); }
  .tab.active { color: var(--primary); border-color: var(--primary); background: var(--bg3); }

  /* Library Modal */
  .modal-backdrop {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    z-index: 100;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }
  .modal-backdrop.open { display: flex; }

  .modal {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    max-width: 960px;
    width: 100%;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
  }

  .modal-header {
    padding: 1.1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .modal-header h2 { font-size: 1.1rem; font-weight: 700; }
  .modal-header h2 span { color: var(--primary); }

  .modal-close {
    background: transparent;
    border: none;
    color: var(--text2);
    font-size: 1.5rem;
    cursor: pointer;
    line-height: 1;
    padding: 0 0.4rem;
  }
  .modal-close:hover { color: var(--text); }

  .library-tabs {
    display: flex;
    gap: 0;
    padding: 0 1.5rem;
    border-bottom: 1px solid var(--border);
    background: var(--bg2);
  }

  .lib-tab {
    padding: 0.85rem 1.2rem;
    font-size: 0.85rem;
    font-weight: 600;
    background: transparent;
    color: var(--text2);
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    font-family: inherit;
  }
  .lib-tab:hover { color: var(--text); }
  .lib-tab.active { color: var(--primary); border-bottom-color: var(--primary); }

  .lib-content {
    padding: 1.25rem 1.5rem;
    overflow-y: auto;
    flex: 1;
  }

  .lib-intro {
    font-size: 0.85rem;
    color: var(--text2);
    margin-bottom: 1rem;
    line-height: 1.5;
  }

  .lib-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 0.9rem;
  }

  .plan-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    cursor: pointer;
    transition: all 0.15s;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .plan-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  }

  .plan-card h3 {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.3;
  }

  .plan-card .meta {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
  }

  .plan-card .tag {
    font-size: 0.68rem;
    padding: 0.15rem 0.5rem;
    background: var(--bg3);
    color: var(--text2);
    border-radius: 10px;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    font-weight: 600;
  }

  .plan-card .tag.primary {
    background: var(--primary);
    color: white;
  }

  .plan-card p {
    font-size: 0.8rem;
    color: var(--text2);
    line-height: 1.5;
    flex: 1;
  }

  .plan-card .source {
    font-size: 0.7rem;
    color: var(--text2);
    font-style: italic;
    border-top: 1px solid var(--border);
    padding-top: 0.5rem;
    margin-top: 0.3rem;
  }

  /* ===== Interactive Tour ===== */
  .tour-backdrop {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 200;
    pointer-events: none;
  }
  .tour-backdrop.active { display: block; pointer-events: auto; }

  .tour-mask {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.72);
    transition: clip-path 0.35s ease-out;
  }

  .tour-highlight {
    position: absolute;
    border: 2px solid var(--primary);
    border-radius: 8px;
    pointer-events: none;
    box-shadow: 0 0 0 4px rgba(108,140,255,0.18), 0 0 24px rgba(108,140,255,0.4);
    transition: all 0.35s ease-out;
    z-index: 201;
  }
  .tour-highlight.pulse {
    animation: tourPulse 1.6s ease-in-out infinite;
  }
  @keyframes tourPulse {
    0%, 100% { box-shadow: 0 0 0 4px rgba(108,140,255,0.18), 0 0 24px rgba(108,140,255,0.4); }
    50% { box-shadow: 0 0 0 10px rgba(108,140,255,0.32), 0 0 36px rgba(108,140,255,0.6); }
  }

  .tour-tooltip {
    position: absolute;
    background: var(--bg);
    border: 1px solid var(--primary);
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
    max-width: 360px;
    color: var(--text);
    z-index: 202;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    transition: opacity 0.2s, transform 0.2s;
  }

  .tour-close {
    position: absolute;
    top: 0.5rem;
    right: 0.6rem;
    background: transparent;
    border: none;
    color: var(--text2);
    font-size: 1.4rem;
    line-height: 1;
    cursor: pointer;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-family: inherit;
  }
  .tour-close:hover { color: var(--text); background: var(--bg3); }

  .tour-esc-hint {
    font-size: 0.7rem;
    color: var(--text2);
    text-align: center;
    margin-top: 0.6rem;
    padding-top: 0.5rem;
    border-top: 1px solid var(--border);
  }
  .tour-esc-hint kbd {
    background: var(--bg3);
    border: 1px solid var(--border);
    padding: 0.05rem 0.35rem;
    border-radius: 3px;
    font-family: var(--font);
    font-size: 0.7rem;
    color: var(--text);
  }

  .tour-tooltip-step {
    font-size: 0.7rem;
    color: var(--primary);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.3rem;
  }

  .tour-tooltip h3 {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--text);
  }

  .tour-tooltip p {
    font-size: 0.85rem;
    line-height: 1.55;
    color: var(--text2);
    margin-bottom: 0.9rem;
  }

  .tour-tooltip p code {
    background: var(--bg3);
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
    font-family: var(--font);
    font-size: 0.78rem;
    color: var(--text);
  }

  .tour-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.25rem;
  }

  .tour-progress {
    display: flex;
    gap: 0.3rem;
  }
  .tour-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--border);
  }
  .tour-dot.active { background: var(--primary); width: 18px; border-radius: 3px; }

  .tour-btn {
    padding: 0.4rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 500;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    border: 1px solid var(--border);
    background: transparent;
    color: var(--text);
  }
  .tour-btn.primary {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
  }
  .tour-btn:hover { background: var(--bg3); }
  .tour-btn.primary:hover { background: var(--primary2); }
  .tour-btn:disabled { opacity: 0.4; cursor: not-allowed; }

  .tour-skip {
    position: fixed;
    top: 1rem;
    right: 1.25rem;
    z-index: 203;
    color: var(--text2);
    background: var(--bg2);
    border: 1px solid var(--border);
    padding: 0.4rem 0.9rem;
    border-radius: 6px;
    font-size: 0.75rem;
    cursor: pointer;
    font-family: inherit;
  }
  .tour-skip:hover { color: var(--text); }

  /* Arrow pointers — nur sichtbar wenn arrow-Klasse gesetzt */
  .tour-tooltip::before {
    content: '';
    position: absolute;
    width: 12px;
    height: 12px;
    background: var(--bg);
    border: 1px solid var(--primary);
    transform: rotate(45deg);
    display: none;
  }
  .tour-tooltip.arrow-top::before,
  .tour-tooltip.arrow-bottom::before,
  .tour-tooltip.arrow-left::before,
  .tour-tooltip.arrow-right::before { display: block; }
  .tour-tooltip.arrow-top::before { top: -7px; left: 28px; border-right: none; border-bottom: none; }
  .tour-tooltip.arrow-bottom::before { bottom: -7px; right: 28px; border-left: none; border-top: none; }
  .tour-tooltip.arrow-left::before { left: -7px; top: 28px; border-right: none; border-top: none; }
  .tour-tooltip.arrow-right::before { right: -7px; top: 28px; border-left: none; border-bottom: none; }

  /* Markdown output styling */
  #output h1 { font-size: 1.2rem; margin-bottom: 0.5rem; color: var(--primary); }
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
    border-left: 3px solid var(--primary);
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
    font-size: 0.8rem;
  }

  /* Cycle-Matrix spezifisch — Deload-Zellen und Wochen-Spalten hervorheben */
  .cycle-view em {
    font-style: normal;
    color: var(--orange);
    background: rgba(245, 158, 11, 0.08);
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
    font-size: 0.78rem;
  }
  .cycle-view table th:nth-child(n+3) {
    text-align: center;
    font-size: 0.72rem;
    color: var(--primary);
  }
  .cycle-view table td:nth-child(n+3) {
    text-align: center;
    font-size: 0.78rem;
    font-family: var(--font);
    color: var(--text);
    font-weight: 500;
  }
  .cycle-view table th:nth-child(-n+2),
  .cycle-view table td:nth-child(-n+2) {
    text-align: left;
  }

  .warning { color: var(--orange); font-size: 0.8rem; margin-top: 0.3rem; }
  .error-msg { color: var(--red); font-size: 0.85rem; padding: 1rem; }

  /* Print view — for PDF export via browser print */
  .print-only { display: none; }

  @media print {
    body { background: white; color: black; }
    header, .branding-panel, .panel:first-child, .panel-header, .stats { display: none !important; }
    main { display: block; height: auto; }
    .panel { overflow: visible; }
    #output {
      padding: 0;
      background: white;
      color: black;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.5;
    }
    #output h1 { color: var(--primary) !important; font-size: 20pt; border-bottom: 2px solid var(--primary); padding-bottom: 0.3em; }
    #output h2 { color: black !important; font-size: 14pt; margin-top: 1em; }
    #output h3 { color: var(--primary) !important; font-size: 11pt; }
    #output th { color: #555 !important; border-bottom: 1px solid #888; }
    #output td { color: black !important; border-bottom: 1px solid #ddd; }
    #output blockquote { color: #555 !important; border-left-color: var(--primary) !important; }
    .print-only { display: block; }
    .print-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.5em;
      padding-bottom: 1em;
      border-bottom: 2px solid var(--primary);
    }
    .print-header img { height: 40px; max-width: 140px; }
    .print-header .meta { text-align: right; font-size: 9pt; color: #555; }
    .print-header .coach { font-weight: 700; color: var(--primary); font-size: 11pt; }
    .print-footer {
      margin-top: 2em;
      padding-top: 0.8em;
      border-top: 1px solid #ddd;
      font-size: 8pt;
      color: #888;
      text-align: center;
    }
    @page { margin: 1.5cm; }
  }

  /* ==================== MOBILE ==================== */
  @media (max-width: 768px) {
    /* Header */
    header {
      padding: 0.75rem 1rem;
      flex-direction: column;
      align-items: stretch;
      gap: 0.6rem;
    }
    .brand h1 { font-size: 1.05rem; }
    .subtitle { display: none; }
    .header-actions {
      gap: 0.35rem;
      justify-content: flex-start;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      padding-bottom: 0.2rem;
    }
    .header-actions::-webkit-scrollbar { display: none; }
    .btn {
      padding: 0.5rem 0.7rem;
      font-size: 0.75rem;
      white-space: nowrap;
      flex-shrink: 0;
    }

    /* Branding-Panel Grid */
    .branding-panel { padding: 0.85rem 1rem; }
    .branding-grid { grid-template-columns: 1fr; gap: 0.75rem; }

    /* Main: vertikal mit festen Höhen, scroll-bar */
    main {
      grid-template-columns: 1fr;
      grid-template-rows: auto auto;
      height: auto;
      min-height: calc(100vh - 120px);
    }
    .panel:first-child {
      border-right: none;
      border-bottom: 1px solid var(--border);
    }
    textarea {
      min-height: 240px;
      font-size: 0.85rem;
      padding: 0.85rem;
    }
    #output {
      min-height: 320px;
      padding: 0.85rem;
      font-size: 0.8rem;
    }
    .panel-header {
      padding: 0.6rem 0.9rem;
      font-size: 0.72rem;
    }
    .tab {
      padding: 0.3rem 0.55rem;
      font-size: 0.68rem;
      margin-left: 0.25rem;
    }

    /* Library Modal fullscreen */
    .modal-backdrop { padding: 0; }
    .modal {
      max-width: 100%;
      max-height: 100vh;
      height: 100vh;
      border-radius: 0;
      border: none;
    }
    .modal-header { padding: 0.9rem 1rem; }
    .modal-header h2 { font-size: 1rem; }
    .lib-content { padding: 1rem; }
    .lib-grid { grid-template-columns: 1fr; gap: 0.7rem; }
    .library-tabs { padding: 0 1rem; }
    .lib-tab { padding: 0.7rem 0.9rem; font-size: 0.8rem; }

    /* Cycle-Matrix horizontal scrollbar */
    #output table { display: block; overflow-x: auto; }

    /* Tour: Mobile = Fullscreen Center Modal, kein Pfeil, kein Highlight-Hole */
    .tour-overlay { background: rgba(0,0,0,0.85) !important; }
    .tour-highlight { display: none !important; }
    .tour-tooltip {
      position: fixed !important;
      top: 50% !important;
      left: 50% !important;
      transform: translate(-50%, -50%) !important;
      width: calc(100vw - 2rem);
      max-width: 420px;
      max-height: calc(100vh - 2rem);
      overflow-y: auto;
    }
    .tour-tooltip::before { display: none !important; }
    .tour-controls { flex-direction: column; gap: 0.75rem; align-items: stretch; }
    .tour-controls > div:last-child { width: 100%; }
    .tour-controls > div:last-child .tour-btn { flex: 1; }
    .tour-btn {
      padding: 0.65rem 1rem;
      font-size: 0.9rem;
    }
  }
</style>
</head>
<body data-theme="dark">

<header>
  <div class="brand">
    <img id="brand-logo" src="" alt="" style="display:none">
    <div>
      <h1><span id="brand-title">WODL</span> <span id="brand-subtitle-heading" style="color:var(--text)">Playground</span></h1>
      <div class="subtitle" id="brand-subtitle">Workout Definition Language — schreib links, sieh rechts</div>
    </div>
  </div>
  <div class="header-actions">
    <button class="btn" onclick="startTour()" id="tour-btn" title="Interaktive Tour starten">🎓 Tour</button>
    <button class="btn primary" onclick="openLibrary()" id="library-btn">📚 Bibliothek</button>
    <button class="btn" onclick="toggleBranding()" id="branding-btn">Branding</button>
    <button class="btn" onclick="copyShareLink()" id="share-btn">Link teilen</button>
    <button class="btn" onclick="window.print()" id="pdf-btn">PDF exportieren</button>
    <button class="theme-toggle" onclick="toggleTheme()" id="theme-btn" title="Dark/Light Mode" aria-label="Theme wechseln">&#9790;</button>
  </div>
</header>

<!-- Tour Overlay -->
<div class="tour-backdrop" id="tour-backdrop">
  <div class="tour-mask" id="tour-mask"></div>
  <div class="tour-highlight pulse" id="tour-highlight"></div>
  <div class="tour-tooltip" id="tour-tooltip">
    <button class="tour-close" onclick="endTour()" title="Tour schließen (Esc)" aria-label="Schließen">×</button>
    <div class="tour-tooltip-step" id="tour-step-num"></div>
    <h3 id="tour-title"></h3>
    <p id="tour-text"></p>
    <div class="tour-controls">
      <div class="tour-progress" id="tour-progress"></div>
      <div style="display: flex; gap: 0.5rem;">
        <button class="tour-btn" id="tour-prev" onclick="tourPrev()">Zurück</button>
        <button class="tour-btn primary" id="tour-next" onclick="tourNext()">Weiter →</button>
      </div>
    </div>
    <div class="tour-esc-hint">
      <kbd>←</kbd> <kbd>→</kbd> Navigation  ·  <kbd>Esc</kbd> Tour beenden
    </div>
  </div>
</div>

<!-- Library Modal -->
<div class="modal-backdrop" id="lib-modal" onclick="if (event.target === this) closeLibrary()">
  <div class="modal">
    <div class="modal-header">
      <h2><span>📚</span> Bibliothek — Evidenzbasierte Beispielpläne</h2>
      <button class="modal-close" onclick="closeLibrary()" aria-label="Schließen">×</button>
    </div>
    <div class="library-tabs">
      <button class="lib-tab active" data-cat="training" onclick="switchLibTab('training', this)">Training</button>
      <button class="lib-tab" data-cat="rehab" onclick="switchLibTab('rehab', this)">Rehabilitation</button>
    </div>
    <div class="lib-content">
      <div class="lib-intro" id="lib-intro">Lade einen Plan, passe ihn an, brande ihn — dann als PDF drucken oder JSON für Apps exportieren.</div>
      <div class="lib-grid" id="lib-grid"></div>
    </div>
  </div>
</div>

<div class="branding-panel" id="branding-panel">
  <div class="branding-grid">
    <div class="field">
      <label>Theme-Preset</label>
      <div class="theme-grid" id="theme-grid"></div>
    </div>
    <div class="field">
      <label>Primärfarbe</label>
      <div class="color-row">
        <input type="color" id="primary-color" value="#6c8cff">
        <input type="text" id="primary-hex" value="#6c8cff">
      </div>
    </div>
    <div class="field">
      <label>Logo-URL (optional)</label>
      <input type="url" id="logo-url" placeholder="https://.../logo.png">
    </div>
    <div class="field">
      <label>Coach / Praxis</label>
      <input type="text" id="coach-name" placeholder="z.B. Praxis Müller">
    </div>
    <div class="field">
      <label>Klient:in (optional)</label>
      <input type="text" id="client-name" placeholder="z.B. Max Mustermann">
    </div>
    <div class="field">
      <label>&nbsp;</label>
      <button class="btn" onclick="resetBranding()">Zurücksetzen</button>
    </div>
  </div>
</div>

<main>
  <div class="panel">
    <div class="panel-header">
      <span>Editor</span>
      <span style="font-size:0.7rem;color:var(--text2);font-weight:400">.wodl</span>
    </div>
    <textarea id="editor" placeholder="Trainingsplan hier eingeben..." spellcheck="false"></textarea>
  </div>

  <div class="panel">
    <div class="panel-header">
      <span>Vorschau</span>
      <div class="tabs">
        <button class="tab active" data-fmt="markdown" onclick="setFormat('markdown', this)">Tabelle</button>
        <button class="tab" data-fmt="cycle" onclick="setFormat('cycle', this)" id="cycle-tab">📅 Zyklus</button>
        <button class="tab" data-fmt="json" onclick="setFormat('json', this)">JSON</button>
        <button class="tab" data-fmt="summary" onclick="setFormat('summary', this)">Summary</button>
      </div>
    </div>
    <div id="output">
      <!-- Print-only header: logo + coach + client -->
      <div class="print-only print-header">
        <div><img id="print-logo" src="" alt=""></div>
        <div class="meta">
          <div class="coach" id="print-coach"></div>
          <div id="print-client"></div>
          <div id="print-date"></div>
        </div>
      </div>

      <div id="output-body">{{ initial_output | safe }}</div>

      <div class="print-only print-footer">
        Erstellt mit WODL — wodl.outoftheb-ox.de
      </div>
    </div>
  </div>
</main>

<script>
  const editor = document.getElementById('editor');
  const outputBody = document.getElementById('output-body');
  const sample = {{ sample_json | safe }};
  const themes = {{ themes_json | safe }};
  let currentFormat = 'markdown';
  let debounceTimer = null;

  // ===== Parse =====
  function parseAndRender() {
    const body = new URLSearchParams({ wodl: editor.value, format: currentFormat });
    fetch('/parse', { method: 'POST', body })
      .then(r => r.text())
      .then(html => { outputBody.innerHTML = html; });
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
    saveToStorage();
  }

  // ===== Interactive Tour =====
  const TOUR_STEPS = [
    {
      target: null,  // full-screen welcome
      title: '👋 Willkommen bei WODL',
      text: '<strong>Warum?</strong> Trainingspläne leben als Excel, PDFs oder WhatsApp-Screenshots — unlesbar für Apps, nicht versionierbar, nicht vergleichbar. WODL macht Pläne zu Text: menschenlesbar und maschinenparsbar. In 60 Sekunden zeig ich dir wie.',
      pos: 'center',
    },
    {
      target: '#library-btn',
      title: '📚 Mit einem Klick starten',
      text: '11 evidenzbasierte Beispielpläne: 7 Training (Push-Pull, Full Body, Powerbuilding …) und 4 Reha-Protokolle (VKB, Rotator Cuff, McGill LBP, Alfredson Achilles). Klick hier, wähl einen Plan — er landet im Editor.',
      pos: 'bottom',
    },
    {
      target: '#editor',
      title: '✏️ Editor & Syntax',
      text: 'Eine Zeile = eine Übung. <code>Bankdrücken 4x8 @RPE8 r120s</code> = 4 Sätze à 8 Reps, RPE 8, 2 Min Pause. Deutsche Namen (Kniebeugen, Klimmzüge, Bankdrücken) werden automatisch erkannt.',
      pos: 'right',
    },
    {
      target: '#output',
      title: '👁 Live-Vorschau',
      text: 'Vier Ansichten: <code>Tabelle</code> zum Lesen, <code>📅 Zyklus</code> projiziert die Progression über alle Wochen (z.B. 4 Wochen Bench-Press-Gewicht + Deload), <code>JSON</code> für Apps, <code>Summary</code> zum Volumen-Check.',
      pos: 'left',
    },
    {
      target: '#cycle-tab',
      title: '📅 Killer-Feature: Wochen-Matrix',
      text: 'Aus <code>@100kg +2.5kg/w</code> wird automatisch W1: 100, W2: 102.5, W3: 105. Deload-Wochen (<code>@cycle 4w: w4 deload</code>) reduzieren die Last um 20%. Ein Plan → alle Wochen auf einen Blick. <strong>Das kann Excel nicht automatisch.</strong>',
      pos: 'left',
    },
    {
      target: '#branding-btn',
      title: '🎨 Dein Branding',
      text: 'Logo-URL, Praxis-/Coach-Name, Klient-Name, Primärfarbe. 6 Presets + Custom Hex. Alles lokal gespeichert — beim nächsten Besuch wieder da. Perfekt für Coach-PDFs.',
      pos: 'bottom',
    },
    {
      target: '#pdf-btn',
      title: '📄 PDF für Klient:innen',
      text: 'Browser-Druck → PDF mit deinem Logo, Coach-Name, Klient-Name und Datum im Header. Sauberes Dokument statt WhatsApp-Screenshot.',
      pos: 'bottom',
    },
    {
      target: '#share-btn',
      title: '🔗 Gebrandeten Link teilen',
      text: 'URL enthält dein Branding + Plan. Klient öffnet den Link → sieht deinen Plan in deinen Farben, mit deinem Logo. Kein Download, kein Account.',
      pos: 'bottom',
    },
    {
      target: '#library-btn',
      title: '🚀 Los geht\'s',
      text: 'Klick jetzt auf <strong>Bibliothek</strong> und wähl einen Plan. Oder schreib einen eigenen im Editor — die Syntax findest du auf <a href="https://github.com/oxscience/wodl#syntax" target="_blank" style="color:var(--primary)">GitHub</a>.',
      pos: 'bottom',
    },
  ];

  let tourIndex = 0;
  let tourActive = false;

  function startTour() {
    tourIndex = 0;
    tourActive = true;
    document.getElementById('tour-backdrop').classList.add('active');
    // Modals schließen falls offen
    closeLibrary();
    document.getElementById('branding-panel').classList.remove('open');
    renderTourStep();
    localStorage.setItem('wodl_tour_started', '1');
  }

  function endTour() {
    tourActive = false;
    document.getElementById('tour-backdrop').classList.remove('active');
    localStorage.setItem('wodl_tour_completed', '1');
  }

  function tourNext() {
    if (tourIndex < TOUR_STEPS.length - 1) {
      tourIndex++;
      renderTourStep();
    } else {
      endTour();
      // Beim letzten Schritt: öffne direkt die Bibliothek
      setTimeout(() => openLibrary(), 300);
    }
  }

  function tourPrev() {
    if (tourIndex > 0) {
      tourIndex--;
      renderTourStep();
    }
  }

  function renderTourStep() {
    const step = TOUR_STEPS[tourIndex];
    const tip = document.getElementById('tour-tooltip');
    const hi = document.getElementById('tour-highlight');

    document.getElementById('tour-step-num').textContent = `Schritt ${tourIndex + 1} von ${TOUR_STEPS.length}`;
    document.getElementById('tour-title').textContent = step.title;
    document.getElementById('tour-text').innerHTML = step.text;

    // Progress dots
    const progress = document.getElementById('tour-progress');
    progress.innerHTML = '';
    TOUR_STEPS.forEach((_, i) => {
      const dot = document.createElement('div');
      dot.className = 'tour-dot' + (i === tourIndex ? ' active' : '');
      progress.appendChild(dot);
    });

    // Buttons
    document.getElementById('tour-prev').disabled = (tourIndex === 0);
    document.getElementById('tour-next').textContent =
      (tourIndex === TOUR_STEPS.length - 1) ? 'Fertig ✓' : 'Weiter →';

    // Clear arrow classes
    tip.className = 'tour-tooltip';

    // Mobile: kein Highlight-Hole, kein Pfeil, Tooltip immer zentriert
    const isMobile = window.matchMedia('(max-width: 768px)').matches;

    if (isMobile || !step.target || step.pos === 'center') {
      hi.style.display = 'none';
      tip.style.top = '50%';
      tip.style.left = '50%';
      tip.style.transform = 'translate(-50%, -50%)';
    } else {
      hi.style.display = 'block';
      const el = document.querySelector(step.target);
      if (!el) { tip.style.display = 'none'; return; }
      const r = el.getBoundingClientRect();
      const pad = 6;
      hi.style.top = (r.top - pad) + 'px';
      hi.style.left = (r.left - pad) + 'px';
      hi.style.width = (r.width + pad * 2) + 'px';
      hi.style.height = (r.height + pad * 2) + 'px';

      // Tooltip-Position
      const tipW = 360;
      const tipEstH = 220;
      tip.style.transform = 'none';
      if (step.pos === 'bottom') {
        tip.style.top = (r.bottom + 16) + 'px';
        tip.style.left = Math.min(window.innerWidth - tipW - 20, Math.max(20, r.left)) + 'px';
        tip.classList.add('arrow-top');
      } else if (step.pos === 'top') {
        tip.style.top = (r.top - tipEstH - 16) + 'px';
        tip.style.left = Math.min(window.innerWidth - tipW - 20, Math.max(20, r.left)) + 'px';
        tip.classList.add('arrow-bottom');
      } else if (step.pos === 'right') {
        tip.style.top = Math.max(20, r.top) + 'px';
        tip.style.left = (r.right + 16) + 'px';
        tip.classList.add('arrow-left');
      } else if (step.pos === 'left') {
        tip.style.top = Math.max(20, r.top) + 'px';
        tip.style.left = (r.left - tipW - 16) + 'px';
        tip.classList.add('arrow-right');
      }
    }
    tip.style.display = 'block';
  }

  // Keyboard-Navigation
  document.addEventListener('keydown', (e) => {
    if (!tourActive) return;
    if (e.key === 'ArrowRight' || e.key === 'Enter') { e.preventDefault(); tourNext(); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); tourPrev(); }
    else if (e.key === 'Escape') { e.preventDefault(); endTour(); }
  });

  // Re-Render bei Resize (Highlight-Position aktualisieren)
  window.addEventListener('resize', () => {
    if (tourActive) renderTourStep();
  });

  // Auto-Start für neue User (statt Library-Auto-Open)
  function maybeAutoStartTour() {
    if (!localStorage.getItem('wodl_tour_started')) {
      setTimeout(() => startTour(), 500);
    }
  }

  editor.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      parseAndRender();
      saveToStorage();
    }, 300);
  });

  // ===== Branding =====
  const BRAND_KEYS = ['primary', 'logo', 'coach', 'client', 'theme'];
  const defaults = {
    primary: '#6c8cff',
    logo: '',
    coach: '',
    client: '',
    theme: 'dark',
  };

  function getBrand() {
    const urlParams = new URLSearchParams(location.search);
    const stored = JSON.parse(localStorage.getItem('wodl_brand') || '{}');
    const brand = { ...defaults, ...stored };
    BRAND_KEYS.forEach(k => {
      if (urlParams.has(k)) brand[k] = urlParams.get(k);
    });
    return brand;
  }

  function applyBrand(brand) {
    // Primary color
    document.documentElement.style.setProperty('--primary', brand.primary);
    document.documentElement.style.setProperty('--primary2', shade(brand.primary, -15));
    document.getElementById('primary-color').value = brand.primary;
    document.getElementById('primary-hex').value = brand.primary;

    // Theme (dark / light) — Icon zeigt was KOMMT beim Klick: Dark = Sonne, Light = Mond
    document.body.setAttribute('data-theme', brand.theme);
    document.getElementById('theme-btn').innerHTML = brand.theme === 'dark' ? '&#9728;' : '&#9790;';

    // Logo
    const logoImg = document.getElementById('brand-logo');
    const printLogo = document.getElementById('print-logo');
    if (brand.logo) {
      logoImg.src = brand.logo;
      logoImg.style.display = 'block';
      printLogo.src = brand.logo;
    } else {
      logoImg.style.display = 'none';
      printLogo.removeAttribute('src');
    }
    document.getElementById('logo-url').value = brand.logo;

    // Coach / Client
    document.getElementById('coach-name').value = brand.coach;
    document.getElementById('client-name').value = brand.client;
    document.getElementById('print-coach').textContent = brand.coach || '';
    document.getElementById('print-client').textContent = brand.client ? 'Für: ' + brand.client : '';
    document.getElementById('print-date').textContent = new Date().toLocaleDateString('de-DE');

    // Active theme swatch
    document.querySelectorAll('.theme-swatch').forEach(sw => {
      sw.classList.toggle('active', sw.dataset.primary === brand.primary);
    });
  }

  function saveBrand() {
    const brand = {
      primary: document.getElementById('primary-hex').value,
      logo: document.getElementById('logo-url').value,
      coach: document.getElementById('coach-name').value,
      client: document.getElementById('client-name').value,
      theme: document.body.getAttribute('data-theme'),
    };
    localStorage.setItem('wodl_brand', JSON.stringify(brand));
    applyBrand(brand);
  }

  function toggleBranding() {
    document.getElementById('branding-panel').classList.toggle('open');
  }

  function toggleTheme() {
    const cur = document.body.getAttribute('data-theme');
    const next = cur === 'dark' ? 'light' : 'dark';
    // Harter Cut: alle Transitions kurz aussetzen, damit das Theme ohne Fade umspringt
    document.documentElement.classList.add('no-transitions');
    document.body.setAttribute('data-theme', next);
    document.getElementById('theme-btn').innerHTML = next === 'dark' ? '&#9728;' : '&#9790;';
    saveBrand();
    // Reflow erzwingen, dann Transitions nach 1 Frame wieder aktivieren
    void document.documentElement.offsetHeight;
    requestAnimationFrame(() => {
      document.documentElement.classList.remove('no-transitions');
    });
  }

  function resetBranding() {
    localStorage.removeItem('wodl_brand');
    applyBrand(defaults);
  }

  function shade(hex, percent) {
    const num = parseInt(hex.replace('#',''), 16);
    const amt = Math.round(2.55 * percent);
    const R = Math.max(0, Math.min(255, (num >> 16) + amt));
    const G = Math.max(0, Math.min(255, ((num >> 8) & 0xFF) + amt));
    const B = Math.max(0, Math.min(255, (num & 0xFF) + amt));
    return '#' + (0x1000000 + R*0x10000 + G*0x100 + B).toString(16).slice(1);
  }

  // Branding-Inputs verdrahten
  function wireBrandingInputs() {
    const picker = document.getElementById('primary-color');
    const hex = document.getElementById('primary-hex');
    picker.addEventListener('input', () => { hex.value = picker.value; saveBrand(); });
    hex.addEventListener('change', () => {
      if (/^#[0-9a-fA-F]{6}$/.test(hex.value)) { picker.value = hex.value; saveBrand(); }
    });
    ['logo-url', 'coach-name', 'client-name'].forEach(id => {
      document.getElementById(id).addEventListener('change', saveBrand);
    });
  }

  // Theme-Swatches
  function renderThemeSwatches() {
    const grid = document.getElementById('theme-grid');
    Object.entries(themes).forEach(([name, cfg]) => {
      const sw = document.createElement('div');
      sw.className = 'theme-swatch';
      sw.style.background = cfg.primary;
      sw.dataset.primary = cfg.primary;
      sw.title = name;
      sw.onclick = () => {
        document.getElementById('primary-hex').value = cfg.primary;
        document.getElementById('primary-color').value = cfg.primary;
        saveBrand();
      };
      grid.appendChild(sw);
    });
  }

  // ===== Editor Persistenz =====
  function saveToStorage() {
    localStorage.setItem('wodl_content', editor.value);
  }

  function loadFromStorage() {
    const urlParams = new URLSearchParams(location.search);
    if (urlParams.has('plan')) {
      try { editor.value = decodeURIComponent(urlParams.get('plan')); return; }
      catch(e) { /* fall through */ }
    }
    const stored = localStorage.getItem('wodl_content');
    editor.value = stored || sample;
  }

  // ===== Share Link =====
  function copyShareLink() {
    const brand = JSON.parse(localStorage.getItem('wodl_brand') || '{}');
    const url = new URL(location.href);
    url.search = '';
    if (brand.primary && brand.primary !== defaults.primary) url.searchParams.set('primary', brand.primary);
    if (brand.logo) url.searchParams.set('logo', brand.logo);
    if (brand.coach) url.searchParams.set('coach', brand.coach);
    if (brand.theme && brand.theme !== defaults.theme) url.searchParams.set('theme', brand.theme);
    // Plan ist oft zu groß für URL — nur bei kurzen Plänen mitgeben
    if (editor.value.length < 1500) {
      url.searchParams.set('plan', encodeURIComponent(editor.value));
    }
    navigator.clipboard.writeText(url.toString()).then(() => {
      const btn = event.target;
      const orig = btn.textContent;
      btn.textContent = 'Kopiert ✓';
      setTimeout(() => btn.textContent = orig, 1500);
    });
  }

  // ===== Library =====
  let libraryData = [];
  let currentLibCat = 'training';

  const LIB_INTROS = {
    training: 'Evidenzbasierte Trainingspläne — jede Kachel zeigt die Peer-Review-Quelle, im Plan-Kommentar steht die vollständige APA-Zitation. Lade einen Plan, passe Gewichte und Progression an, drucke ihn als PDF für dich oder deine Klient:innen.',
    rehab: 'Klinische Reha-Protokolle als Referenz für Physiotherapeut:innen und Sportärzt:innen. Alle Protokolle sind phasiert, mit Meilensteinen und den Original-Quellen im Plan-Kommentar. Ersetzen KEINE individuelle Betreuung.',
  };

  async function loadLibrary() {
    if (libraryData.length > 0) return;
    try {
      const res = await fetch('/api/examples');
      libraryData = await res.json();
    } catch(e) {
      console.error('Library laden fehlgeschlagen:', e);
    }
  }

  function renderLibrary(cat) {
    currentLibCat = cat;
    document.getElementById('lib-intro').textContent = LIB_INTROS[cat];
    const grid = document.getElementById('lib-grid');
    grid.innerHTML = '';
    const plans = libraryData.filter(p => p.category === cat);
    plans.forEach(p => {
      const card = document.createElement('div');
      card.className = 'plan-card';
      card.onclick = () => loadPlan(p.file);

      const tags = [];
      if (p.level) tags.push(`<span class="tag">${p.level}</span>`);
      if (p.freq) tags.push(`<span class="tag">${p.freq}</span>`);
      if (p.split) tags.push(`<span class="tag">${p.split}</span>`);
      if (p.indication) tags.push(`<span class="tag primary">${p.indication}</span>`);

      card.innerHTML = `
        <h3>${p.title}</h3>
        <div class="meta">${tags.join('')}</div>
        <p>${p.desc}</p>
        ${p.source ? `<div class="source">📖 ${p.source}</div>` : ''}
      `;
      grid.appendChild(card);
    });
  }

  function switchLibTab(cat, btn) {
    document.querySelectorAll('.lib-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    renderLibrary(cat);
  }

  async function openLibrary() {
    await loadLibrary();
    renderLibrary(currentLibCat);
    document.getElementById('lib-modal').classList.add('open');
  }

  function closeLibrary() {
    document.getElementById('lib-modal').classList.remove('open');
  }

  async function loadPlan(fileName) {
    try {
      const res = await fetch('/api/examples/' + encodeURIComponent(fileName));
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const text = await res.text();
      editor.value = text;
      parseAndRender();
      saveToStorage();
      closeLibrary();
    } catch(e) {
      alert('Plan konnte nicht geladen werden: ' + e.message);
    }
  }

  // ESC schließt Modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLibrary();
  });

  // ===== Init =====
  renderThemeSwatches();
  wireBrandingInputs();
  applyBrand(getBrand());
  loadFromStorage();
  parseAndRender();
  maybeAutoStartTour();
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

        if "**" in stripped or ("_" in stripped and not stripped.startswith("|")):
            stripped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            stripped = re.sub(r'(?<![\w])_([^_\n]+)_(?![\w])', r'<em>\1</em>', stripped)
            html_lines.append(f"<p>{stripped}</p>")
            continue

        if stripped.startswith("> "):
            html_lines.append(f"<blockquote>{stripped[2:]}</blockquote>")
            continue

        if stripped.startswith("|") and set(stripped.replace("|", "").strip()) <= {"-", " "}:
            continue

        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # Inline markup in cells: _italic_ -> <em>italic</em>
            cells = [re.sub(r'(?<![\w])_([^_\n]+)_(?![\w])', r'<em>\1</em>', c) for c in cells]
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

        if in_table and not stripped.startswith("|"):
            html_lines.append("</tbody></table>")
            in_table = False
            header_done = False

        if stripped.startswith("- "):
            html_lines.append(f"<div class='warning'>{stripped}</div>")
            continue

        if not stripped:
            continue

    if in_table:
        html_lines.append("</tbody></table>")

    return "\n".join(html_lines)


@app.route("/")
def index():
    plan = parse(SAMPLE_WODL)
    initial_html = _md_to_html(to_markdown(plan))
    return render_template_string(
        HTML,
        sample_json=json.dumps(SAMPLE_WODL),
        themes_json=json.dumps(THEMES),
        initial_output=initial_html,
    )


@app.route("/parse", methods=["POST"])
def parse_wodl():
    wod_text = request.form.get("wodl", "")
    fmt = request.form.get("format", "markdown")

    if not wod_text.strip():
        return "<p style='color: var(--text2)'>Trainingsplan eingeben...</p>"

    try:
        plan = parse(wod_text)
    except Exception as e:
        return f"<div class='error-msg'>Parser-Fehler: {e}</div>"

    if fmt == "json":
        return f"<pre>{to_json(plan)}</pre>"

    if fmt == "cycle":
        md = to_cycle_matrix(plan)
        return f'<div class="cycle-view">{_md_to_html(md)}</div>'

    if fmt == "summary":
        lines = []
        lines.append(f"<strong>Plan:</strong> {plan.name or '(unbenannt)'}<br>")
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
            lines.append(f"<strong>[{session.name}]</strong> {days} — {ex_count} Übungen<br>")
        if plan.warnings:
            lines.append("<br><strong style='color: var(--orange)'>Warnings:</strong><br>")
            for w in plan.warnings:
                lines.append(f"<div class='warning'>- {w}</div>")
        return "".join(lines)

    md = to_markdown(plan)
    return _md_to_html(md)


@app.route("/api/examples")
def list_examples():
    """Liste aller verfügbaren Beispielpläne mit Metadata."""
    return jsonify(EXAMPLE_LIBRARY)


@app.route("/api/examples/<name>")
def get_example(name: str):
    """Rohtext eines Beispielplans."""
    # Pfad-Traversal verhindern
    if "/" in name or ".." in name or "\\" in name:
        abort(400)
    safe_name = name.replace(".wodl", "")
    path = EXAMPLES_DIR / f"{safe_name}.wodl"
    if not path.is_file() or path.parent != EXAMPLES_DIR:
        abort(404)
    return path.read_text(encoding="utf-8"), 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/healthz")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5051))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
