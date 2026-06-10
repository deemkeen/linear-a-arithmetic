# Phase 2 — Veröffentlichungsplan & Entwürfe (11.06.2026)

Reihenfolge (Abhängigkeiten beachten):
1. Repo publizieren (→ erst dann haben Issue, Mail, Thread einen Link)
2. Upstream-Issue an mwenge/lineara.xyz
3. Autoren-Mail an die Bologna-Gruppe
4. Twitter-Thread (v2)
5. Manuskript ausarbeiten (MANUSKRIPT.md), Preprint, Einreichung

---

## 1. Repo-Veröffentlichung — Checkliste

- [ ] **Lizenz:** MIT für unseren Code (LICENSE liegt bei).
- [ ] **Daten-Attribution:** lineara.xyz hat KEINE Lizenz; die
      Transkriptions-*Daten* (Zeichenfolgen = Fakten) sind nach
      h. M. nur dünn schutzfähig, aber: prominenter Hinweis in
      README („extracted from mwenge/lineara.xyz, based on GORILA
      and J. Younger's transcriptions; will be removed on request"),
      plus Regenerations-Weg (`git clone … && node extract.js`).
- [ ] **Nicht publizieren:** corpus-src/ (ignoriert ✓), papers_*
      (ignoriert ✓). ENTSCHEIDUNG NÖTIG: `papers_KNZg57_Ariadne.pdf`
      ist seit Commit 1 in der Historie (Open-Access-Artikel der
      Univ. Kreta — vertretbar; alternativ Historie neu aufsetzen).
- [ ] **data/gorila_apparatus.json:** eigene Forschungsdaten
      (Apparat-Exzerpte paraphrasiert, Seitenzitate) — ok.
- [ ] Repo-Name-Vorschlag: `linear-a-arithmetic` oder
      `linear-a-decipherment-toolkit`; public; danach Zenodo-DOI.

## 2. Upstream-Issue-Entwurf (mwenge/lineara.xyz)

> **Title:** Data-quality findings from a systematic arithmetic
> audit (support fields, fraction signs, silent disambiguations)
>
> Hi — I've been running corpus-wide arithmetic checks on your
> dataset (great resource, thank you!). Along the way I found some
> systematic data issues you may want to fix:
>
> 1. **All 44 plain-numbered ZA tablets (ZA 1–ZA 33) are labelled
>    `"support": "Stone vessel"`** — they are clay tablets (GORILA
>    III). Same pattern for a few others (PH 10/25 "Label" → Tablet;
>    HT Wd 1617/1663, PH Wg 45, SAM We 4 "Tablet" → nodules). I can
>    open a PR with a corrections file (53 entries, derived from the
>    GORILA series system, conservatively bucket-level only).
> 2. **Fraction signs are encoded lossily:** A711 "X" renders as
>    ".3", A701/A706 both as "≈ ¹⁄₆". On HT 123a the SA-RU *308
>    entry is encoded A701 where GORILA's drawing (and Montecchi's
>    2019 autopsy) show A711 X.
> 3. **Silent disambiguations vs GORILA:** HT 9a total "31 ¾"
>    (GORILA: 31 ⅍ with scribal insertion noted); HT 13 RE-ZA
>    "5 ½" (GORILA: "5[]J"); HT 119 entry 67 (GORILA: 68);
>    HT 27a total 335 (GORILA word list: 355).
>
> Happy to share the audit scripts / open PRs for any of these.

## 3. Autoren-Mail-Entwurf (B. Montecchi / S. Ferrara, Bologna)

> Subject: HT 123 column arithmetic and the value of fraction sign H
> — a question arising from your 2019/2021 publications
>
> Dear Dr. Montecchi, dear Prof. Ferrara,
>
> I have been running machine-checked arithmetic over the Linear A
> corpus (column-aware summation checks, verified against GORILA I
> facsimiles; repository: [LINK]). Two results touch your work
> directly, and I would value your judgement:
>
> 1. Cross-referencing summation results with GORILA's apparatus
> shows that all genuinely deviating tablets carry erasures in their
> numeral lines, while exactly-summing ones do not (p ≈ 0.003;
> your palimpsest list in Contare a Haghia Triada independently
> shows the same tendency). This seems to favour reading the
> "calculation errors" as residues of document updates rather than
> as scribal incompetence — I would be very interested in your view.
>
> 2. The pure column-sum of HT 123a's *308 column gives
> H = (SA-RU entry sign) + 1/4 — hence H ≥ 1/4, compatible with the
> classical H = 1/3 you discuss as a live option in 2019, but not
> with the tentative H = 1/16 of Corazza et al. 2021. Was HT 123
> excluded there solely on the Montecchi 2009 reading concerns, and
> would the exact OLIV control column (31+31½+16+15 = 93½) change
> that assessment?
>
> I would also be grateful for PDFs of Cash & Cash 2011 and your
> 2009 article, which I have not been able to access.
>
> With best regards, [NAME]
> (Analyses performed with AI assistance — Anthropic's Fable 5 —
> all critical readings verified against the GORILA facsimiles.)

## 4. Twitter-Thread v2 — Korrekturen gegenüber v1

- Post 5/6 (Bruchwerte) ERSETZEN durch:
  > 5/ Result 1: Tablet HT 123 is a multi-column ledger. Its olive
  > column sums EXACTLY (31+31½+16+15 = 93½) — the entries are
  > complete. The fraction column then forces: H = entry-sign + 1/4.
  > So H ≥ 1/4 — the recent tentative H = 1/16 cannot be right.
  >
  > 6/ Funny twist: H = 1/3 — the value our constraint favours — is
  > the CLASSICAL assignment (Bennett 1950), still listed as a live
  > option in 2019… by a co-author of the 2021 study that went with
  > 1/16. Old school might win this one. The unpublished Knossos
  > sceptre will referee (pre-registered).
- Post 8 ergänzen (Montecchi-Kontrast):
  > 8/ … The standard view called Minoan bookkeepers unprofessional
  > (30% of tablets have erasures — taken as sloppiness). The
  > correlation flips the reading: corrections sit exactly where
  > ledgers were UPDATED. Version history, not incompetence.
- Post 10: Repo-Link ergänzen, "repo to follow" streichen.

## 5. Offene Entscheidungen (Nutzer)

- [ ] Repo public? Name? (dann: `gh repo create` + Push durch mich)
- [ ] Zenodo-Verknüpfung (DOI) — nach erstem Push
- [ ] Issue posten (Text oben) — durch dich oder mich (nach Freigabe)
- [ ] Mail versenden (Text oben, [NAME]/[LINK] einsetzen)
- [ ] Thread posten — erst nach Repo-Publikation
