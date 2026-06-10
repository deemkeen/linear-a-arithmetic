# PREDICTIONS — registered, falsifiable (English translation)

*The German originals in `PREDICTIONS.md` are the registered versions,
timestamped by this repository's git history (registered 10 June 2026;
P-III sharpened and re-conditioned the same day; P-VI resolved the
same day). This file is a faithful translation, added 11 June 2026.
Each prediction carries an explicit failure criterion — a prediction
that cannot fail does not count.*

The most important pending test case is the sign-by-sign edition of
the Knossos ivory sceptre (KN Zg 57–58) in *Anetaki II* (Kanta ed.,
forthcoming) — a text that exists but is not yet published.

---

## P-I — Ring KN Zg 57: cult-register morphology (from H4b)

The Ring is a cult object. The -E suffixes {-NE, -ME, -TE, -RE, -SE}
are nearly twice as frequent word-finally in the cult register as in
administration (30.6% vs 17.5%).

**Prediction:** Among the legible phonetic sign groups of the Ring
(≥6 on Face B, ≥9 on Face C), **≥ 25%** end in one of the five signs
{NE, ME, TE, RE, SE}.

**Failure:** < 18% (administrative level or below).

## P-II — Handle KN Zg 58: positional syntax of the KU-R paradigm (from H5)

**Prediction:** If a KU-R-/KI-R form appears on the handle (an
accounting text): KU-RO/KI-RO stand only list-finally, immediately
before a numeral; a KU-RA/KI-RA form may stand in opening/heading
position.

**Failure:** KU-RO opens a list, or KU-RA stands list-finally as an
arithmetically exact column total.

## P-III — Zg 58, Face δ: the fraction-sign sequence (from H6/H9)

From the *308 column of HT 123+124a follows the equation
**A706 (H) = ¼ + s**, where s is the entry sign of the SA-RU *308
field. Core prediction (independent of the reading of s):
**H ≥ ¼** — far above the tentative H = 1/16(?) of Corazza et al.
2021 (Table 8), and compatible with the classical H = 1/3 (Bennett
1950; a live option in Montecchi 2019 and Schrijver 2014).

- If s = A701 "A" (lineara.xyz encoding): we favour A = 1/12,
  H = 1/3 — which also fills the 1/3 gap in the Corazza system.
- If s = A711 "X" (GORILA's drawing; Montecchi's 2019 autopsy):
  H = X + ¼; X was excluded from Corazza's system.

**Failure:** The published value ordering of Zg 58 (or a new
collation of HT 123a) places H below E (= ¼) — in particular,
Corazza's H = 1/16 would then be vindicated and our column equation
shown to rest on a misreading.

## P-IV — New libation inscriptions: slot congruence (from H1)

So far the formula-slot variants covary perfectly (S3 = -TI ⟺
S4 = -MI-NA ⟺ S1 = -WA-E), but N = 3–5.

**Prediction:** Among the next 10 newly published libation-formula
texts with ≥ 2 filled slots, **at most one** incongruent document.

**Failure:** ≥ 2 incongruent documents (the congruence thesis is then
dead and the variants are free variation).

## P-V — New administrative tablets, any site (from H4b/H6)

**Prediction (replication):**
1. Words ending in -NE/-TE have a header share > 40% (global header
   share ≈ 29%).
2. Among undamaged single-column summation formulas, the majority
   (> 50%) sum exactly; multi-column tablets sum column-wise (as
   HT 123+124a OLIV does).

**Failure:** -NE/-TE header share ≤ 30%, or systematically
non-summing intact totals.

## P-VI — Erasure localisation on deviating tablets (from H10;
## registered 10 June 2026, BEFORE reading the apparatus concerned)

On the 11 single-column checkable KU-RO tablets examined first, the
criterion "erasure/correction in a numeral-bearing line or the totals
line" separates deviators (3/3) from exact tablets (0/8) perfectly.
The GORILA apparatus of the remaining deviating tablets (HT 27a, 102,
110a, 118, 119, 122a) was **deliberately left unread** at
registration time.

**Prediction:** Among the structurally sound of these tablets
(genuine small summation deviation, no parser/damage artefact), the
majority show erasures/corrections in numeric context; exactly
summing tablets continue not to.

**Failure:** Numeric erasures appear on newly checked exact tablets
at similar rates as on deviators, or the majority of genuine
deviators are apparatus-clean.

**→ RESOLVED 10 June 2026 (same day, after blind classification):**
Genuine candidates among the six: HT 102, HT 119. Result:
**HT 102 ✅** (tens written over an erasure ⟦||⟧; GORILA itself notes
a fraction trace "not carried into the total" — the update mechanism
in action); **HT 119 ❌** (no erasure, but an uncertain numeral
reading 67/68 — the deviation may be a modern reading artefact, not
an ancient error). Strict score: 1/2 — **indeterminate**, neither
confirmed nor falsified. The core thesis is supported directly by
HT 102 and indirectly by HT 119. Addendum: HT 118 (full palimpsest,
".1-5 sur ⟦ ⟧") turned out to be a second two-column tablet with an
exactly-summing KI column and a deviating main column — marked post
hoc. Details: `test_erasures.py` / `data/gorila_apparatus.json`.

---

*Method: exact Fisher tests and arithmetic checks as implemented in
this repository's test_*.py scripts; evaluation will use the same
scripts against the then-published transcriptions.*
