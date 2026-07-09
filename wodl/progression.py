"""Progression engine — projiziert Trainingspläne über Wochen zu einem Block.

Zwei Pfade, eine Config:

- **Semantisch** (WODL): Der geparste Plan wird pro Woche mit konkreten
  Sets/Reps/Lasten projiziert und als gültiges WODL re-emittiert. Damit
  funktionieren alle bestehenden Renderer (Tabelle, PDF) pro Woche.
- **Freitext**: Zeilenbasierte Regex-Transformation für beliebige Pläne
  (kein Parsing nötig, Coach-Stil bleibt erhalten). Portiert aus Progressio.

Evidenz-Verankerung (Hintergrund, nicht UI):
- Last- und Rep-Progression sind für Hypertrophie gleichwertig
  (Plotkin et al. 2022, 10.7717/peerj.14142) — beides ist wählbar.
- Für Maximalkraft sind schwere Lasten spezifisch überlegen
  (Schoenfeld et al. 2017, 10.1519/JSC.0000000000002200) — das
  Kraft-Preset progressiert Last statt Reps.
- Doppelprogression (Reps bis Schwelle, dann Last hoch, Reps zurück) ist
  Praktiker-Standard (Helms, Muscle & Strength Pyramid); die Schwelle
  selbst ist Konvention und daher konfigurierbar.
- Deload: Praktiker-Konsens = alle 4-8 Wochen, Volumen deutlich runter,
  Last moderat oder gehalten (Bell et al. 2023, 10.1186/s40798-023-00633-0).
  Es gibt keine "richtige" Definition — deshalb konfigurierbar.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from wodl.parser import (
    ExerciseGroup,
    ExerciseLine,
    Plan,
    _parse_load_kg,
    _parse_progression,
    _phase_for_week,
    _total_cycle_weeks,
    parse,
)

GOALS = ("hypertrophie", "kraft", "ausdauer")
DELOAD_RHYTHMS = ("auto", "none", "last", "every4", "every5", "every6")


@dataclass
class ProgressionConfig:
    """Alle Stellschrauben des Progressions-Blocks."""

    weeks: int = 4
    goal: str = "hypertrophie"      # hypertrophie | kraft | ausdauer
    rep_increment: int = 1          # +Reps pro Aufbau-Woche
    rep_threshold: int | None = None  # Umschaltpunkt Doppelprogression; None = Range-Top bzw. 15
    load_increment: float = 2.5     # kg pro Last-Steigerung
    time_increment: int = 10        # +Sekunden pro Aufbau-Woche (Zeit-Übungen)
    deload_rhythm: str = "auto"     # auto | none | last | every4 | every5 | every6
    deload_sets_factor: float = 0.5   # Volumen: Sätze × Faktor
    deload_load_factor: float = 1.0   # Last: × Faktor (1.0 = Last halten)

    def threshold_for(self, range_top: int | None) -> int:
        if self.rep_threshold:
            return self.rep_threshold
        if range_top:
            return range_top
        return 15


@dataclass
class WeekResult:
    """Eine projizierte Woche des Blocks."""

    week: int
    kind: str    # start | build | deload
    label: str
    text: str    # WODL (semantisch) bzw. Klartext (Freitext)


# ---------------------------------------------------------------------------
# Wochen-Schema
# ---------------------------------------------------------------------------


def week_kinds(config: ProgressionConfig, plan: Plan | None = None) -> list[str]:
    """Liefert pro Woche 'build' oder 'deload' (Woche 1 ist immer 'start')."""
    rhythm = config.deload_rhythm
    if rhythm == "auto":
        # Wenn der Plan selbst einen Zyklus mit passender Länge definiert,
        # respektieren wir seine Phasen; sonst: letzte Woche = Deload ab 4 Wochen.
        if plan is not None and plan.cycle_phases and _total_cycle_weeks(plan) == config.weeks:
            kinds = []
            for w in range(1, config.weeks + 1):
                phase = _phase_for_week(w, plan.cycle_phases)
                kinds.append("deload" if phase == "deload" else "build")
            kinds[0] = "start"
            return kinds
        rhythm = "last" if config.weeks >= 4 else "none"

    kinds = []
    for w in range(1, config.weeks + 1):
        if rhythm == "last" and w == config.weeks and config.weeks >= 2:
            kinds.append("deload")
        elif rhythm in ("every4", "every5", "every6"):
            n = int(rhythm[-1])
            kinds.append("deload" if w % n == 0 else "build")
        else:
            kinds.append("build")
    kinds[0] = "start"
    return kinds


def _week_label(kind: str, goal: str) -> str:
    if kind == "start":
        return "Ausgangsplan"
    if kind == "deload":
        return "Deload — Volumen ↓"
    if goal == "kraft":
        return "Aufbau — Last ↑"
    return "Aufbau — Reps ↑"


# ---------------------------------------------------------------------------
# Semantischer Pfad: Reps-Parsing + Übungs-Zustand
# ---------------------------------------------------------------------------


RE_REPS_INT = re.compile(r"^(\d+)$")
RE_REPS_RANGE = re.compile(r"^(\d+)-(\d+)$")
RE_REPS_TIME = re.compile(r"^(\d+)s$")
RE_REPS_PYRAMID = re.compile(r"^\d+(?:,\d+)+$")


def _parse_reps(reps: str | None):
    """Zerlegt den Reps-String in (kind, value)."""
    if not reps:
        return ("none", None)
    s = reps.strip()
    m = RE_REPS_INT.match(s)
    if m:
        return ("int", int(m.group(1)))
    m = RE_REPS_RANGE.match(s)
    if m:
        return ("range", (int(m.group(1)), int(m.group(2))))
    m = RE_REPS_TIME.match(s)
    if m:
        return ("time", int(m.group(1)))
    if RE_REPS_PYRAMID.match(s):
        return ("pyramid", [int(x) for x in s.split(",")])
    return ("raw", s)


def _round_load(kg: float) -> float:
    return round(kg * 2) / 2


class _ExState:
    """Zustand einer Übung über den Block (Reps/Last laufen Woche für Woche mit)."""

    def __init__(self, ex: ExerciseLine, config: ProgressionConfig):
        self.ex = ex
        self.config = config
        self.kind, val = _parse_reps(ex.reps)
        self.load_kg, self.load_prefix = _parse_load_kg(ex.intensity)
        self.token = _parse_progression(ex.progression)

        if self.kind == "int":
            self.rep_start = val
            self.reps = val
            self.threshold = config.threshold_for(None)
        elif self.kind == "range":
            self.rep_start = val[0]
            self.reps = val[0]
            self.threshold = config.threshold_for(val[1])
        elif self.kind == "pyramid":
            self.pyramid = list(val)
        elif self.kind == "time":
            self.seconds = val
        # Merken, was diese Woche passiert ist (für Kommentar im Output)
        self.note: str | None = None

    # -- Aufbau-Woche: Zustand einen Schritt weiterdrehen --------------------

    def advance(self):
        self.note = None
        cfg = self.config

        # Explizites Token an der Übung gewinnt immer (+2.5kg/w, +1rep/w, +5%/w)
        if self.token:
            t_kind, step = self.token
            if t_kind == "kg":
                if self.load_kg is not None:
                    self.load_kg += step
                else:
                    # Kein numerisches Gewicht (@RPE/@%) → Anweisung statt Zahl
                    self.note = f"Last +{step:g} kg vs. Vorwoche"
            elif t_kind == "pct":
                if self.load_kg is not None:
                    self.load_kg *= 1 + step / 100
                else:
                    self.note = f"Last +{step:g} % vs. Vorwoche"
            elif t_kind == "rep" and self.kind in ("int", "range"):
                self.reps += int(step)
            return

        if self.kind == "time":
            self.seconds += cfg.time_increment
            return

        if cfg.goal == "kraft":
            if self.load_kg is not None:
                self.load_kg += cfg.load_increment
            else:
                self.note = f"Last +{cfg.load_increment:g} kg vs. Vorwoche"
            return

        if self.kind == "pyramid":
            self.pyramid = [n + cfg.rep_increment for n in self.pyramid]
            return

        if self.kind in ("int", "range"):
            new = self.reps + cfg.rep_increment
            if cfg.goal == "hypertrophie" and new > self.threshold:
                # Doppelprogression: Schwelle erreicht → Last hoch, Reps zurück
                if self.load_kg is not None:
                    self.load_kg += cfg.load_increment
                    self.note = f"Last +{cfg.load_increment:g} kg, Reps zurück auf {self.rep_start}"
                else:
                    self.note = (
                        f"Schwelle {self.threshold} erreicht: Last erhöhen "
                        f"(+{cfg.load_increment:g} kg), zurück auf {self.rep_start} Wdh"
                    )
                self.reps = self.rep_start
            else:
                self.reps = new

    # -- Snapshot der Woche rendern ------------------------------------------

    def project(self, deload: bool) -> dict:
        cfg = self.config
        ex = self.ex

        sets = ex.sets
        if deload and sets:
            sets = max(1, round(sets * cfg.deload_sets_factor))

        if self.kind == "int" or self.kind == "range":
            reps = str(self.reps)
        elif self.kind == "time":
            reps = f"{self.seconds}s"
        elif self.kind == "pyramid":
            reps = ",".join(str(n) for n in self.pyramid)
        elif self.kind == "raw":
            reps = ex.reps
        else:
            reps = None

        if self.load_kg is not None:
            kg = self.load_kg * cfg.deload_load_factor if deload else self.load_kg
            intensity = f"@{self.load_prefix}{_round_load(kg):g}kg"
        else:
            intensity = ex.intensity

        return {
            "sets": sets,
            "reps": reps,
            "intensity": intensity,
            "note": None if deload else self.note,
        }


# ---------------------------------------------------------------------------
# Semantischer Pfad: WODL re-emittieren
# ---------------------------------------------------------------------------


def _emit_exercise(ex: ExerciseLine, proj: dict) -> str:
    name = ex.display_name or ex.canonical_name or ex.raw_name
    parts = [f"{name:<22}"]
    if proj["sets"] and proj["reps"]:
        parts.append(f"{proj['sets']}x{proj['reps']}")
    elif proj["sets"]:
        parts.append(f"{proj['sets']}x")
    elif proj["reps"]:
        parts.append(str(proj["reps"]))
    if proj["intensity"]:
        val = proj["intensity"]
        parts.append(val if val.startswith("@") else f"@{val}")
    if ex.rest:
        parts.append(f"r{ex.rest}")
    if ex.tempo:
        parts.append(f"t{ex.tempo}")
    for mod in ex.modifiers:
        parts.append(mod)
    line = "  ".join(p for p in parts if p).rstrip()
    if proj["note"]:
        line += f"   # {proj['note']}"
    return line


GROUP_KEYWORD = {"superset": "ss", "circuit": "circuit", "giant": "giant"}


def progress_plan(plan: Plan, config: ProgressionConfig) -> list[WeekResult]:
    """Projiziert einen geparsten Plan über den Block. Output: WODL pro Woche."""
    kinds = week_kinds(config, plan)
    total = config.weeks

    # Zustand pro Übung aufbauen (Gruppen-Übungen inklusive)
    states: dict[tuple, _ExState] = {}
    for si, session in enumerate(plan.sessions):
        for ii, item in enumerate(session.items):
            if isinstance(item, ExerciseGroup):
                for gi, sub in enumerate(item.exercises):
                    states[(si, ii, gi)] = _ExState(sub, config)
            else:
                states[(si, ii, None)] = _ExState(item, config)

    results: list[WeekResult] = []
    for w, kind in enumerate(kinds, start=1):
        if kind == "build" and w > 1:
            for st in states.values():
                st.advance()
        deload = kind == "deload"

        lines: list[str] = []
        label = _week_label(kind, config.goal)
        title = plan.name or "Trainingsplan"
        lines.append(f'@plan "{title} — Woche {w}/{total}"')
        if plan.frequency:
            lines.append(f"@freq {plan.frequency}")
        if plan.unit and plan.unit != "kg":
            lines.append(f"@unit {plan.unit}")
        lines.append(f"# Woche {w}/{total} — {label}")

        for si, session in enumerate(plan.sessions):
            lines.append("")
            days = " ".join(session.days)
            lines.append(f"---[{session.name}]" + (f" {days}" if days else ""))
            for note in session.notes:
                lines.append(f"> {note}")
            lines.append("")
            for ii, item in enumerate(session.items):
                if isinstance(item, ExerciseGroup):
                    lines.append(f"{GROUP_KEYWORD.get(item.kind, 'ss')} {{")
                    for gi, sub in enumerate(item.exercises):
                        st = states[(si, ii, gi)]
                        lines.append("  " + _emit_exercise(sub, st.project(deload)))
                    lines.append("}")
                else:
                    st = states[(si, ii, None)]
                    lines.append(_emit_exercise(item, st.project(deload)))

        results.append(WeekResult(week=w, kind=kind, label=label, text="\n".join(lines) + "\n"))
    return results


# ---------------------------------------------------------------------------
# Freitext-Pfad (portiert aus Progressio, vereinheitlichte Deload-Semantik)
# ---------------------------------------------------------------------------

# kg-Lasten erkennen: "5kg", "12,5kg", "2x5kg" (Kurzhantel-Paar)
_LOAD = re.compile(r"\d+(?:[.,]\d+)?(?:\s*[x×]\s*\d+(?:[.,]\d+)?)?\s*kg", re.I)
_PLUS = re.compile(r"\d+(?:\+\d+)+")                 # 8+10+12
_RANGE = re.compile(r"\d+(?:-\d+)+")                 # 10-12-14 / 8-12
# 3x10 / 4 x 8-12 — aber NICHT Sätze×Zeit (3x45sek): dann ist die Zahl Zeit
_SETSXREPS = re.compile(r"(\d+)(\s*[x×]\s*)(\d+)(-\d+)?(?!\d)(?!\s*(?:sek|sec|min|minuten)\b)", re.I)
_SINGLE = re.compile(r"(\d+)(\s*[x×])(?!\s*[\d\x00])")   # 12x (Reps)
_REPSWORD = re.compile(r"(\d+)(\s*)(Wdh|Wiederholungen|reps?)\b", re.I)
_TIME = re.compile(r"(\d+)(\s*)(sek|sec|s|min|minuten|min\.)\b", re.I)


def _shift_reps(n: int, delta: int, cap: int | None) -> int:
    """Reps anheben, aber nur bis zur Schwelle; was schon drüber liegt, bleibt stehen."""
    new = max(1, n + delta)
    if cap:
        new = min(new, max(n, cap))
    return new


def _scale(n: int, factor: float) -> int:
    return max(1, round(n * factor))


def transform_line(line: str, config: ProgressionConfig,
                   rep_delta: int = 0, deload: bool = False) -> str:
    """Eine Freitext-Zeile progressieren.

    Aufbau: Reps/Zeit +delta (Schwelle als Obergrenze). Deload: Sätze × Faktor,
    kg × Last-Faktor, Reps bleiben. Behandelte Muster werden gestasht, damit
    spätere Muster dieselbe Zahl nicht doppelt anfassen.
    """
    if not line.strip():
        return line

    cap = config.threshold_for(None) if config.goal != "ausdauer" or config.rep_threshold else None
    stash: list[str] = []

    def put(val: str) -> str:
        stash.append(val)
        return f"\x00{len(stash) - 1}\x00"

    def _load(m):
        if deload and config.deload_load_factor < 1.0:
            def kgshift(km):
                return f"{_round_load(float(km.group().replace(',', '.')) * config.deload_load_factor):g}"
            return put(re.sub(r"\d+(?:[.,]\d+)?", kgshift, m.group()))
        return put(m.group())

    def _chain(m):                        # 8+10+12 und 10-12-14 / 8-12
        if deload:
            return put(m.group())
        return put(re.sub(r"\d+", lambda km: str(_shift_reps(int(km.group()), rep_delta, cap)), m.group()))

    def _sr(m):                           # Sätze×Reps: Aufbau bewegt Reps, Deload die Sätze
        sets, x, reps, rng = int(m.group(1)), m.group(2), int(m.group(3)), m.group(4) or ""
        if deload:
            return put(f"{_scale(sets, config.deload_sets_factor)}{x}{reps}{rng}")
        reps2 = _shift_reps(reps, rep_delta, cap)
        rng2 = f"-{_shift_reps(int(rng[1:]), rep_delta, cap)}" if rng else ""
        return put(f"{sets}{x}{reps2}{rng2}")

    def _single(m):
        n = int(m.group(1))
        n2 = _scale(n, config.deload_sets_factor) if deload else _shift_reps(n, rep_delta, cap)
        return put(f"{n2}{m.group(2)}")

    def _repsword(m):
        n = int(m.group(1))
        n2 = _scale(n, config.deload_sets_factor) if deload else _shift_reps(n, rep_delta, cap)
        return f"{n2}{m.group(2)}{m.group(3)}"

    def _t(m):                            # Zeit: Aufbau +increment, Deload × Volumen-Faktor
        n, sp, unit = int(m.group(1)), m.group(2), m.group(3)
        if deload:
            n2 = _scale(n, config.deload_sets_factor)
        elif unit.lower().startswith("min"):
            n2 = n + max(1, rep_delta // 2) if rep_delta else n
        else:
            n2 = n + (config.time_increment * rep_delta // max(1, config.rep_increment)
                      if rep_delta else 0)
        return f"{n2}{sp}{unit}"

    work = _LOAD.sub(_load, line)
    work = _PLUS.sub(_chain, work)
    work = _RANGE.sub(_chain, work)
    work = _SETSXREPS.sub(_sr, work)
    work = _SINGLE.sub(_single, work)
    work = _REPSWORD.sub(_repsword, work)
    work = _TIME.sub(_t, work)

    for i, val in enumerate(stash):
        work = work.replace(f"\x00{i}\x00", val)
    return work


def progress_text(text: str, config: ProgressionConfig) -> list[WeekResult]:
    """Freitext-Plan über den Block projizieren. Output: Klartext pro Woche."""
    kinds = week_kinds(config)
    lines = text.rstrip("\n").split("\n")
    results: list[WeekResult] = []
    build_steps = 0
    for w, kind in enumerate(kinds, start=1):
        if kind == "build" and w > 1:
            build_steps += 1
        deload = kind == "deload"
        delta = build_steps * config.rep_increment
        new_lines = [transform_line(ln, config, rep_delta=delta, deload=deload)
                     for ln in lines]
        results.append(WeekResult(
            week=w, kind=kind, label=_week_label(kind, config.goal),
            text="\n".join(new_lines),
        ))
    return results


# ---------------------------------------------------------------------------
# Auto-Weiche
# ---------------------------------------------------------------------------


def looks_like_wodl(text: str) -> Plan | None:
    """Gibt den geparsten Plan zurück, wenn der Text als WODL durchgeht."""
    try:
        plan = parse(text)
    except Exception:
        return None
    if plan.sessions and any(s.items for s in plan.sessions):
        return plan
    return None


def progress_auto(text: str, config: ProgressionConfig) -> tuple[str, list[WeekResult]]:
    """Weiche: WODL-Plan → semantische Engine, sonst Freitext-Engine."""
    plan = looks_like_wodl(text)
    if plan is not None:
        return ("wodl", progress_plan(plan, config))
    return ("freetext", progress_text(text, config))


def block_as_text(results: list[WeekResult]) -> str:
    """Gesamten Block als einen Klartext-Export."""
    parts = []
    for r in results:
        parts.append(f"=== Woche {r.week} — {r.label} ===")
        parts.append(r.text.rstrip("\n"))
        parts.append("")
    return "\n".join(parts).strip() + "\n"
