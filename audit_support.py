#!/usr/bin/env python3
"""Audit der support-Felder gegen die GORILA-Seriensystematik der IDs.

Die GORILA-IDs kodieren den Dokumenttyp: plain Nummer = Tontafel,
Wa/Wb/Wd/We = Noduli, Wc = Roundel, Za = Steingefäß, Zb = Tongefäß,
Zc = Tuschinschrift, Zd = Graffito, Ze = Architektur, Zf = Metall,
Zg = Steinobjekt. Anlass: alle plain-ZA-Tafeln (ZA1-ZA33) waren in
lineara.xyz als 'Stone vessel' geführt.

Korrigiert wird KONSERVATIV: nur wenn die abgeleitete Kategorie in einen
anderen Analyse-Bucket (Verwaltung/Siegel/Stein-Kult/Sonstiges) fällt
als das vorhandene support-Feld. Innerhalb eines Buckets (z.B. Nodule
vs. Sealing) wird nichts angefasst.

Output: data/support_corrections.json  {id: korrigiertes support}
corpus_lib.load_inscriptions() wendet die Korrekturen automatisch an.
"""
import json, re
from collections import Counter
from pathlib import Path

DATA = Path(__file__).parent / "data"
insc = json.load(open(DATA / "inscriptions.json"))

SERIES_SUPPORT = {
    None: "Tablet",
    "Wa": "Nodule", "Wb": "Nodule", "Wd": "Nodule", "We": "Nodule",
    "Wf": "Nodule", "Wg": "Nodule", "Wc": "Roundel",
    "Za": "Stone vessel", "Zb": "Clay vessel", "Zc": "Inked inscription",
    # Zd/Ze/Zf/Zg bewusst NICHT korrigiert: die Serie ist dort gröber als
    # das Material-Feld (KN Zg 57 ist Elfenbein, THE Zg 16 ein Triton —
    # die spezifischen Datensatz-Labels sind korrekt und bleiben)
}


def bucket(supp):
    s = (supp or "").lower()
    if "tablet" in s or "lames" in s or "bar" in s:
        return "Verwaltung"
    if any(k in s for k in ("nodule", "roundel", "sealing", "label")):
        return "Siegel"
    if "stone" in s or "architecture" in s:
        return "Stein-Kult"
    return "Sonstiges"


def derive(name):
    m = re.match(r"^([A-Z]+(?:\(\?\))?)(W[a-z]|Z[a-z])?<?(\d)", name)
    if not m:
        return None, None
    return m.group(2), SERIES_SUPPORT.get(m.group(2))


corrections = {}
mismatch_kinds = Counter()
unparsed = []
for name, rec in insc.items():
    series, derived = derive(name)
    if derived is None:
        if series is None:
            unparsed.append(name)
        continue   # Zd/Ze/Zf/Zg: keine Korrektur (s. o.)
    current = rec.get("support", "")
    if bucket(derived) != bucket(current):
        corrections[name] = derived
        mismatch_kinds[(current or "(leer)", derived)] += 1

print(f"Dokumente: {len(insc)}, nicht parsbare IDs: {len(unparsed)} {unparsed[:8]}")
print(f"Korrekturen (Bucket-Wechsel): {len(corrections)}\n")
print(f"{'support (Datensatz)':<28} {'-> abgeleitet (GORILA-Serie)':<28} {'n':>4}")
for (cur, der), n in mismatch_kinds.most_common():
    print(f"{cur:<28} -> {der:<28} {n:>4}")
print("\nBeispiele:", ", ".join(list(corrections)[:12]))

json.dump(corrections, open(DATA / "support_corrections.json", "w"),
          indent=1, sort_keys=True)
print(f"\ngeschrieben: data/support_corrections.json ({len(corrections)} Einträge)")
