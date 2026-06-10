#!/usr/bin/env python3
"""H4c — gleicher Testaufbau wie test_e_suffix.py, angewandt auf das
wortfinale -O (Nebenbefund aus H4b: Final-Neigung 1.83x, die stärkste
aller Vokale, bei nur 3.7% Korpusanteil von /o/).

Besonderheit gegenüber -E: Die gesicherten Funktionswörter KU-RO
('Summe'), KI-RO ('Fehlbetrag') und PO-TO-KU-RO ('Gesamtsumme') enden
auf -RO und stellen einen grossen Teil aller -O-Finale. Jeder Befund
könnte ein lexikalisches Artefakt dieser drei Wörter sein. Deshalb
läuft jede Analyse doppelt:
   (a) alle Wörter   (b) ohne KU-RO/KI-RO/PO-TO-KU-RO

P1  Konzentriert sich der -O-Überschuss auf wenige O-Zeichen — und
    überlebt er den Ausschluss der Funktionswörter?
P2  Beteiligt sich O an Vokal-Paradigmen am letzten Zeichen?
P4  Unterscheidet sich die -O-Rate nach Dokumenttyp (Register)?
P5  Sind einzelne O-Zeichen positionsgebunden (Header vs. Liste)?
"""
import random, re
from collections import Counter, defaultdict
from corpus_lib import (classify, fisher2x2, load_inscriptions, vowel_of,
                        word_signs)

insc = load_inscriptions()
rng = random.Random(42)
V = "O"
FUNC = {"KU-RO", "KI-RO", "PO-TO-KU-RO"}
VARIANTS = [("alle Wörter", frozenset()),
            ("ohne KU-RO/KI-RO/PO-TO-KU-RO", frozenset(FUNC))]


def cv(sign):
    s = re.sub(r"\d", "", sign)
    m = re.fullmatch(r"([A-Z]*?)([AEIOU])", s)
    if not m:
        return None
    c, v = m.groups()
    if any(ch in "AEIOU" for ch in c):
        return None
    return c, v


def collect(exclude):
    wt = Counter()
    for rec in insc.values():
        for t in rec.get("transliteratedWords", []):
            if classify(t) == "word" and t not in exclude:
                wt[t] += 1
    return wt


def sign_stats(word_tok):
    su, sf = Counter(), Counter()
    for w, c in word_tok.items():
        s = word_signs(w)
        for x in s:
            su[x] += c
        sf[s[-1]] += c
    return su, sf


# ===========================================================================
print("=" * 78)
print("P1 — Final-Neigung der O-Zeichen (mit/ohne Funktionswörter)")
print("=" * 78)
for label, excl in VARIANTS:
    wt = collect(excl)
    su, sf = sign_stats(wt)
    TU, TF = sum(su.values()), sum(sf.values())
    base = TF / TU
    print(f"\n--- {label}  (Basisrate {base:.1%}) ---")
    print(f"{'Zeichen':<8}{'Tokens':>7}{'final':>7}{'Neigung':>9}{'p':>9}")
    rows = []
    for s, u in su.items():
        p = cv(s)
        if not p or p[1] != V or u < 10:
            continue
        f = sf[s]
        pref = (f / u) / base
        pv = fisher2x2(f, u - f, TF - f, (TU - u) - (TF - f))
        rows.append((s, u, f, pref, pv))
    for s, u, f, pref, pv in sorted(rows, key=lambda r: -r[3]):
        mark = "  ***" if pv < 0.05 and pref > 1 else ""
        print(f"-{s:<7}{u:>7}{f:>7}{pref:>8.2f}x{pv:>9.3f}{mark}")
    U = sum(u for s, u in su.items() if (q := cv(s)) and q[1] == V)
    F = sum(sf[s] for s in su if (q := cv(s)) and q[1] == V)
    print(f"   -{V} aggregiert: {(F/U)/base:.2f}x  ({F}/{U})")

# ===========================================================================
print()
print("=" * 78)
print("P2 — O in Vokal-Paradigmen am letzten Zeichen")
print("=" * 78)
types = [w for w in collect(frozenset()) if len(word_signs(w)) >= 3]
groups = defaultdict(list)
for w in types:
    s = word_signs(w)
    groups[tuple(s[:-1])].append(s[-1])


def pair_class(a, b):
    pa, pb = cv(a), cv(b)
    if not pa or not pb:
        return "other"
    if pa[0] == pb[0] and pa[1] != pb[1]:
        return "vokal-alt"
    if pa[1] == pb[1] and pa[0] != pb[0]:
        return "kons-alt"
    return "other"


o_pairs = []
n_valt = 0
for pre, fins in groups.items():
    for i in range(len(fins)):
        for j in range(i + 1, len(fins)):
            if pair_class(fins[i], fins[j]) == "vokal-alt":
                n_valt += 1
                if V in (cv(fins[i])[1], cv(fins[j])[1]):
                    o_pairs.append("-".join(pre) + f"-[{fins[i]}|{fins[j]}]")
print(f"O beteiligt an {len(o_pairs)}/{n_valt} Vokal-Alternationen:")
for e in o_pairs:
    print(f"   {e}")
# dazu die 2-Zeichen-Paare mit O (informativ, nicht im Permutationstest):
wset = set(collect(frozenset()))
short = []
for w in sorted(wset):
    s = word_signs(w)
    if len(s) == 2 and (q := cv(s[1])) and q[1] == V:
        for v2 in "AEIU":
            alt = s[0] + "-" + (q[0] + v2 if q[0] else v2)
            if alt in wset:
                short.append(f"{w} ~ {alt}")
print("2-Zeichen-Paare mit O-Alternation (nur informativ):")
for e in short:
    print(f"   {e}")

# ===========================================================================
print()
print("=" * 78)
print("P4 — -O-Finalrate nach Dokumenttyp (mit/ohne Funktionswörter)")
print("=" * 78)


def bucket(rec):
    s = rec.get("support", "")
    if "Tablet" in s or "Lames" in s or "bar" in s:
        return "Verwaltung"
    if any(k in s for k in ("Nodule", "Roundel", "Sealing", "Label")):
        return "Siegel"
    if "Stone" in s or "Architecture" in s:
        return "Stein/Kult"
    return None


for label, excl in VARIANTS:
    rates = defaultdict(lambda: [0, 0])
    for rec in insc.values():
        b = bucket(rec)
        if not b:
            continue
        for t in rec.get("transliteratedWords", []):
            if classify(t) == "word" and t not in excl:
                rates[b][0] += vowel_of(word_signs(t)[-1]) == V
                rates[b][1] += 1
    print(f"\n--- {label} ---")
    for b, (e, n) in sorted(rates.items()):
        print(f"   {b:<12} {e:>4}/{n:<5} = {e/n:.1%} -O-final")
    names = sorted(rates)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, bb = names[i], names[j]
            e1, n1 = rates[a]; e2, n2 = rates[bb]
            p = fisher2x2(e1, n1 - e1, e2, n2 - e2)
            sig = "  ***" if p < 0.05 else ""
            print(f"   {a} vs. {bb}: p={p:.4f}{sig}")

# ===========================================================================
print()
print("=" * 78)
print("P5 — Positionsprofil der O-Zeichen (Tafeln: Header vs. Liste)")
print("=" * 78)
for label, excl in VARIANTS:
    hb, H, B = {}, 0, 0
    for rec in insc.values():
        if "Tablet" not in rec.get("support", ""):
            continue
        toks = rec.get("transliteratedWords", [])
        fn = next((i for i, t in enumerate(toks) if classify(t) == "num"), None)
        if fn is None:
            continue
        for i, t in enumerate(toks):
            if classify(t) != "word" or t in excl:
                continue
            s = word_signs(t)[-1]
            d = hb.setdefault(s, [0, 0])
            if i < fn:
                d[0] += 1; H += 1
            else:
                d[1] += 1; B += 1
    print(f"\n--- {label} ---  (Headeranteil global {H/(H+B):.0%}, n={H+B})")
    for s, (h, b) in sorted(hb.items(), key=lambda kv: -sum(kv[1])):
        q = cv(s)
        if not q or q[1] != V or h + b < 6:
            continue
        p = fisher2x2(h, b, H - h, B - b)
        sig = "  ***" if p < 0.05 else ""
        print(f"   -{s:<4} Header {h:>3}  Liste {b:>3}  "
              f"(Headeranteil {h/(h+b):.0%})  p={p:.3f}{sig}")
