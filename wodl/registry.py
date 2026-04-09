"""
Exercise Registry — Kanonische Uebungsnamen mit Aliases.

Jede Uebung hat einen englischen Canonical Name.
Deutsche Namen, Kurzformen und haeufige Tippfehler werden
automatisch auf den kanonischen Namen aufgeloest.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Registry: canonical_name -> metadata
# ---------------------------------------------------------------------------
EXERCISES: dict[str, dict] = {
    # --- Chest ---
    "Bench Press": {
        "muscles": ["chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Bankdrücken", "Bankdruecken", "Flat Bench", "BB Bench",
            "Barbell Bench Press", "Flat Bench Press",
        ],
    },
    "Incline Bench Press": {
        "muscles": ["upper_chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Schrägbankdrücken", "Schraegbankdruecken",
            "Incline BB Bench", "Incline Barbell Bench",
        ],
    },
    "Dumbbell Bench Press": {
        "muscles": ["chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "KH Bankdrücken", "KH Bankdruecken",
            "DB Bench Press", "DB Bench",
        ],
    },
    "Incline DB Press": {
        "muscles": ["upper_chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Incline Dumbbell Press", "KH Schrägbankdrücken",
            "Incline DB Bench",
        ],
    },
    "Dip": {
        "muscles": ["chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": ["Dips", "Chest Dip", "Brust-Dip"],
    },
    "Cable Fly": {
        "muscles": ["chest"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": [
            "Cable Flye", "Kabelzug Fly", "Cable Crossover",
        ],
    },
    "Incline DB Fly": {
        "muscles": ["upper_chest"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Incline Dumbbell Fly", "Incline Flye",
            "KH Schrägbank Fly",
        ],
    },
    "Push-up": {
        "muscles": ["chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": ["Pushup", "Push Up", "Liegestütz", "Liegestuetz"],
    },

    # --- Back ---
    "Deadlift": {
        "muscles": ["back", "glutes", "hamstrings"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Kreuzheben", "Conventional Deadlift", "DL",
        ],
    },
    "Sumo Deadlift": {
        "muscles": ["back", "glutes", "quads"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Sumo DL", "Sumo Kreuzheben"],
    },
    "RDL": {
        "muscles": ["hamstrings", "glutes", "lower_back"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Romanian Deadlift", "Rumänisches Kreuzheben",
            "Rumaenisches Kreuzheben", "Stiff Leg Deadlift",
        ],
    },
    "Barbell Row": {
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "LH Rudern", "BB Row", "Bent Over Row",
            "Vorgebeugtes Rudern", "Barbell Bent Over Row",
        ],
    },
    "Dumbbell Row": {
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "KH Rudern", "DB Row", "One Arm Row",
            "Einarmiges Rudern",
        ],
    },
    "Pull-up": {
        "muscles": ["back", "biceps"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": [
            "Pullup", "Pull Up", "Klimmzug", "Klimmzüge",
            "Klimmzuege",
        ],
    },
    "Chin-up": {
        "muscles": ["back", "biceps"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": ["Chinup", "Chin Up"],
    },
    "Lat Pulldown": {
        "muscles": ["back", "biceps"],
        "category": "compound",
        "equipment": "cable",
        "aliases": [
            "Latzug", "Lat Pull Down", "Latziehen",
        ],
    },
    "Cable Row": {
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "cable",
        "aliases": [
            "Seated Cable Row", "Kabelrudern", "Seated Row",
        ],
    },
    "T-Bar Row": {
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["T-Bar Rudern", "T Bar Row"],
    },

    # --- Shoulders ---
    "OHP": {
        "muscles": ["front_delt", "triceps"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Overhead Press", "Schulterdrücken", "Schulterdruecken",
            "Military Press", "Standing Press", "Press",
        ],
    },
    "Dumbbell OHP": {
        "muscles": ["front_delt", "triceps"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "DB OHP", "KH Schulterdrücken", "Dumbbell Shoulder Press",
            "DB Shoulder Press",
        ],
    },
    "Lateral Raise": {
        "muscles": ["side_delt"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Seitheben", "Side Raise", "Lat Raise",
            "KH Seitheben", "DB Lateral Raise",
        ],
    },
    "Face Pull": {
        "muscles": ["rear_delt", "rotator_cuff"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": ["Facepull", "Face Pulls"],
    },
    "Rear Delt Fly": {
        "muscles": ["rear_delt"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Reverse Fly", "Butterfly Reverse",
            "Hintere Schulter Fly",
        ],
    },
    "Shrug": {
        "muscles": ["traps"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": ["Shrugs", "BB Shrug", "Schulterheben"],
    },
    "Upright Row": {
        "muscles": ["traps", "side_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Aufrechtes Rudern"],
    },

    # --- Arms ---
    "Barbell Curl": {
        "muscles": ["biceps"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": [
            "BB Curl", "LH Curl", "Langhantel Curl",
            "Bizeps Curl", "Bicep Curl",
        ],
    },
    "Dumbbell Curl": {
        "muscles": ["biceps"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["DB Curl", "KH Curl", "Kurzhantel Curl"],
    },
    "Hammer Curl": {
        "muscles": ["biceps", "brachialis"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Hammercurl", "Hammer Curls"],
    },
    "Preacher Curl": {
        "muscles": ["biceps"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": ["Scott Curl", "Larry Curl"],
    },
    "Incline Curl": {
        "muscles": ["biceps"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Incline DB Curl", "Schrägbank Curl"],
    },
    "Tricep Pushdown": {
        "muscles": ["triceps"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": [
            "Cable Pushdown", "Trizepsdrücken", "Trizepsdruecken",
            "Tricep Push Down", "Pushdown",
        ],
    },
    "Overhead Tricep Extension": {
        "muscles": ["triceps"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": [
            "Overhead Extension", "French Press",
            "Trizeps Überkopf", "Cable Overhead Extension",
        ],
    },
    "Skull Crusher": {
        "muscles": ["triceps"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": [
            "Skullcrusher", "Lying Tricep Extension",
            "Stirndrücken", "Nosebreaker",
        ],
    },

    # --- Legs ---
    "Squat": {
        "muscles": ["quads", "glutes", "hamstrings"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Back Squat", "Kniebeuge", "Kniebeugen",
            "BB Squat", "Barbell Squat",
        ],
    },
    "Front Squat": {
        "muscles": ["quads", "glutes", "core"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Frontkniebeuge", "Front Kniebeuge"],
    },
    "Leg Press": {
        "muscles": ["quads", "glutes"],
        "category": "compound",
        "equipment": "machine",
        "aliases": ["Beinpresse", "LP"],
    },
    "Leg Extension": {
        "muscles": ["quads"],
        "category": "isolation",
        "equipment": "machine",
        "aliases": [
            "Leg Ext", "Beinstrecker", "Beinstrecken",
        ],
    },
    "Leg Curl": {
        "muscles": ["hamstrings"],
        "category": "isolation",
        "equipment": "machine",
        "aliases": [
            "Lying Leg Curl", "Seated Leg Curl",
            "Beinbeuger", "Beinbeugen",
        ],
    },
    "Bulgarian Split Squat": {
        "muscles": ["quads", "glutes"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "BSS", "Bulgarian Squat", "Split Squat",
            "Bulgarische Kniebeuge",
        ],
    },
    "Lunge": {
        "muscles": ["quads", "glutes"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": ["Lunges", "Ausfallschritt", "Ausfallschritte"],
    },
    "Hip Thrust": {
        "muscles": ["glutes", "hamstrings"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Hüftheben", "Hueftheben", "BB Hip Thrust"],
    },
    "Calf Raise": {
        "muscles": ["calves"],
        "category": "isolation",
        "equipment": "machine",
        "aliases": [
            "Standing Calf Raise", "Seated Calf Raise",
            "Wadenheben", "Calf Raises",
        ],
    },
    "Hack Squat": {
        "muscles": ["quads", "glutes"],
        "category": "compound",
        "equipment": "machine",
        "aliases": ["Hackenschmidt", "Hack Kniebeuge"],
    },

    # --- Core ---
    "Plank": {
        "muscles": ["core"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": ["Unterarmstütz", "Unterarmstuetz"],
    },
    "Hanging Leg Raise": {
        "muscles": ["core", "hip_flexors"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": [
            "Leg Raise", "Beinheben hängend",
            "Hanging Knee Raise",
        ],
    },
    "Cable Crunch": {
        "muscles": ["core"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": ["Kabel Crunch", "Kabelzug Crunch"],
    },
    "Ab Wheel Rollout": {
        "muscles": ["core"],
        "category": "isolation",
        "equipment": "other",
        "aliases": ["Ab Wheel", "Rollout", "Ab Roller"],
    },
    "Mountain Climber": {
        "muscles": ["core", "hip_flexors"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": ["Mountain Climbers", "Bergsteiger"],
    },

    # --- Cardio / Conditioning ---
    "Rowing Machine": {
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "machine",
        "aliases": ["Rudergerät", "Rudergeraet", "Rower", "Erg"],
    },
    "Assault Bike": {
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "machine",
        "aliases": ["Air Bike", "Airbike", "Fan Bike"],
    },
}


# ---------------------------------------------------------------------------
# Lookup index  (built once on import)
# ---------------------------------------------------------------------------
_ALIAS_MAP: dict[str, str] = {}


def _build_index() -> None:
    """Build a case-insensitive alias -> canonical name lookup."""
    for canonical, meta in EXERCISES.items():
        key = canonical.lower().strip()
        _ALIAS_MAP[key] = canonical
        for alias in meta.get("aliases", []):
            _ALIAS_MAP[alias.lower().strip()] = canonical


_build_index()


def resolve(name: str) -> str | None:
    """Resolve any exercise name/alias to its canonical form.

    Returns the canonical name or None if not found.
    """
    return _ALIAS_MAP.get(name.lower().strip())


def resolve_fuzzy(name: str, threshold: float = 0.75) -> str | None:
    """Best-effort fuzzy match when exact lookup fails.

    Uses bigram similarity (Sorensen-Dice coefficient).
    Returns None if below threshold.
    """
    name_lower = name.lower().strip()

    # Exact match first
    exact = _ALIAS_MAP.get(name_lower)
    if exact:
        return exact

    # Ratio-based similarity (Sorensen-Dice on bigrams)
    def bigrams(s: str) -> set[str]:
        return {s[i : i + 2] for i in range(len(s) - 1)}

    name_bi = bigrams(name_lower)
    if not name_bi:
        return None

    best_score = 0.0
    best_match = None
    for alias, canonical in _ALIAS_MAP.items():
        alias_bi = bigrams(alias)
        if not alias_bi:
            continue
        overlap = len(name_bi & alias_bi)
        score = (2 * overlap) / (len(name_bi) + len(alias_bi))
        if score > best_score:
            best_score = score
            best_match = canonical

    return best_match if best_score >= threshold else None


def get_muscles(canonical_name: str) -> list[str]:
    """Return target muscles for a canonical exercise name."""
    entry = EXERCISES.get(canonical_name)
    return entry["muscles"] if entry else []


def list_exercises(category: str | None = None) -> list[str]:
    """List all canonical exercise names, optionally filtered by category."""
    if category is None:
        return sorted(EXERCISES.keys())
    return sorted(
        name
        for name, meta in EXERCISES.items()
        if meta.get("category") == category
    )
