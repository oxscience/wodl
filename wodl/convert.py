"""
Freitext → WODL: Pläne aus WhatsApp, Excel oder Notizen übersetzen.

Pro Zeile wird erkannt:
- Einheiten-Kopf: Wochentag ("Montag – Oberkörper"), "Tag 1", "Training A:", "# Beine"
- Übung: Name, dann Sätze/Wdh. ("3x10", "3 x 8-12", "3 Sätze à 15", "3x45 sek"),
  Last ("60kg" → @60kg), RPE/RIR/%, Körpergewicht, Pause ("Pause 90 Sek" → r90s), Tempo
- "pro Seite"/"je Bein" → je Seite; Minuten → 1x20min
- Rest der Zeile wird Kommentar; reine Textzeilen werden Notizen (> …)

Das Ergebnis ist ein Vorschlag, den der Coach im Editor prüft.
"""

from __future__ import annotations

import re

from wodl.registry import resolve_fuzzy

_DAYS = {
    "Mo": ("mo", "mon", "montag", "monday"),
    "Di": ("di", "die", "dienstag", "tue", "tuesday"),
    "Mi": ("mi", "mittwoch", "wed", "wednesday"),
    "Do": ("do", "don", "donnerstag", "thu", "thursday"),
    "Fr": ("fr", "fre", "freitag", "fri", "friday"),
    "Sa": ("sa", "samstag", "sat", "saturday"),
    "So": ("so", "sonntag", "sun", "sunday"),
}
_DAY_OF = {word: day for day, words in _DAYS.items() for word in words}
_DAY_WORD = re.compile(r"\b(" + "|".join(sorted(_DAY_OF, key=len, reverse=True)) + r")\b\.?", re.I)

_MARKER = re.compile(r"^\s*(?:[-*•–]|\d+[.)])\s+")
_HEAD_WORD = re.compile(r"^(tag|day|einheit|training|workout|session|woche|week|block|phase|teil)\b", re.I)

# Längste Alternative zuerst, sonst frisst "s" das "Sek"
_UNIT_S = r"(?:sekunden|seconds|sek|sec|s)"
_UNIT_MIN = r"(?:minuten|minutes|min)"
# 3x10 / 3 x 8-12 / 3x45 sek — aber nicht 2x20kg (Kurzhantel-Paar)
_SETS_REPS = re.compile(
    rf"(\d+)\s*[x×]\s*(\d+(?:\s*-\s*\d+)?)(?:\s*({_UNIT_S}|{_UNIT_MIN})\.?)?(?![\d.,]*\s*kg)(?=\W|$)", re.I)
_SETS_WORD = re.compile(
    r"(\d+)\s*(?:sätze|saetze|sätzen|sets?|serien)\s*(?:à|a|x|zu|mit|je|of)?\s*(\d+(?:\s*-\s*\d+)?)"
    r"(?:\s*(?:wdh\.?|wiederholungen|reps?))?", re.I)
_SETS_MAX = re.compile(r"(\d+)\s*[x×]\s*(?:max|amrap)\b", re.I)
_REPS_WORD = re.compile(r"(\d+(?:\s*-\s*\d+)?)\s*(?:wdh\.?|wiederholungen|reps?)(?=\W|$)", re.I)
_TIME = re.compile(rf"(\d+)\s*({_UNIT_S}|{_UNIT_MIN})\.?(?=\W|$)", re.I)

_LOAD = re.compile(r"(?:\d+\s*[x×]\s*)?(\d+(?:[.,]\d+)?)\s*kg\b", re.I)
_PCT = re.compile(r"(\d+)\s*%")
_RPE = re.compile(r"\bRPE\s*(\d+(?:[.,]5)?)", re.I)
_RIR = re.compile(r"\bRIR\s*(\d)", re.I)
_BW = re.compile(r"\b(körpergewicht|eigengewicht|bodyweight|bw|kgw)\b", re.I)
_REST = re.compile(
    rf"(?:\bpause|\brest)\s*:?\s*(\d+(?:\s*-\s*\d+)?)\s*({_UNIT_S}|{_UNIT_MIN}|m)?\.?(?=\W|$)"
    rf"|(\d+(?:\s*-\s*\d+)?)\s*({_UNIT_S}|{_UNIT_MIN})\.?\s*(?:pause|rest)\b", re.I)
_SIDE = re.compile(r"\b(?:je|pro)\s+(seite|bein|arm)\b", re.I)
_TEMPO = re.compile(r"\btempo\s*:?\s*(\d)[\s-]?(\d)[\s-]?(\d)[\s-]?(\d)", re.I)


def _rest_token(m: re.Match) -> str:
    n = (m.group(1) or m.group(3)).replace(" ", "")
    unit = (m.group(2) or m.group(4) or "").lower()
    if unit.startswith("m"):
        return f"r{n}m"
    if not unit and int(n.split("-")[-1]) <= 5:  # "Pause 2" = Minuten
        return f"r{n}m"
    return f"r{n}s"


def _header(line: str) -> tuple[str, list[str]] | None:
    """Einheiten-Kopf erkennen → (Name, Tage) oder None."""
    text = line.lstrip("#").strip()
    if re.search(r"\d+\s*[x×]\s*\d|\d+\s*kg|\bsätze\b|\bwdh\b", text, re.I):
        return None
    days = [_DAY_OF[w.lower().rstrip(".")] for w in _DAY_WORD.findall(text)]
    if len(text.split()) > 5:  # "So oft wie möglich, sauber ausführen" ist kein Kopf
        days = []
    if not (days or line.startswith("#") or _HEAD_WORD.match(text) or text.endswith(":")):
        return None
    name = _DAY_WORD.sub("", text) if days else text
    name = re.sub(r"\s+", " ", name).strip(" \t:–—-|/,")
    return name, list(dict.fromkeys(days))


def _exercise(line: str) -> str | None:
    """Übungszeile → WODL-Zeile, oder None wenn keine Übung erkennbar ist."""
    spans: list[tuple[int, int]] = []

    def take(m: re.Match | None) -> re.Match | None:
        if m and not any(a < m.end() and m.start() < b for a, b in spans):
            spans.append(m.span())
            return m
        return None

    if m := take(_REST.search(line)):
        rest = _rest_token(m)
    else:
        rest = None
    tempo = take(_TEMPO.search(line))

    sets_reps = None
    if m := take(_SETS_REPS.search(line)):
        reps, unit = m.group(2).replace(" ", ""), (m.group(3) or "").lower()
        suffix = "min" if unit.startswith("m") else "s" if unit else ""
        sets_reps = f"{m.group(1)}x{reps}{suffix}"
    elif m := take(_SETS_MAX.search(line)):
        sets_reps = f"{m.group(1)}x"  # AMRAP
    elif m := take(_SETS_WORD.search(line)):
        sets_reps = f"{m.group(1)}x{m.group(2).replace(' ', '')}"
    elif m := take(_REPS_WORD.search(line)):
        sets_reps = f"1x{m.group(1).replace(' ', '')}"
    elif m := take(_TIME.search(line)):
        sets_reps = f"1x{m.group(1)}{'min' if m.group(2).lower().startswith('m') else 's'}"

    intensities = []
    for rx, fmt in ((_LOAD, "@{}kg"), (_PCT, "@{}%"), (_RPE, "@RPE{}"), (_RIR, "@RIR{}"), (_BW, "@BW")):
        if m := take(rx.search(line)):
            intensities.append(fmt.format(m.group(1).replace(",", ".")) if "{}" in fmt else fmt)

    if not spans:
        return None
    start = min(a for a, _ in spans)
    name = line[:start].strip(" \t,:;–—-|/(")
    leftover = "".join(ch if not any(a <= i < b for a, b in spans) else " "
                       for i, ch in enumerate(line[start:], start))
    leftover = re.sub(r"\s+", " ", leftover).strip(" ,;:–—-|/()")
    if not name:
        return None

    side = _SIDE.search(leftover)
    if side:
        leftover = (leftover[: side.start()] + leftover[side.end():]).strip(" ,;:")
    tokens = [t for t in (sets_reps, intensities[0] if intensities else None, rest) if t]
    if side:
        tokens.append(f"je {side.group(1).capitalize()}")
    if tempo:
        tokens.append("t" + "".join(tempo.groups()))
    extra = [t.lstrip("@") for t in intensities[1:]]
    if re.search(r"[A-Za-zÄÖÜäöüß]", leftover):
        extra.append(leftover)
    if extra:
        tokens.append("# " + ", ".join(extra))
    return f"{name}  {' '.join(tokens)}"


def freetext_to_wodl(text: str) -> str:
    """Freitext-Plan → WODL-Text (Vorschlag)."""
    out: list[str] = []
    have_session = False
    letters = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    for raw in text.splitlines():
        if "\t" in raw:  # aus Excel kopiert: Übung | Sätze | Wdh. | Gewicht | …
            cells = [c.strip() for c in raw.split("\t") if c.strip()]
            if len(cells) >= 3 and cells[1].isdigit() and re.fullmatch(r"\d+(-\d+)?", cells[2]):
                load = f"{cells[3]}kg" if len(cells) > 3 and re.fullmatch(r"\d+([.,]\d+)?", cells[3]) else ""
                raw = " ".join([cells[0], f"{cells[1]}x{cells[2]}", load, *cells[3 + bool(load):]])
            elif re.search(r"übung|exercise", raw, re.I) and re.search(r"sätze|sets|wdh|reps", raw, re.I):
                continue  # Tabellenkopf
            else:
                raw = " ".join(cells)
        line = _MARKER.sub("", raw).strip()
        if not line:
            if out and out[-1]:
                out.append("")
            continue

        head = _header(line)
        if head:
            name, days = head
            if not name:
                name = f"Tag {next(letters)}"
            if out and out[-1]:
                out.append("")
            out.append(f"---[{name}]" + (" " + " ".join(days) if days else ""))
            have_session = True
            continue

        wodl = _exercise(line)
        if wodl is None and not re.search(r"\d", line) and resolve_fuzzy(line):
            wodl = line  # nur ein Übungsname
        if not have_session and wodl is not None:
            out.append("---[Training]")
            have_session = True
        out.append(wodl if wodl is not None else f"> {line}")

    return "\n".join(out).strip() + "\n"
