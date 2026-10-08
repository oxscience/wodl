"""
Exercise Registry — Kanonische Uebungsnamen mit Aliases.

Jede Uebung hat einen englischen Canonical Name und einen deutschen
Anzeigenamen (`de`), der in Vorschau und Editor-Vorschlaegen erscheint.
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
        "de": "Bankdrücken",
        "muscles": ["chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Bankdrücken", "Bankdruecken", "Flat Bench", "BB Bench",
            "Barbell Bench Press", "Flat Bench Press",
        ],
    },
    "Incline Bench Press": {
        "de": "Schrägbankdrücken",
        "muscles": ["upper_chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Schrägbankdrücken", "Schraegbankdruecken",
            "Incline BB Bench", "Incline Barbell Bench",
        ],
    },
    "Dumbbell Bench Press": {
        "de": "Kurzhantel-Bankdrücken",
        "muscles": ["chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "KH Bankdrücken", "KH Bankdruecken",
            "DB Bench Press", "DB Bench",
        ],
    },
    "Incline DB Press": {
        "de": "Kurzhantel-Schrägbankdrücken",
        "muscles": ["upper_chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Incline Dumbbell Press", "KH Schrägbankdrücken",
            "Incline DB Bench",
        ],
    },
    "Dip": {
        "de": "Dips",
        "muscles": ["chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": ["Dips", "Chest Dip", "Brust-Dip"],
    },
    "Cable Fly": {
        "de": "Kabelzug-Fliegende",
        "muscles": ["chest"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": [
            "Cable Flye", "Kabelzug Fly", "Cable Crossover",
        ],
    },
    "Incline DB Fly": {
        "de": "Schrägbank-Fliegende",
        "muscles": ["upper_chest"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Incline Dumbbell Fly", "Incline Flye",
            "KH Schrägbank Fly",
        ],
    },
    "Push-up": {
        "de": "Liegestütz",
        "muscles": ["chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": ["Pushup", "Push Up", "Liegestütz", "Liegestuetz"],
    },

    # --- Back ---
    "Deadlift": {
        "de": "Kreuzheben",
        "muscles": ["back", "glutes", "hamstrings"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Kreuzheben", "Conventional Deadlift", "DL",
        ],
    },
    "Sumo Deadlift": {
        "de": "Sumo-Kreuzheben",
        "muscles": ["back", "glutes", "quads"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Sumo DL", "Sumo Kreuzheben"],
    },
    "RDL": {
        "de": "Rumänisches Kreuzheben",
        "muscles": ["hamstrings", "glutes", "lower_back"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Romanian Deadlift", "Rumänisches Kreuzheben",
            "Rumaenisches Kreuzheben", "Stiff Leg Deadlift",
        ],
    },
    "Barbell Row": {
        "de": "Langhantel-Rudern",
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "LH Rudern", "BB Row", "Bent Over Row",
            "Vorgebeugtes Rudern", "Barbell Bent Over Row",
        ],
    },
    "Dumbbell Row": {
        "de": "Kurzhantel-Rudern",
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "KH Rudern", "DB Row", "One Arm Row",
            "Einarmiges Rudern",
        ],
    },
    "Pull-up": {
        "de": "Klimmzug",
        "muscles": ["back", "biceps"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": [
            "Pullup", "Pull Up", "Klimmzug", "Klimmzüge",
            "Klimmzuege",
        ],
    },
    "Chin-up": {
        "de": "Klimmzug im Untergriff",
        "muscles": ["back", "biceps"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": ["Chinup", "Chin Up"],
    },
    "Lat Pulldown": {
        "de": "Latzug",
        "muscles": ["back", "biceps"],
        "category": "compound",
        "equipment": "cable",
        "aliases": [
            "Latzug", "Lat Pull Down", "Latziehen",
        ],
    },
    "Cable Row": {
        "de": "Kabelrudern",
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "cable",
        "aliases": [
            "Seated Cable Row", "Kabelrudern", "Seated Row",
        ],
    },
    "T-Bar Row": {
        "de": "T-Bar-Rudern",
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["T-Bar Rudern", "T Bar Row"],
    },

    # --- Shoulders ---
    "OHP": {
        "de": "Schulterdrücken",
        "muscles": ["front_delt", "triceps"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Overhead Press", "Schulterdrücken", "Schulterdruecken",
            "Military Press", "Standing Press", "Press",
        ],
    },
    "Dumbbell OHP": {
        "de": "Kurzhantel-Schulterdrücken",
        "muscles": ["front_delt", "triceps"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "DB OHP", "KH Schulterdrücken", "Dumbbell Shoulder Press",
            "DB Shoulder Press",
        ],
    },
    "Lateral Raise": {
        "de": "Seitheben",
        "muscles": ["side_delt"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Seitheben", "Side Raise", "Lat Raise",
            "KH Seitheben", "DB Lateral Raise", "Shoulder Abduction",
        ],
    },
    "Face Pull": {
        "de": "Face Pull",
        "muscles": ["rear_delt", "rotator_cuff"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": ["Facepull", "Face Pulls"],
    },
    "Rear Delt Fly": {
        "de": "Vorgebeugtes Seitheben",
        "muscles": ["rear_delt"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Reverse Fly", "Butterfly Reverse",
            "Hintere Schulter Fly",
        ],
    },
    "Shrug": {
        "de": "Schulterheben",
        "muscles": ["traps"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": ["Shrugs", "BB Shrug", "Schulterheben"],
    },
    "Upright Row": {
        "de": "Aufrechtes Rudern",
        "muscles": ["traps", "side_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Aufrechtes Rudern"],
    },

    # --- Arms ---
    "Barbell Curl": {
        "de": "Langhantel-Curl",
        "muscles": ["biceps"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": [
            "BB Curl", "LH Curl", "Langhantel Curl",
            "Bizeps Curl", "Bicep Curl",
        ],
    },
    "Dumbbell Curl": {
        "de": "Kurzhantel-Curl",
        "muscles": ["biceps"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["DB Curl", "KH Curl", "Kurzhantel Curl"],
    },
    "Hammer Curl": {
        "de": "Hammer-Curl",
        "muscles": ["biceps", "brachialis"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Hammercurl", "Hammer Curls"],
    },
    "Preacher Curl": {
        "de": "Scott-Curl",
        "muscles": ["biceps"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": ["Scott Curl", "Larry Curl"],
    },
    "Incline Curl": {
        "de": "Schrägbank-Curl",
        "muscles": ["biceps"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Incline DB Curl", "Incline Dumbbell Curl", "Schrägbank Curl"],
    },
    "Tricep Pushdown": {
        "de": "Trizepsdrücken",
        "muscles": ["triceps"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": [
            "Cable Pushdown", "Trizepsdrücken", "Trizepsdruecken",
            "Tricep Push Down", "Pushdown",
        ],
    },
    "Overhead Tricep Extension": {
        "de": "Überkopf-Trizepsstrecken",
        "muscles": ["triceps"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": [
            "Overhead Extension", "French Press",
            "Trizeps Überkopf", "Cable Overhead Extension",
        ],
    },
    "Skull Crusher": {
        "de": "Stirndrücken",
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
        "de": "Kniebeuge",
        "muscles": ["quads", "glutes", "hamstrings"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Back Squat", "Kniebeuge", "Kniebeugen",
            "BB Squat", "Barbell Squat",
        ],
    },
    "Front Squat": {
        "de": "Frontkniebeuge",
        "muscles": ["quads", "glutes", "core"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Frontkniebeuge", "Front Kniebeuge"],
    },
    "Leg Press": {
        "de": "Beinpresse",
        "muscles": ["quads", "glutes"],
        "category": "compound",
        "equipment": "machine",
        "aliases": ["Beinpresse", "LP"],
    },
    "Leg Extension": {
        "de": "Beinstrecker",
        "muscles": ["quads"],
        "category": "isolation",
        "equipment": "machine",
        "aliases": [
            "Leg Ext", "Knee Extension", "Beinstrecker", "Beinstrecken",
        ],
    },
    "Leg Curl": {
        "de": "Beinbeuger",
        "muscles": ["hamstrings"],
        "category": "isolation",
        "equipment": "machine",
        "aliases": [
            "Lying Leg Curl", "Seated Leg Curl", "Standing Leg Curl",
            "Beinbeuger", "Beinbeugen",
        ],
    },
    "Bulgarian Split Squat": {
        "de": "Bulgarische Kniebeuge",
        "muscles": ["quads", "glutes"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "BSS", "Bulgarian Squat", "Split Squat",
            "Bulgarische Kniebeuge",
        ],
    },
    "Lunge": {
        "de": "Ausfallschritt",
        "muscles": ["quads", "glutes"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": ["Lunges", "Ausfallschritt", "Ausfallschritte"],
    },
    "Hip Thrust": {
        "de": "Hip Thrust",
        "muscles": ["glutes", "hamstrings"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Hüftheben", "Hueftheben", "BB Hip Thrust"],
    },
    "Calf Raise": {
        "de": "Wadenheben",
        "muscles": ["calves"],
        "category": "isolation",
        "equipment": "machine",
        "aliases": [
            "Standing Calf Raise", "Seated Calf Raise",
            "Double-Leg Calf Raise", "Beidbeiniges Wadenheben",
            "Wadenheben", "Calf Raises",
        ],
    },
    "Hack Squat": {
        "de": "Hackenschmidt",
        "muscles": ["quads", "glutes"],
        "category": "compound",
        "equipment": "machine",
        "aliases": ["Hackenschmidt", "Hack Kniebeuge"],
    },

    # --- Core ---
    "Plank": {
        "de": "Unterarmstütz",
        "muscles": ["core"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": ["Unterarmstütz", "Unterarmstuetz"],
    },
    "Hanging Leg Raise": {
        "de": "Hängendes Beinheben",
        "muscles": ["core", "hip_flexors"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": [
            "Leg Raise", "Beinheben hängend",
            "Hanging Knee Raise",
        ],
    },
    "Cable Crunch": {
        "de": "Kabelzug-Crunch",
        "muscles": ["core"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": ["Kabel Crunch", "Kabelzug Crunch"],
    },
    "Ab Wheel Rollout": {
        "de": "Bauchroller",
        "muscles": ["core"],
        "category": "isolation",
        "equipment": "other",
        "aliases": ["Ab Wheel", "Rollout", "Ab Roller"],
    },
    "Mountain Climber": {
        "de": "Bergsteiger",
        "muscles": ["core", "hip_flexors"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": ["Mountain Climbers", "Bergsteiger"],
    },

    # --- Cardio / Conditioning ---
    "Rowing Machine": {
        "de": "Rudergerät",
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "machine",
        "aliases": ["Rudergerät", "Rudergeraet", "Rower", "Erg"],
    },
    "Assault Bike": {
        "de": "Air Bike",
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "machine",
        "aliases": ["Air Bike", "Airbike", "Fan Bike"],
    },

    # ========================================================================
    # REHAB — Evidenzbasierte Reha-Übungen (ACL, Rotator Cuff, LBP, Achilles)
    # Quellen: Wilk & Arrigo 2017 (ACL), Ellenbecker 2017 (Shoulder),
    # McGill 2016 (Low Back), Alfredson 1998 (Achilles Tendinopathy)
    # ========================================================================

    # --- Knee Rehab ---
    "Quad Set": {
        "de": "Quadrizeps-Anspannung",
        "muscles": ["quads"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Quad Sets", "Quadrizeps-Anspannung", "Quad Contraction", "VMO Set"],
    },
    "Straight Leg Raise": {
        "de": "Gestrecktes Beinheben",
        "muscles": ["quads", "hip_flexors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["SLR", "Gestrecktes Beinheben", "Aktives Beinheben"],
    },
    "Terminal Knee Extension": {
        "de": "Knie-Endstreckung",
        "muscles": ["quads"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["TKE", "Knie-Endstreckung", "Endstreckung Knie"],
    },
    "Heel Slide": {
        "de": "Fersenrutschen",
        "muscles": ["hamstrings", "knee_rom"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Heel Slides", "Fersenrutschen", "Knieflexion-Slide"],
    },
    "Mini Squat": {
        "de": "Teilkniebeuge",
        "muscles": ["quads", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Mini Squats", "Teilkniebeuge", "Partial Squat",
            "Knee Bend", "Knee Bends",
        ],
    },
    "Wall Sit": {
        "de": "Wandsitz",
        "muscles": ["quads", "glutes"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": ["Wall Squat", "Wandsitz"],
    },
    "Step-up": {
        "de": "Step-up",
        "muscles": ["quads", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Step Up", "Stepups", "Aufsteiger"],
    },
    "Step-down": {
        "de": "Step-down",
        "muscles": ["quads", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Step Down", "Stepdowns", "Absteiger"],
    },
    "Single Leg Bridge": {
        "de": "Einbeinige Hüftbrücke",
        "muscles": ["glutes", "hamstrings"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["SL Bridge", "Einbeinige Brücke", "One-Leg Bridge"],
    },
    "Glute Bridge": {
        "de": "Hüftbrücke",
        "muscles": ["glutes", "hamstrings"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Bridge", "Hüftbrücke", "Hip Bridge", "Bridging"],
    },
    "Clamshell": {
        "de": "Clamshell",
        "muscles": ["glute_med", "hip_abductors"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Clamshells", "Muschel", "Hip Clamshell"],
    },
    "Side-Lying Hip Abduction": {
        "de": "Hüftabduktion in Seitenlage",
        "muscles": ["glute_med", "hip_abductors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Side Leg Raise", "Side-Lying Leg Raise",
            "Seitheben Bein", "Hip Abduction",
        ],
    },
    "Single Leg Balance": {
        "de": "Einbeinstand",
        "muscles": ["proprioception"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "SL Balance", "Einbeinstand", "One Leg Stance", "One Leg Stand",
            "Single Leg Balance Eyes Closed", "Single Leg Ball Toss",
        ],
    },

    # --- Shoulder Rehab ---
    "Pendulum": {
        "de": "Pendelübung",
        "muscles": ["shoulder_rom"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Pendelübung", "Pendulum Exercise", "Codman Pendulum"],
    },
    "Wall Walk": {
        "de": "Wandklettern",
        "muscles": ["shoulder_rom", "front_delt"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Wall Climb", "Finger Walk", "Wandklettern"],
    },
    "Band External Rotation": {
        "de": "Außenrotation mit Band",
        "muscles": ["rotator_cuff", "infraspinatus", "teres_minor"],
        "category": "rehab",
        "equipment": "band",
        "aliases": [
            "External Rotation", "ER Band", "Theraband Außenrotation",
            "Band ER", "Rotator Cuff ER",
        ],
    },
    "Band Internal Rotation": {
        "de": "Innenrotation mit Band",
        "muscles": ["rotator_cuff", "subscapularis"],
        "category": "rehab",
        "equipment": "band",
        "aliases": [
            "Internal Rotation", "IR Band", "Theraband Innenrotation",
            "Band IR",
        ],
    },
    "Scapular Retraction": {
        "de": "Schulterblatt-Retraktion",
        "muscles": ["rhomboids", "mid_traps"],
        "category": "rehab",
        "equipment": "band",
        "aliases": [
            "Scap Retraction", "Schulterblatt-Retraktion",
            "Band Pull-Apart", "Pull Apart",
        ],
    },
    "Prone Y": {
        "de": "Y-Heben in Bauchlage",
        "muscles": ["lower_traps", "rotator_cuff"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Y Raise", "Prone Y Raise", "Bauchlage Y"],
    },
    "Prone T": {
        "de": "T-Heben in Bauchlage",
        "muscles": ["mid_traps", "rear_delt"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["T Raise", "Prone T Raise", "Bauchlage T"],
    },
    "Prone W": {
        "de": "W-Heben in Bauchlage",
        "muscles": ["rotator_cuff", "mid_traps"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["W Raise", "Prone W Raise", "Bauchlage W"],
    },
    "Full Can Raise": {
        "de": "Full Can",
        "muscles": ["supraspinatus", "side_delt"],
        "category": "rehab",
        "equipment": "dumbbell",
        "aliases": ["Full Can", "Scaption", "Scaption Raise"],
    },

    # --- Low Back / Core Rehab (McGill Big 3 + progression) ---
    "McGill Curl-up": {
        "de": "McGill Curl-up",
        "muscles": ["rectus_abdominis"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Curl-up", "Modified Curl-up", "McGill Curl Up"],
    },
    "Side Plank": {
        "de": "Seitstütz",
        "muscles": ["obliques", "qlm", "core"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": [
            "Side Bridge", "Seitstütz", "Seitliche Planke",
            "Lateral Plank",
        ],
    },
    "Bird Dog": {
        "de": "Bird Dog",
        "muscles": ["erectors", "glutes", "core"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Bird-Dog", "Vierfüßlerstand", "Quadruped",
            "Opposite Arm Leg",
        ],
    },
    "Dead Bug": {
        "de": "Dead Bug",
        "muscles": ["core", "transverse_abdominis"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Dead-Bug", "Toter Käfer", "Dying Bug"],
    },
    "Cat-Cow": {
        "de": "Katze-Kuh",
        "muscles": ["spine_mobility"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Cat Cow", "Katzenbuckel", "Katze-Kuh"],
    },

    # --- Achilles / Calf Rehab (Alfredson Protocol) ---
    "Eccentric Heel Drop": {
        "de": "Exzentrisches Fersensenken",
        "muscles": ["gastrocnemius", "achilles_tendon"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Alfredson Heel Drop", "Eccentric Calf Drop",
            "Exzentrisches Fersensenken", "Heel Drops",
        ],
    },
    "Bent-Knee Heel Drop": {
        "de": "Fersensenken mit gebeugtem Knie",
        "muscles": ["soleus", "achilles_tendon"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Bent Knee Heel Drop", "Soleus Heel Drop",
            "Gebeugtes Fersensenken",
        ],
    },
    "Single-Leg Calf Raise": {
        "de": "Einbeiniges Wadenheben",
        "muscles": ["calves"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "SL Calf Raise", "One-Leg Calf Raise",
            "Einbeiniges Wadenheben",
        ],
    },
    "Isometric Calf Hold": {
        "de": "Isometrisches Wadenheben",
        "muscles": ["calves", "achilles_tendon"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": ["Iso Calf", "Wadenheben Halten", "Static Calf Hold"],
    },

    # --- Zusätzliche Reha / Plyo / Funktionell ---
    "Ankle Pumps": {
        "de": "Fußwippe",
        "muscles": ["calves", "circulation"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Ankle Pump", "Fußwippe", "Sprunggelenkspumpe"],
    },
    "Box Jump": {
        "de": "Kastensprung",
        "muscles": ["quads", "glutes", "calves"],
        "category": "plyometric",
        "equipment": "box",
        "aliases": ["Box Jumps", "Kastensprung", "Kastensprünge"],
    },
    "Lateral Bound": {
        "de": "Seitwärtssprung",
        "muscles": ["glutes", "quads", "hip_abductors"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Lateral Bounds", "Seitwärtssprung", "Side Bound"],
    },
    "Goblet Squat": {
        "de": "Goblet-Kniebeuge",
        "muscles": ["quads", "glutes", "core"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": ["Goblet Kniebeuge", "DB Goblet Squat", "KH Goblet Squat"],
    },
    "Isometric Shoulder Hold": {
        "de": "Isometrisches Schulterhalten",
        "muscles": ["rotator_cuff", "front_delt"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": [
            "Iso Shoulder", "Shoulder Iso Press",
            "Isometrisches Schulterhalten", "Wall Press",
        ],
    },

    # ========================================================================
    # KATALOG-AUSBAU — Übungen aus den 29 Default-Katalog-Protokollen
    # (Nordic/Copenhagen-Prevention, Askling, Otago, Thrower's Ten,
    # Tennis-Elbow, Ankle/Achilles, Knie-OA-Zirkel, S&C-Klassiker)
    # ========================================================================

    # --- Strength & Conditioning Klassiker ---
    "Close Grip Bench Press": {
        "de": "Enges Bankdrücken",
        "muscles": ["triceps", "chest"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Close-Grip Bench Press", "CG Bench Press",
            "Enges Bankdrücken", "Enges Bankdruecken",
        ],
    },
    "Back Extension": {
        "de": "Rückenstrecken",
        "muscles": ["erectors", "glutes", "hamstrings"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": [
            "Hyperextension", "Hyperextensions",
            "Rückenstrecken", "Rueckenstrecken",
        ],
    },
    "Dumbbell Pullover": {
        "de": "Überzüge",
        "muscles": ["chest", "lats"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["DB Pullover", "Pullover", "Überzüge", "Ueberzuege"],
    },
    "Trap Bar Deadlift": {
        "de": "Trapbar-Kreuzheben",
        "muscles": ["back", "glutes", "quads"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Hex Bar Deadlift", "Trap Bar DL", "Trapbar-Kreuzheben"],
    },
    "Power Clean": {
        "de": "Umsetzen",
        "muscles": ["quads", "glutes", "traps"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Power Cleans", "Umsetzen", "Standumsetzen"],
    },
    "Push Press": {
        "de": "Schwungdrücken",
        "muscles": ["front_delt", "triceps", "quads"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Push-Press", "Schwungdrücken", "Schwungdruecken"],
    },
    "Jump Squat": {
        "de": "Sprungkniebeuge",
        "muscles": ["quads", "glutes"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Jump Squats", "Squat Jump", "Sprungkniebeuge"],
    },
    "Jumping Chin-up": {
        "de": "Sprungklimmzug",
        "muscles": ["back", "biceps"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": ["Jumping Chin Up", "Jumping Pull-up", "Sprungklimmzug"],
    },
    "Sit-up": {
        "de": "Sit-up",
        "muscles": ["core", "hip_flexors"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": ["Situp", "Sit Up", "Sit-ups", "Situps", "Rumpfbeugen"],
    },
    "Pallof Press": {
        "de": "Pallof Press",
        "muscles": ["core", "obliques"],
        "category": "isometric",
        "equipment": "cable",
        "aliases": ["Palloff Press", "Pallof-Press", "Anti-Rotation Press"],
    },
    "Reverse Curl": {
        "de": "Curl im Obergriff",
        "muscles": ["brachioradialis", "forearms"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": ["Reverse Curls", "Reverse Barbell Curl", "Reverse-Curl"],
    },
    "Lateral Lunge": {
        "de": "Seitlicher Ausfallschritt",
        "muscles": ["adductors", "quads", "glutes"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": [
            "Side Lunge", "Seitlicher Ausfallschritt", "Seitausfallschritt",
        ],
    },
    "Cable Hip Adduction": {
        "de": "Kabelzug-Adduktion",
        "muscles": ["adductors"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": ["Standing Cable Hip Adduction", "Kabel-Adduktion"],
    },

    # --- Prevention (Nordic / Copenhagen / Groin) ---
    "Nordic Hamstring Curl": {
        "de": "Nordic Hamstring Curl",
        "muscles": ["hamstrings"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Nordic Curl", "Nordic Curls", "Nordics", "NHE",
            "Nordic Hamstring Exercise", "Nordischer Hamstring-Curl",
        ],
    },
    "Copenhagen Adduction": {
        "de": "Kopenhagen-Adduktion",
        "muscles": ["adductors", "core"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Copenhagen Plank", "Copenhagen Adductor Exercise",
            "Copenhagen", "Kopenhagen-Adduktion", "Kopenhagen-Plank",
        ],
    },
    "Adductor Squeeze": {
        "de": "Adduktorenpressen",
        "muscles": ["adductors"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": [
            "Adductor Squeeze Feet", "Adductor Squeeze Knees",
            "Isometric Adduction", "Adduktorenpressen",
        ],
    },

    # --- Plyometrie / Return-to-Sport ---
    "Broad Jump": {
        "de": "Standweitsprung",
        "muscles": ["glutes", "quads"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Broad Jumps", "Standing Long Jump", "Standweitsprung"],
    },
    "Depth Jump": {
        "de": "Tiefsprung",
        "muscles": ["quads", "glutes", "calves"],
        "category": "plyometric",
        "equipment": "box",
        "aliases": ["Depth Jumps", "Drop Jump", "Tiefsprung"],
    },
    "Vertical Jump": {
        "de": "Vertikalsprung",
        "muscles": ["quads", "glutes", "calves"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Countermovement Jump", "CMJ", "Vertikalsprung"],
    },
    "Single-Leg Hop": {
        "de": "Einbeinsprung",
        "muscles": ["calves", "quads", "glutes"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Single Leg Hop", "SL Hop", "Einbeinsprung"],
    },
    "Double-Leg Hop": {
        "de": "Beidbeinsprung",
        "muscles": ["calves", "quads"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Double Leg Hop", "Beidbeinsprung"],
    },
    "Pogo Hop": {
        "de": "Pogo-Sprung",
        "muscles": ["calves"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Pogo Hops", "Pogos", "Pogo-Sprünge", "Pogo-Spruenge"],
    },
    "Bound": {
        "de": "Sprunglauf",
        "muscles": ["glutes", "hamstrings"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Bounds", "Bounding", "Sprunglauf"],
    },

    # --- Hamstring Rehab (Askling L-Protokoll) ---
    "Extender": {
        "de": "Askling Extender",
        "muscles": ["hamstrings"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["The Extender", "Askling Extender"],
    },
    "Diver": {
        "de": "Askling Diver",
        "muscles": ["hamstrings", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["The Diver", "Askling Diver"],
    },
    "Glider": {
        "de": "Askling Glider",
        "muscles": ["hamstrings", "adductors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["The Glider", "Askling Glider"],
    },

    # --- Balance & Gangschule (Otago, Sturzprävention) ---
    "Sit to Stand": {
        "de": "Aufstehen vom Stuhl",
        "muscles": ["quads", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Chair Stand", "Chair Rise", "STS", "Aufstehen vom Stuhl",
        ],
    },
    "Wobble Board Balance": {
        "de": "Wackelbrett",
        "muscles": ["proprioception"],
        "category": "rehab",
        "equipment": "other",
        "aliases": [
            "Wobble Board", "Balance Board", "Balance Board Stand",
            "Wackelbrett", "Therapiekreisel",
        ],
    },
    "Tandem Stance": {
        "de": "Tandemstand",
        "muscles": ["proprioception"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Tandemstand", "Heel-to-Toe Stance"],
    },
    "Tandem Walk": {
        "de": "Tandemgang",
        "muscles": ["proprioception"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Tandemgang", "Heel-to-Toe Walk", "Backwards Tandem Walk",
        ],
    },
    "Heel Walking": {
        "de": "Fersengang",
        "muscles": ["tibialis_anterior"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Heel Walk", "Fersengang"],
    },
    "Toe Walking": {
        "de": "Zehenspitzengang",
        "muscles": ["calves"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Toe Walk", "Zehengang", "Zehenspitzengang"],
    },
    "Backwards Walking": {
        "de": "Rückwärtsgehen",
        "muscles": ["full_body"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Backward Walking", "Rückwärtsgehen", "Rueckwaertsgehen",
        ],
    },
    "Sideways Walking": {
        "de": "Seitwärtsgehen",
        "muscles": ["glute_med"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Side Stepping", "Seitwärtsgehen", "Seitwaertsgehen"],
    },
    "Figure-Eight Walk": {
        "de": "Achtergang",
        "muscles": ["proprioception"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Figure 8 Walk", "Figure-8 Walk", "Achtergang", "Achterschleife",
        ],
    },
    "Toe Raise": {
        "de": "Zehenheben",
        "muscles": ["tibialis_anterior"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Toe Raises", "Tibialis Raise", "Zehenheben"],
    },
    "Lateral Band Walk": {
        "de": "Seitwärtsgehen mit Band",
        "muscles": ["glute_med", "hip_abductors"],
        "category": "rehab",
        "equipment": "band",
        "aliases": [
            "Band Walk", "Lateral Walk", "Monster Walk",
            "Seitwärtsgehen mit Band", "Seitwaertsgehen mit Band",
        ],
    },

    # --- Sprunggelenk (Ankle Sprain / Achilles-Ruptur) ---
    "Ankle Plantarflexion": {
        "de": "Aktive Plantarflexion",
        "muscles": ["calves"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Active Plantarflexion", "Plantarflexion",
            "Aktive Plantarflexion",
        ],
    },
    "Ankle Dorsiflexion": {
        "de": "Aktive Dorsalextension",
        "muscles": ["tibialis_anterior"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Active Dorsiflexion", "Dorsiflexion",
            "Aktive Dorsalextension",
        ],
    },
    "Ankle Inversion": {
        "de": "Aktive Inversion",
        "muscles": ["tibialis_posterior"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Active Inversion", "Inversion", "Aktive Inversion"],
    },
    "Ankle Eversion": {
        "de": "Aktive Eversion",
        "muscles": ["peroneals"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Active Eversion", "Eversion", "Aktive Eversion"],
    },
    "Band Plantarflexion": {
        "de": "Plantarflexion mit Band",
        "muscles": ["calves"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Theraband Plantarflexion", "Plantarflexion mit Band"],
    },
    "Band Dorsiflexion": {
        "de": "Dorsalextension mit Band",
        "muscles": ["tibialis_anterior"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Theraband Dorsalextension", "Dorsalextension mit Band"],
    },
    "Band Inversion": {
        "de": "Inversion mit Band",
        "muscles": ["tibialis_posterior"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Theraband Inversion", "Inversion mit Band"],
    },
    "Band Eversion": {
        "de": "Eversion mit Band",
        "muscles": ["peroneals"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Theraband Eversion", "Eversion mit Band"],
    },
    "Ankle Circles": {
        "de": "Fußkreisen",
        "muscles": ["ankle_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Ankle Circle", "Fußkreisen", "Fusskreisen"],
    },
    "Ankle Alphabet": {
        "de": "Fuß-Alphabet",
        "muscles": ["ankle_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Fuß-Alphabet", "Fuss-Alphabet"],
    },

    # --- Achilles / Wade / Fuß (Silbernagel, Plantarfasziitis) ---
    "Quick Rebounding Toe Raise": {
        "de": "Federndes Wadenheben",
        "muscles": ["calves", "achilles_tendon"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": [
            "Quick Rebounding Toe Raises", "Quick Rebounding Calf Raise",
            "Federndes Wadenheben",
        ],
    },
    "Seated Eccentric Calf Raise": {
        "de": "Sitzendes exzentrisches Wadenheben",
        "muscles": ["soleus", "achilles_tendon"],
        "category": "rehab",
        "equipment": "machine",
        "aliases": [
            "Seated Eccentric Heel Raise",
            "Sitzendes exzentrisches Wadenheben",
        ],
    },
    "Calf Stretch": {
        "de": "Wadendehnung",
        "muscles": ["calves"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": [
            "Gastrocnemius Stretch", "Wall Calf Stretch", "Wadendehnung",
        ],
    },
    "Towel Scrunch": {
        "de": "Zehenkrallen",
        "muscles": ["foot_intrinsics"],
        "category": "rehab",
        "equipment": "other",
        "aliases": [
            "Towel Scrunches", "Towel Curl",
            "Handtuch-Krallen", "Zehenkrallen",
        ],
    },

    # --- Knie-OA / Neuromuskulärer Zirkel ---
    "Band Knee Extension": {
        "de": "Kniestreckung mit Band",
        "muscles": ["quads"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Banded Knee Extension", "Kniestreckung mit Band"],
    },
    "Standing Hip Abduction": {
        "de": "Hüftabduktion im Stand",
        "muscles": ["glute_med", "hip_abductors"],
        "category": "rehab",
        "equipment": "band",
        "aliases": [
            "Hip Abduction Standing",
            "Hüftabduktion im Stand", "Hueftabduktion im Stand",
        ],
    },
    "Sliding Board Skating": {
        "de": "Gleitbrett-Skating",
        "muscles": ["adductors", "glutes"],
        "category": "rehab",
        "equipment": "other",
        "aliases": [
            "Slide Board Skating", "Slideboard Skating",
            "Gleitbrett-Skating",
        ],
    },
    "Slide Forward-Backward": {
        "de": "Slide Vor-Zurück",
        "muscles": ["quads", "hamstrings"],
        "category": "rehab",
        "equipment": "other",
        "aliases": [
            "Forward-Backward Slide", "Slide Vor-Zurück", "Slide Vor-Zurueck",
        ],
    },
    "Slide Sideways": {
        "de": "Slide Seitwärts",
        "muscles": ["adductors", "glute_med"],
        "category": "rehab",
        "equipment": "other",
        "aliases": ["Sideways Slide", "Slide Seitwärts", "Slide Seitwaerts"],
    },

    # --- Schulter (Frozen Shoulder, Thrower's Ten) ---
    "Wand External Rotation": {
        "de": "Außenrotation mit Stab",
        "muscles": ["rotator_cuff", "shoulder_rom"],
        "category": "rehab",
        "equipment": "other",
        "aliases": [
            "Stick External Rotation",
            "Außenrotation mit Stab", "Aussenrotation mit Stab",
        ],
    },
    "External Rotation Stretch with Stick": {
        "de": "Außenrotationsdehnung mit Stab",
        "muscles": ["shoulder_rom"],
        "category": "mobility",
        "equipment": "other",
        "aliases": [
            "Wand External Rotation Stretch",
            "Außenrotationsdehnung mit Stab",
            "Aussenrotationsdehnung mit Stab",
        ],
    },
    "Cross-Body Stretch": {
        "de": "Cross-Body-Dehnung",
        "muscles": ["posterior_capsule", "shoulder_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": [
            "Cross Body Stretch", "Posterior Capsule Stretch",
            "Cross-Body-Dehnung",
        ],
    },
    "Behind-Back Towel Stretch": {
        "de": "Handtuchdehnung",
        "muscles": ["shoulder_rom"],
        "category": "mobility",
        "equipment": "other",
        "aliases": [
            "Behind the Back Towel Stretch", "Handtuchdehnung",
        ],
    },
    "Sleeper Stretch": {
        "de": "Sleeper Stretch",
        "muscles": ["posterior_capsule"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Sleeper-Stretch", "Schläfer-Dehnung", "Schlaefer-Dehnung"],
    },
    "Doorway Stretch": {
        "de": "Türrahmen-Dehnung",
        "muscles": ["chest", "shoulder_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Pec Stretch", "Türrahmen-Dehnung", "Tuerrahmen-Dehnung"],
    },
    "PNF D2 Flexion": {
        "de": "PNF-Diagonale D2 Flexion",
        "muscles": ["rotator_cuff", "front_delt"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["D2 Flexion", "PNF-Diagonale D2 Flexion"],
    },
    "PNF D2 Extension": {
        "de": "PNF-Diagonale D2 Extension",
        "muscles": ["rotator_cuff", "lats"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["D2 Extension", "PNF-Diagonale D2 Extension"],
    },
    "Sidelying External Rotation": {
        "de": "Außenrotation in Seitenlage",
        "muscles": ["rotator_cuff", "infraspinatus"],
        "category": "rehab",
        "equipment": "dumbbell",
        "aliases": [
            "Sidelying Dumbbell External Rotation",
            "Side-Lying External Rotation",
            "Außenrotation in Seitenlage", "Aussenrotation in Seitenlage",
        ],
    },
    "Prone Horizontal Abduction": {
        "de": "Horizontale Abduktion in Bauchlage",
        "muscles": ["rear_delt", "mid_traps"],
        "category": "rehab",
        "equipment": "dumbbell",
        "aliases": [
            "Prone Horizontal Abduction Full ER",
            "Horizontale Abduktion in Bauchlage",
        ],
    },
    "Prone Rowing": {
        "de": "Rudern in Bauchlage",
        "muscles": ["back", "rear_delt"],
        "category": "rehab",
        "equipment": "dumbbell",
        "aliases": [
            "Prone Row", "Prone Rowing into ER", "Rudern in Bauchlage",
        ],
    },
    "Seated Press-up": {
        "de": "Sitzender Stütz",
        "muscles": ["scapular_depressors", "triceps"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Seated Press Up", "Sitzender Stütz", "Sitzender Stuetz",
        ],
    },

    # --- Nacken (Deep Neck Flexor Training) ---
    "Craniocervical Flexion": {
        "de": "Kraniozervikale Flexion",
        "muscles": ["deep_neck_flexors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "CCF", "Kraniozervikale Flexion",
            "Deep Neck Flexor Activation", "Tiefe Nackenbeuger",
        ],
    },
    "Chin Tuck": {
        "de": "Kinnretraktion",
        "muscles": ["deep_neck_flexors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Chin Tucks", "Kinnretraktion"],
    },

    # --- Unterarm / Tennisellenbogen ---
    "Wrist Extension": {
        "de": "Handgelenkstreckung",
        "muscles": ["forearm_extensors"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Wrist Extensions", "Reverse Wrist Curl", "Handgelenkstreckung",
        ],
    },
    "Wrist Flexion": {
        "de": "Handgelenkbeugung",
        "muscles": ["forearm_flexors"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Wrist Curl", "Handgelenkbeugung"],
    },
    "Wrist Supination": {
        "de": "Unterarm-Supination",
        "muscles": ["forearms"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Forearm Supination", "Unterarm-Supination"],
    },
    "Wrist Pronation": {
        "de": "Unterarm-Pronation",
        "muscles": ["forearms"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Forearm Pronation", "Unterarm-Pronation"],
    },
    "Tyler Twist": {
        "de": "Tyler Twist",
        "muscles": ["forearm_extensors"],
        "category": "rehab",
        "equipment": "other",
        "aliases": ["FlexBar Tyler Twist", "Tyler-Twist"],
    },
    "Grip Squeeze": {
        "de": "Ballpressen",
        "muscles": ["forearms"],
        "category": "rehab",
        "equipment": "other",
        "aliases": ["Grip Squeezes", "Ball Squeeze", "Ballpressen"],
    },

    # ========================================================================
    # KATALOG-RESTE — verbleibende Übungen aus Prävention/Reha-Protokollen
    # (FIFA 11+ Lauf-/Agility-Drills, Nacken-Isometrie, Frozen-Shoulder-
    # Mobilisation, Hölmich-Leiste, Thrower's-Ten-90°, Otago, Landetechnik)
    # ========================================================================

    # --- FIFA 11+ (Lauf- & Agility-Drills, Warm-up) ---
    "Running Straight Ahead": {
        "de": "Geradeauslaufen",
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Geradeauslaufen", "Straight Ahead Run"],
    },
    "Running Hip Out": {
        "de": "Hüfte nach außen",
        "muscles": ["hip_abductors", "hip_rotators"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Hüfte nach außen", "Hip Out Run"],
    },
    "Running Hip In": {
        "de": "Hüfte nach innen",
        "muscles": ["hip_adductors", "hip_rotators"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Hüfte nach innen", "Hip In Run"],
    },
    "Running Circling Partner": {
        "de": "Partner umkreisen",
        "muscles": ["full_body", "hip_abductors"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Partner umkreisen", "Circle Partner"],
    },
    "Jumping with Shoulder Contact": {
        "de": "Sprung mit Schulterkontakt",
        "muscles": ["quads", "glutes", "core"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Sprung mit Schulterkontakt", "Shoulder Contact Jump"],
    },
    "Running Quick Forwards Backwards": {
        "de": "Schnell vor und zurück",
        "muscles": ["quads", "glutes"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Schnell vor und zurück", "Quick Forward-Backward"],
    },
    "Running Across the Pitch": {
        "de": "Über das Feld laufen",
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Über das Feld laufen", "Straight Sprint"],
    },
    "Plant and Cut": {
        "de": "Richtungswechsel",
        "muscles": ["quads", "glutes", "hip_abductors"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Richtungswechsel", "Cutting Drill", "Plant-and-Cut"],
    },

    # --- Sprunggelenk (Ankle Sprain) ---
    "Isometric Eversion": {
        "de": "Isometrische Eversion",
        "muscles": ["peroneals"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": ["Iso Eversion", "Isometrische Eversion"],
    },
    "Agility Drill": {
        "de": "Agility-Übung",
        "muscles": ["full_body", "proprioception"],
        "category": "plyometric",
        "equipment": "other",
        "aliases": ["Agility Drills", "Koordinationsleiter", "Agility-Übung"],
    },

    # --- Frozen Shoulder (Mobilisation) ---
    "Supine Assisted Flexion": {
        "de": "Assistierte Flexion in Rückenlage",
        "muscles": ["shoulder_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Assistierte Flexion Rückenlage", "Assisted Flexion"],
    },
    "Table Slide": {
        "de": "Tischgleiten",
        "muscles": ["shoulder_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Table Slides", "Tischgleiten", "Tisch-Slide"],
    },
    "Pulley Flexion": {
        "de": "Seilzug-Flexion",
        "muscles": ["shoulder_rom"],
        "category": "mobility",
        "equipment": "other",
        "aliases": ["Seilzug-Flexion", "Pulley Exercise", "Umlenkrolle Flexion"],
    },

    # --- Leiste (Hölmich) ---
    "Folding Knife Sit-up": {
        "de": "Klappmesser",
        "muscles": ["adductors", "core", "hip_flexors"],
        "category": "rehab",
        "equipment": "other",
        "aliases": ["Klappmesser", "Folding Knife", "Jackknife Sit-up"],
    },
    "Cross-Country Skiing One Leg": {
        "de": "Einbeiniges Skilanglauf-Imitat",
        "muscles": ["quads", "glutes", "coordination"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Einbeiniges Skilanglauf-Imitat", "One-Leg Ski"],
    },
    "Fitter Sideways Training": {
        "de": "Fitter seitlich",
        "muscles": ["adductors", "glute_med"],
        "category": "rehab",
        "equipment": "other",
        "aliases": ["Fitter seitlich", "Slideboard seitlich", "Sideways Slide Training"],
    },

    # --- Nacken (Deep Neck Flexor / Extensor) ---
    "Supine Head Lift": {
        "de": "Kopfheben in Rückenlage",
        "muscles": ["deep_neck_flexors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Kopfheben Rückenlage", "Supine Neck Lift"],
    },
    "Prone Head Lift": {
        "de": "Kopfheben in Bauchlage",
        "muscles": ["neck_extensors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Kopfheben Bauchlage", "Prone Neck Lift"],
    },
    "Isometric Neck Flexion": {
        "de": "Isometrische Nackenflexion",
        "muscles": ["deep_neck_flexors"],
        "category": "isometric",
        "equipment": "band",
        "aliases": ["Iso Nackenbeugung", "Isometrische Nackenflexion"],
    },
    "Isometric Neck Flexion Diagonal": {
        "de": "Isometrische Nackenflexion diagonal",
        "muscles": ["deep_neck_flexors", "sternocleidomastoid"],
        "category": "isometric",
        "equipment": "band",
        "aliases": ["Iso Nackenbeugung diagonal", "Isometrische Nackenflexion diagonal"],
    },
    "Isometric Neck Extension": {
        "de": "Isometrische Nackenextension",
        "muscles": ["neck_extensors"],
        "category": "isometric",
        "equipment": "band",
        "aliases": ["Iso Nackenstreckung", "Isometrische Nackenextension"],
    },

    # --- Tennisarm (Isometrie & Dehnung) ---
    "Isometric Wrist Extension": {
        "de": "Isometrische Handgelenkstreckung",
        "muscles": ["forearm_extensors"],
        "category": "isometric",
        "equipment": "dumbbell",
        "aliases": ["Iso Handgelenkstreckung", "Isometrische Handgelenkextension"],
    },
    "Wrist Extensor Stretch": {
        "de": "Unterarmstrecker-Dehnung",
        "muscles": ["forearm_extensors"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Handgelenkstrecker-Dehnung", "Unterarmstrecker-Dehnung"],
    },

    # --- Thrower's Ten (90°-Abduktion) ---
    "External Rotation at Shoulder Level": {
        "de": "Außenrotation in Schulterhöhe",
        "muscles": ["rotator_cuff", "infraspinatus"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Außenrotation Schulterhöhe", "ER at 90 Degrees", "ER 90 Abduktion"],
    },
    "Internal Rotation at Shoulder Level": {
        "de": "Innenrotation in Schulterhöhe",
        "muscles": ["rotator_cuff", "subscapularis"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Innenrotation Schulterhöhe", "IR at 90 Degrees", "IR 90 Abduktion"],
    },

    # --- Otago (Ausdauer) ---
    "Walking": {
        "de": "Gehen",
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Gehen", "Spazieren", "Gehtraining"],
    },

    # --- Landetechnik / Plyo ---
    "Box Landing Drill": {
        "de": "Landetechnik",
        "muscles": ["quads", "glutes", "calves"],
        "category": "plyometric",
        "equipment": "box",
        "aliases": ["Landetechnik", "Drop Landing", "Box Landing"],
    },
}


# ---------------------------------------------------------------------------
# Lookup index  (built once on import)
# ---------------------------------------------------------------------------
_ALIAS_MAP: dict[str, str] = {}
_NORMALIZED_MAP: dict[str, str] = {}  # spaces/hyphens stripped -> canonical


def _normalize(name: str) -> str:
    """Compact form for spacing-insensitive lookup ("Push-up" -> "pushup")."""
    return name.lower().replace("-", "").replace(" ", "")


def _build_index() -> None:
    """Build a case-insensitive alias -> canonical name lookup."""
    for canonical, meta in EXERCISES.items():
        key = canonical.lower().strip()
        _ALIAS_MAP[key] = canonical
        _NORMALIZED_MAP.setdefault(_normalize(canonical), canonical)
        for alias in [meta["de"], *meta.get("aliases", [])]:
            _ALIAS_MAP[alias.lower().strip()] = canonical
            _NORMALIZED_MAP.setdefault(_normalize(alias), canonical)


_build_index()


def resolve(name: str) -> str | None:
    """Resolve any exercise name/alias to its canonical form.

    Returns the canonical name or None if not found.
    """
    return _ALIAS_MAP.get(name.lower().strip())


def _bigrams(s: str) -> set[str]:
    return {s[i : i + 2] for i in range(len(s) - 1)}


def _dice(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return (2 * len(a & b)) / (len(a) + len(b))


# Ein Wortpaar gilt als Tippfehler-Variante ab dieser Bigram-Ähnlichkeit.
# 0.7 trennt "squatt"/"squat" (0.89) von "wand"/"band" (0.67) — ein anderes
# erstes Wort ist meist eine andere Übung, kein Tippfehler.
_WORD_SIMILARITY = 0.7


def resolve_fuzzy(name: str, threshold: float = 0.8) -> str | None:
    """Best-effort fuzzy match when exact lookup fails.

    Fuzzy matching is a typo-corrector, not a synonym finder — variants
    belong in the registry as aliases. Three stages:

    1. Exact lookup.
    2. Spacing-insensitive lookup ("Benchpress" -> "Bench Press").
    3. Bigram similarity (Sorensen-Dice) with guards: the candidate must
       have the same word count (so "Knee Extension" never matches
       "Terminal Knee Extension"), and every aligned word pair must itself
       be similar (so "Wand External Rotation" never matches
       "Band External Rotation").

    Returns None if below threshold.
    """
    name_lower = name.lower().strip()

    # Exact match first
    exact = _ALIAS_MAP.get(name_lower)
    if exact:
        return exact

    normalized = _NORMALIZED_MAP.get(_normalize(name_lower))
    if normalized:
        return normalized

    name_bi = _bigrams(name_lower)
    if not name_bi:
        return None
    name_words = name_lower.split()

    best_score = 0.0
    best_match = None
    for alias, canonical in _ALIAS_MAP.items():
        alias_words = alias.split()
        if len(alias_words) != len(name_words):
            continue
        score = _dice(name_bi, _bigrams(alias))
        if score < threshold or score <= best_score:
            continue
        if all(
            nw == aw or _dice(_bigrams(nw), _bigrams(aw)) >= _WORD_SIMILARITY
            for nw, aw in zip(name_words, alias_words)
        ):
            best_score = score
            best_match = canonical

    return best_match


def suggest(name: str, limit: int = 3, threshold: float = 0.45) -> list[str]:
    """Vorschläge für einen unbekannten Namen ("Meintest du …?"), als deutsche Namen.

    Lockerer als resolve_fuzzy (keine Wortzahl-/Wortpaar-Wächter), weil hier
    nur vorgeschlagen und nie still ersetzt wird.
    """
    name_bi = _bigrams(name.lower().strip())
    best: dict[str, float] = {}
    for alias, canonical in _ALIAS_MAP.items():
        score = _dice(name_bi, _bigrams(alias))
        if score >= threshold and score > best.get(canonical, 0):
            best[canonical] = score
    ranked = sorted(best, key=best.get, reverse=True)[:limit]
    # Nur Vorschläge nahe am besten Treffer (sonst "Facepulls" → auch Klimmzug)
    return [EXERCISES[c]["de"] for c in ranked if best[c] >= best[ranked[0]] * 0.8]


def german_name(canonical_name: str) -> str:
    """Return the German display name, falling back to the canonical name."""
    entry = EXERCISES.get(canonical_name)
    return entry["de"] if entry else canonical_name


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
