"""Gemeinsame Korpus-Helfer für analyze.py und die Hypothesen-Tests."""
import json, math, re
from fractions import Fraction
from pathlib import Path

DATA = Path(__file__).parent / "data"

SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def load_inscriptions():
    """Korpus laden; support-Korrekturen (audit_support.py) werden,
    falls vorhanden, automatisch angewandt."""
    insc = json.load(open(DATA / "inscriptions.json"))
    corr_file = DATA / "support_corrections.json"
    if corr_file.exists():
        for name, supp in json.load(open(corr_file)).items():
            if name in insc:
                insc[name]["support"] = supp
    return insc


def parse_number(tok):
    """integer or fraction token -> Fraction, else None"""
    t = tok.strip().lstrip("≈").strip()
    if re.fullmatch(r"\d+", t):
        return Fraction(int(t))
    m = re.fullmatch(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+)⁄([₀₁₂₃₄₅₆₇₈₉]+)", t)
    if m:
        return Fraction(int(m.group(1).translate(SUP)), int(m.group(2).translate(SUB)))
    m = re.fullmatch(r"(\d+)/(\d+)", t)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    return None


SYL = re.compile(r"[A-Z]{1,2}[0-9]?|\*\d+[A-Z]*")  # KU, RA2, PA3, *301


def is_word(tok):
    """syllabic sequence of >=2 signs, undamaged, joined by '-'"""
    if "-" not in tok or "[" in tok or "]" in tok or "?" in tok or "•" in tok:
        return False
    parts = tok.translate(SUB).split("-")
    if any(p in ("", "VS", "VAS") for p in parts):
        return False
    return all(SYL.fullmatch(p) for p in parts)


def word_signs(tok):
    return tok.translate(SUB).split("-")


def classify(tok):
    t = tok.strip()
    if t in ("", "\n"):                      return "nl"
    if t == "𐄁":                            return "sep"
    if parse_number(t) is not None:          return "num"
    if t == "—":                             return "dash"
    if is_word(t):                           return "word"
    if "[" in t or "]" in t or "?" in t:     return "damaged"
    return "logo"   # logograms, single signs, ligatures, *NNN


VOWEL = {"A", "E", "I", "O", "U"}


def vowel_of(sign):
    s = re.sub(r"\d", "", sign)
    return s[-1] if s and s[-1] in VOWEL else None


def cv(sign):
    """sign -> (consonant, vowel) oder None für *NNN, AU etc."""
    s = re.sub(r"\d", "", sign)
    m = re.fullmatch(r"([A-Z]*?)([AEIOU])", s)
    if not m:
        return None
    c, v = m.groups()
    if any(ch in "AEIOU" for ch in c):
        return None
    return c, v


def fisher2x2(a, b, c, d):
    """two-sided exact Fisher for [[a,b],[c,d]]"""
    n, r1, c1 = a + b + c + d, a + b, a + c
    if n == 0:
        return 1.0
    def pt(x):
        return math.comb(c1, x) * math.comb(n - c1, r1 - x) / math.comb(n, r1)
    p0 = pt(a)
    lo, hi = max(0, r1 + c1 - n), min(r1, c1)
    return min(1.0, sum(pt(x) for x in range(lo, hi + 1) if pt(x) <= p0 * (1 + 1e-9)))
