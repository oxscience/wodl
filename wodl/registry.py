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
            "Barbell Bench Press", "Flat Bench Press", "Wide-Grip Barbell Bench Press",
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
            "DB Bench Press", "DB Bench", "One Arm Dumbbell Bench Press",
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
            "Cable Flye", "Kabelzug Fly", "Cable Crossover", "Low Cable Crossover",
        ],
    },
    "Incline DB Fly": {
        "muscles": ["upper_chest"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Incline Dumbbell Fly", "Incline Flye",
            "KH Schrägbank Fly", "Incline Dumbbell Flyes",
        ],
    },
    "Push-up": {
        "muscles": ["chest", "triceps", "front_delt"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": ["Pushup", "Push Up", "Liegestütz", "Liegestuetz", "Push-Up Wide", "Pushups", "Single-Arm Push-Up"],
    },

    # --- Back ---
    "Deadlift": {
        "muscles": ["back", "glutes", "hamstrings"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Kreuzheben", "Conventional Deadlift", "DL", "Barbell Deadlift", "Deadlift with Bands",
        ],
    },
    "Sumo Deadlift": {
        "muscles": ["back", "glutes", "quads"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Sumo DL", "Sumo Kreuzheben", "Sumo Deadlift with Bands"],
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
            "Vorgebeugtes Rudern", "Barbell Bent Over Row", "Bent Over Barbell Row",
        ],
    },
    "Dumbbell Row": {
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "KH Rudern", "DB Row", "One Arm Row",
            "Einarmiges Rudern", "One-Arm Dumbbell Row",
        ],
    },
    "Pull-up": {
        "muscles": ["back", "biceps"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": [
            "Pullup", "Pull Up", "Klimmzug", "Klimmzüge",
            "Klimmzuege", "Pullups",
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
            "Latzug", "Lat Pull Down", "Latziehen", "One Arm Lat Pulldown", "Wide-Grip Lat Pulldown",
        ],
    },
    "Cable Row": {
        "muscles": ["back", "biceps", "rear_delt"],
        "category": "compound",
        "equipment": "cable",
        "aliases": [
            "Seated Cable Row", "Kabelrudern", "Seated Row", "Seated Cable Rows",
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
            "Military Press", "Standing Press", "Press", "Seated Barbell Military Press", "Standing Military Press",
        ],
    },
    "Dumbbell OHP": {
        "muscles": ["front_delt", "triceps"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "DB OHP", "KH Schulterdrücken", "Dumbbell Shoulder Press",
            "DB Shoulder Press", "Dumbbell One-Arm Shoulder Press",
        ],
    },
    "Lateral Raise": {
        "muscles": ["side_delt"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Seitheben", "Side Raise", "Lat Raise",
            "KH Seitheben", "DB Lateral Raise", "Shoulder Abduction", "Lying One-Arm Lateral Raise", "Side Lateral Raise",
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
            "Hintere Schulter Fly", "Reverse Flyes",
        ],
    },
    "Shrug": {
        "muscles": ["traps"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": ["Shrugs", "BB Shrug", "Schulterheben", "Barbell Shrug"],
    },
    "Upright Row": {
        "muscles": ["traps", "side_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Aufrechtes Rudern", "Upright Barbell Row"],
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
        "aliases": ["Hammercurl", "Hammer Curls", "Alternate Hammer Curl"],
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
        "aliases": ["Incline DB Curl", "Incline Dumbbell Curl", "Schrägbank Curl", "Alternate Incline Dumbbell Curl", "Flexor Incline Dumbbell Curls"],
    },
    "Tricep Pushdown": {
        "muscles": ["triceps"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": [
            "Cable Pushdown", "Trizepsdrücken", "Trizepsdruecken",
            "Tricep Push Down", "Pushdown", "Triceps Pushdown",
        ],
    },
    "Overhead Tricep Extension": {
        "muscles": ["triceps"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": [
            "Overhead Extension", "French Press",
            "Trizeps Überkopf", "Cable Overhead Extension", "Cable Rope Overhead Triceps Extension",
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
            "BB Squat", "Barbell Squat", "Barbell Full Squat", "Olympic Squat", "One Leg Barbell Squat", "Squat with Bands", "Weighted Squat",
        ],
    },
    "Front Squat": {
        "muscles": ["quads", "glutes", "core"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Frontkniebeuge", "Front Kniebeuge", "Front Barbell Squat"],
    },
    "Leg Press": {
        "muscles": ["quads", "glutes"],
        "category": "compound",
        "equipment": "machine",
        "aliases": ["Beinpresse", "LP", "Smith Machine Leg Press"],
    },
    "Leg Extension": {
        "muscles": ["quads"],
        "category": "isolation",
        "equipment": "machine",
        "aliases": [
            "Leg Ext", "Knee Extension", "Beinstrecker", "Beinstrecken", "Leg Extensions", "Single-Leg Leg Extension",
        ],
    },
    "Leg Curl": {
        "muscles": ["hamstrings"],
        "category": "isolation",
        "equipment": "machine",
        "aliases": [
            "Lying Leg Curl", "Seated Leg Curl", "Standing Leg Curl",
            "Beinbeuger", "Beinbeugen", "Lying Leg Curls",
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
        "aliases": ["Lunges", "Ausfallschritt", "Ausfallschritte", "Dumbbell Lunges"],
    },
    "Hip Thrust": {
        "muscles": ["glutes", "hamstrings"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Hüftheben", "Hueftheben", "BB Hip Thrust", "Barbell Hip Thrust"],
    },
    "Calf Raise": {
        "muscles": ["calves"],
        "category": "isolation",
        "equipment": "machine",
        "aliases": [
            "Standing Calf Raise", "Seated Calf Raise",
            "Double-Leg Calf Raise", "Beidbeiniges Wadenheben",
            "Wadenheben", "Calf Raises", "Smith Machine Calf Raise", "Standing Calf Raises",
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

    # ========================================================================
    # REHAB — Evidenzbasierte Reha-Übungen (ACL, Rotator Cuff, LBP, Achilles)
    # Quellen: Wilk & Arrigo 2017 (ACL), Ellenbecker 2017 (Shoulder),
    # McGill 2016 (Low Back), Alfredson 1998 (Achilles Tendinopathy)
    # ========================================================================

    # --- Knee Rehab ---
    "Quad Set": {
        "muscles": ["quads"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Quad Sets", "Quadrizeps-Anspannung", "Quad Contraction", "VMO Set"],
    },
    "Straight Leg Raise": {
        "muscles": ["quads", "hip_flexors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["SLR", "Gestrecktes Beinheben", "Aktives Beinheben"],
    },
    "Terminal Knee Extension": {
        "muscles": ["quads"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["TKE", "Knie-Endstreckung", "Endstreckung Knie"],
    },
    "Heel Slide": {
        "muscles": ["hamstrings", "knee_rom"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Heel Slides", "Fersenrutschen", "Knieflexion-Slide"],
    },
    "Mini Squat": {
        "muscles": ["quads", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Mini Squats", "Teilkniebeuge", "Partial Squat",
            "Knee Bend", "Knee Bends",
        ],
    },
    "Wall Sit": {
        "muscles": ["quads", "glutes"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": ["Wall Squat", "Wandsitz"],
    },
    "Step-up": {
        "muscles": ["quads", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Step Up", "Stepups", "Aufsteiger"],
    },
    "Step-down": {
        "muscles": ["quads", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Step Down", "Stepdowns", "Absteiger"],
    },
    "Single Leg Bridge": {
        "muscles": ["glutes", "hamstrings"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["SL Bridge", "Einbeinige Brücke", "One-Leg Bridge"],
    },
    "Glute Bridge": {
        "muscles": ["glutes", "hamstrings"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Bridge", "Hüftbrücke", "Hip Bridge", "Bridging"],
    },
    "Clamshell": {
        "muscles": ["glute_med", "hip_abductors"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Clamshells", "Muschel", "Hip Clamshell"],
    },
    "Side-Lying Hip Abduction": {
        "muscles": ["glute_med", "hip_abductors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Side Leg Raise", "Side-Lying Leg Raise",
            "Seitheben Bein", "Hip Abduction", "Side Leg Raises",
        ],
    },
    "Single Leg Balance": {
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
        "muscles": ["shoulder_rom"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Pendelübung", "Pendulum Exercise", "Codman Pendulum"],
    },
    "Wall Walk": {
        "muscles": ["shoulder_rom", "front_delt"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Wall Climb", "Finger Walk", "Wandklettern"],
    },
    "Band External Rotation": {
        "muscles": ["rotator_cuff", "infraspinatus", "teres_minor"],
        "category": "rehab",
        "equipment": "band",
        "aliases": [
            "External Rotation", "ER Band", "Theraband Außenrotation",
            "Band ER", "Rotator Cuff ER", "External Rotation with Band",
        ],
    },
    "Band Internal Rotation": {
        "muscles": ["rotator_cuff", "subscapularis"],
        "category": "rehab",
        "equipment": "band",
        "aliases": [
            "Internal Rotation", "IR Band", "Theraband Innenrotation",
            "Band IR", "Internal Rotation with Band",
        ],
    },
    "Scapular Retraction": {
        "muscles": ["rhomboids", "mid_traps"],
        "category": "rehab",
        "equipment": "band",
        "aliases": [
            "Scap Retraction", "Schulterblatt-Retraktion",
            "Band Pull-Apart", "Pull Apart",
        ],
    },
    "Prone Y": {
        "muscles": ["lower_traps", "rotator_cuff"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Y Raise", "Prone Y Raise", "Bauchlage Y"],
    },
    "Prone T": {
        "muscles": ["mid_traps", "rear_delt"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["T Raise", "Prone T Raise", "Bauchlage T"],
    },
    "Prone W": {
        "muscles": ["rotator_cuff", "mid_traps"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["W Raise", "Prone W Raise", "Bauchlage W"],
    },
    "Full Can Raise": {
        "muscles": ["supraspinatus", "side_delt"],
        "category": "rehab",
        "equipment": "dumbbell",
        "aliases": ["Full Can", "Scaption", "Scaption Raise"],
    },

    # --- Low Back / Core Rehab (McGill Big 3 + progression) ---
    "McGill Curl-up": {
        "muscles": ["rectus_abdominis"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Curl-up", "Modified Curl-up", "McGill Curl Up"],
    },
    "Side Plank": {
        "muscles": ["obliques", "qlm", "core"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": [
            "Side Bridge", "Seitstütz", "Seitliche Planke",
            "Lateral Plank",
        ],
    },
    "Bird Dog": {
        "muscles": ["erectors", "glutes", "core"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Bird-Dog", "Vierfüßlerstand", "Quadruped",
            "Opposite Arm Leg",
        ],
    },
    "Dead Bug": {
        "muscles": ["core", "transverse_abdominis"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Dead-Bug", "Toter Käfer", "Dying Bug"],
    },
    "Cat-Cow": {
        "muscles": ["spine_mobility"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Cat Cow", "Katzenbuckel", "Katze-Kuh"],
    },

    # --- Achilles / Calf Rehab (Alfredson Protocol) ---
    "Eccentric Heel Drop": {
        "muscles": ["gastrocnemius", "achilles_tendon"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Alfredson Heel Drop", "Eccentric Calf Drop",
            "Exzentrisches Fersensenken", "Heel Drops",
        ],
    },
    "Bent-Knee Heel Drop": {
        "muscles": ["soleus", "achilles_tendon"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Bent Knee Heel Drop", "Soleus Heel Drop",
            "Gebeugtes Fersensenken",
        ],
    },
    "Single-Leg Calf Raise": {
        "muscles": ["calves"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "SL Calf Raise", "One-Leg Calf Raise",
            "Einbeiniges Wadenheben",
        ],
    },
    "Isometric Calf Hold": {
        "muscles": ["calves", "achilles_tendon"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": ["Iso Calf", "Wadenheben Halten", "Static Calf Hold"],
    },

    # --- Zusätzliche Reha / Plyo / Funktionell ---
    "Ankle Pumps": {
        "muscles": ["calves", "circulation"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Ankle Pump", "Fußwippe", "Sprunggelenkspumpe"],
    },
    "Box Jump": {
        "muscles": ["quads", "glutes", "calves"],
        "category": "plyometric",
        "equipment": "box",
        "aliases": ["Box Jumps", "Kastensprung", "Kastensprünge"],
    },
    "Lateral Bound": {
        "muscles": ["glutes", "quads", "hip_abductors"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Lateral Bounds", "Seitwärtssprung", "Side Bound"],
    },
    "Goblet Squat": {
        "muscles": ["quads", "glutes", "core"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": ["Goblet Kniebeuge", "DB Goblet Squat", "KH Goblet Squat"],
    },
    "Isometric Shoulder Hold": {
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
        "muscles": ["triceps", "chest"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Close-Grip Bench Press", "CG Bench Press",
            "Enges Bankdrücken", "Enges Bankdruecken", "Close-Grip Barbell Bench Press",
        ],
    },
    "Back Extension": {
        "muscles": ["erectors", "glutes", "hamstrings"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": [
            "Hyperextension", "Hyperextensions",
            "Rückenstrecken", "Rueckenstrecken",
        ],
    },
    "Dumbbell Pullover": {
        "muscles": ["chest", "lats"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["DB Pullover", "Pullover", "Überzüge", "Ueberzuege", "Bent-Arm Dumbbell Pullover"],
    },
    "Trap Bar Deadlift": {
        "muscles": ["back", "glutes", "quads"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Hex Bar Deadlift", "Trap Bar DL", "Trapbar-Kreuzheben"],
    },
    "Power Clean": {
        "muscles": ["quads", "glutes", "traps"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Power Cleans", "Umsetzen", "Standumsetzen"],
    },
    "Push Press": {
        "muscles": ["front_delt", "triceps", "quads"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": ["Push-Press", "Schwungdrücken", "Schwungdruecken"],
    },
    "Jump Squat": {
        "muscles": ["quads", "glutes"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Jump Squats", "Squat Jump", "Sprungkniebeuge", "Weighted Jump Squat"],
    },
    "Jumping Chin-up": {
        "muscles": ["back", "biceps"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": ["Jumping Chin Up", "Jumping Pull-up", "Sprungklimmzug"],
    },
    "Sit-up": {
        "muscles": ["core", "hip_flexors"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": ["Situp", "Sit Up", "Sit-ups", "Situps", "Rumpfbeugen"],
    },
    "Pallof Press": {
        "muscles": ["core", "obliques"],
        "category": "isometric",
        "equipment": "cable",
        "aliases": ["Palloff Press", "Pallof-Press", "Anti-Rotation Press"],
    },
    "Reverse Curl": {
        "muscles": ["brachioradialis", "forearms"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": ["Reverse Curls", "Reverse Barbell Curl", "Reverse-Curl"],
    },
    "Lateral Lunge": {
        "muscles": ["adductors", "quads", "glutes"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": [
            "Side Lunge", "Seitlicher Ausfallschritt", "Seitausfallschritt",
        ],
    },
    "Cable Hip Adduction": {
        "muscles": ["adductors"],
        "category": "isolation",
        "equipment": "cable",
        "aliases": ["Standing Cable Hip Adduction", "Kabel-Adduktion"],
    },

    # --- Prevention (Nordic / Copenhagen / Groin) ---
    "Nordic Hamstring Curl": {
        "muscles": ["hamstrings"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Nordic Curl", "Nordic Curls", "Nordics", "NHE",
            "Nordic Hamstring Exercise", "Nordischer Hamstring-Curl",
        ],
    },
    "Copenhagen Adduction": {
        "muscles": ["adductors", "core"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Copenhagen Plank", "Copenhagen Adductor Exercise",
            "Copenhagen", "Kopenhagen-Adduktion", "Kopenhagen-Plank",
        ],
    },
    "Adductor Squeeze": {
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
        "muscles": ["glutes", "quads"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Broad Jumps", "Standing Long Jump", "Standweitsprung", "Side Standing Long Jump"],
    },
    "Depth Jump": {
        "muscles": ["quads", "glutes", "calves"],
        "category": "plyometric",
        "equipment": "box",
        "aliases": ["Depth Jumps", "Drop Jump", "Tiefsprung"],
    },
    "Vertical Jump": {
        "muscles": ["quads", "glutes", "calves"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Countermovement Jump", "CMJ", "Vertikalsprung"],
    },
    "Single-Leg Hop": {
        "muscles": ["calves", "quads", "glutes"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Single Leg Hop", "SL Hop", "Einbeinsprung"],
    },
    "Double-Leg Hop": {
        "muscles": ["calves", "quads"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Double Leg Hop", "Beidbeinsprung"],
    },
    "Pogo Hop": {
        "muscles": ["calves"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Pogo Hops", "Pogos", "Pogo-Sprünge", "Pogo-Spruenge"],
    },
    "Bound": {
        "muscles": ["glutes", "hamstrings"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Bounds", "Bounding", "Sprunglauf"],
    },

    # --- Hamstring Rehab (Askling L-Protokoll) ---
    "Extender": {
        "muscles": ["hamstrings"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["The Extender", "Askling Extender"],
    },
    "Diver": {
        "muscles": ["hamstrings", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["The Diver", "Askling Diver"],
    },
    "Glider": {
        "muscles": ["hamstrings", "adductors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["The Glider", "Askling Glider"],
    },

    # --- Balance & Gangschule (Otago, Sturzprävention) ---
    "Sit to Stand": {
        "muscles": ["quads", "glutes"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Chair Stand", "Chair Rise", "STS", "Aufstehen vom Stuhl",
        ],
    },
    "Wobble Board Balance": {
        "muscles": ["proprioception"],
        "category": "rehab",
        "equipment": "other",
        "aliases": [
            "Wobble Board", "Balance Board", "Balance Board Stand",
            "Wackelbrett", "Therapiekreisel",
        ],
    },
    "Tandem Stance": {
        "muscles": ["proprioception"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Tandemstand", "Heel-to-Toe Stance"],
    },
    "Tandem Walk": {
        "muscles": ["proprioception"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Tandemgang", "Heel-to-Toe Walk", "Backwards Tandem Walk",
        ],
    },
    "Heel Walking": {
        "muscles": ["tibialis_anterior"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Heel Walk", "Fersengang"],
    },
    "Toe Walking": {
        "muscles": ["calves"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Toe Walk", "Zehengang", "Zehenspitzengang"],
    },
    "Backwards Walking": {
        "muscles": ["full_body"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Backward Walking", "Rückwärtsgehen", "Rueckwaertsgehen",
        ],
    },
    "Sideways Walking": {
        "muscles": ["glute_med"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Side Stepping", "Seitwärtsgehen", "Seitwaertsgehen"],
    },
    "Figure-Eight Walk": {
        "muscles": ["proprioception"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Figure 8 Walk", "Figure-8 Walk", "Achtergang", "Achterschleife",
        ],
    },
    "Toe Raise": {
        "muscles": ["tibialis_anterior"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Toe Raises", "Tibialis Raise", "Zehenheben"],
    },
    "Lateral Band Walk": {
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
        "muscles": ["calves"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Active Plantarflexion", "Plantarflexion",
            "Aktive Plantarflexion",
        ],
    },
    "Ankle Dorsiflexion": {
        "muscles": ["tibialis_anterior"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Active Dorsiflexion", "Dorsiflexion",
            "Aktive Dorsalextension",
        ],
    },
    "Ankle Inversion": {
        "muscles": ["tibialis_posterior"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Active Inversion", "Inversion", "Aktive Inversion"],
    },
    "Ankle Eversion": {
        "muscles": ["peroneals"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Active Eversion", "Eversion", "Aktive Eversion"],
    },
    "Band Plantarflexion": {
        "muscles": ["calves"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Theraband Plantarflexion", "Plantarflexion mit Band"],
    },
    "Band Dorsiflexion": {
        "muscles": ["tibialis_anterior"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Theraband Dorsalextension", "Dorsalextension mit Band"],
    },
    "Band Inversion": {
        "muscles": ["tibialis_posterior"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Theraband Inversion", "Inversion mit Band"],
    },
    "Band Eversion": {
        "muscles": ["peroneals"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Theraband Eversion", "Eversion mit Band"],
    },
    "Ankle Circles": {
        "muscles": ["ankle_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Ankle Circle", "Fußkreisen", "Fusskreisen"],
    },
    "Ankle Alphabet": {
        "muscles": ["ankle_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Fuß-Alphabet", "Fuss-Alphabet"],
    },

    # --- Achilles / Wade / Fuß (Silbernagel, Plantarfasziitis) ---
    "Quick Rebounding Toe Raise": {
        "muscles": ["calves", "achilles_tendon"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": [
            "Quick Rebounding Toe Raises", "Quick Rebounding Calf Raise",
            "Federndes Wadenheben",
        ],
    },
    "Seated Eccentric Calf Raise": {
        "muscles": ["soleus", "achilles_tendon"],
        "category": "rehab",
        "equipment": "machine",
        "aliases": [
            "Seated Eccentric Heel Raise",
            "Sitzendes exzentrisches Wadenheben",
        ],
    },
    "Calf Stretch": {
        "muscles": ["calves"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": [
            "Gastrocnemius Stretch", "Wall Calf Stretch", "Wadendehnung", "Seated Calf Stretch",
        ],
    },
    "Towel Scrunch": {
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
        "muscles": ["quads"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Banded Knee Extension", "Kniestreckung mit Band"],
    },
    "Standing Hip Abduction": {
        "muscles": ["glute_med", "hip_abductors"],
        "category": "rehab",
        "equipment": "band",
        "aliases": [
            "Hip Abduction Standing",
            "Hüftabduktion im Stand", "Hueftabduktion im Stand",
        ],
    },
    "Sliding Board Skating": {
        "muscles": ["adductors", "glutes"],
        "category": "rehab",
        "equipment": "other",
        "aliases": [
            "Slide Board Skating", "Slideboard Skating",
            "Gleitbrett-Skating",
        ],
    },
    "Slide Forward-Backward": {
        "muscles": ["quads", "hamstrings"],
        "category": "rehab",
        "equipment": "other",
        "aliases": [
            "Forward-Backward Slide", "Slide Vor-Zurück", "Slide Vor-Zurueck",
        ],
    },
    "Slide Sideways": {
        "muscles": ["adductors", "glute_med"],
        "category": "rehab",
        "equipment": "other",
        "aliases": ["Sideways Slide", "Slide Seitwärts", "Slide Seitwaerts"],
    },

    # --- Schulter (Frozen Shoulder, Thrower's Ten) ---
    "Wand External Rotation": {
        "muscles": ["rotator_cuff", "shoulder_rom"],
        "category": "rehab",
        "equipment": "other",
        "aliases": [
            "Stick External Rotation",
            "Außenrotation mit Stab", "Aussenrotation mit Stab",
        ],
    },
    "External Rotation Stretch with Stick": {
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
        "muscles": ["posterior_capsule", "shoulder_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": [
            "Cross Body Stretch", "Posterior Capsule Stretch",
            "Cross-Body-Dehnung",
        ],
    },
    "Behind-Back Towel Stretch": {
        "muscles": ["shoulder_rom"],
        "category": "mobility",
        "equipment": "other",
        "aliases": [
            "Behind the Back Towel Stretch", "Handtuchdehnung",
        ],
    },
    "Sleeper Stretch": {
        "muscles": ["posterior_capsule"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Sleeper-Stretch", "Schläfer-Dehnung", "Schlaefer-Dehnung"],
    },
    "Doorway Stretch": {
        "muscles": ["chest", "shoulder_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Pec Stretch", "Türrahmen-Dehnung", "Tuerrahmen-Dehnung"],
    },
    "PNF D2 Flexion": {
        "muscles": ["rotator_cuff", "front_delt"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["D2 Flexion", "PNF-Diagonale D2 Flexion"],
    },
    "PNF D2 Extension": {
        "muscles": ["rotator_cuff", "lats"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["D2 Extension", "PNF-Diagonale D2 Extension"],
    },
    "Sidelying External Rotation": {
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
        "muscles": ["rear_delt", "mid_traps"],
        "category": "rehab",
        "equipment": "dumbbell",
        "aliases": [
            "Prone Horizontal Abduction Full ER",
            "Horizontale Abduktion in Bauchlage",
        ],
    },
    "Prone Rowing": {
        "muscles": ["back", "rear_delt"],
        "category": "rehab",
        "equipment": "dumbbell",
        "aliases": [
            "Prone Row", "Prone Rowing into ER", "Rudern in Bauchlage",
        ],
    },
    "Seated Press-up": {
        "muscles": ["scapular_depressors", "triceps"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "Seated Press Up", "Sitzender Stütz", "Sitzender Stuetz",
        ],
    },

    # --- Nacken (Deep Neck Flexor Training) ---
    "Craniocervical Flexion": {
        "muscles": ["deep_neck_flexors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": [
            "CCF", "Kraniozervikale Flexion",
            "Deep Neck Flexor Activation", "Tiefe Nackenbeuger",
        ],
    },
    "Chin Tuck": {
        "muscles": ["deep_neck_flexors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Chin Tucks", "Kinnretraktion"],
    },

    # --- Unterarm / Tennisellenbogen ---
    "Wrist Extension": {
        "muscles": ["forearm_extensors"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Wrist Extensions", "Reverse Wrist Curl", "Handgelenkstreckung",
        ],
    },
    "Wrist Flexion": {
        "muscles": ["forearm_flexors"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Wrist Curl", "Handgelenkbeugung"],
    },
    "Wrist Supination": {
        "muscles": ["forearms"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Forearm Supination", "Unterarm-Supination"],
    },
    "Wrist Pronation": {
        "muscles": ["forearms"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": ["Forearm Pronation", "Unterarm-Pronation"],
    },
    "Tyler Twist": {
        "muscles": ["forearm_extensors"],
        "category": "rehab",
        "equipment": "other",
        "aliases": ["FlexBar Tyler Twist", "Tyler-Twist"],
    },
    "Grip Squeeze": {
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
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Geradeauslaufen", "Straight Ahead Run"],
    },
    "Running Hip Out": {
        "muscles": ["hip_abductors", "hip_rotators"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Hüfte nach außen", "Hip Out Run"],
    },
    "Running Hip In": {
        "muscles": ["hip_adductors", "hip_rotators"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Hüfte nach innen", "Hip In Run"],
    },
    "Running Circling Partner": {
        "muscles": ["full_body", "hip_abductors"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Partner umkreisen", "Circle Partner"],
    },
    "Jumping with Shoulder Contact": {
        "muscles": ["quads", "glutes", "core"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Sprung mit Schulterkontakt", "Shoulder Contact Jump"],
    },
    "Running Quick Forwards Backwards": {
        "muscles": ["quads", "glutes"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Schnell vor und zurück", "Quick Forward-Backward"],
    },
    "Running Across the Pitch": {
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Über das Feld laufen", "Straight Sprint"],
    },
    "Plant and Cut": {
        "muscles": ["quads", "glutes", "hip_abductors"],
        "category": "plyometric",
        "equipment": "bodyweight",
        "aliases": ["Richtungswechsel", "Cutting Drill", "Plant-and-Cut"],
    },

    # --- Sprunggelenk (Ankle Sprain) ---
    "Isometric Eversion": {
        "muscles": ["peroneals"],
        "category": "isometric",
        "equipment": "bodyweight",
        "aliases": ["Iso Eversion", "Isometrische Eversion"],
    },
    "Agility Drill": {
        "muscles": ["full_body", "proprioception"],
        "category": "plyometric",
        "equipment": "other",
        "aliases": ["Agility Drills", "Koordinationsleiter", "Agility-Übung"],
    },

    # --- Frozen Shoulder (Mobilisation) ---
    "Supine Assisted Flexion": {
        "muscles": ["shoulder_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Assistierte Flexion Rückenlage", "Assisted Flexion"],
    },
    "Table Slide": {
        "muscles": ["shoulder_rom"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Table Slides", "Tischgleiten", "Tisch-Slide"],
    },
    "Pulley Flexion": {
        "muscles": ["shoulder_rom"],
        "category": "mobility",
        "equipment": "other",
        "aliases": ["Seilzug-Flexion", "Pulley Exercise", "Umlenkrolle Flexion"],
    },

    # --- Leiste (Hölmich) ---
    "Folding Knife Sit-up": {
        "muscles": ["adductors", "core", "hip_flexors"],
        "category": "rehab",
        "equipment": "other",
        "aliases": ["Klappmesser", "Folding Knife", "Jackknife Sit-up"],
    },
    "Cross-Country Skiing One Leg": {
        "muscles": ["quads", "glutes", "coordination"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Einbeiniges Skilanglauf-Imitat", "One-Leg Ski"],
    },
    "Fitter Sideways Training": {
        "muscles": ["adductors", "glute_med"],
        "category": "rehab",
        "equipment": "other",
        "aliases": ["Fitter seitlich", "Slideboard seitlich", "Sideways Slide Training"],
    },

    # --- Nacken (Deep Neck Flexor / Extensor) ---
    "Supine Head Lift": {
        "muscles": ["deep_neck_flexors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Kopfheben Rückenlage", "Supine Neck Lift"],
    },
    "Prone Head Lift": {
        "muscles": ["neck_extensors"],
        "category": "rehab",
        "equipment": "bodyweight",
        "aliases": ["Kopfheben Bauchlage", "Prone Neck Lift"],
    },
    "Isometric Neck Flexion": {
        "muscles": ["deep_neck_flexors"],
        "category": "isometric",
        "equipment": "band",
        "aliases": ["Iso Nackenbeugung", "Isometrische Nackenflexion"],
    },
    "Isometric Neck Flexion Diagonal": {
        "muscles": ["deep_neck_flexors", "sternocleidomastoid"],
        "category": "isometric",
        "equipment": "band",
        "aliases": ["Iso Nackenbeugung diagonal", "Isometrische Nackenflexion diagonal"],
    },
    "Isometric Neck Extension": {
        "muscles": ["neck_extensors"],
        "category": "isometric",
        "equipment": "band",
        "aliases": ["Iso Nackenstreckung", "Isometrische Nackenextension"],
    },

    # --- Tennisarm (Isometrie & Dehnung) ---
    "Isometric Wrist Extension": {
        "muscles": ["forearm_extensors"],
        "category": "isometric",
        "equipment": "dumbbell",
        "aliases": ["Iso Handgelenkstreckung", "Isometrische Handgelenkextension"],
    },
    "Wrist Extensor Stretch": {
        "muscles": ["forearm_extensors"],
        "category": "mobility",
        "equipment": "bodyweight",
        "aliases": ["Handgelenkstrecker-Dehnung", "Unterarmstrecker-Dehnung"],
    },

    # --- Thrower's Ten (90°-Abduktion) ---
    "External Rotation at Shoulder Level": {
        "muscles": ["rotator_cuff", "infraspinatus"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Außenrotation Schulterhöhe", "ER at 90 Degrees", "ER 90 Abduktion"],
    },
    "Internal Rotation at Shoulder Level": {
        "muscles": ["rotator_cuff", "subscapularis"],
        "category": "rehab",
        "equipment": "band",
        "aliases": ["Innenrotation Schulterhöhe", "IR at 90 Degrees", "IR 90 Abduktion"],
    },

    # --- Otago (Ausdauer) ---
    "Walking": {
        "muscles": ["full_body"],
        "category": "cardio",
        "equipment": "bodyweight",
        "aliases": ["Gehen", "Spazieren", "Gehtraining"],
    },

    # --- Landetechnik / Plyo ---
    "Box Landing Drill": {
        "muscles": ["quads", "glutes", "calves"],
        "category": "plyometric",
        "equipment": "box",
        "aliases": ["Landetechnik", "Drop Landing", "Box Landing"],
    },
    # ========================================================================
    # IMPORT: free-exercise-db (Unlicense) - kuratierte Ergaenzungen fehlender
    # Grunduebungen. Quelle: data/raw/free-exercise-db/exercises.json,
    # siehe data/raw/PROVENANCE.md. Entscheidungen: data/review/DECISIONS.csv.
    # ========================================================================

    "Hang Clean": {
        "muscles": ["quads", "hamstrings", "glutes", "traps", "front_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Hang Power Clean", "Alternating Hang Clean", "Kettlebell Hang Clean",
            "KB Hang Clean", "Smith Machine Hang Power Clean", "Double Kettlebell Alternating Hang Clean",
            "BB Hang Clean", "LH Hang Clean", "Hangumsetzen",
        ],
    },
    "Arnold Press": {
        "muscles": ["front_delt", "side_delt", "triceps"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Arnold Dumbbell Press", "Kettlebell Arnold Press", "KB Arnold Press",
            "DB Arnold Press", "KH Arnold Press",
        ],
    },
    "Good Morning": {
        "muscles": ["hamstrings", "lower_back", "glutes"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Good Mornings", "Band Good Morning", "Seated Good Morning",
            "Seated Good Mornings", "Stiff Leg Barbell Good Morning", "BB Good Morning",
            "LH Good Morning",
        ],
    },
    "Walking Lunge": {
        "muscles": ["quads", "glutes", "hamstrings"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Walking Lunges", "Barbell Walking Lunge", "Bodyweight Walking Lunge",
            "BB Walking Lunge", "LH Walking Lunge", "Gehender Ausfallschritt",
        ],
    },
    "Glute-Ham Raise": {
        "muscles": ["hamstrings", "glutes", "calves"],
        "category": "compound",
        "equipment": "machine",
        "aliases": [
            "GHR", "GHD Raise", "Glute Ham Raise",
            "Floor Glute-Ham Raise", "Natural Glute Ham Raise",
        ],
    },
    "Pistol Squat": {
        "muscles": ["quads", "glutes", "hamstrings"],
        "category": "compound",
        "equipment": "bodyweight",
        "aliases": [
            "Pistol Squats", "Single Leg Squat", "One Leg Squat",
            "Kettlebell Pistol Squat", "KB Pistol Squat", "Smith Machine Pistol Squat",
            "Pistolenkniebeuge", "Einbeinkniebeuge",
        ],
    },
    "Snatch": {
        "muscles": ["quads", "hamstrings", "glutes", "traps", "front_delt"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Snatches", "One-Arm Kettlebell Snatch", "KB Snatch",
            "Reißen", "Reissen",
        ],
    },
    "Concentration Curl": {
        "muscles": ["biceps", "forearms"],
        "category": "isolation",
        "equipment": "dumbbell",
        "aliases": [
            "Concentration Curls", "Standing Concentration Curl", "Seated Close-Grip Concentration Barbell Curl",
            "DB Concentration Curl", "KH Concentration Curl", "Konzentrationscurl",
        ],
    },
    "Renegade Row": {
        "muscles": ["back", "core", "triceps"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Renegade Rows", "Alternating Renegade Row", "Kettlebell Renegade Row",
            "KB Renegade Row", "DB Renegade Row", "KH Renegade Row",
        ],
    },
    "Ab Rollout": {
        "muscles": ["core", "lower_back", "front_delt"],
        "category": "isolation",
        "equipment": "barbell",
        "aliases": [
            "Barbell Ab Rollout", "Barbell Ab Rollout - On Knees", "BB Ab Rollout",
            "LH Ab Rollout",
        ],
    },
    "Russian Twist": {
        "muscles": ["obliques", "core"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": [
            "Russian Twists", "Cable Russian Twists", "Weighted Russian Twist",
            "Russische Drehung",
        ],
    },
    "Farmer's Walk": {
        "muscles": ["forearms", "traps", "core"],
        "category": "compound",
        "equipment": "dumbbell",
        "aliases": [
            "Farmers Walk", "Farmer's Carry", "Farmers Carry",
            "Kettlebell Farmer's Walk", "KB Farmer's Walk", "DB Farmer's Walk",
            "KH Farmer's Walk",
        ],
    },
    "Windmill": {
        "muscles": ["obliques", "side_delt", "hamstrings"],
        "category": "compound",
        "equipment": "kettlebell",
        "aliases": [
            "Windmills", "Kettlebell Windmill", "KB Windmill",
            "Turkish Windmill",
        ],
    },
    "Cable Pull Through": {
        "muscles": ["glutes", "hamstrings", "lower_back"],
        "category": "compound",
        "equipment": "cable",
        "aliases": [
            "Pull Through", "Pull-Through", "Cable Pull-Through",
            "Rope Pull Through",
        ],
    },
    "Sissy Squat": {
        "muscles": ["quads"],
        "category": "isolation",
        "equipment": "bodyweight",
        "aliases": [
            "Sissy Squats", "Weighted Sissy Squat", "BB Sissy Squat",
            "LH Sissy Squat",
        ],
    },
    "Zercher Squat": {
        "muscles": ["quads", "glutes", "core"],
        "category": "compound",
        "equipment": "barbell",
        "aliases": [
            "Zercher Squats", "BB Zercher Squat", "LH Zercher Squat",
        ],
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
        for alias in meta.get("aliases", []):
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
