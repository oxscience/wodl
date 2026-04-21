"""
WODL Parser — Workout Definition Language -> structured data.

Parses `.wodl` text blocks into a structured Python dict / JSON
that can be consumed by apps, rendered as Markdown tables,
or exported to calendar events.

Usage:
    from wodl import parse

    plan = parse(wod_text)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Literal

from wodl.registry import resolve, resolve_fuzzy

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

GroupKind = Literal["superset", "circuit", "giant"]


@dataclass
class ExerciseLine:
    """A single exercise within a session."""

    raw_name: str
    canonical_name: str | None  # resolved via registry
    display_name: str = ""  # what to render in output (respects user language)
    sets: int | None = None
    reps: str | None = None  # "8", "8-12", "AMRAP", "30s"
    intensity: str | None = None  # "@RPE8", "@70%", "@60kg", "@BW"
    rest: str | None = None  # "90s", "2m", "60-90s"
    tempo: str | None = None  # "3010"
    progression: str | None = None  # "+2.5kg/w"
    modifiers: list[str] = field(default_factory=list)
    comment: str | None = None


@dataclass
class ExerciseGroup:
    """A group of exercises performed together (superset / circuit / giant)."""

    kind: GroupKind
    exercises: list[ExerciseLine] = field(default_factory=list)


@dataclass
class Session:
    """One training day / session."""

    name: str
    days: list[str] = field(default_factory=list)
    items: list[ExerciseLine | ExerciseGroup] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass
class CycleWeek:
    """Describes one phase within a cycle."""

    weeks: str  # "w1-3", "w4"
    phase: str  # "progress", "deload", "test", etc.


@dataclass
class Plan:
    """Top-level training plan."""

    name: str | None = None
    frequency: str | None = None
    cycle_length: str | None = None
    cycle_phases: list[CycleWeek] = field(default_factory=list)
    unit: str = "kg"
    sessions: list[Session] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

RE_META_PLAN = re.compile(r'^@plan\s+"([^"]+)"', re.IGNORECASE)
RE_META_FREQ = re.compile(r"^@freq\s+(.+)", re.IGNORECASE)
RE_META_CYCLE = re.compile(r"^@cycle\s+(.+)", re.IGNORECASE)
RE_META_UNIT = re.compile(r"^@unit\s+(kg|lb)", re.IGNORECASE)

RE_SESSION = re.compile(r"^---\[(.+?)\]\s*(.*)")

RE_GROUP_OPEN = re.compile(r"^(ss|superset|circuit|giant)\s*\{")
RE_GROUP_CLOSE = re.compile(r"^\}")

RE_NOTE = re.compile(r"^>\s*(.*)")
RE_COMMENT = re.compile(r"^#(?!#)")  # line starting with single #

# Exercise line tokens
RE_SETS_REPS = re.compile(
    r"""
    (?:(\d+)x)?          # optional sets (4x)
    (?:
        (\d+)(?:-(\d+))? # reps or rep range (8, 8-12)
        |(\d+s)           # time-based (30s)
    )
    """,
    re.VERBOSE,
)

RE_SETS_ONLY = re.compile(r"^(\d+)x$")  # e.g. "3x" (AMRAP)
RE_TIME_ONLY = re.compile(r"^(\d+)s$")  # e.g. "60s" standalone
RE_PYRAMID = re.compile(r"^(\d+(?:,\d+){1,5})$")  # reverse pyramid "10,8,6" or "12,10,8,6"

RE_INTENSITY = re.compile(
    r"@(RPE\d+\.?\d*|RIR\d+|ISO|\d+%|\d+(?:\.\d+)?kg|\d+(?:\.\d+)?lb|BW(?:[+-]\d+(?:\.\d+)?kg)?|low|mid|high)",
    re.IGNORECASE,
)
RE_REST = re.compile(r"r(\d+(?:-\d+)?(?:s|m))", re.IGNORECASE)
RE_TEMPO = re.compile(r"t(\d{4})")
RE_PROGRESSION = re.compile(r"\+(\d+(?:\.\d+)?(?:kg|lb|rep|reps?)/w)", re.IGNORECASE)
RE_MODIFIER = re.compile(r"\b(drop|cluster|pause-rep|myo|rest-pause)\b", re.IGNORECASE)

DAY_MAP = {
    "mo": "Mo", "mon": "Mo", "montag": "Mo",
    "di": "Di", "tue": "Di", "dienstag": "Di",
    "mi": "Mi", "wed": "Mi", "mittwoch": "Mi",
    "do": "Do", "thu": "Do", "donnerstag": "Do",
    "fr": "Fr", "fri": "Fr", "freitag": "Fr",
    "sa": "Sa", "sat": "Sa", "samstag": "Sa",
    "so": "So", "sun": "So", "sonntag": "So",
}


# ---------------------------------------------------------------------------
# Parser helpers
# ---------------------------------------------------------------------------


def _parse_days(text: str) -> list[str]:
    """Parse day abbreviations from a string like 'Mo Do'."""
    days = []
    for token in text.strip().split():
        normalized = DAY_MAP.get(token.lower())
        if normalized:
            days.append(normalized)
    return days


def _parse_cycle(text: str) -> tuple[str, list[CycleWeek]]:
    """Parse cycle spec like '4w: w1-3 progress, w4 deload'."""
    parts = text.split(":", 1)
    length = parts[0].strip()
    phases: list[CycleWeek] = []
    if len(parts) > 1:
        for segment in parts[1].split(","):
            segment = segment.strip()
            tokens = segment.split()
            if len(tokens) >= 2:
                phases.append(CycleWeek(weeks=tokens[0], phase=tokens[1]))
    return length, phases


def _parse_exercise_line(line: str) -> ExerciseLine:
    """Parse a single exercise line into an ExerciseLine."""
    # Strip inline comment
    comment = None
    if "#" in line:
        idx = line.index("#")
        comment = line[idx + 1:].strip()
        line = line[:idx].strip()

    tokens = line.split()
    if not tokens:
        return ExerciseLine(raw_name="", canonical_name=None)

    # Strategy: scan tokens consuming known patterns.
    # What remains is the exercise name.
    consumed = set()
    ex = ExerciseLine(raw_name="", canonical_name=None, comment=comment)

    for i, tok in enumerate(tokens):
        # Sets x Reps
        if not consumed and RE_SETS_ONLY.match(tok):
            ex.sets = int(tok[:-1])
            ex.reps = "AMRAP"
            consumed.add(i)
            continue

        # Reverse pyramid reps: "10,8,6" = 3 Sätze mit absteigenden Reps
        m = RE_PYRAMID.fullmatch(tok)
        if m and i not in consumed:
            reps_list = tok.split(",")
            ex.sets = len(reps_list)
            ex.reps = tok  # behält die Originalnotation "10,8,6"
            consumed.add(i)
            continue

        m = RE_SETS_REPS.fullmatch(tok)
        if m and i not in consumed:
            ex.sets = int(m.group(1)) if m.group(1) else 1
            if m.group(4):  # time-based
                ex.reps = m.group(4)
            elif m.group(2):
                ex.reps = f"{m.group(2)}-{m.group(3)}" if m.group(3) else m.group(2)
            consumed.add(i)
            continue

        if RE_TIME_ONLY.match(tok) and i not in consumed:
            ex.sets = 1
            ex.reps = tok
            consumed.add(i)
            continue

        m = RE_INTENSITY.match(tok)
        if m and i not in consumed:
            ex.intensity = tok
            consumed.add(i)
            continue

        m = RE_REST.fullmatch(tok)
        if m and i not in consumed:
            ex.rest = m.group(1)
            consumed.add(i)
            continue

        m = RE_TEMPO.fullmatch(tok)
        if m and i not in consumed:
            ex.tempo = m.group(1)
            consumed.add(i)
            continue

        m = RE_PROGRESSION.fullmatch(tok)
        if m and i not in consumed:
            ex.progression = m.group(0)
            consumed.add(i)
            continue

        m = RE_MODIFIER.fullmatch(tok)
        if m and i not in consumed:
            ex.modifiers.append(tok.lower())
            consumed.add(i)
            continue

    # Remaining tokens form the exercise name
    name_tokens = [tokens[i] for i in range(len(tokens)) if i not in consumed]
    raw_name = " ".join(name_tokens).strip()
    ex.raw_name = raw_name

    # Resolve canonical name. Exact match (canonical or alias) respects the
    # user's language in output; fuzzy match overrides with canonical so
    # typos get corrected.
    canonical_exact = resolve(raw_name)
    if canonical_exact:
        ex.canonical_name = canonical_exact
        ex.display_name = raw_name
    else:
        canonical_fuzzy = resolve_fuzzy(raw_name, threshold=0.7)
        ex.canonical_name = canonical_fuzzy
        ex.display_name = canonical_fuzzy if canonical_fuzzy else raw_name

    return ex


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------


def parse(text: str) -> Plan:
    """Parse a WOD text block into a Plan structure.

    Args:
        text: The WOD source text (multiline string).

    Returns:
        A Plan dataclass with all parsed data.
    """
    plan = Plan()
    lines = text.splitlines()
    current_session: Session | None = None
    group_stack: list[ExerciseGroup] | None = None
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        i += 1

        # Skip empty lines
        if not stripped:
            continue

        # Comments
        if RE_COMMENT.match(stripped):
            continue

        # --- Metadata ---
        m = RE_META_PLAN.match(stripped)
        if m:
            plan.name = m.group(1)
            continue

        m = RE_META_FREQ.match(stripped)
        if m:
            plan.frequency = m.group(1).strip()
            continue

        m = RE_META_CYCLE.match(stripped)
        if m:
            plan.cycle_length, plan.cycle_phases = _parse_cycle(m.group(1))
            continue

        m = RE_META_UNIT.match(stripped)
        if m:
            plan.unit = m.group(1).lower()
            continue

        # --- Session header ---
        m = RE_SESSION.match(stripped)
        if m:
            current_session = Session(
                name=m.group(1).strip(),
                days=_parse_days(m.group(2)) if m.group(2) else [],
            )
            plan.sessions.append(current_session)
            group_stack = None
            continue

        # --- Notes ---
        m = RE_NOTE.match(stripped)
        if m:
            if current_session:
                current_session.notes.append(m.group(1))
            continue

        # --- Group open ---
        m = RE_GROUP_OPEN.match(stripped)
        if m:
            kind_raw = m.group(1).lower()
            kind_map = {
                "ss": "superset", "superset": "superset",
                "circuit": "circuit", "giant": "giant",
            }
            kind = kind_map.get(kind_raw, "superset")
            group_stack = []
            group = ExerciseGroup(kind=kind)
            if current_session:
                current_session.items.append(group)
                group_stack = [group]
            continue

        # --- Group close ---
        if RE_GROUP_CLOSE.match(stripped):
            group_stack = None
            continue

        # --- Exercise line ---
        if stripped and current_session is not None:
            ex = _parse_exercise_line(stripped)
            if ex.raw_name:
                if group_stack:
                    group_stack[-1].exercises.append(ex)
                else:
                    current_session.items.append(ex)

                # Warn about unresolved names
                if ex.canonical_name is None and ex.raw_name:
                    plan.warnings.append(
                        f"Unknown exercise: '{ex.raw_name}' "
                        f"(in session '{current_session.name}')"
                    )

    return plan


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------


def to_dict(plan: Plan) -> dict:
    """Convert a Plan to a JSON-serializable dict."""
    return asdict(plan)


def to_json(plan: Plan, indent: int = 2) -> str:
    """Convert a Plan to a JSON string."""
    return json.dumps(to_dict(plan), indent=indent, ensure_ascii=False)


def to_markdown(plan: Plan) -> str:
    """Render a Plan as readable Markdown tables."""
    lines: list[str] = []

    # Header
    if plan.name:
        lines.append(f"# {plan.name}")
    if plan.frequency:
        lines.append(f"**Frequenz:** {plan.frequency}")
    if plan.cycle_length:
        cycle_desc = plan.cycle_length
        if plan.cycle_phases:
            phases = ", ".join(f"{p.weeks} {p.phase}" for p in plan.cycle_phases)
            cycle_desc += f" ({phases})"
        lines.append(f"**Zyklus:** {cycle_desc}")
    lines.append("")

    for session in plan.sessions:
        day_str = " ".join(session.days)
        lines.append(f"## {session.name}" + (f" \u00b7 {day_str}" if day_str else ""))
        lines.append("")
        lines.append("| Exercise | Sets x Reps | Intensity | Rest | Notes |")
        lines.append("|----------|-------------|-----------|------|-------|")

        def _fmt_exercise(ex: ExerciseLine, prefix: str = "") -> str:
            name = prefix + (ex.display_name or ex.canonical_name or ex.raw_name)
            sr = ""
            if ex.sets and ex.reps:
                sr = f"{ex.sets}x{ex.reps}"
            elif ex.reps:
                sr = ex.reps
            intensity = ex.intensity or ""
            rest = ex.rest or ""
            notes_parts = []
            if ex.tempo:
                notes_parts.append(f"Tempo {ex.tempo}")
            if ex.progression:
                notes_parts.append(ex.progression)
            if ex.modifiers:
                notes_parts.extend(ex.modifiers)
            if ex.comment:
                notes_parts.append(ex.comment)
            notes = ", ".join(notes_parts)
            return f"| {name} | {sr} | {intensity} | {rest} | {notes} |"

        for item in session.items:
            if isinstance(item, ExerciseGroup):
                label = {
                    "superset": "SS",
                    "circuit": "Circuit",
                    "giant": "Giant",
                }
                for j, ex in enumerate(item.exercises):
                    pfx = f"{label.get(item.kind, 'SS')}: " if j == 0 else "  + "
                    lines.append(_fmt_exercise(ex, pfx))
            else:
                lines.append(_fmt_exercise(item))

        if session.notes:
            lines.append("")
            for note in session.notes:
                lines.append(f"> {note}")
        lines.append("")

    if plan.warnings:
        lines.append("### Warnings")
        for w in plan.warnings:
            lines.append(f"- {w}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cycle matrix — Progression über Wochen projizieren
# ---------------------------------------------------------------------------

RE_CYCLE_WEEKS = re.compile(r"^(\d+)w$", re.IGNORECASE)
RE_WEEK_RANGE = re.compile(r"^w(\d+)(?:-(\d+))?$", re.IGNORECASE)
RE_PROG_KG = re.compile(r"^\+(\d+(?:\.\d+)?)kg/w$", re.IGNORECASE)
RE_PROG_REP = re.compile(r"^\+(\d+)reps?/w$", re.IGNORECASE)
RE_PROG_PCT = re.compile(r"^\+(\d+(?:\.\d+)?)%/w$", re.IGNORECASE)
RE_INT_KG = re.compile(r"^@(\d+(?:\.\d+)?)kg$", re.IGNORECASE)
RE_INT_PCT = re.compile(r"^@(\d+)%$", re.IGNORECASE)
RE_INT_BW_ADD = re.compile(r"^@BW\+(\d+(?:\.\d+)?)kg$", re.IGNORECASE)

# Deload-Standardregel (wenn keine explizite Angabe im Plan): Last -20%, Sets & Reps wie Vorwoche.
DELOAD_LOAD_FACTOR = 0.80


def _total_cycle_weeks(plan: Plan, default: int = 4) -> int:
    """Extrahiert die Anzahl Wochen aus `@cycle 4w: ...`. Fallback: default."""
    if not plan.cycle_length:
        return default
    m = RE_CYCLE_WEEKS.match(plan.cycle_length.strip())
    if m:
        return int(m.group(1))
    return default


def _phase_for_week(week: int, phases: list) -> str | None:
    """Gibt den Phasen-Namen für eine gegebene Woche zurück (progress/deload/...)."""
    for ph in phases:
        m = RE_WEEK_RANGE.match(ph.weeks.strip())
        if not m:
            continue
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) else start
        if start <= week <= end:
            return ph.phase.lower()
    return None


def _parse_load_kg(intensity: str | None) -> tuple[float | None, str]:
    """Extrahiert numerisches kg-Gewicht aus einer Intensity-Angabe.

    Returns:
        (load_kg, suffix) — suffix ist Kontext wie "" oder "BW+" für Bodyweight-Add.
        Gibt (None, intensity) zurück wenn nicht numerisch auflösbar.
    """
    if not intensity:
        return None, ""
    m = RE_INT_KG.match(intensity.strip())
    if m:
        return float(m.group(1)), ""
    m = RE_INT_BW_ADD.match(intensity.strip())
    if m:
        return float(m.group(1)), "BW+"
    return None, intensity


def _parse_progression(prog: str | None) -> tuple[str, float] | None:
    """Parse progression token into (kind, value).

    Returns:
        ("kg", 2.5) für "+2.5kg/w"
        ("rep", 1) für "+1rep/w"
        ("pct", 5.0) für "+5%/w"
        None wenn keine oder nicht parsbar.
    """
    if not prog:
        return None
    s = prog.strip().lstrip("+")
    s = "+" + s  # sicherstellen dass + vorhanden
    m = RE_PROG_KG.match(s)
    if m:
        return ("kg", float(m.group(1)))
    m = RE_PROG_REP.match(s)
    if m:
        return ("rep", float(m.group(1)))
    m = RE_PROG_PCT.match(s)
    if m:
        return ("pct", float(m.group(1)))
    return None


def _project_exercise_week(ex: ExerciseLine, week: int, phase: str | None) -> dict:
    """Projiziert eine Übung auf eine konkrete Trainingswoche.

    Args:
        ex: ExerciseLine
        week: 1-indexierte Wochennummer
        phase: "progress", "deload", "intensity", etc. (oder None)

    Returns:
        dict mit keys: sets, reps, intensity (als String), deload (bool)
    """
    load_kg, load_prefix = _parse_load_kg(ex.intensity)
    prog = _parse_progression(ex.progression)
    is_deload = (phase == "deload")

    # Sets & Reps: default von der Übung übernommen
    sets = ex.sets
    reps = ex.reps

    # Progression anwenden: (week-1) * step, solange es keine Deload-Woche ist
    if prog and not is_deload:
        kind, step = prog
        weeks_progressed = week - 1  # Woche 1 = Start
        if kind == "kg" and load_kg is not None:
            load_kg = load_kg + step * weeks_progressed
        elif kind == "pct" and load_kg is not None:
            load_kg = load_kg * (1 + step / 100) ** weeks_progressed
        elif kind == "rep" and reps:
            try:
                # Einfachste Form: reps ist "8" oder "8-12" → heuristisch Endwert
                base = reps.split("-")[-1] if "-" in reps else reps
                base_n = int(base.rstrip("s"))
                reps = str(base_n + int(step * weeks_progressed))
            except (ValueError, AttributeError):
                pass

    # Deload: Last -20% von der fortgeschrittenen Progression bzw. Start
    if is_deload and load_kg is not None:
        # Nimm Last der letzten Progress-Woche (week-1) und reduziere
        if prog and prog[0] == "kg":
            prior_load = load_kg + prog[1] * (week - 2)
            load_kg = prior_load * DELOAD_LOAD_FACTOR
        elif prog and prog[0] == "pct":
            prior_load = load_kg * (1 + prog[1] / 100) ** max(0, week - 2)
            load_kg = prior_load * DELOAD_LOAD_FACTOR
        else:
            load_kg = load_kg * DELOAD_LOAD_FACTOR

    # Intensity-String neu bauen
    if load_kg is not None:
        # Runde auf 0.5kg
        rounded = round(load_kg * 2) / 2
        intensity_str = f"@{load_prefix}{rounded:g}kg"
    else:
        intensity_str = ex.intensity or ""

    return {
        "sets": sets,
        "reps": reps,
        "intensity": intensity_str,
        "deload": is_deload,
    }


def to_cycle_matrix(plan: Plan) -> str:
    """Rendert einen Plan als Wochen-Matrix (Markdown-Tabelle).

    Zeigt pro Session eine Tabelle: Zeilen = Übungen, Spalten = Wochen.
    Progressions-Tokens (+2.5kg/w etc.) werden automatisch über die Wochen
    angewandt. Deload-Wochen (aus @cycle) werden mit -20% Last markiert.
    """
    lines: list[str] = []
    total_weeks = _total_cycle_weeks(plan, default=4)

    if plan.name:
        lines.append(f"# {plan.name} — Wochen-Matrix")
    if plan.cycle_length:
        cycle_desc = plan.cycle_length
        if plan.cycle_phases:
            phases = ", ".join(f"{p.weeks} {p.phase}" for p in plan.cycle_phases)
            cycle_desc += f" ({phases})"
        lines.append(f"**Zyklus:** {cycle_desc}")
    lines.append("")
    lines.append(f"_Progression wird pro Woche automatisch angewandt. **💤 Deload** = Last -{round((1-DELOAD_LOAD_FACTOR)*100)}% vs. Vorwoche · **🔥 Intensity** = Peak-/Test-Woche · **🎯 Test** = 1RM-Testing_")
    lines.append("")

    # Header-Zellen: Übung + W1, W2, ... Wn
    week_headers = []
    for w in range(1, total_weeks + 1):
        phase = _phase_for_week(w, plan.cycle_phases)
        label = f"W{w}"
        if phase == "deload":
            label += " 💤"
        elif phase == "intensity":
            label += " 🔥"
        elif phase == "test":
            label += " 🎯"
        week_headers.append(label)

    for session in plan.sessions:
        day_str = " ".join(session.days)
        lines.append(f"## {session.name}" + (f" \u00b7 {day_str}" if day_str else ""))
        lines.append("")

        # Tabellen-Header
        header_row = "| Übung | Sets×Reps | " + " | ".join(week_headers) + " |"
        sep_row = "|" + "|".join(["---"] * (len(week_headers) + 2)) + "|"
        lines.append(header_row)
        lines.append(sep_row)

        def render_exercise_row(ex: ExerciseLine, prefix: str = "") -> str:
            name = prefix + (ex.display_name or ex.canonical_name or ex.raw_name)
            base_sets_reps = ""
            if ex.sets and ex.reps:
                base_sets_reps = f"{ex.sets}×{ex.reps}"
            elif ex.reps:
                base_sets_reps = ex.reps

            cells = [name, base_sets_reps]
            for w in range(1, total_weeks + 1):
                phase = _phase_for_week(w, plan.cycle_phases)
                proj = _project_exercise_week(ex, w, phase)
                intensity = proj["intensity"]
                if proj["deload"]:
                    cell = f"_{intensity}_" if intensity else "_Deload_"
                else:
                    cell = intensity if intensity else "—"
                # Falls reps sich durch +rep/w geändert haben, zeig es
                if proj.get("reps") and proj["reps"] != ex.reps:
                    cell = f"{proj['reps']} reps {cell}".strip()
                cells.append(cell)
            return "| " + " | ".join(cells) + " |"

        for item in session.items:
            if isinstance(item, ExerciseGroup):
                label_map = {"superset": "SS", "circuit": "Circuit", "giant": "Giant"}
                for j, sub in enumerate(item.exercises):
                    pfx = f"{label_map.get(item.kind, 'SS')}: " if j == 0 else "  + "
                    lines.append(render_exercise_row(sub, pfx))
            else:
                lines.append(render_exercise_row(item))

        lines.append("")

    return "\n".join(lines)
