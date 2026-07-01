# Linear A — Computational Arithmetic & Decipherment Toolkit

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21115703.svg)](https://doi.org/10.5281/zenodo.21115703)

> **Cite as:** Gurdzhi, D. F. (2026). *Erasures, not errors: machine-checked
> arithmetic and the correction record of the Linear A accounting tablets.*
> Zenodo. https://doi.org/10.5281/zenodo.21115703

Machine-checked arithmetic, hypothesis testing, and apparatus mining
over the Linear A corpus (GORILA / J. Younger, via
[lineara.xyz](https://github.com/mwenge/lineara.xyz)).
Working documents are in German; key artefacts are bilingual.

## Key findings (June 2026)

1. **Erasures, not errors.** Cross-referencing column-aware summation
   checks (28 checks corpus-wide, 10 exact) with the critical
   apparatus of GORILA I shows that all genuinely deviating tablets
   carry erasures/corrections in their *numeral lines*, while
   exactly-summing tablets carry none (Fisher's exact, **p = 0.003**;
   independently supported by Montecchi's 2019 palimpsest list,
   p = 0.077). The "calculation errors" of Linear A look like
   residues of document *updates* — actively maintained records, not
   unprofessional scribes.
2. **HT 13's famous discrepancy is value-independent:** the equation
   reduces to 2J = J — unsatisfiable for any value of the ½-sign.
3. **HT 123 column constraints bear on the disputed fraction
   values:** the exactly-summing olive column validates the ledger;
   the *308 column then forces H = (entry sign) + ¼, hence **H ≥ ¼**
   — compatible with the classical H = 1/3 (Bennett 1950; a live
   option in Montecchi 2019) but not with the tentative H = 1/16 of
   Corazza et al. 2021. Readings are explicitly conditioned (see
   `LITERATUR.md`).
4. **Six pre-registered, falsifiable predictions** — including for
   the unpublished Knossos ivory sceptre (KN Zg 57–58, Anetaki II) —
   are git-timestamped: see `PREDICTIONS_EN.md` / `PREDICTIONS.md`.
5. **Data-quality fixes for lineara.xyz:** 53 corrected support
   fields (e.g. all 44 plain-numbered ZA tablets mislabelled "Stone
   vessel"), lossy fraction-sign encodings, four silent
   disambiguations vs GORILA (details: `audit_support.py`,
   `LITERATUR.md`).

## Reproduce

```bash
git clone https://github.com/mwenge/lineara.xyz corpus-src
node extract.js               # JS corpus -> data/*.json
python3 analyze.py            # corpus statistics, morphology, anchors
python3 check_arithmetic.py   # column-aware summation checks
python3 test_erasures.py      # H10: erasures x arithmetic
python3 solve_fractions.py    # fraction-value constraints (Max-SAT)
```

All analyses are plain Python 3 (stdlib only). Every critical reading
was verified against the GORILA I facsimiles; apparatus excerpts are
in `data/gorila_apparatus.json` (with book page numbers).

**Data attribution:** `data/*.json` is extracted from
[mwenge/lineara.xyz](https://github.com/mwenge/lineara.xyz), which
transcribes GORILA (Godart/Olivier 1976–85) and John G. Younger's
editions. Reproduced for scholarly purposes with attribution; will be
removed on request of the rights holders. Tablet commentary quoted in
research notes is © John G. Younger. Code: MIT (see LICENSE).

---

## Deutsche Projektdokumentation

- **`ANSATZ.md`** — das Entzifferungs-Konzept: Problemdiagnose,
  Arbeitspakete, alle getesteten Hypothesen (H1–H10) mit Ergebnissen
- **`LITERATUR.md`** — Novitätsprüfung der Kernbefunde mit
  Prior-Art-Dokumentation (Younger, Montecchi, Corazza et al.)
- **`PREDICTIONS.md`** — registrierte Vorhersagen (deutsches Original;
  englische Übersetzung: `PREDICTIONS_EN.md`)
- **`MANUSKRIPT.md`** / **`PHASE2.md`** — Publikationsplanung
- `extract.js` — extrahiert das lineara.xyz-Korpus nach `data/*.json`
- `corpus_lib.py` — gemeinsamer Tokenizer/Parser
- `analyze.py` — Korpusstatistik, Positionsanalyse, Morphologie,
  Libationsformel, Linear-B-Anker (`report_raw.txt`)
- `check_arithmetic.py` — generalisierter, segmentierter
  Spalten-Checker (`arithmetic_results.txt`)
- `test_hypotheses.py` — H1–H4 (`hypotheses_results.txt`)
- `test_e_suffix.py` / `test_o_suffix.py` — H4b/H4c Suffix-Inventare
  (`e_suffix_results.txt`, `o_suffix_results.txt`)
- `test_dialect.py` — H5 KU-RO ~ KU-RA (`dialect_results.txt`)
- `test_kiro_columns.py` — H6-Prototyp Mehrspalten-Arithmetik
  (`kiro_columns_results.txt`)
- `test_te_suffix.py` / `test_ligatures.py` — H7/H8
  (`te_suffix_results.txt`, `ligatures_results.txt`)
- `test_erasures.py` — H10 Rasur-Korrelation via GORILA-Apparat-Mining
  (`data/gorila_apparatus.json`, `erasures_results.txt`)
- `test_lb_names.py` — Anker-Abgleich Linear A ↔ Linear B
  (`lb_names_results.txt`)
- `solve_fractions.py` — H9 Bruchwert-Inferenz inkl. Corazza-Abgleich
  (`fractions_results.txt`)
- `build_lexicon.py` — Wortklassen-Lexikon (`data/lexicon_classes.json`)
- `audit_support.py` — Dokumenttyp-Audit aus der GORILA-Seriensystematik
  (`data/support_corrections.json`, von corpus_lib automatisch angewandt)
- `data/supplements.json` — Neufunde (KN Zg 57–58, Elfenbein-Zepter
  Knossos 2024; Quelle: Ariadne Suppl. 5; `papers_KNZg57_Ariadne.pdf`)
- `corpus-src/` — lokaler Klon von mwenge/lineara.xyz (nicht im Repo)

Bekannte Datenqualitäts-Probleme der Quelle und alle stillen
Glättungen sind in `LITERATUR.md` und den Commit-Messages dokumentiert.
