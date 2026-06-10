#!/usr/bin/env python3
"""H5 — Dialekt-Test: Ist KU-RO vs. KU-RA eine Ost-/Zentralkreta-Variante?

Entscheidungsmatrix:
  gleiche Funktion + komplementäre Geographie        -> Dialekt
  beide Formen am selben Ort, verschiedene Kontexte  -> Grammatik
  gemischt / zu wenig Belege                         -> unentscheidbar

D1  Geographie der Summen-/Defizitwörter (KU-RO/KU-RA/KU-RE,
    KI-RO/KI-RA/KI-RU, PO-TO-KU-RO): Ort x Form; kritische Frage:
    benutzt Ostkreta (Zakros) AUCH KU-RO?
D2  Funktionstest: verhält sich KU-RA auf ZA20 arithmetisch wie eine
    Summe? (Einträge davor aufsummieren, mit 130 vergleichen.)
D3  Kontrolle: splitten auch andere -O/-A-Minimalpaare regional?
D4  Konvergenz: zeigen die unabhängigen Libationsformel-Varianten (H1)
    dieselbe Ost-Abweichung?
"""
from collections import Counter, defaultdict
from corpus_lib import (classify, cv, fisher2x2, load_inscriptions,
                        parse_number, word_signs)

insc = load_inscriptions()

REGION = {
    "Haghia Triada": "Zentral", "Phaistos": "Zentral", "Knossos": "Zentral",
    "Tylissos": "Zentral", "Arkhalkhori": "Zentral", "Iouktas": "Zentral",
    "Troullos": "Zentral", "Kophinas": "Zentral", "Apodoulou": "Zentral",
    "Arkhanes": "Zentral",
    "Zakros": "Ost", "Palaikastro": "Ost", "Petras": "Ost", "Gournia": "Ost",
    "Mokhilos": "Ost", "Pyrgos": "Ost", "Petsophas": "Ost", "Praisos": "Ost",
    "Psykhro": "Ost",
    "Khania": "West", "Vrysinas": "West",
    # bewusst nicht binär klassifiziert: Malia, Syme (Grenzlagen), Ägäis-Inseln
}


def region(site):
    return REGION.get(site)


# ===========================================================================
print("=" * 78)
print("D1 — Geographie der Summen-/Defizitwörter")
print("=" * 78)
FORMS = ["KU-RO", "KU-RA", "KU-RE", "KI-RO", "KI-RA", "KI-RU", "PO-TO-KU-RO"]
occ = []
for name, rec in insc.items():
    toks = rec.get("transliteratedWords", [])
    for i, t in enumerate(toks):
        if t in FORMS:
            nxt_num = next((x for x in toks[i + 1:i + 4]
                            if classify(x) == "num"), None)
            occ.append((t, rec.get("site", "?"), name,
                        rec.get("support", "?"), nxt_num is not None))

for f in FORMS:
    sites = Counter((s, region(s)) for t, s, *_ in [o for o in occ if o[0] == f])
    if not sites:
        continue
    docs = [(n, sup, num) for t, s, n, sup, num in occ if t == f]
    where = ", ".join(f"{s} [{r or '?'}] {c}x" for (s, r), c in sites.most_common())
    with_num = sum(1 for *_, num in docs if num)
    print(f"   {f:<12} {sum(sites.values()):>3} Belege | {where} | vor Zahl: {with_num}/{len(docs)}")

print("\nKritische Frage: Hat Ostkreta (Zakros & Co.) auch KU-RO?")
east_kuro = [(n, s) for t, s, n, *_ in occ if t == "KU-RO" and region(s) == "Ost"]
print(f"   KU-RO in Ostkreta: {len(east_kuro)}x " +
      (f"({', '.join(n for n, _ in east_kuro)})" if east_kuro else ""))

cnt = Counter()
for t, s, *_ in occ:
    r = region(s)
    if r in ("Zentral", "Ost") and (t.endswith("RO") or t.endswith("RA")):
        cnt[(r, "O" if t.endswith("RO") else "A")] += 1
a, b = cnt[("Zentral", "O")], cnt[("Zentral", "A")]
c, d = cnt[("Ost", "O")], cnt[("Ost", "A")]
p = fisher2x2(a, b, c, d)
print(f"\n2x2 (nur KU-R-/KI-R-Formen): Zentral O:{a} A:{b}  |  Ost O:{c} A:{d}")
print(f"   Fisher p = {p:.4f}" + ("  ***" if p < 0.05 else ""))

# ===========================================================================
print()
print("=" * 78)
print("D2 — Funktionstest: Ist KU-RA auf ZA20 arithmetisch eine Summe?")
print("=" * 78)
for docname, formword in (("ZA20", "KU-RA"), ("ARKH2", "KU-RA"),
                          ("HT103", "KI-RA"), ("ZA8", "KI-RA")):
    rec = insc.get(docname)
    if not rec:
        continue
    toks = rec.get("transliteratedWords", [])
    print(f"\n{docname} ({rec.get('site')}, {rec.get('support')}):")
    print("   " + " ".join(t if t != "\n" else "¶" for t in toks))
    if formword in toks:
        i = toks.index(formword)
        acc, j = [], 0
        while j < i:
            v = parse_number(toks[j])
            if v is not None:
                run = v
                while j + 1 < i and (nv := parse_number(toks[j + 1])) is not None:
                    j += 1; run += nv
                acc.append(run)
            j += 1
        total = None
        j = i + 1
        while j < len(toks) and j < i + 5:
            v = parse_number(toks[j])
            if v is not None:
                total = v
                while j + 1 < len(toks) and (nv := parse_number(toks[j + 1])) is not None:
                    j += 1; total += nv
                break
            j += 1
        if acc and total is not None:
            s = sum(acc)
            print(f"   Einträge davor: {[float(x) for x in acc]}  Summe={float(s):g}"
                  f"  |  {formword} {float(total):g}"
                  f"  ->  {'EXAKT ✓' if s == total else f'Δ={float(abs(s-total)):g}'}")
        elif total is not None:
            print(f"   {formword} {float(total):g} — keine summierbaren Einträge davor erhalten")

# ===========================================================================
print()
print("=" * 78)
print("D3 — Kontrolle: splitten andere -O/-A-Minimalpaare regional?")
print("=" * 78)
word_sites = defaultdict(Counter)
for name, rec in insc.items():
    for t in rec.get("transliteratedWords", []):
        if classify(t) == "word":
            word_sites[t][rec.get("site", "?")] += 1


def regs(w):
    return {region(s) for s in word_sites[w] if region(s)}


pairs = []
for w in sorted(word_sites):
    s = word_signs(w)
    q = cv(s[-1])
    if q and q[1] == "O":
        alt = "-".join(s[:-1] + [q[0] + "A" if q[0] else "A"])
        if alt in word_sites and alt not in FORMS and w not in FORMS:
            pairs.append((w, alt))
split_zo = split_other = same = 0
for w, alt in pairs:
    ro, ra = regs(w), regs(alt)
    so = ", ".join(f"{s}({c})" for s, c in word_sites[w].most_common())
    sa = ", ".join(f"{s}({c})" for s, c in word_sites[alt].most_common())
    if ro and ra and not (ro & ra):
        if "Zentral" in ro and "Ost" in ra:
            tag = "  << Zentral-O/Ost-A"; split_zo += 1
        else:
            tag = "  << disjunkt"; split_other += 1
    else:
        tag = ""; same += 1
    print(f"   {w:<14} [{so}]  ~  {alt:<14} [{sa}]{tag}")
print(f"\nBilanz: Zentral-O/Ost-A-Splits: {split_zo}, andere Splits: {split_other}, "
      f"überlappend/unklar: {same}")

# ===========================================================================
print()
print("=" * 78)
print("D4 — Konvergenz: Libationsformel-Varianten nach Region (aus H1)")
print("=" * 78)
MARKERS = ("TA-I-*301", "SA-SA-RA", "SA-RA-ME", "U-NA-", "I-PI-NA")
DEVIANT = {"S1": "E", "S3": "TI", "S4": "MINA"}
rows = []
for name, rec in insc.items():
    seq = [t for t in rec.get("transliteratedWords", []) if classify(t) == "word"]
    if not any(m in w for w in seq for m in MARKERS):
        continue
    sv = {}
    for w in seq:
        if "TA-I-*301" in w:
            sv["S1"] = "E" if w.endswith("WA-E") else "JA" if w.endswith("WA-JA") else None
        elif w.startswith("U-NA") and word_signs(w)[-1] in ("SI", "TI"):
            sv["S3"] = word_signs(w)[-1]
        elif w.startswith("I-PI-NA"):
            sv["S4"] = "MA" if w.endswith("MA") else "MINA" if w.endswith("MI-NA") else None
        elif "SA-SA-RA" in w or w.endswith("SA-RA-ME"):
            sv["S2"] = word_signs(w)[0]
    sv = {k: v for k, v in sv.items() if v}
    if not sv:
        continue
    r = region(rec.get("site", "?"))
    dev = any(sv.get(k) == v for k, v in DEVIANT.items()) or sv.get("S2") == "SA"
    rows.append((name, rec.get("site"), r, dev, sv))
    print(f"   {name:<9} {str(rec.get('site'))[:13]:<14} [{r or '?'}]  "
          f"{'ABWEICHEND' if dev else 'Standard  '}  {sv}")
zc = Counter((r, dev) for _, _, r, dev, _ in rows if r in ("Zentral", "Ost"))
a, b = zc[("Zentral", True)], zc[("Zentral", False)]
c, d = zc[("Ost", True)], zc[("Ost", False)]
p = fisher2x2(a, b, c, d)
print(f"\n2x2 Formel-Abweichung: Zentral {a}/{a+b} abweichend | Ost {c}/{c+d} abweichend")
print(f"   Fisher p = {p:.4f}" + ("  ***" if p < 0.05 else ""))
