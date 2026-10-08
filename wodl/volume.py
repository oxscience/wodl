"""
Wochenvolumen — Sätze pro Muskelgruppe.

Zählweise: Der erste Muskel einer Übung (Registry `muscles[0]`) bekommt den
vollen Satz, alle weiteren einen halben (fractional counting, Pelland et al.
2025, Sports Med, 10.1007/s40279-025-02344-w). Mobility und Cardio zählen
nicht. Eine Einheit läuft so oft pro Woche, wie sie Wochentage hat (ohne
Tage: 1x).

Phasen-Pläne (mind. zwei Einheiten heißen "Phase …", "Stufe …", "Block …",
"Pre-OP …") laufen nacheinander, nicht parallel — dort gibt es eine Spalte
pro Einheit statt einer Wochensumme.
"""

from __future__ import annotations

import re

from wodl.parser import ExerciseGroup, Plan
from wodl.registry import EXERCISES

# Anzeige-Reihenfolge = anatomisch (Push/Pull-Balance lesbar). Slugs ohne
# Gruppe (full_body, *_rom, proprioception, …) sind keine Muskeln → zählen nicht.
GROUPS: dict[str, tuple[str, ...]] = {
    "Brust": ("chest", "upper_chest"),
    "Rücken": ("back", "lats", "rhomboids", "mid_traps", "lower_traps", "traps", "scapular_depressors"),
    "Schulter vorne": ("front_delt",),
    "Schulter seitlich": ("side_delt",),
    "Schulter hinten": ("rear_delt",),
    "Rotatorenmanschette": ("rotator_cuff", "infraspinatus", "subscapularis", "supraspinatus", "teres_minor"),
    "Bizeps": ("biceps", "brachialis", "brachioradialis"),
    "Trizeps": ("triceps",),
    "Unterarme": ("forearms", "forearm_extensors", "forearm_flexors"),
    "Rumpf": ("core", "obliques", "rectus_abdominis", "transverse_abdominis", "qlm"),
    "Unterer Rücken": ("erectors", "lower_back"),
    "Gesäß": ("glutes", "glute_med", "hip_abductors", "hip_rotators"),
    "Quadrizeps": ("quads",),
    "Hamstrings": ("hamstrings",),
    "Adduktoren": ("adductors", "hip_adductors"),
    "Hüftbeuger": ("hip_flexors",),
    "Waden": ("calves", "soleus", "gastrocnemius", "achilles_tendon"),
    "Schienbein & Fuß": ("tibialis_anterior", "tibialis_posterior", "peroneals", "foot_intrinsics"),
    "Nacken": ("deep_neck_flexors", "neck_extensors", "sternocleidomastoid"),
}
_SLUG_GROUP = {slug: group for group, slugs in GROUPS.items() for slug in slugs}
_SKIP_CATEGORIES = {"mobility", "cardio"}
INDIRECT = 0.5
_PHASE_NAME = re.compile(r"^(Phase|Stufe|Block|Pre-OP)\b", re.I)


def _exercises(session):
    for item in session.items:
        if isinstance(item, ExerciseGroup):
            yield from item.exercises
        else:
            yield item


def _session_sets(session) -> tuple[dict[str, float], int]:
    """Sätze pro Gruppe für EINEN Durchlauf der Einheit + Zahl unbekannter Übungen."""
    sets: dict[str, float] = {}
    unknown = 0
    for ex in _exercises(session):
        meta = EXERCISES.get(ex.canonical_name or "")
        if meta is None:
            unknown += 1
            continue
        if meta["category"] in _SKIP_CATEGORIES:
            continue
        weights: dict[str, float] = {}
        for i, slug in enumerate(meta["muscles"]):
            group = _SLUG_GROUP.get(slug)
            if group:
                weights[group] = max(weights.get(group, 0), 1.0 if i == 0 else INDIRECT)
        n = ex.sets or 1
        for group, w in weights.items():
            sets[group] = sets.get(group, 0) + n * w
    return sets, unknown


def weekly_volume(plan: Plan) -> tuple[list[str], dict[str, list[float]], int]:
    """Sätze pro Muskelgruppe und Woche.

    Returns:
        (Spalten, {Gruppe: [Sätze je Spalte]}, Zahl unbekannter Übungen).
        Split-Plan: eine Spalte "pro Woche"; Phasen-Plan: eine Spalte je Phase.
    """
    phased = sum(bool(_PHASE_NAME.match(s.name)) for s in plan.sessions) >= 2
    blocks = [[s] for s in plan.sessions] if phased else [plan.sessions]
    columns = ([re.sub(r"\s*\(.*\)$", "", s.name.split(":")[0]) for s in plan.sessions]
               if phased else ["pro Woche"])

    totals: list[dict[str, float]] = []
    unknown = 0
    for block in blocks:
        col: dict[str, float] = {}
        for session in block:
            sets, unk = _session_sets(session)
            unknown += unk
            per_week = max(1, len(session.days))
            for group, n in sets.items():
                col[group] = col.get(group, 0) + n * per_week
        totals.append(col)

    rows = {
        group: [col.get(group, 0) for col in totals]
        for group in GROUPS
        if any(col.get(group) for col in totals)
    }
    return columns, rows, unknown
