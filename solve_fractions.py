#!/usr/bin/env python3
"""H9 — Bruchwert-Inferenz: Klasma-Zeichenwerte aus Arithmetik-Constraints.

Idee: Die Werte der Linear-A-Bruchzeichen (A701 ff.) werden als Unbekannte
behandelt. Jede KU-RO-Summenformel, die Bruchzeichen enthält, liefert eine
Gleichung  Σ Einträge = Total. Gesucht ist die Wertebelegung, die maximal
viele Gleichungen exakt erfüllt (Max-SAT; einzelne Verstöße sind erlaubt —
Schreiberfehler wie HT13 sind belegt).

Wichtig: gearbeitet wird auf den Unicode-Originalzeichen aus rec['words'],
nicht auf den teils geratenen Transliterations-Brüchen von lineara.xyz
('≈ ¹⁄₆', '.3').

Zusätzlich fließt die Spalten-Gleichung aus H6 ein:
HT123+124a, *308-Spalte:  A706(H) − A701(A) = ¼.
"""
import itertools, re, unicodedata
from collections import Counter, defaultdict
from fractions import Fraction
from corpus_lib import classify, load_inscriptions, parse_number

insc = load_inscriptions()
KLASMA = lambda s: [ch for ch in s if 0x10740 <= ord(ch) <= 0x1075F]


def kname(ch):
    return unicodedata.name(ch, hex(ord(ch))).replace("LINEAR A SIGN ", "")


class SymVal:
    """Wert = rationale Konstante + Summe von Klasma-Variablen."""
    def __init__(self, const=Fraction(0), vars=None):
        self.const, self.vars = const, Counter(vars or {})

    def __add__(self, o):
        return SymVal(self.const + o.const, self.vars + o.vars)

    def __str__(self):
        v = " + ".join(f"{kname(k)}" * c if c == 1 else f"{c}*{kname(k)}"
                       for k, c in self.vars.items())
        return f"{self.const}{' + ' + v if v else ''}"


def token_symval(t, u):
    """numerischer Token -> SymVal oder None.
    Ganzzahl aus Transliteration, Klasma-Variablen aus Unicode."""
    ks = KLASMA(u)
    m = re.fullmatch(r"\d+", t.strip())
    if m:
        return SymVal(Fraction(int(m.group())), Counter(ks))
    if ks:
        return SymVal(Fraction(0), Counter(ks))
    return None


def is_damaged(t):
    return any(c in t for c in "[]?•𐝫")


# ---- Constraints aus einspaltigen KU-RO-Tafeln (Stream-Modell) -----------
constraints = []   # (name, lhs SymVal, rhs SymVal)
for name, rec in insc.items():
    tw, uw = rec.get("transliteratedWords", []), rec.get("words", [])
    if len(tw) != len(uw) or "KU-RO" not in tw:
        continue
    if not any(KLASMA(u) for u in uw):
        continue
    if name.startswith("HT123"):
        continue   # mehrspaltig, separat unten
    acc, i, seg_start = [], 0, 0
    while i < len(tw):
        if tw[i] == "KU-RO":
            j, total = i + 1, None
            while j < len(tw) and j < i + 6:
                sv = token_symval(tw[j], uw[j])
                if sv is not None:
                    total = sv
                    while j + 1 < len(tw) and (nv := token_symval(tw[j+1], uw[j+1])) is not None:
                        j += 1; total = total + nv
                    break
                if classify(tw[j]) == "word":
                    break
                j += 1
            # Schadens-Check nur im betroffenen Segment, nicht tafelweit
            clean = not any(is_damaged(t) for t in tw[seg_start:j + 1])
            if total is not None and acc and clean:
                lhs = SymVal()
                for v in acc:
                    lhs = lhs + v
                constraints.append((name, lhs, total))
            acc, i, seg_start = [], j + 1, j + 1
            continue
        sv = token_symval(tw[i], uw[i])
        if sv is not None:
            run = sv
            while i + 1 < len(tw) and (nv := token_symval(tw[i+1], uw[i+1])) is not None:
                i += 1; run = run + nv
            acc.append(run)
        i += 1

# ---- Spalten-Constraint aus H6 (HT123+124a, *308) -------------------------
A701 = "\U00010740"; A706 = "\U00010745"
J707 = "\U00010746"; E704 = "\U00010743"; JE732 = "\U00010755"
constraints.append(("HT123+124a:*308",
                    SymVal(Fraction(101, 4), Counter({A701: 1})),
                    SymVal(Fraction(25), Counter({A706: 1}))))
# Struktur-Axiom: A732 'JE' ist die Ligatur aus J und E
constraints.append(("Axiom JE=J+E",
                    SymVal(Fraction(0), Counter({JE732: 1})),
                    SymVal(Fraction(0), Counter({J707: 1, E704: 1}))))

print("=" * 78)
print("H9 — Arithmetik-Constraints (Unicode-Klasma als Unbekannte)")
print("=" * 78)
used_vars = Counter()
for name, lhs, rhs in constraints:
    for k in (lhs.vars + rhs.vars):
        used_vars[k] += 1
    print(f"   {name:<16} {lhs}  =  {rhs}")
print(f"\nVariablen in Constraints: "
      f"{', '.join(f'{kname(k)}({c} Gl.)' for k, c in used_vars.most_common())}")

# ---- Max-SAT über Kandidatenwerte -----------------------------------------
CAND = [Fraction(a, b) for a, b in
        [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (1, 6), (5, 6),
         (1, 8), (3, 8), (5, 8), (1, 10), (1, 12), (5, 12), (1, 16)]]
varlist = sorted(used_vars, key=lambda k: -used_vars[k])
print(f"Suchraum: {len(CAND)}^{len(varlist)} = {len(CAND)**len(varlist):,} Belegungen")


def check(assign):
    sat, unsat = 0, []
    for name, lhs, rhs in constraints:
        l = lhs.const + sum(assign[k] * c for k, c in lhs.vars.items())
        r = rhs.const + sum(assign[k] * c for k, c in rhs.vars.items())
        if l == r:
            sat += 1
        else:
            unsat.append((name, l - r))
    return sat, unsat


best = []
for combo in itertools.product(CAND, repeat=len(varlist)):
    assign = dict(zip(varlist, combo))
    # Plausibilität: Kompositzeichen JE muss = J + E sein, falls alle drei da
    sat, unsat = check(assign)
    best.append((sat, assign, unsat))
best.sort(key=lambda x: -x[0])

top_sat = best[0][0]
print(f"\nBeste Belegungen erfüllen {top_sat}/{len(constraints)} Gleichungen exakt.")
print("Alle Belegungen mit Maximum (Werte der mehrfach belegten Variablen):")
seen = set()
for sat, assign, unsat in best:
    if sat < top_sat:
        break
    key = tuple(assign[k] for k in varlist if used_vars[k] >= 2)
    sig = ", ".join(f"{kname(k)}={assign[k]}" for k in varlist)
    if key in seen:
        continue
    seen.add(key)
    viol = "; ".join(f"{n} (Δ={float(d):+g})" for n, d in unsat)
    print(f"   [{sat}/{len(constraints)}] {sig}")
    print(f"        verletzt: {viol}")

# ---- verankerter Modus: J=1/2, E=1/4 sind etabliert -----------------------
print("\n" + "=" * 78)
print("Verankerter Modus (J=1/2, E=1/4 fix; Literaturkonsens)")
print("=" * 78)
ANCHOR = {J707: Fraction(1, 2), E704: Fraction(1, 4)}
free = [k for k in varlist if k not in ANCHOR]
results = []
for combo in itertools.product(CAND, repeat=len(free)):
    assign = {**ANCHOR, **dict(zip(free, combo))}
    sat, unsat = check(assign)
    results.append((sat, assign, unsat))
results.sort(key=lambda x: -x[0])
top = results[0][0]
seen = set()
for sat, assign, unsat in results:
    if sat < top:
        break
    sig = ", ".join(f"{kname(k)}={assign[k]}" for k in free)
    if sig in seen:
        continue
    seen.add(sig)
    viol = "; ".join(f"{n} (Δ={float(d):+g})" for n, d in unsat) or "—"
    print(f"   [{sat}/{len(constraints)}] {sig}")
    print(f"        verletzt: {viol}")
print("\nInterpretation: Verletzte Gleichungen unter J=1/2 sind Kandidaten")
print("für Schreiberfehler (HT13 ist für JEDEN J-Wert unerfüllbar: 2J=J).")
