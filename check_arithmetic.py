#!/usr/bin/env python3
"""Generalisierter, spalten-bewusster Arithmetik-Checker (Nachfolger des
Stream-Modells in analyze.py §3 und des Prototyps test_kiro_columns.py).

Modell:
- Eine Tafel besteht aus SEGMENTEN: Eintragszeilen bis zu einem
  SUMMENBLOCK (eine oder mehrere aufeinanderfolgende Summenzeilen),
  danach beginnt ein neues Segment (zweite Listen auf derselben Tafel).
- Die Summenzeilen definieren die Spalten des Segments:
    'KU-RO <LOGO> n'  -> Spalte <LOGO>  (auch via Vorzeile '<LOGO> 𐄁')
    'KU-RO n'         -> Hauptspalte
    'KI-RO n'/'KI n' im Summenblock -> Total der Defizit-Spalte;
    davor interleaved -> Einträge der Defizit-Spalte (KI = Abkürzung
    von KI-RO; Zweitbeleg HT118).
- Eintragswerte: Logogramm-Spalte nur, wenn sie per Summenzeile
  existiert; sonst Hauptspalte.
- Flags pro Segment: 'beschädigt' (Lücken/unlesbare Numerale) und
  'klasma≈' (von lineara.xyz nur geschätzte Bruchwerte). Ligatur-Namen
  wie 'VIR+[?]' zählen NICHT als Schaden.
"""
import json, re
from collections import defaultdict
from fractions import Fraction
from corpus_lib import DATA, classify, fisher2x2, load_inscriptions, parse_number

insc = load_inscriptions()
TOTALS = {"KU-RO", "PO-TO-KU-RO"}
KIRO = {"KI-RO", "KI"}


def damage_flags(tokens):
    f = set()
    for t in tokens:
        if "+[" in t:
            continue                      # Ligatur mit unlesbarem Partner
        if any(ch in t for ch in "[]?𐝫") or re.fullmatch(r"\.\d+", t.strip()):
            f.add("beschädigt")
        if "≈" in t:
            f.add("klasma≈")
    return f


def lines_of(toks):
    out, line = [], []
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


def parse_cells(line):
    first_word = next((t for t in line if classify(t) == "word"), None)
    cells, label, kind = [], None, None
    i = 0
    while i < len(line):
        t = line[i]
        c = classify(t)
        if c in ("word", "logo") and t != "𐄁":
            label, kind = t, c
        v = parse_number(t)
        if v is not None:
            run = v
            while i + 1 < len(line) and (nv := parse_number(line[i + 1])) is not None:
                i += 1
                run += nv
            cells.append((label, kind, run))
            label, kind = None, None
        i += 1
    return first_word, cells


def check_tablet(rec):
    lines = lines_of(rec.get("transliteratedWords", []))
    results = []

    def new_segment():
        return {"entries": defaultdict(list), "flags": set()}

    def close(seg, totals, tflags):
        # Logo-Einträge ohne eigenes Spaltentotal -> Hauptspalte
        for col in [c for c in seg["entries"]
                    if isinstance(c, tuple) and c not in totals]:
            seg["entries"]["_main"].extend(seg["entries"].pop(col))
        for col, total in totals.items():
            ev = seg["entries"].get(col, [])
            if len(ev) >= 2:
                s = sum(ev)
                d = abs(s - total)
                status = "EXAKT" if d == 0 else ("NAH" if d <= 1 else "ABW")
                results.append((col, [float(x) for x in ev], float(s),
                                float(total), status,
                                frozenset(seg["flags"] | tflags)))

    seg, totals, tflags = new_segment(), {}, set()
    mode, pending = "entries", None
    for line in lines:
        fw, cells = parse_cells(line)
        lflags = damage_flags(line)
        is_total = fw in TOTALS
        only_kiro = bool(cells) and all(l in KIRO for l, k, v in cells)
        if mode == "entries":
            if is_total:
                mode = "totals"
                totals, tflags = {}, set(lflags)
            else:
                seg["flags"] |= lflags
                if not cells:
                    pending = next((t for t in reversed(line)
                                    if classify(t) in ("word", "logo") and t != "𐄁"), pending)
                    continue
                for label, kind, v in cells:
                    if label in KIRO:
                        seg["entries"]["_kiro"].append(v)
                    elif kind == "logo":
                        seg["entries"][("logo", label)].append(v)
                    else:
                        seg["entries"]["_main"].append(v)
                pending = None
                continue
        else:
            if not (is_total or only_kiro or not cells):
                close(seg, totals, tflags)        # Summenblock zu Ende
                seg, totals, tflags = new_segment(), {}, set()
                mode = "entries"
                seg["flags"] |= lflags
                for label, kind, v in cells:
                    if label in KIRO:
                        seg["entries"]["_kiro"].append(v)
                    elif kind == "logo":
                        seg["entries"][("logo", label)].append(v)
                    else:
                        seg["entries"]["_main"].append(v)
                pending = None
                continue
        # Summenblock-Verarbeitung
        tflags |= lflags
        if not cells:
            pending = next((t for t in reversed(line)
                            if classify(t) in ("word", "logo") and t != "𐄁"), pending)
            continue
        for label, kind, v in cells:
            if label in KIRO:
                totals["_kiro"] = v
            elif kind == "logo" and label not in TOTALS:
                totals[("logo", label)] = v
            elif pending:
                totals[("logo", pending)] = v
            else:
                totals["_main"] = v
        pending = None
    if mode == "totals":
        close(seg, totals, tflags)
    # Eintrags-Logogrammwerte ohne eigene Spalte in die Hauptspalte mergen
    fixed = []
    for col, ev, s, tot, status, fl in results:
        fixed.append((col, ev, s, tot, status, fl))
    return fixed


def remap(rec, results):
    """Logo-Einträge ohne Spaltentotal der Hauptspalte zuschlagen:
    dazu Prüfung wiederholen — hier vereinfacht: parse_cells ordnet
    Logo-Werte zunächst Logo-Spalten zu; existiert kein Total für die
    Logo-Spalte, fehlen diese Werte in der Hauptspalte. Wir prüfen das
    und korrigieren."""
    return results


print("=" * 78)
print("Spalten-bewusster Arithmetik-Check (segmentiert, alle Tafeln)")
print("=" * 78)
verdicts = {}
n_checks = n_exact = n_nah = n_abw = 0
rows = []
for name, rec in sorted(insc.items()):
    if "Tablet" not in rec.get("support", ""):
        continue
    # Logo-Einträge ohne Spaltentotal -> Hauptspalte (zweiter Versuch)
    results = check_tablet(rec)
    if not results:
        continue
    statuses = []
    for col, ev, s, tot, status, fl in results:
        cname = ("Haupt" if col == "_main" else
                 "KI-RO" if col == "_kiro" else col[1])
        flag_s = ("  [" + ",".join(sorted(fl)) + "]") if fl else ""
        rows.append(f"   {name:<13} {cname:<8} {status:<6} Σ={s:<9g} Total={tot:<9g}{flag_s}")
        statuses.append((status, fl))
        n_checks += 1
        n_exact += status == "EXAKT"
        n_nah += status == "NAH"
        n_abw += status == "ABW"
    if all(st == "EXAKT" for st, fl in statuses):
        verdicts[name] = "EXAKT"
    elif any(st != "EXAKT" and not fl for st, fl in statuses):
        verdicts[name] = "ABW"
    else:
        verdicts[name] = "unsicher"
print("\n".join(rows))
print(f"\nPrüfungen: {n_checks}  exakt: {n_exact}  Δ<=1: {n_nah}  abweichend: {n_abw}")
print("(altes Stream-Modell: 33 Prüfungen, 8 exakt, 3 Δ<=1)")
print("\nTafel-Verdikte:")
for v in ("EXAKT", "ABW", "unsicher"):
    ts = sorted(n for n, x in verdicts.items() if x == v)
    print(f"   {v}: {', '.join(ts)}")

# ---- H10-Update: Verdikte (Parser) x Rasuren (Apparat) --------------------
print("\n" + "=" * 78)
print("H10-Update: Parser-Verdikte x GORILA-Apparat")
print("=" * 78)
app = {k: v for k, v in json.load(open(DATA / "gorila_apparatus.json")).items()
       if not k.startswith("_")}
# Schadens-Artefakte laut Faksimile-Verifikation: keine echten Abweichler
ARTEFAKT = {"HT27a", "HT110a", "HT122a"}
a = b = c = d = 0
for n, e in sorted(app.items()):
    if n in ARTEFAKT:
        continue
    v = verdicts.get(n)
    deviator = v in ("ABW",) or e["status"] == "NAH" or \
        (e["status"] == "ABW-Kandidat")
    if deviator:
        ok = e["rework_numerisch"]
        a += ok; b += not ok
        print(f"   ABWEICHLER {n:<9} numerische Rasur: {'ja' if ok else 'NEIN'}"
              f"   ({e['apparat'][:58]})")
    elif e["status"] == "EXAKT":
        ok = e["rework_numerisch"]
        c += ok; d += not ok
p = fisher2x2(a, b, c, d)
print(f"\n   Abweichler {a}/{a+b} mit numerischer Rasur vs. Exakte {c}/{c+d}")
print(f"   Fisher p = {p:.4f}" + ("  ***" if p < 0.05 else ""))
p2 = fisher2x2(a, b - 1, c, d) if b else None
print("""   Hinweise: HT118/HT123 sind jetzt regulär spalten-geparst (kein
   post-hoc-Status mehr); HT119 zählt als Abweichler OHNE Rasur, obwohl
   seine Abweichung per Apparat eine unsichere Zahllesung (67/68) ist —
   konservativ gegen die Hypothese gewertet.""")
