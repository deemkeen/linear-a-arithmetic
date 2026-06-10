#!/usr/bin/env python3
"""Linear A — computational decipherment toolkit.

Works on the lineara.xyz corpus export (GORILA / J. Younger transcriptions).
Sections:
  1. corpus overview & the data problem (hapax ratio, Zipf)
  2. sign inventory & positional statistics (syllabary structure)
  3. arithmetic validation of KU-RO / PO-TO-KU-RO ("total")
  4. morphology: stem/affix alternations (prefix vs suffix typology)
  5. libation-formula alignment (the religious parallel corpus)
  6. Linear B anchors (toponyms, shared vocabulary)
"""
import json, math, re
from collections import Counter, defaultdict

from corpus_lib import (DATA, parse_number, is_word, word_signs, classify,
                        vowel_of, load_inscriptions)

insc = load_inscriptions()

# corpus-wide collections ----------------------------------------------------
words = Counter()           # word -> count
word_sites = defaultdict(set)
sign_uni = Counter()        # syllabogram unigrams (within words)
sign_init, sign_fin = Counter(), Counter()
bigrams = Counter()
docs_by_class = Counter()

for name, rec in insc.items():
    docs_by_class[rec.get("support", "?")] += 1
    site = rec.get("site", "?")
    for t in rec.get("transliteratedWords", []):
        if classify(t) == "word":
            words[t] += 1
            word_sites[t].add(site)
            s = word_signs(t)
            sign_uni.update(s)
            sign_init[s[0]] += 1
            sign_fin[s[-1]] += 1
            bigrams.update(zip(s, s[1:]))

print("=" * 78)
print("1. KORPUS-ÜBERBLICK — wie gross ist das Datenproblem?")
print("=" * 78)
n_tok = sum(words.values()); n_typ = len(words)
hapax = sum(1 for w, c in words.items() if c == 1)
print(f"Dokumente gesamt:            {len(insc)}")
for k, v in docs_by_class.most_common(6):
    print(f"   {k:<28} {v}")
print(f"Wort-Tokens (sauber, >=2 Silben): {n_tok}")
print(f"Wort-Typen:                  {n_typ}")
print(f"Hapax legomena:              {hapax}  ({hapax/n_typ:.0%} aller Typen!)")
print(f"Silbenzeichen-Tokens:        {sum(sign_uni.values())}")
print(f"Silbenzeichen-Inventar:      {len(sign_uni)} distinkte Zeichen")
print(f"mittl. Wortlänge:            {sum(sign_uni.values())/n_tok:.2f} Zeichen")

print("\nTop-20 Wörter (Frequenz, #Fundorte):")
for w, c in words.most_common(20):
    print(f"   {w:<22} {c:>4}x   an {len(word_sites[w])} Orten")

# Zipf
print("\nZipf-Profil (Rang -> Frequenz):")
freqs = sorted(words.values(), reverse=True)
for r in (1, 2, 5, 10, 20, 50, 100, 200, 500):
    if r <= len(freqs):
        print(f"   Rang {r:>4}: {freqs[r-1]}")

print()
print("=" * 78)
print("2. SCHRIFTSTRUKTUR — Positionsstatistik der Silbenzeichen")
print("=" * 78)
tot_i, tot_f, tot_u = sum(sign_init.values()), sum(sign_fin.values()), sum(sign_uni.values())
print("Vokal der Silbe   gesamt   wortinitial   wortfinal")
for v in "AEIOU":
    u = sum(c for s, c in sign_uni.items() if vowel_of(s) == v)
    i = sum(c for s, c in sign_init.items() if vowel_of(s) == v)
    f = sum(c for s, c in sign_fin.items() if vowel_of(s) == v)
    print(f"   -{v}            {u/tot_u:5.1%}      {i/tot_i:5.1%}        {f/tot_f:5.1%}")

pure_v = {"A", "I", "U", "E", "O", "JA", "JU", "WA", "WI"}
pv_i = sum(c for s, c in sign_init.items() if s in {"A","I","U","E","O"})
pv_all = sum(c for s, c in sign_uni.items() if s in {"A","I","U","E","O"})
print(f"\nReine Vokalzeichen (A,E,I,O,U): {pv_all/tot_u:.1%} aller Zeichen,"
      f" aber {pv_i/tot_i:.1%} aller WORTANFÄNGE")
print("-> starke Anfangs-Präferenz reiner Vokale = typologisches Merkmal")

print("\nTop-15 wortinitiale vs. wortfinale Zeichen:")
ii = ", ".join(f"{s}({c})" for s, c in sign_init.most_common(15))
ff = ", ".join(f"{s}({c})" for s, c in sign_fin.most_common(15))
print(f"   initial: {ii}")
print(f"   final:   {ff}")

# information: is the language suffixing or prefixing?
def cond_entropy(pairs):
    """H(X|Y) for Counter of (y,x)"""
    tot = sum(pairs.values())
    py = Counter();
    for (y, x), c in pairs.items(): py[y] += c
    h = 0.0
    for (y, x), c in pairs.items():
        p = c / tot
        h -= p * math.log2(c / py[y])
    return h

stem_last = Counter(); stem_first = Counter()
for w, c in words.items():
    s = word_signs(w)
    if len(s) >= 3:
        stem_last[(tuple(s[:-1]), s[-1])] += c   # predict last sign from rest
        stem_first[(tuple(s[1:]), s[0])] += c    # predict first sign from rest
print(f"\nH(letztes Zeichen | Rest)  = {cond_entropy(stem_last):.3f} bit")
print(f"H(erstes Zeichen  | Rest)  = {cond_entropy(stem_first):.3f} bit")
print("-> höherer Wert = mehr Variation an dieser Wortkante (Affix-Position)")

print()
print("=" * 78)
print("3. ARITHMETIK-TEST — KU-RO als 'Summe' (validiert Lesung+Zahlsystem)")
print("=" * 78)
def is_clean(toks):
    """no damage markers / unparseable numerals on the whole tablet"""
    for t in toks:
        if any(ch in t for ch in "[]?•"):
            return False
        if re.fullmatch(r"\.\d+", t.strip()):
            return False
    return True

ok, near, fail, dmg, checked = [], [], [], 0, 0
for name, rec in insc.items():
    toks = rec.get("transliteratedWords", [])
    clean = is_clean(toks)
    acc, i, kuro_vals = [], 0, []
    while i < len(toks):
        t = toks[i]
        if t in ("KU-RO", "PO-TO-KU-RO"):
            j = i + 1
            total = None
            while j < len(toks) and j < i + 6:
                v = parse_number(toks[j])
                if v is not None:
                    total = v
                    while j + 1 < len(toks) and (nv := parse_number(toks[j+1])) is not None:
                        j += 1; total += nv     # split numerals across line breaks
                    break
                if classify(toks[j]) == "word":
                    break
                j += 1
            expect = sum(kuro_vals) if (t == "PO-TO-KU-RO" and kuro_vals) else sum(acc)
            if total is not None and expect > 0:
                checked += 1
                diff = abs(total - expect)
                re_ = (name, t, expect, total)
                if diff == 0: ok.append(re_)
                elif diff <= 1: near.append(re_)
                elif not clean: dmg += 1
                else: fail.append(re_)
            if t == "KU-RO" and total is not None:
                kuro_vals.append(total)
            acc = []
            i = j + 1
            continue
        v = parse_number(t)
        if v is not None:
            run = v
            while i + 1 < len(toks) and (nv := parse_number(toks[i+1])) is not None:
                i += 1; run += nv
            acc.append(run)
        i += 1
print(f"prüfbare Summenformeln: {checked}")
print(f"   exakt richtig:        {len(ok)}  ({len(ok)/checked:.0%})")
print(f"   Abweichung <=1 (Bruchrundung des Schreibers): {len(near)}")
print(f"   auf beschädigten/unvollständigen Tafeln:      {dmg}")
print(f"   echte Abweichung auf intakter Tafel:          {len(fail)}")
print("\nBeispiele exakter Summen:")
for name, t, e, tt in ok[:14]:
    fe = f"{float(e):g}"
    print(f"   {name:<10} Einträge summieren zu {fe:>7}  ->  {t} {float(tt):g}  ✓")
print("\nSchreiber-Rundungsfälle (Evidenz für echte Buchhaltung):")
for name, t, e, tt in near[:6]:
    print(f"   {name:<10} Summe {float(e):g} vs. {t} {float(tt):g}  (Δ={float(abs(tt-e)):g})")

# vowel-vowel co-occurrence across adjacent syllables (harmony / assimilation?)
print("\nVokal-zu-Vokal-Übergänge benachbarter Silben (beob./erwartet):")
vv = Counter(); vtot = Counter()
for (s1, s2), c in bigrams.items():
    v1, v2 = vowel_of(s1), vowel_of(s2)
    if v1 and v2:
        vv[(v1, v2)] += c; vtot[v1] += c
allv = sum(vv.values())
colf = {v: sum(c for (a, b), c in vv.items() if b == v) / allv for v in "AEIOU"}
print("      " + "".join(f"{v:>7}" for v in "AEIOU"))
for v1 in "AEIOU":
    row = []
    for v2 in "AEIOU":
        exp = vtot[v1] * colf[v2]
        o_e = (vv[(v1, v2)] / exp) if exp else 0
        row.append(f"{o_e:7.2f}")
    print(f"   {v1}  " + "".join(row))
print("   (>1 = überrepräsentiert; Diagonale >1 wäre Vokalharmonie-Signal)")

print()
print("=" * 78)
print("4. MORPHOLOGIE — Stamm-Alternationen (was sind die Affixe?)")
print("=" * 78)
wl = [w for w in words if len(word_signs(w)) >= 2]
by_stem = defaultdict(set)
for w in wl:
    s = word_signs(w)
    if len(s) >= 3:
        by_stem[tuple(s[:2])].add(w)

# suffix pairs: same stem (>=2 signs), endings differ
suffix_alt = []
for stem, group in by_stem.items():
    if len(group) >= 2:
        suffix_alt.append((stem, sorted(group)))
suffix_alt.sort(key=lambda x: -len(x[1]))
print("Wortfamilien mit gemeinsamem Stamm (erste 2 Zeichen), >=3 Mitglieder:")
shown = 0
for stem, group in suffix_alt:
    if len(group) >= 3 and shown < 12:
        tot = sum(words[w] for w in group)
        print(f"   {'-'.join(stem):<10} -> {', '.join(group[:6])}{' …' if len(group)>6 else ''}")
        shown += 1

# the famous J-/A- prefix alternation
print("\nPräfix-Alternation (gleiches Wort mit/ohne Anlautwechsel):")
wset = set(wl)
seen = set()
for w in sorted(wset):
    s = word_signs(w)
    if len(s) < 3:
        continue
    tail = "-".join(s[1:])
    for w2 in sorted(wset):
        s2 = word_signs(w2)
        if w2 != w and len(s2) >= 3 and "-".join(s2[1:]) == tail and (w2, w) not in seen:
            seen.add((w, w2))
            print(f"   {w:<24} ~ {w2:<24} (Stamm -{tail})")
            break
    if len(seen) >= 12:
        break

# suffix minimal pairs on full stems
print("\nSuffix-Minimalpaare (identischer Stamm bis aufs letzte Zeichen):")
by_butlast = defaultdict(set)
for w in wl:
    s = word_signs(w)
    if len(s) >= 3:
        by_butlast[tuple(s[:-1])].add(s[-1])
cnt = 0
for stem, ends in sorted(by_butlast.items(), key=lambda kv: -len(kv[1])):
    if len(ends) >= 2 and cnt < 12:
        print(f"   {'-'.join(stem)}-[{'|'.join(sorted(ends))}]")
        cnt += 1
suffix_sign_inventory = Counter()
for stem, ends in by_butlast.items():
    if len(ends) >= 2:
        suffix_sign_inventory.update(ends)
print("\nHäufigste alternierende Endzeichen (Suffix-Kandidaten):")
print("   " + ", ".join(f"{s}({c})" for s, c in suffix_sign_inventory.most_common(12)))

print()
print("=" * 78)
print("5. LIBATIONSFORMEL — der parallele 'religiöse' Mini-Rosetta-Text")
print("=" * 78)
lib_words = ["A-TA-I-*301-WA-JA", "JA-TA-I-*301-U-JA", "A-SA-SA-RA-ME",
             "JA-SA-SA-RA-ME", "U-NA-KA-NA-SI", "U-NA-RU-KA-NA-TI",
             "I-PI-NA-MA", "SI-RU-TE", "TA-NA-RA-TE-U-TI-NU", "I-NA-TA-I-ZU-DI-SI-KA"]
hits = defaultdict(list)
for name, rec in insc.items():
    seq = [t for t in rec.get("transliteratedWords", []) if classify(t) == "word"]
    if any(w in seq for w in lib_words):
        hits[name] = seq
print(f"Inschriften mit Formelwörtern: {len(hits)}  (Steingefässe von {len({insc[n]['site'] for n in hits})} Orten)")
for n in list(hits)[:10]:
    print(f"   {n:<8} ({insc[n]['site'][:18]:<18}): {' / '.join(hits[n][:7])}")

print()
print("=" * 78)
print("6. LINEAR-B-ANKER — Wörter, die in Linear B wieder auftauchen")
print("=" * 78)
ident = json.load(open(DATA / "identicalWordsInLinearB.json"))
print(f"identische Wörter in Linear-B-Texten: {len(ident)}")
print("   " + ", ".join(sorted(ident)[:30]))

print()
print("=" * 78)
print("7. SUPPLEMENTE — Neufunde jenseits des lineara.xyz-Standes")
print("=" * 78)
supp_file = DATA / "supplements.json"
if supp_file.exists():
    supp = json.load(open(supp_file))
    for sid, rec in supp.items():
        print(f"\n{rec['name']}  ({rec['site']})")
        print(f"   Status:  {rec['transcriptionStatus'][:90]}")
        if "signCountTotal" in rec:
            print(f"   Umfang:  {rec['signCountTotal']}")
            print(f"   Zahlen:  {rec['numerals'][:90]}")
        if "type" in rec:
            print(f"   Typ:     {rec['type'][:90]}")
        if "fractionSequence" in rec:
            print(f"   Brüche:  {rec['fractionSequence'][:90]}")
    print("\nHinweis: Diese Dokumente fliessen NICHT in die Statistik der Sektionen")
    print("1-4 ein, solange keine zeichengenaue Edition publiziert ist (Anetaki II).")
