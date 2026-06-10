#!/usr/bin/env python3
"""Empirische Tests der Hypothesen H1-H4 aus ANSATZ.md (Abschnitt 4).

H1  -SI ~ -TI in der Libationsformel ist grammatische Opposition:
    Varianten verschiedener Formel-Slots müssten kovariieren (Kongruenz).
H2  J- vor Vokal ist Proklitikon: J-Formen meiden die Textanfangs-
    position, A-/Grundformen nicht.
H3  SA-RA2 ist Funktionswort der Zuteilung, kein Personenname:
    Distributionsprofil (Logogramm-Folge, Mengenhöhe) muss sich vom
    Personennamen-Pool unterscheiden.
H4  -E am Wortende ist Kopfzeilen-/Empfänger-Suffix: -E-Formen stehen
    überzufällig VOR der ersten Zahl (Header) statt im Listenkörper.

Statistik: exakter Fisher-Test (zweiseitig). Kleine N werden ehrlich
als 'nicht entscheidbar' ausgewiesen.
"""
from collections import Counter, defaultdict
from corpus_lib import (classify, fisher2x2, is_word, load_inscriptions,
                        parse_number, vowel_of, word_signs)

insc = load_inscriptions()


def verdict(p, n_note=""):
    if p < 0.05:  return f"SIGNIFIKANT (p={p:.3f}){n_note}"
    if p < 0.15:  return f"Tendenz, nicht signifikant (p={p:.3f}){n_note}"
    return f"nicht entscheidbar (p={p:.2f}){n_note}"


def doc_words(rec):
    toks = rec.get("transliteratedWords", [])
    return toks, [(i, t) for i, t in enumerate(toks) if classify(t) == "word"]


# ===========================================================================
print("=" * 78)
print("H1 — Slot-Kongruenz in der Libationsformel (-SI ~ -TI usw.)")
print("=" * 78)
MARKERS = ("TA-I-*301", "SA-SA-RA", "SA-RA-ME", "U-NA-", "I-PI-NA", "SI-RU")
lib_docs = {}
for name, rec in insc.items():
    seq = [t for _, t in doc_words(rec)[1]]
    if any(m in w for w in seq for m in MARKERS):
        lib_docs[name] = (rec, seq)

def slot_variant(seq):
    s = {}
    for w in seq:
        if "TA-I-*301" in w:
            s["S1_anruf"] = ("JA" if w.endswith("WA-JA") else
                             "E" if w.endswith("WA-E") else
                             "UJA" if w.endswith("U-JA") else "var:" + w.split("-")[-1])
        elif "SA-SA-RA" in w or w.endswith("SA-RA-ME"):
            s["S2_asasarame"] = word_signs(w)[0]      # JA / A / SA (Prafix)
        elif w.startswith("U-NA"):
            v = word_signs(w)[-1]                     # SI / TI
            if v in ("SI", "TI"):                     # TLZa1 'U-NA-KA-NA' ist
                s["S3_unakanasi"] = v                 # Segmentierungs-Krux -> raus
        elif w.startswith("I-PI-NA"):
            s["S4_ipinama"] = "MA" if w.endswith("MA") else "MINA" if w.endswith("MI-NA") else word_signs(w)[-1]
        elif w.startswith("SI-RU"):
            s["S5_sirute"] = w
    return s

table = {}
for name, (rec, seq) in sorted(lib_docs.items()):
    sv = slot_variant(seq)
    if sv:
        table[name] = (rec.get("site", "?"), rec.get("support", "?"), sv)

print(f"{'Doc':<9} {'Ort':<13} {'S1':<5} {'S2':<4} {'S3':<4} {'S4':<5}")
for name, (site, sup, sv) in table.items():
    if len(sv) >= 2:
        print(f"{name:<9} {site[:12]:<13} {sv.get('S1_anruf','—'):<5} "
              f"{sv.get('S2_asasarame','—'):<4} {sv.get('S3_unakanasi','—'):<4} "
              f"{sv.get('S4_ipinama','—'):<5}")

# Kongruenz-Paare: S3(SI/TI) x S4(MA/MINA) und S3 x S1(JA/E)
def pairs(slot_a, slot_b, val_a, val_b):
    a = b = c = d = 0
    for _, (_, _, sv) in table.items():
        if slot_a in sv and slot_b in sv:
            x, y = sv[slot_a] == val_a, sv[slot_b] == val_b
            if x and y: a += 1
            elif x and not y: b += 1
            elif not x and y: c += 1
            else: d += 1
    return a, b, c, d

print("\nKongruenz-Test S3 x S4  (SI<->MA gegen TI<->MI-NA):")
a, b, c, d = pairs("S3_unakanasi", "S4_ipinama", "SI", "MA")
p1 = fisher2x2(a, b, c, d)
print(f"   SI&MA={a}  SI&MINA={b}  TI&MA={c}  TI&MINA={d}   -> {verdict(p1, f', N={a+b+c+d}')}")

print("Kongruenz-Test S3 x S1  (SI<->WA-JA gegen TI<->WA-E):")
a, b, c, d = pairs("S3_unakanasi", "S1_anruf", "SI", "JA")
p2 = fisher2x2(a, b, c, d)
print(f"   SI&JA={a}  SI&E={b}  TI&JA={c}  TI&E={d}   -> {verdict(p2, f', N={a+b+c+d}')}")

print("Kongruenz-Test S1 x S2  (WA-JA<->JA- gegen WA-E<->A-/SA-):")
a, b, c, d = pairs("S1_anruf", "S2_asasarame", "JA", "JA")
p3 = fisher2x2(a, b, c, d)
print(f"   JA&JA={a}  JA&¬JA={b}  E&JA={c}  E&¬JA={d}   -> {verdict(p3, f', N={a+b+c+d}')}")

# ===========================================================================
print()
print("=" * 78)
print("H2 — J-Präfix meidet die Textanfangsposition (Proklitikon-These)")
print("=" * 78)
# Alternationspaare (JA-X ~ A-X oder JA-X ~ X) im Korpus
all_words = Counter()
for name, rec in insc.items():
    for _, w in doc_words(rec)[1]:
        all_words[w] += 1
wset = set(all_words)
pairs_ja = []
for w in sorted(wset):
    s = word_signs(w)
    if s[0] == "JA" and len(s) >= 3:
        tail = "-".join(s[1:])
        for cand in ("A-" + tail, tail):
            if cand in wset:
                pairs_ja.append((w, cand))
print("Alternationspaare im Korpus:")
for j, a in pairs_ja:
    print(f"   {j:<22} ~ {a}   ({all_words[j]}x / {all_words[a]}x)")

def initial_counts(target_words, support=None):
    """'textinitial' = erstes Wort des erhaltenen Texts. Achtung: bei
    Steinfragmenten ist der echte Anfang oft verloren — Tafeln sind die
    verlässlichere Stichprobe (support='Tablet')."""
    ini = non = 0
    examples = []
    for name, rec in insc.items():
        if support and support not in rec.get("support", ""):
            continue
        toks, ws = doc_words(rec)
        for k, (_, w) in enumerate(ws):
            if w in target_words:
                if k == 0:
                    ini += 1; examples.append((name, w))
                else:
                    non += 1
    return ini, non, examples

jset = {j for j, _ in pairs_ja}
aset = {a for _, a in pairs_ja}
ji, jn, jex = initial_counts(jset)
ai, an, aex = initial_counts(aset)
p = fisher2x2(ji, jn, ai, an)
print(f"\nPaar-Test:  J-Formen textinitial {ji}/{ji+jn}   Gegenformen textinitial {ai}/{ai+an}")
print(f"   -> {verdict(p, f', N={ji+jn+ai+an}')}")
if jex: print("   J-initial-Belege:", ", ".join(f"{n}:{w}" for n, w in jex[:6]))
if aex: print("   Gegenform-initial-Belege:", ", ".join(f"{n}:{w}" for n, w in aex[:6]))

# breiter (alle JA-… vs alle A-…-Wörter), stratifiziert:
# Tafeln haben i.d.R. einen erhaltenen Anfang, Steinfragmente nicht.
jall = {w for w in wset if word_signs(w)[0] == "JA"}
aall = {w for w in wset if word_signs(w)[0] == "A"}
for label, sup in (("alle Dokumente", None), ("nur Tafeln (Anfang erhalten)", "Tablet")):
    ji2, jn2, jex2 = initial_counts(jall, sup)
    ai2, an2, _ = initial_counts(aall, sup)
    p_broad = fisher2x2(ji2, jn2, ai2, an2)
    print(f"\nAlle JA-Wörter vs. alle A-Wörter — {label}:")
    print(f"   JA- textinitial {ji2}/{ji2+jn2} = {ji2/(ji2+jn2):.0%}   "
          f"A- textinitial {ai2}/{ai2+an2} = {ai2/(ai2+an2):.0%}   -> {verdict(p_broad)}")
    if sup and jex2:
        print("   JA-tafelinitial-Belege:", ", ".join(f"{n}:{w}" for n, w in jex2[:8]))

# ===========================================================================
print()
print("=" * 78)
print("H3 — SA-RA2: Funktionswort oder Personenname? (Distributionsprofil)")
print("=" * 78)
SARA2 = "SA-RA₂"
LOGO_COMMODITY = {"GRA", "VIN", "OLE", "OLIV", "FIC", "NI", "CYP", "TE+RO", "AROM", "FAR"}

def entry_profile(target, site="Haghia Triada"):
    """per occurrence: does a commodity logogram stand between word and its
    number, and how large is the number?"""
    n = ini = logo = 0
    qtys = []
    for name, rec in insc.items():
        if site and rec.get("site") != site:
            continue
        toks, ws = doc_words(rec)
        wpos = {i: k for k, (i, _) in enumerate(ws)}
        for k, (i, w) in enumerate(ws):
            if w != target:
                continue
            n += 1
            if k == 0:
                ini += 1
            saw_logo, qty, j = False, None, i + 1
            while j < len(toks):
                c = classify(toks[j])
                if c == "word":
                    break
                if c == "logo":
                    saw_logo = saw_logo or any(toks[j].startswith(l) for l in LOGO_COMMODITY)
                if c == "num":
                    qty = parse_number(toks[j])
                    while j + 1 < len(toks) and (nv := parse_number(toks[j + 1])) is not None:
                        j += 1; qty += nv
                    break
                j += 1
            if saw_logo: logo += 1
            if qty is not None: qtys.append(float(qty))
    return n, ini, logo, qtys

def fmt_profile(word, prof):
    n, ini, logo, qtys = prof
    med = sorted(qtys)[len(qtys) // 2] if qtys else float("nan")
    big = sum(1 for q in qtys if q >= 5)
    return (f"   {word:<12} n={n:<3} initial={ini/n:4.0%}  Logogramm-vor-Zahl={logo/n:4.0%}  "
            f"medianMenge={med:5.1f}  Mengen>=5: {big}/{len(qtys)}")

prof_sara = entry_profile(SARA2)
prof_kuro = entry_profile("KU-RO")
prof_kiro = entry_profile("KI-RO")
print("Profil (nur Haghia Triada):")
print(fmt_profile(SARA2, prof_sara))
print(fmt_profile("KU-RO", prof_kuro))
print(fmt_profile("KI-RO", prof_kiro))

# Personennamen-Pool: häufige HT-Wörter, nicht Funktionswörter
ht_words = Counter()
for name, rec in insc.items():
    if rec.get("site") == "Haghia Triada":
        for _, w in doc_words(rec)[1]:
            ht_words[w] += 1
FUNC = {SARA2, "KU-RO", "KI-RO", "PO-TO-KU-RO"}
name_pool = [w for w, c in ht_words.items() if c >= 4 and w not in FUNC]
pool_prof = [0, 0, 0, []]
print(f"\nVergleichspool (HT-Wörter mit n>=4, mutmaßl. Namen): {', '.join(name_pool)}")
for w in name_pool:
    n, ini, logo, qtys = entry_profile(w)
    pool_prof[0] += n; pool_prof[1] += ini; pool_prof[2] += logo; pool_prof[3] += qtys
print(fmt_profile("POOL", pool_prof))

# Tests: Logogramm-vor-Zahl und Mengen>=5, SA-RA2 vs Pool
a, b = prof_sara[2], prof_sara[0] - prof_sara[2]
c, d = pool_prof[2], pool_prof[0] - pool_prof[2]
p_logo = fisher2x2(a, b, c, d)
big_s = sum(1 for q in prof_sara[3] if q >= 5)
big_p = sum(1 for q in pool_prof[3] if q >= 5)
p_qty = fisher2x2(big_s, len(prof_sara[3]) - big_s, big_p, len(pool_prof[3]) - big_p)
print(f"\nTest 'Warenlogogramm zwischen Wort und Zahl': SA-RA2 {a}/{a+b} vs. Pool {c}/{c+d}")
print(f"   -> {verdict(p_logo)}")
print(f"Test 'Menge >= 5': SA-RA2 {big_s}/{len(prof_sara[3])} vs. Pool {big_p}/{len(pool_prof[3])}")
print(f"   -> {verdict(p_qty)}")

# ===========================================================================
print()
print("=" * 78)
print("H4 — Wortfinales -E gehäuft in Kopfzeilen (vor der ersten Zahl)?")
print("=" * 78)
he = ho = be = bo = 0     # header-E, header-other, body-E, body-other
header_e_examples = Counter()
for name, rec in insc.items():
    if "Tablet" not in rec.get("support", ""):
        continue
    toks, ws = doc_words(rec)
    first_num = next((i for i, t in enumerate(toks) if classify(t) == "num"), None)
    if first_num is None or not ws:
        continue
    for i, w in ws:
        is_e = vowel_of(word_signs(w)[-1]) == "E"
        if i < first_num:
            if is_e: he += 1; header_e_examples[w] += 1
            else: ho += 1
        else:
            if is_e: be += 1
            else: bo += 1
p_h4 = fisher2x2(he, ho, be, bo)
print(f"Tafeln: Header-Wörter (vor erster Zahl): {he+ho}, davon -E: {he} = {he/(he+ho):.0%}")
print(f"        Listenkörper-Wörter:             {be+bo}, davon -E: {be} = {be/(be+bo):.0%}")
print(f"   -> {verdict(p_h4)}")
print("   häufigste -E-Header-Wörter:",
      ", ".join(f"{w}({c})" for w, c in header_e_examples.most_common(8)))
