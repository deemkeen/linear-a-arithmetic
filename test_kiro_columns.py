#!/usr/bin/env python3
"""H6 — Mehrspalten-Arithmetik und KI-RO als Komplement ('geschuldet').

Tafeln vom Typ HT123 führen pro Eintrag mehrere Spalten (z.B. OLIV-Menge,
*308-Menge, KI-RO-Fehlbetrag) und schliessen mit Spalten-Summen (KU-RO
OLIV …, KU-RO …, KI-RO …). Der einspaltige Parser aus analyze.py kann
das nicht prüfen — dieser hier modelliert Zeilen als (Label -> Wert).

Zwei Tests:
T1  Spaltensummen: für jedes Label L (Logogramm oder KI-RO), das in >=2
    Eintragszeilen UND in einer Summenzeile mit Wert steht:
    Summe der Einträge  ==  Summenzeilen-Wert?
T2  KI-RO-Komplement: summieren die KI-RO-Einzelwerte einer Tafel zu
    einer eigenen KI-RO-Schlusssumme?

Zeilenmodell: Tokens je Zeile; ein 'Label' ist das letzte Wort/Logogramm
vor einer Zahl(enfolge); Zeilen, deren erstes Wort KU-RO/PO-TO-KU-RO
ist, sind Summenzeilen; eine KI-RO-Zeile ist Summenzeile, wenn zuvor
>=2 KI-RO-Eintragswerte aufgelaufen sind.
"""
from collections import defaultdict
from fractions import Fraction
from corpus_lib import classify, load_inscriptions, parse_number

insc = load_inscriptions()
TOTAL_WORDS = ("KU-RO", "PO-TO-KU-RO")


def lines_of(toks):
    line, out = [], []
    for t in toks:
        if classify(t) == "nl":
            if line:
                out.append(line)
            line = []
        else:
            line.append(t)
    if line:
        out.append(line)
    return out


def parse_line(line):
    """-> (is_total, [(label, value)]): Label = letztes Wort/Logogramm vor
    einer Zahlenfolge; value = Summe der unmittelbar folgenden Numerale."""
    cells, label = [], None
    is_total = bool(line) and line[0] in TOTAL_WORDS
    i = 0
    while i < len(line):
        t = line[i]
        c = classify(t)
        if c in ("word", "logo") and t != "𐄁":
            label = t
        v = parse_number(t)
        if v is not None:
            run = v
            while i + 1 < len(line) and (nv := parse_number(line[i + 1])) is not None:
                i += 1
                run += nv
            cells.append((label, run))
            label = None
        i += 1
    return is_total, cells


def has_unparseable(toks):
    import re
    return any(re.fullmatch(r"\.\d+", t.strip()) for t in toks)


print("=" * 78)
print("H6 — Spaltensummen & KI-RO-Komplement (mehrspaltige Tafeln)")
print("=" * 78)

t1_ok, t1_near, t1_off = [], [], []
t2_results = []
for name, rec in insc.items():
    if "Tablet" not in rec.get("support", ""):
        continue
    toks = rec.get("transliteratedWords", [])
    entry_vals = defaultdict(list)     # label -> Werte aus Eintragszeilen
    total_vals = {}                    # label -> Wert aus Summenzeilen
    kiro_entries, kiro_total = [], None
    pending_label = None               # Label einer zahlenlosen Vorzeile
    seen_total = False                 # schon eine KU-RO-Summenzeile passiert?
    for line in lines_of(toks):
        is_total, cells = parse_line(line)
        first_word = next((t for t in line if classify(t) == "word"), None)
        if first_word == "KI-RO":
            kiro_cells = [v for l, v in cells if l == "KI-RO"]
            if kiro_cells and seen_total:
                kiro_total = kiro_cells[0]        # Schlusssumme nach KU-RO
            elif kiro_cells:
                kiro_entries.append(kiro_cells[0])
            continue
        if is_total:
            seen_total = True
        if not cells:
            # Zeile wie '*308 𐄁': Label gilt für die Folgezeile (Summen-
            # zeile 'KU-RO 25 …' gehört dann zu dieser Spalte)
            pending_label = next((t for t in reversed(line)
                                  if classify(t) in ("word", "logo") and t != "𐄁"), None)
            continue
        for label, v in cells:
            if label in TOTAL_WORDS and pending_label:
                label = pending_label
            if label is None or label in TOTAL_WORDS:
                continue
            if is_total:
                total_vals[label] = v
            else:
                entry_vals[label].append(v)
        pending_label = None

    # T1: Spaltensummen über Logogramm-Labels
    for label, total in total_vals.items():
        ev = entry_vals.get(label, [])
        if len(ev) >= 2:
            s = sum(ev)
            d = abs(s - total)
            row = (name, label, [float(x) for x in ev], float(s), float(total))
            if d == 0:
                t1_ok.append(row)
            elif d <= 1:
                t1_near.append(row)
            else:
                t1_off.append(row)
    # T2: KI-RO-Komplement
    if kiro_total is not None and len(kiro_entries) >= 2:
        s = sum(kiro_entries)
        t2_results.append((name, [float(x) for x in kiro_entries],
                           float(s), float(kiro_total),
                           has_unparseable(toks)))

print(f"\nT1 — Spaltensummen (Label kommt in >=2 Einträgen UND Summenzeile vor):")
print(f"   exakt: {len(t1_ok)}   Δ<=1: {len(t1_near)}   abweichend: {len(t1_off)}")
for name, label, ev, s, tot in t1_ok:
    print(f"   ✓ {name:<12} Spalte {label:<8} {ev} -> Σ={s:g} == KU-RO {tot:g}")
for name, label, ev, s, tot in t1_near:
    print(f"   ~ {name:<12} Spalte {label:<8} {ev} -> Σ={s:g} vs. {tot:g} (Δ={abs(s-tot):g})")
for name, label, ev, s, tot in t1_off[:8]:
    print(f"   ✗ {name:<12} Spalte {label:<8} {ev} -> Σ={s:g} vs. {tot:g}")

print(f"\nT2 — KI-RO-Komplement (Einzel-Fehlbeträge vs. KI-RO-Schlusssumme):")
if not t2_results:
    print("   keine Tafel mit >=2 KI-RO-Einträgen + KI-RO-Schlusssumme parsbar")
for name, ev, s, tot, dirty in t2_results:
    flag = " [enthält unparsbare Werte!]" if dirty else ""
    verdict = "EXAKT ✓" if s == tot else f"Δ={abs(s-tot):g}"
    print(f"   {name:<12} KI-RO-Einträge {ev} -> Σ={s:g} vs. Schluss-KI-RO {tot:g}: {verdict}{flag}")

# Detailblick auf den Haupt-Kandidaten HT123+124a
print("\nDetail HT123+124a (Roh-Zeilen):")
rec = insc.get("HT123+124a")
if rec:
    for line in lines_of(rec["transliteratedWords"]):
        print("   |", " ".join(line))
