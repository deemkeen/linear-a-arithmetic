#!/usr/bin/env python3
"""H8 — Akrophonie-Test: Sind ligierte Silbenzeichen auf Gefäß-Logogrammen
die Anfangssilben der ausgeschriebenen Gefäßwörter?

HT31 listet Gefäßtypen mit ausgeschriebenen Namen UND Gefäß-Logogrammen.
Das Zepter-Paper (Zg 57) bestätigt VAS+Silbenzeichen-Ligaturen als
Typ-/Inhaltsangaben. Wenn das Prinzip akrophon ist, sollten die ligierten
Silbenzeichen überzufällig oft als Anfangssilbe belegter Wörter aus
Gefäß-Kontexten auftreten.
"""
import json, re
from collections import Counter
from corpus_lib import classify, load_inscriptions, word_signs, DATA

insc = load_inscriptions()

# Gefäß-Ligaturen aus den Transliterationen: Tokens wie '*402VAS+KA', '*401+RU'
lig_signs = Counter()
for rec in insc.values():
    for t in rec.get("transliteratedWords", []):
        m = re.fullmatch(r"\*4\d+(?:VAS)?\+([A-Z]{1,2}\d?)", t.strip())
        if m:
            lig_signs[m.group(1)] += 1

print("=" * 78)
print("H8 — Gefäß-Ligaturen (*4xx+Silbenzeichen) im Korpus")
print("=" * 78)
print("ligierte Zeichen:", ", ".join(f"{s}({c}x)" for s, c in lig_signs.most_common()))

# Referenz: HT31, die Gefäßnamen-Tafel
ht31 = [t for t in insc["HT31"]["transliteratedWords"] if classify(t) == "word"]
print(f"\nHT31-Gefäßwörter: {ht31}")


def name_initial(w):
    """erste Silbe des Namens — führende *8xx-Logogramme überspringen"""
    return next((s for s in word_signs(w) if not s.startswith("*")), None)


vessel_initials = Counter(name_initial(w) for w in ht31 if name_initial(w))
print(f"Anfangssilben der Gefäßwörter: {sorted(vessel_initials)}")

# Treffer: ligiertes Zeichen == Anfangssilbe eines HT31-Gefäßworts?
hits = {s: (s in vessel_initials) for s in lig_signs}
n_hit = sum(lig_signs[s] for s, h in hits.items() if h)
n_tot = sum(lig_signs.values())
print(f"\nTreffer (tokenweise): {n_hit}/{n_tot} Ligatur-Vorkommen tragen eine "
      f"HT31-Gefäßwort-Anfangssilbe")
for s, c in lig_signs.most_common():
    match = [w for w in ht31 if name_initial(w) == s]
    print(f"   +{s:<5} {c}x  ->  {', '.join(match) if match else '—'}")

# Nullmodell: Wahrscheinlichkeit, dass ein zufälliges wortinitiales Zeichen
# eine HT31-Anfangssilbe ist (gewichtet mit korpusweiter Initial-Frequenz)
init_freq = Counter()
for rec in insc.values():
    for t in rec.get("transliteratedWords", []):
        if classify(t) == "word":
            init_freq[word_signs(t)[0]] += 1
tot_init = sum(init_freq.values())
p0 = sum(c for s, c in init_freq.items() if s in vessel_initials) / tot_init
from math import comb
p_binom = sum(comb(n_tot, k) * p0**k * (1 - p0)**(n_tot - k)
              for k in range(n_hit, n_tot + 1))
print(f"\nNullmodell: P(zufälliges Initialzeichen ist HT31-Anfangssilbe) = {p0:.2f}")
print(f"Binomialtest P(>= {n_hit}/{n_tot} Treffer) = {p_binom:.4f}"
      + ("  ***" if p_binom < 0.05 else ""))
