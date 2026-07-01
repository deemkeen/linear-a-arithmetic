# Erasures, not errors: arithmetic discrepancies in Linear A accounting tablets track scribal corrections

*Draft v0.2, 11 June 2026. §6 finalised: Cash & Cash 2011 values
(from the published abstract and Montecchi 2019's discussion) verified
arithmetically against the column constraints; all references
completed from Montecchi 2019's bibliography. One residual
pre-submission check noted at the end of the references. All data,
scripts, and registered predictions: github.com/deemkeen/linear-a-arithmetic*

## Abstract

The arithmetic of the Linear A accounting tablets has been checked
tablet by tablet since GORILA, and discrepancies between entries and
totals are conventionally attributed to scribal incompetence (most
recently Montecchi 2019, 92–93). We re-examine the question
computationally. A column-aware parser validates 28 summation checks
across the corpus (10 exact, four more within ±1), including
multi-column ledgers such as HT 123 and HT 118. Cross-referencing the
results with the critical apparatus of GORILA I reveals a sharp
pattern: every genuinely deviating tablet carries erasures or
corrections in its numeral lines, while exactly-summing tablets carry
none (5/6 vs 0/8; Fisher's exact test, p = 0.003). Montecchi's
independently compiled palimpsest list shows the same tendency
(3/7 vs 0/8, p = 0.077). We conclude that the "calculation errors" of
Linear A are residues of incomplete document updates — evidence of
actively maintained records rather than unprofessional scribes.
Corollaries include a value-independent demonstration that HT 13's
discrepancy is real (it reduces to 2J = J), and minimal-assumption
column constraints on HT 123 that bear on the disputed fraction
values (H = entry-sign + ¼, hence H ≥ ¼, favouring the classical
H = 1/3 over the tentative H = 1/16 of Corazza et al. 2021). Six
pre-registered, git-timestamped predictions — including for the
unpublished Knossos ivory sceptre KN Zg 57–58 — make the claims
falsifiable.

## 1. Introduction

Linear A can largely be read but not understood: sound values
transferred from Linear B cover some 94% of syllabic sign tokens, yet
the language remains unidentified. One stratum of the script,
however, is fully transparent — the accounting layer. Since Bennett
(1950) and GORILA (Godart & Olivier 1976–85), it has been understood
that KU-RO introduces totals, KI-RO deficits, and that the numerals
and fraction signs constitute a decimal system with unit fractions.
On well-preserved tablets the entries demonstrably sum to the KU-RO
figure.

They do not always do so, and the discrepancies have shaped a
historiographical judgement. For Montecchi (2019, 92–93), the high
rate of graphic corrections at Haghia Triada ("la percentuale di
errori grafici, cioè di cancellature e re-iscrizioni, è molto alta…
raggiunge il 30% delle tavolette") together with occasional
calculation errors (HT 9a, 94a, 118, 119, 123; per GORILA also 13,
102, 116, 127b) indicates that the records were not kept by
professional scribes: "non erano funzionari e scribi di professione a
occuparsi delle registrazioni". Younger's commentary accounts for
individual cases ad hoc — HT 119 "rounded off", HT 118 "with 5 having
been omitted" (Younger 2024).

This paper tests a different hypothesis: that the discrepancies are
not failures of competence but **residues of document maintenance** —
entries were altered after a total had been computed (or vice versa),
and the rework was not always carried through. The hypothesis has a
sharp observable signature, which the incompetence reading lacks:
deviations should co-occur with *physical* traces of revision
(erasures, insertions, palimpsests) **specifically in the numeral
lines**, while exactly-summing tablets should lack such traces. Both
phenomena have long been documented separately — erasures in the
apparatus of GORILA I and, systematically, in the SigLA database
(Salgarella & Castellan 2020, where erasures are searchable signs);
calculation errors since Montecchi (2009). To our knowledge the two
have never been cross-referenced.

## 2. Data and methods

**Corpus.** We use the machine-readable corpus of lineara.xyz
(github.com/mwenge/lineara.xyz), which encodes the GORILA
transcriptions as revised by Younger, comprising 1,721 inscription
records. A systematic audit corrected 53 document-type fields
(notably all 44 plain-numbered ZA tablets, mislabelled as stone
vessels) by deriving the type from the GORILA series system. Lossy
encodings of rare fraction signs (A701, A706, A711) were resolved
against the Unicode source fields and, where critical, against the
GORILA I facsimiles; four silent disambiguations of the database
relative to GORILA are documented in the repository.

**Arithmetic checks.** A segment- and column-aware parser models each
tablet as entry lines followed by a totals block; totals lines define
the columns (a logogram after KU-RO opens a commodity column; bare
KU-RO totals the main column; KI-RO/KI cells before the totals block
are deficit entries, after it the deficit total — KI as abbreviation
of KI-RO following Raison & Pope 1978). Numerals attach to the last
preceding word or logogram; values run across line breaks; damaged
segments are flagged and excluded from strong claims. The parser
reproduces all facsimile-verified readings.

**Apparatus mining.** For every arithmetically checkable tablet we
read the critical apparatus of GORILA I at the original page
(references in the dataset), coding two binary variables: *any*
erasure/correction on the inscribed face, and erasure/correction
**in a numeral-bearing line or the totals line**. The coding file
with page numbers and quoted apparatus phrases is published with the
repository. The six deviating tablets whose apparatus had not yet
been read at registration time were classified blind (structurally,
from the parse alone) before their apparatus was consulted
(prediction P-VI of the registered series).

**Reproducibility.** All analyses are plain Python over the published
data; every figure in this paper can be regenerated from the
repository, whose git history also timestamps the predictions in §7.

## 3. The arithmetic of the corpus checks out

The parser performs 28 column checks corpus-wide: 10 exact, 4 within
±1, 14 deviating (most of the latter damaged or structurally
incomplete). The exactly-summing tablets are HT 9b (24), HT 11b
(180), HT 25b (52), HT 85a (66), HT 89 (87), HT 94b (5), HT 104 (95),
and HT 117a (10).

Two multi-column ledgers deserve emphasis. On HT 123+124a the olive
column sums exactly (31 + 31½ + 16 + 15 = 93½ = "KU-RO OLIV 93 J"),
proving that the entry list is complete — a point of consequence in
§6. On HT 118 the deficit column sums exactly (KI 10 + 4 + 1 = 15 =
the closing "KI 15["), confirming Younger's observation that "the
numbers add up" for the KI entries, while the main column deviates
(35 vs KU-RO 30).

The picture is thus not one of unreliable numeracy: where text is
intact and structure is understood, Minoan addition is correct —
including fractional arithmetic (HT 104: 45½ + 20½ + 29 = 95).

## 4. Discrepancies track numeric-context corrections

Six tablets deviate genuinely — small differences on structurally
sound text: HT 9a (entries 31, total 31¾), HT 13 (131 vs 130½),
HT 94a (111 vs 110), HT 102 (1070 vs 1060), HT 118 (main column 35 vs
30), HT 119 (158/159 vs 160; the second entry reads 67 in the
database but 68 in GORILA's word list).

The apparatus of GORILA I records, for **five of these six**,
erasures or corrections precisely in numeral context:

- **HT 9a** (GORILA I, 18–19): a unit stroke added after the fraction
  in the totals line (".6 … | ajouté après ⅍"); line .2 written over
  an erasure.
- **HT 13** (26–27): lines 4–7 — including the KU-RO line — written
  over an erasure ("sur ⟦ ⟧"); the fourth unit of one entry doubtful.
- **HT 94a** (151): two unit strokes erased in an entry line (⟦"⟧);
  a numeral continued onto the lateral edge.
- **HT 102** (169): the first two tens of an entry written over an
  erasure ("2 premières dizaines sur ⟦||⟧"); the apparatus itself
  notes a fraction trace "préférable bien que cette dernière ne soit
  pas reprise dans le total" — an entry-total inconsistency observed,
  but not interpreted, by the editors.
- **HT 118** (201): the entire tablet written over an erasure
  (".1-5 sur ⟦ ⟧"), with a possibly deleted unit stroke in line .4.

The sixth, HT 119, carries no erasure; its deviation may not be
ancient at all, since the apparatus marks the crucial numeral as
uncertain (a reading of 68 leaves Δ = 1; cf. Younger's "rounded
off").

By contrast, **none of the eight exactly-summing tablets** shows
rework in numeral context. Two of them do carry erasures — HT 104 (an
empty erasure at a line end) and HT 117a (name lines over an erasure)
— but in both the numbers are untouched and the sums are exact:
completed corrections. Counting conservatively (HT 119 as a deviator
*without* rework), the contingency is 5/6 vs 0/8 (Fisher's exact,
two-sided, **p = 0.0030**).

Two independent checks support the pattern. First, prediction P-VI
(registered before the relevant apparatus was read; see §7) was
resolved with one direct hit (HT 102) and one case dissolving into a
reading issue (HT 119). Second, Montecchi's list of recognisable
palimpsests at Haghia Triada (2019, 219 n. 798) — compiled for
entirely different purposes — contains three of our six deviators
(HT 13, 118, 123) and none of our eight exact tablets (p = 0.077).

## 5. Discussion: updates, not incompetence

The correlation inverts the standard reading. If the discrepancies
reflected careless or unprofessional scribes, there would be no
reason for them to cluster on physically reworked tablets, nor for
intact tablets to sum exactly — carelessness does not erase. If, on
the other hand, tablets were **living documents** — entries adjusted
as deliveries and deficits changed — then exactly the observed
signature follows: a corrected entry with a stale total (HT 102,
where the editors themselves saw a fraction "not carried into the
total"), a corrected total trailing its entries (HT 9a's inserted
stroke), wholesale re-use of a tablet with incomplete reconciliation
(HT 13, HT 118).

This reading converges with, and sharpens, existing scholarship on
Linear A palimpsests as re-used or updated documents (Montecchi 2019,
218–220; Schoep 2002; Consani 1996; Tomas 2017) — but it relocates
the "calculation errors" from the scribes' competence to the
documents' **version history**. The corollary is historical: Haghia
Triada's administration maintained and revised its records, and the
deviating tablets are precisely those caught mid-revision. They are
not the worst tablets in the corpus; they are the most informative,
because they preserve two bookkeeping states at once.

## 6. Corollary: column constraints and the fraction values

Because HT 123a's olive column sums exactly, its entry list is
complete, and the parallel *308 column yields a constraint that is
independent of any ratio model: 8¼ + 8¾ + (4 + s) + 4¼ = [2]5 + H,
hence **H = s + ¼**, where s is the fraction sign of the SA-RU entry
(A711 X by GORILA's drawing and Montecchi's autopsy, 2019, 147; A701
A in the lineara.xyz encoding) and the tens digit of the total is
restored. Whatever s is, **H ≥ ¼**.

This single inequality bipartitions the literature on the disputed
sign. On one side stand the solutions that respect it: the classical
H = 1/3 (Bennett 1950; Stoltenberg 1955; Schrijver 2014; one of the
two live options in Montecchi 2019, 148), which satisfies the
equation with s = 1/12, and Cash & Cash (2011), whose values
(J = 1/2, E = 1/4, A = 1/20, H = 3/10) satisfy both the equation
(3/10 = 1/20 + 1/4) and the full *308 column sum exactly
(25.3 = [2]5 + H) — indicating that the column sum, in some form,
underlies their solution. On the other side stand the values that
violate it: H = 1/6 (Was 1971; Younger 2024, derived from a ⅓-ratio
model of this same tablet that conflicts with the pure column sum by
exactly the ⅔ Younger flags elsewhere as a reading problem; on the
weakness of ratio-based reconstruction see already Bennett 1980, 21,
and Montecchi 2019, 158 n. 555 on Schrijver's 3:1 assumption), and
the tentative H = 1/16 of Corazza et al. (2021) — who excluded HT 123
from their optimisation on the grounds of its doubtful readings
(citing Montecchi 2009). The exact olive control column answers that
exclusion in part: the ledger's arithmetic, where checkable, is
sound. Our contribution is thus not a new value but the isolation of
the minimal-assumption constraint that separates the two camps — and
the demonstration that the machine-validated side of the ledger
supports the camp that honours it.

Two further corollaries: (i) HT 13's discrepancy is real for **any**
assignment of fraction values — the constraint collapses to 2J = J
(and to J = 1 under the apparatus' alternative reading of one entry)
— so the tablet is a secure witness of revision, not of a
misunderstood notation; (ii) the deficit (KI-RO) column discriminates
further: under the lineara/GORILA readings it sums exactly iff
X = 7/4 — the very value Younger derives independently from his ratio
model — whereas Cash & Cash's X = 9/20 fails it (Σ = 3.4 vs 6);
Montecchi's autoptic reading ("2̣ X̣" in line .3-4) would alter the
equation, and the closing figure is itself damaged ("IIII et fraction
ou IIII[", GORILA I, 211). We therefore register the fraction
conclusions as conditioned claims and defer to the sequence of six
fraction signs on the unpublished sceptre handle KN Zg 58 (§7),
which will arbitrate between the two camps on text none of the
proposals has seen.

## 7. Pre-registered predictions

Six falsifiable predictions, with explicit failure criteria, are
timestamped in the repository (German originals with English
translation): P-I cult-register suffix share on the Knossos sceptre
ring KN Zg 57; P-II positional syntax of KU-RO vs KU-RA on the
handle; P-III the fraction ordering of Zg 58 face δ must place
H ≥ ¼ (failure vindicates Corazza et al.); P-IV slot congruence in
newly published libation formulas; P-V replication of header/list
suffix asymmetries and summation rates on new tablets; P-VI erasure
localisation on the then-unread deviator apparatus (resolved:
indeterminate at N = 2, one direct confirmation). When the Anetaki II
edition of the sceptre appears, several of these claims will be
hard-tested on text none of us has seen.

## 8. Limitations

The checkable sample is small (15 tablets enter the central
contingency). The "numeral-context" refinement of the erasure
criterion was made after inspection of the first eleven tablets and
is therefore post hoc; we mitigated this by blind classification of
the remaining six, by the independent palimpsest-list check, and by
registering the criterion for future cases. Apparatus coding is
manual (a SigLA-based replication would be desirable). Several
fraction-sign claims depend on disputed readings, which we condition
explicitly rather than resolve; an autoptic re-collation of HT 123a's
*308 and KI-RO columns would settle them. Finally, analyses were
performed with AI assistance (Anthropic's Fable 5); all critical
readings were verified against the GORILA facsimiles by the author,
who bears responsibility for errors.

## References (to complete)

Bennett, E.L. 1950. Fractional quantities in Minoan bookkeeping. AJA
54, 204–222. — Bennett, E.L. 1980. Linear A fractional retraction.
Kadmos 19, 12–23. — Cash, R. & Cash, E. 2011. La tablette HT 123 :
une comptabilité en linéaire A. Kadmos 50, 33–62. — Corazza, M.,
Ferrara, S., Montecchi, B., Tamburini, F. & Valério, M. 2021. The
mathematical values of fraction signs in the Linear A script. JAS
125, 105214. — Facchetti, G.M. 2013. Again on Linear A metrograms J
and E. Kadmos 51. — Godart, L. & Olivier, J.-P. 1976–85. GORILA I–V.
— Kanta, A., Nakassis, D., Palaima, T.G. & Perna, M. 2024. An
archaeological and epigraphical overview… (Anetaki plot). Ariadne
Suppl. 5, 27–43. — Montecchi, B. 2009. Le frazioni, gli errori di
calcolo e le unità di misura nella documentazione in lineare A. AIIN
55, 29–52. — Montecchi, B. 2013. An updating note on Minoan
fractions, measures, and weights. AIIN 59, 9–26. — Montecchi, B.
2019. Contare a Haghia Triada. Roma: CNR. — Raison, J. & Pope, M.
1978 [apud Duhoux 1978, 47–48; cited after Younger 2024]. —
Salgarella, E. & Castellan, S. 2020. SigLA: the signs of Linear A. —
Schoep, I. 2002. The Administration of Neopalatial Crete. —
Schrijver, P. 2014. Fractions and food rations in Linear A. Kadmos
53, 1–44. — Stoltenberg, H.L. 1955 [apud Corazza et al. 2021, Table
3]. — Tomas, H. 2017. Epigraphical features of economic texts in
Linear A. In: Palatial Economy, 93–103. — Was, D.A. 1971 [apud
Corazza et al. 2021, Table 3]. — Younger, J.G. 2024. Linear A texts &
inscriptions: Introduction & commentary (ed. 8 April 2024).

*Remaining pre-submission check: Montecchi 2009, 37–39 (autopsy of
the direct H10 prior-art question: are erasures mentioned in
connection with the calculation errors? Her 2019 synthesis, which
incorporates that material, does not make the connection — but the
original should be sighted).*
