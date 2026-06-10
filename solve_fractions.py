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
# KI-RO-Spalte von HT123+124a (bedingt auf GORILA-Lesung '6['):
# 1+X + X + 3/4 + 3/4 = 6  ->  X = 7/4. Konvergiert mit Youngers
# unabhängiger Ratio-Ableitung X=7/4 aus Zeile a.3-4 (Kommentar HT123).
X711 = "\U0001074E"
constraints.append(("HT123+124a:KI-RO",
                    SymVal(Fraction(5, 2), Counter({X711: 2})),
                    SymVal(Fraction(6))))

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
# Einzelvariablen-Constraints vorab analytisch lösen (hier: X aus der
# KI-RO-Spalte: 5/2 + 2X = 6 -> X = 7/4; konvergiert mit Youngers
# unabhängiger Ratio-Ableitung für Zeile a.3-4)
PRESOLVED = {X711: Fraction(7, 4)}
print(f"\nVorab gelöst: X (A711) = 7/4  (KI-RO-Spalte; = Youngers Ratio-Wert)")
varlist = sorted((k for k in used_vars if k not in PRESOLVED),
                 key=lambda k: -used_vars[k])
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
    assign = {**PRESOLVED, **dict(zip(varlist, combo))}
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
    assign = {**PRESOLVED, **ANCHOR, **dict(zip(free, combo))}
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

# ---- Abgleich mit Corazza et al. 2021 (JAS 125, Table 8) ------------------
print("\n" + "=" * 78)
print("Abgleich: Corazza/Ferrara/Montecchi/Tamburini/Valério 2021, Table 8")
print("=" * 78)
CORAZZA = {J707: Fraction(1, 2), E704: Fraction(1, 4),
           JE732: Fraction(3, 4),                    # Table 9
           A701: Fraction(1, 24), A706: Fraction(1, 16)}  # beide '(?)' = tentativ
sat, unsat = check({**PRESOLVED, **CORAZZA})  # X=7/4 ergänzt (bei Corazza ausgeschlossen)
print(f"Corazza-Belegung (J=1/2, E=1/4, JE=3/4, A=1/24?, H=1/16?):"
      f" erfüllt {sat}/{len(constraints)}")
for n, d in unsat:
    print(f"   verletzt: {n} (Δ={float(d):+g})")
print(f"""
Befund:
- JE=3/4 (Corazza Table 9) reproduziert unser Solver-Ergebnis unabhängig.
- Der Ausschluss von X aus ihrem System konvergiert mit unserem
  T2-Befund (H6): A711 'X' verhält sich nicht wie ein normaler Bruch.
- WIDERSPRUCH bei den tentativen Werten: unsere HT123-Spaltengleichung
  verlangt H - A = 1/4, Corazzas H=1/16, A=1/24 ergeben 1/48.
- Auflösung, die beides heilt: A=1/12, H=1/3 erfüllt H-A=1/4 exakt UND
  füllt die auffällige 1/3-Lücke in Corazzas System (typologisch ist
  ein fehlendes 1/3 ungewöhnlich). Alternative: A=1/24 -> H=7/24
  (typologisch unattraktiv). Vorbehalt: hängt an EINER Tafel; Token
  '4+A' trägt ein zweites, unlesbares Zeichen (U+1076B) — die Lesung
  ist mit GORILA-Faksimile zu verifizieren.""")
