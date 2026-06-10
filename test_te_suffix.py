#!/usr/bin/env python3
"""H7 — Sind -TE und -NE abtrennbare Suffixe mit Positionsfunktion?

Aus H4b: -TE/-NE sind kopfzeilen-affin. Schärferer Test: Existieren
Paare aus Stamm X und X-TE (bzw. X-NE), und stehen die suffigierten
Formen komplementär zu den Grundformen (Header vs. Listenkörper)?
Das wäre der erste Funktionsnachweis für ein einzelnes Suffix
(Arbeitsdeutung -TE: Herkunfts-/Transaktionsmarker 'von X').
"""
from collections import Counter
from corpus_lib import classify, fisher2x2, load_inscriptions, word_signs

insc = load_inscriptions()

words = Counter()
for rec in insc.values():
    for t in rec.get("transliteratedWords", []):
        if classify(t) == "word":
            words[t] += 1
wset = set(words)


def position_counts(target):
    """(header, body) auf Tafeln (vor/nach erster Zahl) + initial sonst"""
    h = b = 0
    for rec in insc.values():
        if "Tablet" not in rec.get("support", ""):
            continue
        toks = rec.get("transliteratedWords", [])
        fn = next((i for i, t in enumerate(toks) if classify(t) == "num"), None)
        if fn is None:
            continue
        for i, t in enumerate(toks):
            if t == target:
                if i < fn:
                    h += 1
                else:
                    b += 1
    return h, b


for SUF in ("TE", "NE"):
    print("=" * 78)
    print(f"H7 — Paare X ~ X-{SUF}")
    print("=" * 78)
    pairs = []
    for w in sorted(wset):
        s = word_signs(w)
        if s[-1] == SUF and len(s) >= 3:
            stem = "-".join(s[:-1])
            if stem in wset:
                pairs.append((stem, w))
    sh = sb = th = tb = 0
    for stem, suff in pairs:
        s_h, s_b = position_counts(stem)
        t_h, t_b = position_counts(suff)
        sh += s_h; sb += s_b; th += t_h; tb += t_b
        print(f"   {stem:<16} ({words[stem]}x, Tafel H/L {s_h}/{s_b})   ~   "
              f"{suff:<18} ({words[suff]}x, Tafel H/L {t_h}/{t_b})")
    if th + tb and sh + sb:
        p = fisher2x2(th, tb, sh, sb)
        print(f"\n   gepoolt: X-{SUF} Header {th}/{th+tb} vs. X Header {sh}/{sh+sb}"
              f"  ->  Fisher p={p:.4f}" + ("  ***" if p < 0.05 else ""))
    else:
        print(f"\n   zu wenig Tafel-Belege für gepoolten Test "
              f"(X-{SUF}: {th+tb}, X: {sh+sb})")
    print()
