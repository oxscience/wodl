"""
Matcher: free-exercise-db -> WODL registry.

Vierstufige Pipeline (exact -> qualifier -> fuzzy -> variant), gefolgt von
zwei Waechtern (Antonym-Guard, Equipment-Guard). Schreibt drei Review-CSVs:

    data/review/aliases_auto.csv     sichere Alias-Kandidaten
    data/review/aliases_review.csv   manuell zu entscheiden (fuzzy / Equipment-Konflikt)
    data/review/candidates_new.csv   Kandidaten fuer neue kanonische Uebungen

Schreibt NICHT in wodl/registry.py. Das passiert erst mit
tools/apply_decisions.py, nach manueller Freigabe in data/review/DECISIONS.csv.

Quelle der Rohdaten: data/raw/free-exercise-db/exercises.json (siehe
data/raw/PROVENANCE.md fuer Lizenz/Herkunft).
"""

from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wodl.registry import EXERCISES  # noqa: E402

RAW_PATH = ROOT / "data" / "raw" / "free-exercise-db" / "exercises.json"
REVIEW_DIR = ROOT / "data" / "review"

# ---------------------------------------------------------------------------
# Normalisierung
# ---------------------------------------------------------------------------


def strip_diacritics(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def normalize(s: str) -> str:
    """lowercase, NFD, Diakritika entfernen, alles ausser [a-z0-9] strippen."""
    s = strip_diacritics(s.lower())
    return re.sub(r"[^a-z0-9]", "", s)


def tokenize(s: str) -> list[str]:
    """Wort-Tokens fuer QUAL/MODIF-Stripping. Bindestriche trennen wie
    Leerzeichen ("One-Arm Row" -> ["one","arm","row"]), damit hyphenierte
    Modifikatoren (haeufig in free-exercise-db) erkannt werden."""
    s = strip_diacritics(s.lower())
    return re.findall(r"[a-z0-9]+", s)




# ---------------------------------------------------------------------------
# Wortlisten aus Abschnitt 2
# ---------------------------------------------------------------------------

QUAL = {
    "barbell", "bb", "dumbbell", "db", "cable", "machine", "smith", "lever",
    "band", "bands", "resistance", "kettlebell", "weighted", "bodyweight",
    "body", "ez", "ezbar", "plate", "sled", "rope", "olympic",
}

MODIF = {
    "alternate", "alternating", "standing", "seated", "single", "one", "two",
    "arm", "arms", "leg", "legs", "wide", "close", "grip", "neutral", "bent",
    "over", "lying", "floor", "high", "low", "half", "full", "strict",
    "assisted", "banded", "paused", "pause", "eccentric", "tempo", "with",
    "the", "on", "to", "a", "and", "of",
}

AMBIG = {
    "press", "row", "curl", "raise", "extension", "fly", "flyes", "flies",
    "pull", "push", "crunch", "pushdown", "pulldown", "jump", "carry",
    "hold", "walk", "twist", "rotation", "bridge", "lunge", "dip", "kick",
    "swing", "thrust", "shrug", "stretch",
}

ANTONYM_PAIRS = [
    ("incline", "decline"), ("internal", "external"), ("front", "rear"),
    ("front", "back"), ("reverse", "forward"), ("seated", "standing"),
    ("sumo", "conventional"), ("close", "wide"), ("high", "low"),
    ("concentric", "eccentric"), ("prone", "supine"), ("single", "double"),
]

FUZZY_THRESHOLD = 0.82

# ---------------------------------------------------------------------------
# Index: normalized(canonical|alias) -> (canonical, matched_string)
# ---------------------------------------------------------------------------


def build_index() -> dict[str, tuple[str, str]]:
    index: dict[str, tuple[str, str]] = {}
    for canonical, meta in EXERCISES.items():
        index.setdefault(normalize(canonical), (canonical, canonical))
        for alias in meta.get("aliases", []):
            index.setdefault(normalize(alias), (canonical, alias))
    return index


INDEX = build_index()
INDEX_KEYS = list(INDEX.keys())


def bigrams(s: str) -> set[str]:
    return {s[i : i + 2] for i in range(len(s) - 1)}


def dice(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return (2 * len(a & b)) / (len(a) + len(b))


def has_antonym_conflict(source_tokens: set[str], target_tokens: set[str]) -> bool:
    for w1, w2 in ANTONYM_PAIRS:
        if (w1 in source_tokens and w2 in target_tokens) or (
            w2 in source_tokens and w1 in target_tokens
        ):
            return True
    return False


# ---------------------------------------------------------------------------
# Matching-Pipeline
# ---------------------------------------------------------------------------


class MatchResult:
    def __init__(
        self,
        source_name: str,
        stage: str,
        canonical: str | None = None,
        matched_string: str | None = None,
        score: float | None = None,
        discarded_reason: str | None = None,
    ):
        self.source_name = source_name
        self.stage = stage  # exact | qualifier | fuzzy | variant | new
        self.canonical = canonical
        self.matched_string = matched_string
        self.score = score
        self.discarded_reason = discarded_reason  # antonym | None


def match_one(source_name: str) -> MatchResult:
    source_tokens_all = set(tokenize(source_name))

    # Stage 1: exact
    raw_norm = normalize(source_name)
    hit = INDEX.get(raw_norm)
    if hit:
        canonical, matched_string = hit
        if has_antonym_conflict(source_tokens_all, set(tokenize(matched_string))):
            return MatchResult(source_name, "new", discarded_reason="antonym")
        return MatchResult(source_name, "exact", canonical, matched_string)

    # Stage 2: qualifier-stripped exact
    tokens = tokenize(source_name)
    qual_stripped = [t for t in tokens if t not in QUAL]
    qual_norm = "".join(qual_stripped)
    if qual_norm and qual_norm != raw_norm:
        hit = INDEX.get(qual_norm)
        if hit:
            canonical, matched_string = hit
            if has_antonym_conflict(source_tokens_all, set(tokenize(matched_string))):
                return MatchResult(source_name, "new", discarded_reason="antonym")
            return MatchResult(source_name, "qualifier", canonical, matched_string)

    # Stage 3: fuzzy (Sorensen-Dice over bigrams of the raw normalized string)
    src_bi = bigrams(raw_norm)
    if src_bi:
        best_score = 0.0
        best_key = None
        for key in INDEX_KEYS:
            score = dice(src_bi, bigrams(key))
            if score > best_score:
                best_score = score
                best_key = key
        if best_key is not None and best_score >= FUZZY_THRESHOLD:
            canonical, matched_string = INDEX[best_key]
            if has_antonym_conflict(source_tokens_all, set(tokenize(matched_string))):
                return MatchResult(
                    source_name, "new", score=best_score, discarded_reason="antonym"
                )
            return MatchResult(
                source_name, "fuzzy", canonical, matched_string, score=best_score
            )

    # Stage 4: qualifier + modifier stripped exact, with ambiguity guard
    variant_stripped = [t for t in qual_stripped if t not in MODIF]
    if len(variant_stripped) == 1 and variant_stripped[0] in AMBIG:
        return MatchResult(source_name, "new")
    variant_norm = "".join(variant_stripped)
    if variant_norm and variant_norm not in (raw_norm, qual_norm):
        hit = INDEX.get(variant_norm)
        if hit:
            canonical, matched_string = hit
            if has_antonym_conflict(source_tokens_all, set(tokenize(matched_string))):
                return MatchResult(source_name, "new", discarded_reason="antonym")
            return MatchResult(source_name, "variant", canonical, matched_string)

    return MatchResult(source_name, "new")


# ---------------------------------------------------------------------------
# Equipment / Muscle / Category Mapping (Abschnitt 6)
# ---------------------------------------------------------------------------

EQUIPMENT_MAP = {
    "bands": "band",
    "barbell": "barbell",
    "body only": "bodyweight",
    "cable": "cable",
    "dumbbell": "dumbbell",
    "e-z curl bar": "barbell",
    "machine": "machine",
    "exercise ball": "other",
    "foam roll": "other",
    "medicine ball": "other",
    "other": "other",
    None: "other",
    "kettlebells": None,  # kein WODL-Aequivalent -> manuell vorschlagen
}

MUSCLE_MAP = {
    "abdominals": ["rectus_abdominis", "core"],
    "abductors": ["hip_abductors"],
    "adductors": ["hip_adductors"],
    "biceps": ["biceps"],
    "calves": ["calves"],
    "chest": ["chest"],
    "forearms": ["forearms"],
    "glutes": ["glutes"],
    "hamstrings": ["hamstrings"],
    "lats": ["lats"],
    "lower back": ["lower_back"],
    "quadriceps": ["quads"],
    "traps": ["traps"],
    "triceps": ["triceps"],
    "middle back": ["rhomboids", "mid_traps"],  # grob, im Zweifel manuell
    "neck": None,  # MANUELL
    "shoulders": None,  # MANUELL (front/side/rear_delt haengt von der Uebung ab)
}


def map_category(fx: dict) -> str | None:
    if fx.get("category") == "stretching":
        return "mobility"
    if fx.get("category") == "cardio":
        return "cardio"
    if fx.get("category") == "plyometrics":
        return "plyometric"
    mech = fx.get("mechanic")
    if mech == "compound":
        return "compound"
    if mech == "isolation":
        return "isolation"
    return None  # MANUELL


def map_equipment(fx_equipment) -> str | None:
    """None = kein Signal (fx.equipment war null). 'other' ist ein echtes,
    wenn auch unspezifisches Signal (fx.equipment war explizit 'other' o.ae.)."""
    if fx_equipment is None:
        return None
    return EQUIPMENT_MAP.get(fx_equipment, "other")


# ---------------------------------------------------------------------------
# Pipeline ausfuehren
# ---------------------------------------------------------------------------


def run():
    data = json.loads(RAW_PATH.read_text())

    stage_counts = Counter()
    antonym_discards = []
    equipment_conflicts = []
    auto_rows = []
    review_rows = []
    new_bucket = []  # (fx, ) unmatched

    seen_auto_pairs = set()  # (canonical, normalized alias) dedup

    for fx in data:
        name = fx["name"]
        result = match_one(name)

        if result.discarded_reason == "antonym":
            antonym_discards.append((name, result.canonical, result.score))
            stage_counts["antonym_discard"] += 1
            new_bucket.append(fx)
            continue

        if result.stage == "new":
            stage_counts["new"] += 1
            new_bucket.append(fx)
            continue

        stage_counts[result.stage] += 1

        # Equipment-Guard: jedes explizit angegebene fx.equipment, das nicht
        # auf das Ziel-Equipment abbildet, ist ein Konflikt (auch "other" -
        # das ist ein echtes, nur unspezifisches Signal). fx.equipment == null
        # ist dagegen kein Signal und loest keinen Konflikt aus.
        is_kettlebell = fx.get("equipment") == "kettlebells"
        fx_equip_mapped = map_equipment(fx.get("equipment"))
        target_equip = EXERCISES[result.canonical]["equipment"]
        equip_conflict = (
            not is_kettlebell
            and fx_equip_mapped is not None
            and fx_equip_mapped != target_equip
        )
        if equip_conflict:
            equipment_conflicts.append((name, result.canonical, fx.get("equipment"), target_equip))

        # Category-Guard: WODL-Kategorie aus fx ableiten (Abschnitt 6) und mit
        # der tatsaechlichen Kategorie des Ziel-Eintrags abgleichen.
        mapped_cat = map_category(fx)
        target_cat = EXERCISES[result.canonical]["category"]
        category_conflict = mapped_cat is not None and mapped_cat != target_cat

        # Ist der Alias-String bereits (bis auf Normalisierung) in der Registry bekannt?
        already_known = normalize(name) in INDEX

        row = {
            "fx_id": fx.get("id", ""),
            "source_name": name,
            "canonical_name": result.canonical,
            "stage": result.stage,
            "score": f"{result.score:.3f}" if result.score is not None else "",
            "fx_equipment": fx.get("equipment") or "",
            "target_equipment": target_equip,
            "equipment_conflict": "yes" if equip_conflict else "",
            "fx_category": fx.get("category") or "",
            "mapped_category": mapped_cat or "",
            "target_category": target_cat,
            "category_conflict": "yes" if category_conflict else "",
            "already_known_alias": "yes" if already_known else "",
        }

        # Routing: nicht die Stufe (exact/qualifier/fuzzy/variant) entscheidet,
        # sondern ob einer der beiden Waechter angeschlagen hat.
        reasons = []
        if equip_conflict:
            reasons.append("equipment_conflict")
        if category_conflict:
            reasons.append("category_conflict")
        if is_kettlebell:
            reasons.append("kettlebell_no_wodl_equipment")
        needs_review = bool(reasons)

        if already_known:
            # Kein neuer Alias-Kandidat, aber fuer Nachvollziehbarkeit sichtbar
            continue

        dedup_key = (result.canonical, normalize(name))
        if dedup_key in seen_auto_pairs:
            continue
        seen_auto_pairs.add(dedup_key)

        if needs_review:
            row["reason"] = ",".join(reasons)
            review_rows.append(row)
        else:
            auto_rows.append(row)

    # --- candidates_new.csv: Bewegungskerne aus dem "new"-Bucket ---
    CURATED_MISSING = [
        "Good Morning", "Arnold Press", "Concentration Curl", "Glute-Ham Raise",
        "Pistol Squat", "Walking Lunge", "Ab Rollout", "Hang Clean", "Push Jerk",
        "Turkish Get-up", "Windmill", "Renegade Row", "Russian Twist",
        "Landmine Press", "Sissy Squat", "Zercher Squat", "Snatch",
        "Farmer's Walk", "Pendlay Row", "Chest Supported Row",
        "Cable Pull Through", "Reverse Hyper", "Nordic Hamstring",
    ]
    curated_norm = {normalize(c): c for c in CURATED_MISSING}

    cores = defaultdict(list)
    for fx in new_bucket:
        name = fx["name"]
        tokens = tokenize(name)
        core_tokens = [t for t in tokens if t not in QUAL and t not in MODIF]
        core = " ".join(core_tokens) if core_tokens else name.lower()
        cores[core].append(fx)

    category_breakdown = Counter(fx.get("category") for fx in new_bucket)

    def token_set(s: str) -> frozenset[str]:
        toks = [t for t in tokenize(s) if t not in QUAL and t not in MODIF]
        singular = [t[:-1] if t.endswith("s") and not t.endswith("ss") and len(t) > 3 else t for t in toks]
        return frozenset(singular)

    curated_token_sets = {label: token_set(label) for label in CURATED_MISSING}

    candidate_rows = []
    for core, items in sorted(cores.items(), key=lambda kv: -len(kv[1])):
        example = items[0]
        core_tokens = token_set(core)
        curated_hit = None
        for label, ct in curated_token_sets.items():
            if not ct:
                continue
            # Bei Ein-Wort-Kernen (zu generisch, z.B. "press", "curl") nur
            # exakte Gleichheit; bei laengeren Kernen 1 Wort Toleranz.
            tolerance = 1 if len(ct) >= 2 and len(core_tokens) >= 2 else 0
            if len(ct.symmetric_difference(core_tokens)) <= tolerance:
                curated_hit = label
                break
        candidate_rows.append({
            "movement_core": core,
            "variant_count": len(items),
            "example_names": "; ".join(sorted({i["name"] for i in items}))[:300],
            "fx_categories": ",".join(sorted({i.get("category") or "" for i in items})),
            "curated_missing_match": curated_hit or "",
            "example_primary_muscles": ",".join(example.get("primaryMuscles") or []),
            "example_equipment": example.get("equipment") or "",
            "example_mechanic": example.get("mechanic") or "",
            "example_level": example.get("level") or "",
            "mapped_category": map_category(example) or "MANUELL",
        })

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    CSV_FIELDS = [
        "fx_id", "source_name", "canonical_name", "stage", "score",
        "fx_equipment", "target_equipment", "equipment_conflict",
        "fx_category", "mapped_category", "target_category", "category_conflict",
        "already_known_alias",
    ]

    with (REVIEW_DIR / "aliases_auto.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for row in auto_rows:
            w.writerow(row)

    with (REVIEW_DIR / "aliases_review.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS + ["reason"])
        w.writeheader()
        for row in review_rows:
            w.writerow(row)

    with (REVIEW_DIR / "candidates_new.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "movement_core", "variant_count", "example_names", "fx_categories",
            "curated_missing_match", "example_primary_muscles",
            "example_equipment", "example_mechanic", "example_level",
            "mapped_category",
        ])
        w.writeheader()
        for row in candidate_rows:
            w.writerow(row)

    # --- DECISIONS.csv Template (von Nutzer:in auszufuellen: decision=accept|reject) ---
    decisions_path = REVIEW_DIR / "DECISIONS.csv"
    if not decisions_path.exists():
        with decisions_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=[
                "id", "type", "source_name", "proposed_canonical", "reason",
                "decision", "override_canonical", "notes",
            ])
            w.writeheader()
            for row in review_rows:
                w.writerow({
                    "id": row["fx_id"],
                    "type": "alias",
                    "source_name": row["source_name"],
                    "proposed_canonical": row["canonical_name"],
                    "reason": row["reason"],
                    "decision": "",
                    "override_canonical": "",
                    "notes": "",
                })
            for row in candidate_rows:
                if row["curated_missing_match"]:
                    w.writerow({
                        "id": "core:" + row["movement_core"],
                        "type": "new_exercise",
                        "source_name": row["movement_core"],
                        "proposed_canonical": row["curated_missing_match"],
                        "reason": "curated_missing_basic_exercise",
                        "decision": "",
                        "override_canonical": "",
                        "notes": row["example_names"],
                    })
    else:
        print(f"HINWEIS: {decisions_path} existiert bereits - nicht ueberschrieben "
              f"(manuelle Entscheidungen bleiben erhalten bei erneutem Lauf).")

    # --- Report ---
    print(f"Gesamt: {len(data)}")
    print(f"exact: {stage_counts['exact']}")
    print(f"qualifier: {stage_counts['qualifier']}")
    print(f"variant: {stage_counts['variant']}")
    print(f"fuzzy: {stage_counts['fuzzy']}")
    print(f"new (inkl. Antonym-Discards): {stage_counts['new'] + stage_counts['antonym_discard']}")
    print(f"  davon durch Antonym-Guard verworfen: {stage_counts['antonym_discard']}")
    matched_total = stage_counts['exact'] + stage_counts['qualifier'] + stage_counts['variant'] + stage_counts['fuzzy']
    print(f"matched total: {matched_total}")
    print()
    print(f"neue Alias-Kandidaten (auto): {len(auto_rows)}")
    print(f"neue Alias-Kandidaten (review): {len(review_rows)}")
    reason_counts = Counter()
    for r in review_rows:
        for reason in r["reason"].split(","):
            reason_counts[reason] += 1
    for reason, cnt in reason_counts.most_common():
        print(f"  davon {reason}: {cnt}")
    total_candidates = len(auto_rows) + len(review_rows)
    canon_touched = {r["canonical_name"] for r in auto_rows} | {r["canonical_name"] for r in review_rows}
    print(f"neue Alias-Kandidaten (gesamt): {total_candidates}")
    print(f"kanonische Uebungen betroffen: {len(canon_touched)}")
    print()
    print("new-Bucket fx.category Verteilung:")
    for cat, cnt in category_breakdown.most_common():
        print(f"  {cat}: {cnt}")
    print()
    print(f"Bewegungskerne im new-Bucket: {len(cores)}")
    print()
    print("Antonym-Guard Discards:")
    for name, canonical, score in antonym_discards:
        print(f"  {name!r} -> {canonical!r} (score={score})")
    print()
    print("Equipment-Konflikte:")
    for name, canonical, fx_eq, target_eq in equipment_conflicts:
        print(f"  {name!r} -> {canonical!r}  fx={fx_eq!r} target={target_eq!r}")


if __name__ == "__main__":
    run()
