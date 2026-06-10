#!/usr/bin/env python3
"""H4b — Anschlussanalyse zum verworfenen H4: Was erklärt das wortfinale -E?

H4 (Kopfzeilen-Suffix) ist verworfen. Konkurrierende Erklärungen für den
-E-Überschuss am Wortende (19.5% final vs. 12.4% gesamt), je mit
messbarer Vorhersage:

P1 (Suffix-Inventar):   Der Überschuss konzentriert sich auf WENIGE
                        E-Zeichen (geschlossene Suffix-Klasse). Wäre er
                        phonotaktisch, müssten ALLE E-Zeichen gleichmäßig
                        final-affin sein.
P2 (Paradigma):         Stämme alternieren am letzten Zeichen den VOKAL
                        (X-RA ~ X-RE): mehr Gleicher-Konsonant/anderer-
                        Vokal-Paare als unter Zufall (Permutationstest).
P3 (E-Beteiligung):     E ist an solchen Vokal-Alternationen beteiligt.
P4 (Dokumenttyp):       Die -E-Rate unterscheidet sich nach Texttyp
                        (Verwaltung vs. Siegelpraxis vs. Stein/Kult).
P5 (Zeichen-Position):  Einzelne E-Zeichen sind positionsgebunden
                        (Header vs. Listenkörper), auch wenn -E gesamt
                        es nicht ist (Ergebnis H4).
"""
import random, re
from collections import Counter, defaultdict
from corpus_lib import (classify, fisher2x2, load_inscriptions, vowel_of,
                        word_signs)

insc = load_inscriptions()
rng = random.Random(42)

word_tok = Counter()
for rec in insc.values():
    for t in rec.get("transliteratedWords", []):
        if classify(t) == "word":
            word_tok[t] += 1

sign_uni, sign_fin = Counter(), Counter()
for w, c in word_tok.items():
    s = word_signs(w)
    for x in s:
        sign_uni[x] += c
    sign_fin[s[-1]] += c
TOT_U, TOT_F = sum(sign_uni.values()), sum(sign_fin.values())
BASE = TOT_F / TOT_U


def cv(sign):
    """sign -> (consonant, vowel) oder None für *NNN / AU etc."""
    s = re.sub(r"\d", "", sign)
    m = re.fullmatch(r"([A-Z]*?)([AEIOU])", s)
    if not m:
        return None
    c, v = m.groups()
    if any(ch in "AEIOU" for ch in c):
        return None
    return c, v


# ===========================================================================
print("=" * 78)
print("P1 — Konzentriert sich der Final-Überschuss auf wenige E-Zeichen?")
print("=" * 78)
print(f"Basisrate P(Zeichen steht wortfinal) = {BASE:.1%}\n")
print(f"{'Zeichen':<8}{'Tokens':>7}{'final':>7}{'Neigung':>9}{'p':>9}")
e_rows = []
for s, u in sorted(sign_uni.items(), key=lambda kv: -kv[1]):
    p = cv(s)
    if not p or u < 15:
        continue
    f = sign_fin[s]
    pref = (f / u) / BASE
    pv = fisher2x2(f, u - f, TOT_F - f, (TOT_U - u) - (TOT_F - f))
    if p[1] == "E":
        e_rows.append((s, u, f, pref, pv))
for s, u, f, pref, pv in sorted(e_rows, key=lambda r: -r[3]):
    mark = "  ***" if pv < 0.05 and pref > 1 else ""
    print(f"-{s:<7}{u:>7}{f:>7}{pref:>8.2f}x{pv:>9.3f}{mark}")

print("\nFinal-Neigung aggregiert je Vokal (Kontrolle):")
for v in "AEIOU":
    U = sum(u for s, u in sign_uni.items() if (q := cv(s)) and q[1] == v)
    F = sum(sign_fin[s] for s in sign_uni if (q := cv(s)) and q[1] == v)
    print(f"   -{v}: {(F/U)/BASE:.2f}x  ({F}/{U})")

# ===========================================================================
print()
print("=" * 78)
print("P2/P3 — Vokal-Paradigmen am letzten Zeichen (Permutationstest)")
print("=" * 78)
types = [w for w in word_tok if len(word_signs(w)) >= 3]
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


def count_classes(group_lists):
    cnt, vpairs = Counter(), Counter()
    for fins in group_lists:
        for i in range(len(fins)):
            for j in range(i + 1, len(fins)):
                k = pair_class(fins[i], fins[j])
                cnt[k] += 1
                if k == "vokal-alt":
                    vpairs[frozenset((cv(fins[i])[1], cv(fins[j])[1]))] += 1
    return cnt, vpairs


obs, obs_v = count_classes(list(groups.values()))
n_pairs = sum(obs.values())
multi = sum(1 for g in groups.values() if len(g) >= 2)
print(f"Wort-Typen (>=3 Zeichen): {len(types)}; Stämme mit >=2 Fortsetzungen: {multi}; Paare: {n_pairs}")
print(f"beobachtet:  Vokal-Alternation={obs['vokal-alt']}   "
      f"Konsonant-Alternation={obs['kons-alt']}   übrige={obs['other']}")
ex = []
for pre, fins in groups.items():
    for i in range(len(fins)):
        for j in range(i + 1, len(fins)):
            if pair_class(fins[i], fins[j]) == "vokal-alt":
                ex.append("-".join(pre) + f"-[{fins[i]}|{fins[j]}]")
print("Vokal-Alternationen im Korpus:")
for e in ex:
    print(f"   {e}")

flat = [f for g in groups.values() for f in g]
shape = [len(g) for g in groups.values()]
N_PERM, ge_v, ge_c, sum_v, sum_c = 5000, 0, 0, 0, 0
for _ in range(N_PERM):
    rng.shuffle(flat)
    idx, rebuilt = 0, []
    for n in shape:
        rebuilt.append(flat[idx:idx + n])
        idx += n
    c, _ = count_classes(rebuilt)
    sum_v += c["vokal-alt"]; sum_c += c["kons-alt"]
    ge_v += c["vokal-alt"] >= obs["vokal-alt"]
    ge_c += c["kons-alt"] >= obs["kons-alt"]
print(f"\nPermutationstest ({N_PERM} Permutationen der Finalzeichen):")
print(f"   Vokal-Alternation:     beobachtet {obs['vokal-alt']}, "
      f"Zufallserwartung {sum_v/N_PERM:.1f}, p={ge_v/N_PERM:.4f}")
print(f"   Konsonant-Alternation: beobachtet {obs['kons-alt']}, "
      f"Zufallserwartung {sum_c/N_PERM:.1f}, p={ge_c/N_PERM:.4f}")
e_inv = sum(v for k, v in obs_v.items() if "E" in k)
print(f"   E beteiligt an {e_inv}/{obs['vokal-alt']} Vokal-Alternationen "
      f"({', '.join('~'.join(sorted(k)) + ':' + str(v) for k, v in obs_v.most_common())})")

# ===========================================================================
print()
print("=" * 78)
print("P4 — -E-Finalrate nach Dokumenttyp")
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


rates = defaultdict(lambda: [0, 0])
for rec in insc.values():
    b = bucket(rec)
    if not b:
        continue
    for t in rec.get("transliteratedWords", []):
        if classify(t) == "word":
            rates[b][0] += vowel_of(word_signs(t)[-1]) == "E"
            rates[b][1] += 1
for b, (e, n) in sorted(rates.items()):
    print(f"   {b:<12} {e:>4}/{n:<5} = {e/n:.1%} -E-final")
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
print("P5 — Positionsprofil einzelner E-Zeichen (Tafeln: Header vs. Liste)")
print("=" * 78)
hb, H, B = {}, 0, 0
for rec in insc.values():
    if "Tablet" not in rec.get("support", ""):
        continue
    toks = rec.get("transliteratedWords", [])
    fn = next((i for i, t in enumerate(toks) if classify(t) == "num"), None)
    if fn is None:
        continue
    for i, t in enumerate(toks):
        if classify(t) != "word":
            continue
        s = word_signs(t)[-1]
        d = hb.setdefault(s, [0, 0])
        if i < fn:
            d[0] += 1; H += 1
        else:
            d[1] += 1; B += 1
print(f"Header-Wörter gesamt: {H}, Listenkörper: {B} (Headeranteil global {H/(H+B):.0%})")
for s, _, _, _, _ in sorted(e_rows, key=lambda r: -r[2]):
    h, b = hb.get(s, (0, 0))
    if h + b < 8:
        continue
    p = fisher2x2(h, b, H - h, B - b)
    sig = "  ***" if p < 0.05 else ""
    print(f"   -{s:<4} Header {h:>3}  Liste {b:>3}  (Headeranteil {h/(h+b):.0%})  p={p:.3f}{sig}")
