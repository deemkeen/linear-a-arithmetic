# Linear A — Computational Decipherment Toolkit

Reproduzierbare Analyse des Linear-A-Korpus (GORILA / J. Younger, via
[lineara.xyz](https://github.com/mwenge/lineara.xyz)).

- **`ANSATZ.md`** — das Entzifferungs-Konzept: Problemdiagnose, 6 Arbeitspakete,
  falsifizierbare Hypothesen, realistische Erwartungen
- `extract.js` — extrahiert das JS-Korpus nach `data/*.json` (Node)
- `analyze.py` — Analysepipeline: Korpusstatistik, Zeichen-Positionsanalyse,
  KU-RO-Arithmetik-Validierung, Morphologie-Extraktion, Libationsformel,
  Linear-B-Anker
- `test_hypotheses.py` — empirische Tests der Hypothesen H1–H4 aus ANSATZ.md
  (Fisher-Exakt-Tests; Ergebnisse in `hypotheses_results.txt`)
- `test_e_suffix.py` — H4b: Suffix-Inventar-Analyse des wortfinalen -E
  (Permutationstest, Register-Vergleich; Ergebnisse in `e_suffix_results.txt`)
- `test_o_suffix.py` — H4c: gleicher Aufbau für -O, mit
  Funktionswort-Kontrolle (Ergebnisse in `o_suffix_results.txt`)
- `test_dialect.py` — H5: KU-RO ~ KU-RA Dialekt- vs. Grammatik-Test
  (Ergebnisse in `dialect_results.txt`)
- `test_kiro_columns.py` — H6: Mehrspalten-Arithmetik & KI-RO-Komplement
  (Ergebnisse in `kiro_columns_results.txt`)
- `solve_fractions.py` — H9: Klasma-Werte als Max-SAT über
  KU-RO-Constraints (`fractions_results.txt`)
- `test_te_suffix.py` — H7: X ~ X-TE/-NE Alternationspaare und Position
  (`te_suffix_results.txt`)
- `test_ligatures.py` — H8: Akrophonie-Test der Gefäß-Ligaturen gegen HT31
  (`ligatures_results.txt`)
- `build_lexicon.py` — Wortklassen-Lexikon aus Distributionsvektoren
  (`data/lexicon_classes.json`, `lexicon_results.txt`)
- `audit_support.py` — leitet Dokumenttypen aus der GORILA-Seriensystematik
  ab und schreibt `data/support_corrections.json` (wird von corpus_lib
  automatisch angewandt)
- **`PREDICTIONS.md`** — registrierte, zeitgestempelte Vorhersagen für
  Out-of-sample-Tests (v. a. Anetaki II / KN Zg 57–58)

Bekannte Datenqualitäts-Probleme der Quelle: Die plain-ZA-Tafeln
(ZA1–ZA33, Zakros) sind im lineara.xyz-Export fälschlich als
"Stone vessel" geführt (tatsächlich Tontafeln, GORILA III).
- `corpus_lib.py` — gemeinsamer Tokenizer/Parser für beide Skripte
- `report_raw.txt` — Ausgabe des letzten Laufs
- `data/supplements.json` — Neufunde jenseits des lineara.xyz-Standes
  (KN Zg 57–58, Elfenbein-Zepter Knossos 2024; Quelle: Ariadne Suppl. 5)
- `papers_KNZg57_Ariadne.pdf` — Originalpublikation Kanta/Nakassis/Palaima/Perna
- `corpus-src/` — Klon von mwenge/lineara.xyz (1 GB, inkl. Tafel-Fotos)

```bash
node extract.js && python3 analyze.py
```
