# Manuskript-Gerüst (Arbeitsstand 11.06.2026)

## Arbeitstitel
**"Erasures, not errors: arithmetic discrepancies in Linear A
accounting tablets track scribal corrections"**

Alternativ: "Version history in Minoan bookkeeping: machine-checked
arithmetic and the erasure record of the Haghia Triada tablets"

## Zieljournal
1. **Kadmos** (Zeitschrift für vor- und frühgriechische Epigraphik) —
   natürliche Heimat; dort erschienen Bennett 1980, Facchetti 2013,
   Cash & Cash 2011.
2. Alternativen: SMEA NS (Studi Micenei ed Egeo-Anatolici);
   Journal of Archaeological Science (falls Methodik-lastig
   aufgezogen — dort Corazza et al. 2021).

## Abstract (Entwurf, EN, ~190 Wörter)
> The arithmetic of the Linear A accounting tablets has been checked
> tablet by tablet since GORILA, and discrepancies between entries
> and totals are conventionally attributed to scribal incompetence
> (most recently Montecchi 2019). We re-examine the question
> computationally: a column-aware parser validates 28 summation
> checks across the corpus (10 exact, including multi-column ledgers
> such as HT 123). Cross-referencing the results with the critical
> apparatus of GORILA I reveals a sharp pattern: all genuinely
> deviating tablets carry erasures or corrections in their numeral
> lines, while exactly-summing tablets carry none (Fisher's exact
> test, p = 0.003). Montecchi's independently compiled palimpsest
> list shows the same tendency (p = 0.077). We conclude that the
> "calculation errors" of Linear A are residues of incomplete
> document updates — evidence of actively maintained records rather
> than unprofessional scribes. Corollaries include a value-independent
> proof that HT 13's discrepancy is real (2J = J), and minimal-
> assumption column constraints on HT 123 that bear on the disputed
> fraction values (H = X + ¼ under stated readings, favouring the
> classical H = 1/3 branch over the tentative H = 1/16). Six
> pre-registered predictions, including for the unpublished Knossos
> ivory sceptre (KN Zg 57–58), make the claims falsifiable.

## Gliederung mit Evidenz-Verweisen

1. **Einleitung** — Linear A als gelesene, nicht verstandene Schrift;
   KU-RO/KI-RO-Buchhaltung; die Dilettantismus-These (Montecchi 2019,
   92-93; Tomas 2014) und ihre Reichweite.
2. **Daten & Methoden** — lineara.xyz-Extrakt (mit dokumentierten
   Korrekturen: Support-Audit, Klasma-Kodierung); spalten-bewusster
   Parser (`check_arithmetic.py`); Faksimile-Verifikation aller
   kritischen Lesungen an GORILA I; Apparat-Mining-Protokoll
   (`data/gorila_apparatus.json`); Reproduzierbarkeit (Git-Historie,
   registrierte Vorhersagen).
3. **Ergebnis 1: Die Arithmetik stimmt** — 28 Spaltenprüfungen,
   10 exakt (Liste); Mehrspalten-Struktur von HT 123 (OLIV exakt)
   und HT 118 (KI-Spalte exakt; KI=KI-RO nach Raison & Pope 1978,
   bestätigt durch Younger „the numbers add up").
4. **Ergebnis 2: Die Abweichungen korrelieren mit Rasuren** —
   T1/T2-Tests (5/6 vs. 0/8, p=0,003); Einzelevidenz: HT 9a
   („| ajouté après ⅍"), HT 13 (Zeilen 4-7 über Rasur; wertunabhängig
   unerfüllbar), HT 94a (⟦"⟧ getilgte Einerstriche), HT 102 (Zehner
   über Rasur + GORILAs „fraction … ne soit pas reprise dans le
   total"), HT 118 (Komplett-Palimpsest); Out-of-sample-Schritt
   (P-VI, Blind-Klassifikation); unabhängige Validierung über
   Montecchis Palimpsest-Liste (3/7 vs. 0/8).
5. **Diskussion: Updates statt Unvermögen** — Antithese zu
   „scarsa professionalità"; lebende Dokumente / zeitliche Tiefe der
   Verwaltung; Anschluss an Palimpsest-Deutungen (Montecchi 219-220,
   Schoep 2002, Consani 1996, Tomas 2017); was das für die
   Interpretation der „Fehler-Tafeln" als Buchungsstadien bedeutet.
6. **Korollar: Bruchwert-Constraints aus HT 123** — reine
   Spaltensummen statt Ratio-Modellen; H = X + ¼ (konditioniert auf
   GORILA/Montecchi-Lesungen, inkl. der autoptischen X-Bestätigung
   Montecchi 2019, 147); Stellung zur offenen Alternative H=1/3
   (Montecchi 2019, 148; Schrijver 2014) vs. H=1/16(?) (Corazza et
   al. 2021) — die Spannung innerhalb derselben Forschungsgruppe;
   ABGRENZUNG zu Cash & Cash 2011 (vor Einreichung lesen!).
7. **Registrierte Vorhersagen** — P-I bis P-VI mit Git-Zeitstempeln;
   insbesondere P-III (Zg 58 als Schiedsrichter der H-Frage).
8. **Grenzen** — N=15 prüfbare Tafeln; T2-Kriterium post hoc
   verfeinert (offen deklariert, zweifach extern validiert);
   Lesungsabhängigkeiten (X=7/4 nur unter lineara/GORILA-Lesung der
   KI-RO-Spalte; Montecchi autoptisch „2̣ X̣"); Apparat-Mining manuell
   (Nachprüfung via SigLA wünschenswert).

## Tabellen/Abbildungen
- T1: Alle 15 Tafeln × Arithmetik-Status × Apparat-Befund (aus
  `erasures_results.txt` + `arithmetic_results.txt`)
- T2: H-Wert-Vorschläge der Literatur vs. Spaltenconstraint
- F1: HT 123a Spaltenstruktur (Schema, keine GORILA-Reproduktion —
  Bildrechte!)
- F2: HT 94a Zeile .1 (nur falls Bildrechte geklärt; sonst Schema)

## Vor Einreichung zwingend
- [ ] Cash & Cash 2011 (Kadmos 50) lesen — Abgrenzung Kap. 6
- [ ] Montecchi 2009 im Original (Fn. 387/553 zitieren korrekt)
- [ ] Tomas 2014 / 2017a einsehen (Dilettantismus-Kontext, Kap. 1/5)
- [ ] Bildrechte: KEINE GORILA-Faksimiles reproduzieren; eigene
      Schemata zeichnen
- [ ] KI-Nutzung offenlegen (Journal-Policy prüfen; Formulierung:
      Analysen mit Unterstützung von Anthropic Fable 5, alle
      Lesungen am Original verifiziert, Verantwortung beim Autor)
- [ ] Muttersprachliche Endredaktion (EN)
- [ ] Repo-DOI (Zenodo) für Zitierbarkeit der Daten/Skripte
