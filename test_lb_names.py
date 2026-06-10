#!/usr/bin/env python3
"""Anker-Abgleich: Linear-A-Wortklassen vs. Linear-B-Fundkontexte.

Die ~40 Wörter, die identisch in Linear B wiederkehren, sind unsere
einzigen extern verankerten Lexeme. Die Linear-B-Serienkürzel kodieren
den Tafelinhalt (As/Ap/An/B = Personallisten, D-Serie = Hirten in
Schafregistern, E-Serie = Landbesitzer, Fp/Fs/Tn = Opferlisten ...).

Test: Stimmen unsere distributionell ermittelten Linear-A-Klassen
(build_lexicon.py) mit den Linear-B-Kontexten überein? LA-Wörter der
Klasse 'personenname?' sollten in LB-Personenkontexten landen,
'kultwort'-Kandidaten in Opferkontexten.
"""
import json, re
from collections import Counter, defaultdict
from corpus_lib import DATA

ident = json.load(open(DATA / "identicalWordsInLinearB.json"))
lexicon = json.load(open(DATA / "lexicon_classes.json"))

# LB-Serie -> Kontexttyp (grob, aber konventionell)
PERSON = {"As", "Ap", "An", "Aq", "B", "C", "Cn", "Da", "Db", "Dc", "Dd",
          "De", "Df", "Dg", "Dk", "Dl", "Dv", "Ea", "Eb", "En", "Eo", "Ep",
          "Jn", "Sc", "V", "Fh"}
CULT = {"Fp", "Fs", "Tn", "Gp", "Un", "Of"}


def series_of(ref):
    m = re.match(r"(KN|PY|TH|MY|TI)\s+([A-Z][a-z]*)", ref)
    return m.group(2) if m else None


def lb_context(refs):
    kinds = Counter()
    for r in refs:
        s = series_of(r)
        if s in PERSON:
            kinds["person"] += 1
        elif s in CULT:
            kinds["kult"] += 1
        elif s:
            kinds["sonstig"] += 1
    if not kinds:
        return "?"
    return kinds.most_common(1)[0][0]


print("=" * 78)
print("Linear-A-Klasse (distributionell) vs. Linear-B-Kontext (Serienkürzel)")
print("=" * 78)
print(f"{'LA-Wort':<14} {'LA-Klasse':<16} {'LB-Kontext':<10} LB-Belege")
rows = []
for w, refs in sorted(ident.items()):
    cls = lexicon.get(w, {}).get("klasse", "(n<3)")
    ctx = lb_context(refs)
    rows.append((w, cls, ctx))
    print(f"{w:<14} {cls:<16} {ctx:<10} {', '.join(refs[:4])}{' …' if len(refs) > 4 else ''}")

# Kreuztabelle
print("\nKreuztabelle LA-Klasse x LB-Kontext:")
xt = Counter((cls, ctx) for _, cls, ctx in rows)
classes = sorted({c for c, _ in xt})
ctxs = ["person", "kult", "sonstig", "?"]
print(f"{'':<18}" + "".join(f"{c:>9}" for c in ctxs))
for cls in classes:
    print(f"   {cls:<15}" + "".join(f"{xt.get((cls, c), 0):>9}" for c in ctxs))

# Trefferquote der inhaltlich gerichteten Klassen
hits = misses = 0
for w, cls, ctx in rows:
    if cls == "personenname?" and ctx != "?":
        hits += ctx == "person"; misses += ctx != "person"
    elif cls == "kultwort" and ctx != "?":
        hits += ctx == "kult"; misses += ctx != "kult"
print(f"\nGerichtete Klassen (personenname?/kultwort) mit LB-Beleg: "
      f"{hits} Treffer, {misses} Fehltreffer")
print("\nQualitative Anker (Auswahl):")
for w in ("MA-DI", "I-TA-JA", "PA-DE", "I-JA-TE", "DA-MA-TE", "KA-PA"):
    if w in ident:
        cls = lexicon.get(w, {}).get("klasse", "(n<3)")
        print(f"   {w:<10} LA: {cls:<16} LB: {', '.join(ident[w][:5])}")
