#!/usr/bin/env python3
"""Wortklassen-Lexikon: Distributionsvektoren + regelbasierte Klassifikation.

Generalisiert die H3-Methode: Jedes Wort mit n>=3 Vorkommen bekommt einen
Distributionsvektor und eine Klassen-Zuordnung mit Begründung:
  funktionswort   häufig + Warenlogogramm zwischen Wort und Zahl
  kultwort        überwiegend im Stein/Kult-Register bzw. Libationsformel
  toponym-anker   identisch in Linear B als Ortsname belegt
  personenname    direkt von kleiner Zahl gefolgt, im Listenkörper
  header-wort     überwiegend textinitial, ohne eigene Zahl
  unklassifiziert Rest
Output: data/lexicon_classes.json + Zusammenfassung.
"""
import json
from collections import Counter, defaultdict
from corpus_lib import DATA, classify, load_inscriptions, parse_number, word_signs

insc = load_inscriptions()
LB_TOPONYMS = {"PA-I-TO", "A-DI-KI-TE", "SU-KI-RI-TA", "I-DA", "KU-DO-NI",
               "DI-KA-TU", "SE-TO-I-JA"}
LIB_MARKERS = ("TA-I-*301", "SA-SA-RA", "U-NA-", "I-PI-NA", "SI-RU")
COMMODITY = ("GRA", "VIN", "OLE", "OLIV", "FIC", "NI", "CYP", "AROM", "FAR")


def bucket(rec):
    s = rec.get("support", "")
    if "Tablet" in s or "Lames" in s or "bar" in s:
        return "verwaltung"
    if any(k in s for k in ("Nodule", "Roundel", "Sealing", "Label")):
        return "siegel"
    if "Stone" in s or "Architecture" in s:
        return "kult"
    return "sonst"


prof = defaultdict(lambda: {"n": 0, "initial": 0, "logo": 0, "num": 0,
                            "qty": [], "reg": Counter(), "sites": set(),
                            "lib": 0})
for name, rec in insc.items():
    toks = rec.get("transliteratedWords", [])
    words_seq = [(i, t) for i, t in enumerate(toks) if classify(t) == "word"]
    is_lib = any(m in w for _, w in words_seq for m in LIB_MARKERS)
    for k, (i, w) in enumerate(words_seq):
        p = prof[w]
        p["n"] += 1
        p["initial"] += (k == 0)
        p["reg"][bucket(rec)] += 1
        p["sites"].add(rec.get("site", "?"))
        p["lib"] += is_lib
        saw_logo, qty, j = False, None, i + 1
        while j < len(toks) and classify(toks[j]) != "word":
            if classify(toks[j]) == "logo":
                saw_logo = saw_logo or any(toks[j].startswith(c) for c in COMMODITY)
            if (v := parse_number(toks[j])) is not None:
                qty = v
                while j + 1 < len(toks) and (nv := parse_number(toks[j + 1])) is not None:
                    j += 1; qty += nv
                break
            j += 1
        p["logo"] += saw_logo
        if qty is not None:
            p["num"] += 1
            p["qty"].append(float(qty))


def classify_word(w, p):
    n = p["n"]
    med = sorted(p["qty"])[len(p["qty"]) // 2] if p["qty"] else None
    if w in LB_TOPONYMS:
        return "toponym-anker", "identisch in Linear B als Ortsname"
    if p["lib"] / n >= 0.5 or p["reg"]["kult"] / n >= 0.5:
        return "kultwort", f"{p['lib']}/{n} in Libationsformel-Texten"
    if n >= 6 and p["logo"] / n >= 0.4:
        return "funktionswort", f"Warenlogogramm vor Zahl in {p['logo']}/{n}"
    if n >= 6 and p["num"] / n >= 0.8 and med is not None and med >= 5:
        return "funktionswort", f"Summenposition: Zahl folgt {p['num']}/{n}, Median {med:g}"
    if p["initial"] / n >= 0.5 and p["num"] / n <= 0.4:
        return "header-wort", f"textinitial {p['initial']}/{n}, selten mit Zahl"
    if p["num"] / n >= 0.6 and med is not None and med <= 3 and p["initial"] / n < 0.5:
        return "personenname?", f"Zahl folgt in {p['num']}/{n}, Median {med:g}"
    return "unklassifiziert", ""


lexicon = {}
for w, p in prof.items():
    if p["n"] < 3 and w not in LB_TOPONYMS:
        continue   # Linear-B-Anker auch unterhalb der Frequenzschwelle
    cls, why = classify_word(w, p)
    lexicon[w] = {
        "klasse": cls, "begruendung": why, "n": p["n"],
        "sites": sorted(p["sites"]),
        "register": dict(p["reg"]),
        "initial_rate": round(p["initial"] / p["n"], 2),
        "zahl_folgt_rate": round(p["num"] / p["n"], 2),
        "median_menge": (sorted(p["qty"])[len(p["qty"]) // 2] if p["qty"] else None),
    }

json.dump(lexicon, open(DATA / "lexicon_classes.json", "w"),
          indent=1, sort_keys=True, ensure_ascii=False)

print("=" * 78)
print(f"Wortklassen-Lexikon: {len(lexicon)} Wörter mit n>=3")
print("=" * 78)
by_class = defaultdict(list)
for w, e in lexicon.items():
    by_class[e["klasse"]].append((e["n"], w))
for cls in sorted(by_class, key=lambda c: -len(by_class[c])):
    ws = sorted(by_class[cls], reverse=True)
    print(f"\n{cls} ({len(ws)}):")
    print("   " + ", ".join(f"{w}({n})" for n, w in ws[:18]))

print("\nSanity-Anker (erwartete Klassen):")
for w, want in [("SA-RA₂", "funktionswort"), ("KU-RO", "funktionswort"),
                ("JA-SA-SA-RA-ME", "kultwort"), ("PA-I-TO", "toponym-anker"),
                ("KU-PA₃-NU", "personenname?")]:
    got = lexicon.get(w, {}).get("klasse", "(n<3)")
    print(f"   {w:<16} erwartet={want:<15} bekommen={got}"
          f"  {'✓' if got == want else '✗'}")
