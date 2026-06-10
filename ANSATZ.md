# Linear A: Ein computergestützter Entzifferungsansatz

*Arbeitsdokument, Juni 2026 — basiert auf eigener Analyse des GORILA-Korpus
(Export von lineara.xyz, Transkriptionen nach J. Younger). Alle Zahlen in
diesem Dokument stammen aus `analyze.py` und sind reproduzierbar.*

---

## 1. Problemdiagnose: Warum 130 Jahre Stillstand?

Linear B wurde 1952 entziffert, weil drei Dinge zusammenkamen: ein großes
Korpus (~30.000 Zeichen allein aus Knossos), eine bekannte Zielsprache
(Griechisch, auch wenn das erst das Ergebnis war) und interne Strukturanker
(Ventris' "Tripletts", Ortsnamen). Bei Linear A fehlen zwei der drei Beine.
Unsere Korpusvermessung zeigt das Problem quantitativ:

| Messgröße | Wert | Konsequenz |
|---|---|---|
| Dokumente | 1.721 (890 Noduli, 435 Tafeln, 151 Roundels …; nach Support-Audit) | meist Kurztexte |
| saubere Wort-Tokens (≥2 Silben) | 1.284 | winziges Korpus |
| Wort-Typen | 930 | — |
| **Hapax legomena** | **781 = 84 % aller Typen** | kaum Wiederholung → kaum Kontext-Triangulation |
| Zeichen-Tokens in Wörtern | 3.802 | ~1/10 von Linear B |
| mittlere Wortlänge | 2,96 Silben | wenig interne Struktur pro Wort |

84 % aller Wörter kommen genau **einmal** vor. Entzifferung lebt aber von
Wiederholung in verschiedenen Kontexten. Das ist der eigentliche Engpass —
nicht fehlende Methodik, sondern fehlende Daten. Jeder seriöse Ansatz muss
deshalb (a) die wenigen wiederholten Strukturen maximal ausbeuten und
(b) Information *unterhalb* der Wortebene erschließen (Zeichenstatistik,
Morphologie), wo das Korpus effektiv größer ist.

## 2. Was als gesichert gelten kann (hier reproduziert)

Diese vier Säulen haben wir computergestützt verifiziert — auf ihnen baut
alles Weitere auf:

**(a) Die Lautwerte sind großteils übertragbar.** 54 Kernzeichen mit
Linear-B-Lautwerten decken **94 %** aller Zeichen-Tokens in Wörtern ab; nur
61 seltene Zeichen (*301, *118, *21F …) sind lautlich offen (6 % der Tokens).
Wir können Linear A also weitgehend *vorlesen* — wir verstehen nur nicht,
was wir sagen. Der Transfer ist gerechtfertigt durch die Systemidentität
der Schriften und wird intern bestätigt (s. (b), (d)).

**(b) Das Zahlensystem und KU-RO = „Summe".** Unser Arithmetik-Test über
alle Tafeln: 33 prüfbare Summenformeln, davon 8 exakt aufgehend (HT9b: 24,
HT11b: 180, HT25b: 52, HT85a: 66, HT89: 87, HT104: 95 …), 3 mit
Bruch-Rundungsdifferenz ≤1 (HT13: Einträge 131 vs. KU-RO 130½ — der Schreiber
hat sich selbst verrechnet, ein starkes Echtheitssignal für *Buchhaltung*),
8 auf beschädigten Tafeln. Die übrigen Abweichungen sind überwiegend
mehrspaltige Tafeln (z. B. HT123: getrennte Summen je Warengruppe OLIV/*308),
die unser einspaltiger Parser noch nicht abbildet. KI-RO markiert
nachweislich Fehlbeträge („geschuldet"). PO-TO-KU-RO = Gesamtsumme über
mehrere Listen.

**(c) Die Logogramme sind lesbar.** GRA (Getreide), VIN (Wein), OLE (Öl),
FIC (Feigen), VIR (Personen) + Maßsystem mit Brüchen (½, ¼, ⅙ …) — die
*Textsorte* (Wirtschaftsverwaltung eines Palastes) ist damit gesichert,
auch ohne ein einziges Wort der Sprache zu verstehen.

**(d) Es gibt einen parallelen Formelkorpus.** Die „Libationsformel" auf
Steingefäßen: 23 Inschriften von 9 Orten (Iouktas, Kophinas, Palaikastro,
Petsophas …) wiederholen dieselbe Wortsequenz mit systematischen Varianten —
unser einziger „Mehrfachkontext-Text" außerhalb der Buchhaltung.

## 3. Der Ansatz: sechs Arbeitspakete

### AP1 — Strukturprofil der Sprache (ohne jede Semantik)

Bevor man *welche* Sprache fragt, muss man fragen: *was für eine Art*
Sprache? Unsere Positionsstatistik liefert ein erstes Profil:

- **Vokalsystem:** a (39 %) > i (22 %) > u (16 %) > e (12 %) ≫ **o (3,7 %)**.
  /o/ ist marginal — das ist das stärkste typologische Einzelsignal im
  Korpus. Sprachen mit a-i-u-(e)-System ohne stabiles /o/: Etruskisch
  (kein o!), Hurritisch, Luwisch, klassisches Semitisch. Griechisch und
  die meisten IE-Sprachen scheiden hier tendenziell aus.
- **Vokalische Anlaute:** reine Vokalzeichen (A, I, U …) stellen 10,8 % der
  Tokens, aber **22 % aller Wortanfänge** — die Sprache liebt V-initiale
  Wörter (oder Präfix-Vokale, s. AP2).
- **Keine Vokalharmonie:** die Vokal-Übergangsmatrix benachbarter Silben
  zeigt keine überbesetzte Diagonale → kein türkisch/uralischer Typ.
- **Wortenden:** -E ist am Wortende fast doppelt so häufig wie im
  Durchschnitt (19,5 % vs. 12,4 %) → Kandidat für ein produktives Suffix
  (-TE, -RE, -NE dominieren die Endposition).

### AP2 — Kombinatorische Morphologie (Affix-Grammatik ohne Übersetzung)

Man kann die *Grammatik* einer Sprache teilweise rekonstruieren, ohne ein
Wort zu verstehen — über Minimalpaare. Unsere Extraktion findet:

- **Suffix-Alternationen** an identischen Stämmen:
  `A-TA-[*350|DE|NA|RE]`, `SI-DA-[RE|RO|TE]`, `KU-PA-[JA|RI|ZU]`,
  `QE-RA₂-[JA|U]`, `DA-TA-[RA|RE]` … Die häufigsten alternierenden
  Endzeichen: **-RO, -JA, -RA, -TE, -RE, -TI/-SI** — das ist der Kern eines
  Flexions- oder Derivationsparadigmas.
- **Präfix-Alternationen:** `A-DA-RA ~ MI-DA-RA`, `DA-KU-NA ~ *47-KU-NA`,
  `A-*325-ZA ~ U-*325-ZA` und vor allem das bekannte **J-/A-Paar**
  (`JA-SA-SA-RA-ME ~ A-SA-SA-RA-ME`).
- **Informationstheoretisch:** H(letztes Zeichen | Rest) = 0,215 bit >
  H(erstes Zeichen | Rest) = 0,164 bit → die Sprache variiert an *beiden*
  Worträndern, etwas stärker am Ende. Linear A ist also **suffigierend UND
  präfigierend** — das passt schlecht zu rein suffigierenden Kandidaten
  und gut zu z. B. Hurritisch (Suffixe) + präfigierenden Elementen oder
  einem gemischten System.

*Nächster Schritt (offen):* die Alternationen in Kontextklassen trennen —
welche Suffixe erscheinen vor Zahlen (Kasus/Status der gezählten Entität?),
welche in der Libationsformel (Verbalmorphologie?).

### AP3 — Anker-Methode: Namen als Rosetta-Ersatz

Ohne Bilingue sind **Eigennamen** die einzigen Wörter mit von außen
bekannter Lautung. Das Korpus liefert:

- **40 Wörter, die identisch in Linear-B-Texten wiederkehren**, darunter
  Toponyme: **PA-I-TO** (Phaistos), **SU-KI-RI-TA** (Sybrita, in den
  Wurzel-Matches), **A-DI-KI-TE** ~ Dikte (auf PKZa11 in der Form
  A-DI-KI-TE-TE — am Dikte-Heiligtum gefunden!), **I-DA** (Ida, auf
  Libationsgefäßen vom Ida-Massiv; dazu I-DA-MA-TE von der Ida-Höhle).
- Diese Anker validieren die Lautwerte unabhängig (b) und geben uns die
  einzigen sicheren Semantiken: *Ortsname X im Kontext Y*.
- Ausbaurichtung: Personennamen-Listen (Tafeln mit VIR + Zahl 1 je Zeile
  sind Personenlisten; HT85b, HT117) gegen die minoischen Namen in
  ägyptischen Quellen (Keftiu-Listen, z. B. Papyrus BM 10056) und
  akkadische/ugaritische Handelsdokumente abgleichen.

### AP4 — Kontextsemantik der Verwaltung (Bedeutung ohne Lautung)

Die Buchhaltungsstruktur erlaubt es, Funktionswörtern Bedeutung zuzuweisen,
ohne die Sprache zu kennen:

- KU-RO „Summe", KI-RO „Fehlbetrag/geschuldet" (gesichert, s. o.);
  PO-TO-KU-RO „Gesamtsumme" — morphologisch interessant: PO-TO- ist ein
  produktives Element vor KU-RO.
- **SA-RA₂** (20×, nur Haghia Triada): erscheint systematisch bei
  GRA/VIN/OLE-Einträgen → Funktionswort der Zuteilung oder eine
  Institution. **A-DU** (10×): Kopfzeilen-Wort → „Lieferung/Abgabe"-Klasse.
  Transaktionszeichen TE nach Kopfzeilen-Wort = wohl „von/an".
- Methode formalisieren: jedes häufige Wort bekommt einen
  **Distributionsvektor** (Position auf Tafel, begleitende Logogramme,
  folgt/geht Zahl voraus, Ort) → Clustering trennt Personennamen,
  Ortsnamen, Warenbegriffe, Funktionswörter. Das ist klassische
  Distributionssemantik — sie funktioniert auch auf 1.300 Tokens.

### AP5 — Sprachvergleich als Hypothesentest statt Etymologie-Fischen

Der methodische Kardinalfehler der bisherigen 130 Jahre: Einzelwörter
einer Wunschsprache zuordnen (es gibt „Entzifferungen" als Griechisch,
Semitisch, Luwisch, Sanskrit …— alle unfalsifizierbar, weil bei 930 Typen
und freier Lautwert-Justierung *immer* Treffer entstehen). Stattdessen:

1. Pro Kandidatensprache K (Anatolisch/Luwisch, Nordwest-Semitisch,
   Hurritisch, Tyrsenisch/Etruskisch, „Ägäisch-isoliert") ein
   **strukturelles Erwartungsprofil** ableiten: Vokalinventar,
   Affix-Typologie, Wortlängenverteilung unter CV-Verschriftung,
   erwartete Morphemfrequenzen.
2. Gegen unser gemessenes Profil (AP1/AP2) scoren — **Bayes-Faktor statt
   Anekdote**. Punktuelle Befunde dieses Laufs: marginales /o/ und
   gemischte Prä-/Suffigierung sprechen *gegen* Griechisch/IE-Kentum,
   sind *kompatibel* mit Tyrsenisch, Hurritisch, Semitisch; die
   V-initiale Präferenz und das J-/A-Präfixpaar passen auffällig gut zu
   einem System mit produktiven Vokal-Präfixen (semitischer Artikel?
   hurritische Relativpräfixe? — als *Hypothesen* zu testen, nicht als
   Schlussfolgerung).
3. Entscheidend: **vorher festlegen**, welche Beobachtung welche Hypothese
   *falsifizieren* würde. Beispiel: Wenn Linear A semitisch wäre, müssten
   die Suffix-Alternationen mit den Logogramm-Klassen (Genus!) korrelieren
   — prüfbar mit AP4-Vektoren.

### AP6 — Moderne algorithmische Verfahren + der Datenhebel

- **Neural decipherment** (Luo, Cao & Barzilay 2019 haben Linear B
  automatisch auf Griechisch gemappt; ihr Ugaritisch-Hebräisch-Setup ist
  das Vorbild): Linear-A-Wortliste gegen Lexika *mehrerer* Kandidaten
  parallel optimieren; die erreichte Mapping-Kohärenz pro Kandidat ist
  selbst ein Sprachverwandtschafts-Score. Mit 930 Typen grenzwertig,
  aber als *Ranking*-Instrument (nicht als Übersetzer) brauchbar.
- **Constraint-Propagation auf der Libationsformel:** 23 Parallel-Texte
  mit Slot-Struktur (`A-TA-I-*301-WA-JA … JA-SA-SA-RA-ME … U-NA-KA-NA-SI …
  I-PI-NA-MA SI-RU-TE`) wie ein Kreuzworträtsel behandeln: Varianten in
  festen Slots (U-NA-KA-NA-SI ~ U-NA-RU-KA-NA-TI; I-PI-NA-MA ~
  I-PI-NA-MI-NA; -WA-JA ~ -WA-E) sind mit hoher Wahrscheinlichkeit
  *Flexion desselben Lexems* → das beste Fenster in die Verbal-/
  Nominalmorphologie, das wir haben.
- **Der eigentliche Hebel ist das Korpus:** SigLA (sigla.phis.me)
  paläographisch nutzen (Schreiberhände trennen wie Younger/Salgarella),
  Neufunde einarbeiten, und die ~6 % unentzifferten Zeichen über
  Ligatur-Zerlegung (141 Ligaturen im Datensatz) reduzieren. Jedes
  Prozent mehr lesbares Korpus wirkt überproportional, weil es
  Hapax-Wörter in Mehrfachkontexte verwandelt.

### Exkurs: Der Neufund KN Zg 57–58 (Elfenbein-Zepter, Knossos 2024)

Im Repositorium des „Fetish Shrine" (Anetaki-Grabung) gefunden, publiziert
als Überblick in Kanta/Nakassis/Palaima/Perna 2024 (*Ariadne Suppl.* 5,
27–43; PDF liegt im Projekt, strukturierte Daten in
`data/supplements.json`). Eine zeichengenaue Edition steht noch aus
(*Anetaki II*, forthcoming) — aber schon der Überblick liefert drei
Ansatz-relevante Neuigkeiten:

1. **Längster Text überhaupt:** ~119 Zeichen (84 erhalten + 35 in Spuren)
   auf den vier Faces des Rings — und **ohne eine einzige Zahl**. Ein
   Ring mit Logogrammen (Gefäße, Textilien, Häute, GRA/FAR?/OLIV) und
   sechs phonetischen Zeichengruppen, der Ritual-Zutaten *aufzählt statt
   abzurechnen* — das verbindet erstmals unsere zwei Teilkorpora
   (Verwaltungslogogramme + Kultkontext) in einem Dokument.
2. **Der Griff (KN Zg 58) ist ein Wirtschaftstext aus einem Kultgebäude**
   (Novum) und enthält **sechs verschiedene Bruchzeichen in einer
   Sequenz** — der erste direkte Beleg für die *relative Ordnung* der
   Linear-A-Bruchwerte, teils abweichend von bisherigen Rekonstruktionen
   (Corazza et al. 2021). Sobald die Edition vorliegt, ist das ein
   Prüfstein für unseren Arithmetik-Parser (AP-Erweiterung: Brüche).
3. **Zwei Schreiberhände** auf einem Objekt (Ring kalligraphisch, Griff
   linearisiert; A+KA-Ligatur unterschiedlich gestapelt) und zwei
   Hieroglyphen-Zeichen (*180, *181) erstmals in Linear A — Munition für
   die Paläographie-Schiene (SigLA) und die Schriftgeschichte
   (Hieroglyphisch ↔ Linear A enger als gedacht).

## 4. Konkrete falsifizierbare Mini-Hypothesen — und ihre Testergebnisse

*Alle vier Hypothesen wurden mit `test_hypotheses.py` gegen das Korpus
getestet (exakter Fisher-Test, zweiseitig; Ausgabe in
`hypotheses_results.txt`). Ergebnis: 1× gestützt, 2× verworfen, 1×
datenlimitiert — genau so soll Falsifizierbarkeit funktionieren.*

1. **H1:** Das Suffix-Paar **-SI ~ -TI** (U-NA-KA-NA-SI ~ U-NA-RU-KA-NA-TI)
   markiert eine grammatische Opposition; Vorhersage: Varianten
   verschiedener Formel-Slots kovariieren (Kongruenz).
   **→ 🔶 Muster wie vorhergesagt, N zu klein.** In *allen* prüfbaren
   Slot-Paaren perfekte Kongruenz (S3×S4: 3/3, S3×S1: 4/4, S1×S2: 3/3);
   PKZa11 (Palaikastro) trägt alle drei abweichenden Varianten *gemeinsam*
   (-WA-E + -TI + -MI-NA + SA- statt JA-). Aber N=3–5 → p=0,25–0,33.
   Auffällig: die Abweichler-Varianten clustern in Ostkreta (Dialekt oder
   andere Formel-Rezension?). TLZa1 wurde wegen der bekannten
   Segmentierungs-Krux (u-na-ka-na-si vs. u-na-ka-na + si-…) aus S3
   ausgeschlossen. Entscheidbar erst mit mehr Za-Inschriften.
2. **H2:** **J- vor Vokal-Anlaut** ist ein Proklitikon; Vorhersage:
   J-Formen meiden die Textanfangsposition.
   **→ ❌ VERWORFEN.** J-Formen stehen textinitial — auch auf Tafeln mit
   erhaltenem Anfang (KH74: JA-DA-SU, KN1a: JA-KU-TI, ZA4a: JA-TO-JA,
   ARKH1b: JA-RE u. a.; JA- initial 32 % vs. A- 41 %, p=0,61: keinerlei
   Positionsrestriktion).
   Das widerlegt nicht die J-Präfigierung selbst (JA-SA-SA-RA-ME ~
   A-SA-SA-RA-ME bleibt real), wohl aber die spezifisch *proklitische*
   Positionsvorhersage.
3. **H3:** **SA-RA₂** ist kein Eigenname, sondern ein Funktionswort der
   Zuteilung; Vorhersage: Distributionsprofil ≠ Personennamen-Pool.
   **→ ✅ GESTÜTZT.** Zwischen SA-RA₂ und seiner Zahl steht in 70 % der
   Fälle ein Waren-Logogramm (GRA/VIN/OLE …) — im Namen-Pool (21 häufige
   HT-Wörter) nur 13 %: **p < 0,001**. SA-RA₂ verhält sich auch klar
   anders als KU-RO (6 % Logogramm, reine Summenposition). Das
   Mengenkriterium allein (Median 10 vs. 6) ist nicht signifikant
   (p=0,31). SA-RA₂ ist distributionell ein Zuteilungs-/Institutionswort,
   kein Personenname.
4. **H4:** Die **-E-Häufung am Wortende** ist ein Kasus-/Direktiv-Suffix
   der Kopfzeile; Vorhersage: -E-Formen überzufällig vor der ersten Zahl.
   **→ ❌ VERWORFEN.** Header 18 % -E vs. Listenkörper 18 % (p=1,0;
   nach Support-Korrektur). Aus der Falsifikation wurde H4b destilliert
   (s. u.) — die erklärt auch, *warum* H4 scheitern musste.
5. **H4b (Nachfolger von H4):** Das finale -E ist kein Positionsmarker,
   sondern ein **kleines geschlossenes Suffix-Inventar mit
   Register-Bindung**. Getestet mit fünf Vorhersagen
   (`test_e_suffix.py`, Ergebnisse in `e_suffix_results.txt`):
   - **P1 ✅ Suffix-Inventar statt Phonotaktik:** Der Final-Überschuss
     konzentriert sich auf genau fünf Zeichen — **-NE (2,07×), -ME
     (2,03×), -TE (1,71×), -RE (1,58×), -SE (1,56×)**, alle p ≤ 0,003 —
     während -DE (1,08×), -KE und -QE (0,70×) unauffällig sind. Wäre der
     Effekt lautlich, müssten alle E-Zeichen betroffen sein.
   - **P2 🔶 Vokal-Paradigmen am Stammende:** Gleicher-Konsonant/anderer-
     Vokal-Paare (DA-TA-RA ~ DA-TA-RE, SI-DA-RE ~ SI-DA-RO, TA-NA-TI ~
     TA-NA-TE …) sind 1,8× häufiger als die Zufallserwartung
     (9 beobachtet vs. 4,9; Permutationstest p=0,060) — Konsonant-
     Alternation liegt dagegen exakt auf Zufallsniveau (p=0,74). Das
     Signal ist also spezifisch vokalisch-paradigmatisch; knapp unter
     Signifikanz, Richtung klar.
   - **P3 ✅:** E ist an 5 von 9 Vokal-Alternationen beteiligt.
   - **P4 ✅ Register-Gradient (stärkster Befund):** -E-final-Rate
     **30,6 % auf Stein-/Kultinschriften ≫ 17,5 % Verwaltung
     (p=0,0004) > 11,1 % Siegelpraxis** (p=0,001; Zahlen nach
     Support-Korrektur). Die -E-Suffixe
     gehören zur religiösen Formelsprache (SI-RU-TE, JA-SA-SA-RA-ME,
     O-SU-QA-RE …) und meiden die namenstragenden Siegel — Verhalten
     von Flexionsmorphologie (Verbal-/Formelendungen), nicht von
     Namenlexik.
   - **P5 ✅ Warum H4 scheiterte:** Auf Tafeln sind die Suffixe
     *gegenläufig* positioniert: **-NE ist kopfzeilen-affin** (50 %
     Headeranteil vs. 29 % global, p=0,038), -TE tendenziell auch (44 %,
     p=0,088), **-RE dagegen listen-affin** (18 %, p=0,125 — nach
     Support-Korrektur nur noch Tendenz). H4 hatte alle -E-Formen
     gepoolt — die Effekte heben sich gegenseitig auf. Aggregation war
     der Fehler, nicht die Suffix-Idee.
   - *Nebenbefund:* Auch **-O** zeigt mit 1,83× die stärkste
     Final-Neigung aller Vokale — der ohnehin marginale Vokal /o/
     (3,7 %) konzentriert sich an der Wortkante (KU-RO, KI-RO,
     SI-DA-RO …). Kandidat für ein weiteres grammatisches Element.

   **Stand H4b:** P1, P3, P4, P5 bestätigt, P2 als klare Tendenz.
   Arbeitsformulierung: *{-NE, -ME, -TE, -RE, -SE} bilden ein
   Suffix-Paradigma der Formel-/Verwaltungssprache; -NE/-TE markieren
   Kopfzeilen-Funktionen (Transaktion/Herkunft?), -RE eine
   Listenkörper-Funktion; auf Siegeln (Namen) fehlt das Paradigma
   weitgehend.*
6. **H4c (gleicher Testaufbau für -O):** Getestet mit `test_o_suffix.py`
   (Ergebnisse in `o_suffix_results.txt`), mit zusätzlicher Kontrolle:
   jede Analyse läuft mit und ohne die Funktionswörter
   KU-RO/KI-RO/PO-TO-KU-RO, die alle auf -RO enden.
   - **P1 ✅ Ein-Zeichen-Effekt:** Der -O-Überschuss ist kein
     Vokalklassen-Effekt wie bei -E, sondern hängt an genau **einem**
     Zeichen: **-RO (2,57×, p < 0,001)**; -TO (0,70×), -O (0,49×) und
     -KO (0,42×) liegen sogar *unter* der Basisrate.
   - **Kontrolle ✅ kein Funktionswort-Artefakt:** -RO überlebt den
     Ausschluss von KU-RO/KI-RO/PO-TO-KU-RO mit **1,97× (23/35,
     p < 0,001)** — auch das übrige Lexikon (SA-RO, SI-DA-RO, A-DA-RO …)
     bevorzugt -RO wortfinal. Das -O-Aggregat fällt dabei auf
     unauffällige 1,17× — der Träger ist allein -RO.
   - **P2 🔶 Paradigma bis in die Funktionswörter:** O alterniert an
     Stämmen (SI-DA-[RE|RO], A-DA-[RA|RO], A-MI-DA-[O|U]); bei
     2-Zeichen-Wörtern (informativ): **KU-RO ~ KU-RA ~ KU-RE und
     KI-RO ~ KI-RA ~ KI-RU**. Kontextbefund: KU-RA steht auf ZA20
     (Zakros) unmittelbar vor „130" in Summenposition, KI-RA auf HT103
     vor „5 ½" — funktional parallel zu KU-RO/KI-RO. Die
     Buchhaltungstermini selbst scheinen Teil eines
     Vokal-Flexionsparadigmas zu sein.
   - **P4 ✅ Spiegelbild von -E:** Registerprofil: Verwaltung 8,3 % ≫
     Kult 0,7 % (p=0,0002) — exakt invers zu -E (Kult 31 % ≫
     Verwaltung 18 %). Ohne Funktionswörter kippt die Spitze zur
     Siegelpraxis (7,4 % > Verwaltung 2,6 %, p=0,028): Rest--RO sitzt
     in der Namen-Sphäre. (Zahlen nach Support-Korrektur.)
   - **P5 🔶:** -RO ist listen-/summenpositioniert (14 % Headeranteil,
     p=0,004); ohne Funktionswörter gleiche Richtung (13 %), aber n=15
     zu klein (p=0,26).

   **Stand H4c:** -O ist kein Suffix-Inventar, sondern **ein einzelnes
   grammatisches Zeichen: -RO** — mit zwei Schichten: (a) die
   Buchhaltungs-Funktionswörter in Summenposition, (b) ein restlicher
   -RO-Ausgang mit Siegel-/Namen-Affinität. Zusammen mit H4b ergibt
   sich ein konsistentes Bild *komplementärer Register-Morphologie*:
   -E-Suffixe tragen die Kult-/Formelsprache, -RO die
   Verwaltungs-/Namensphäre. Prüfstein für die Zukunft: die
   Funktionsdifferenz KU-RO vs. KU-RA (Ost- vs. Zentralkreta?
   Kasus/Genus der summierten Größe?) an neuen Texten.
7. **H5 (KU-RO ~ KU-RA als Ost-/Zentralkreta-Dialekt):** Getestet mit
   `test_dialect.py` (Ergebnisse in `dialect_results.txt`).
   Entscheidungsmatrix: gleiche Funktion + komplementäre Geographie →
   Dialekt; Koexistenz am selben Ort + verschiedene Syntax → Grammatik.
   - **D1 ❌ keine komplementäre Verteilung:** KU-RO ist auch in
     Ostkreta belegt (ZA15b: „KU-RO 𐄁 VIN 78" — klassische
     Summenfunktion in Zakros), KU-RA auch in Zentralkreta (ARKH2),
     KI-RA auch in Haghia Triada (HT103). Das formal signifikante 2×2
     (Zentral O:54/A:2 vs. Ost O:1/A:2, p=0,010) hängt an nur drei
     Ost-Token und wird durch die direkten Gegenbeispiele entkräftet.
   - **D2 ✅ stattdessen funktionale Differenz:** KU-RA (ARKH2) und
     KI-RA (ZA8) stehen in **Eröffnungs-/Kopfposition vor der Liste** —
     eine Position, die KU-RO nie einnimmt (35/37 unmittelbar vor Zahl
     am Listenende). ZA20 („KU-RA 130") ist wegen Anfangslücke
     arithmetisch unentscheidbar (erhaltene Einträge summieren nur zu
     26). KU-RE (2×, HT) steht nie vor einer Zahl; auf HT39 allein in
     der Zeile direkt über der KU-RO-Summenzeile.
   - **D3 ∅:** Nur zwei weitere -O/-A-Minimalpaare im Korpus, keine
     regionalen Splits — kein systematischer Regional-Vokalismus.
   - **D4 ❌ keine Ost-Exklusivität der Formelvarianten:** Abweichende
     Varianten auch zentral (IOZa12, KHZc106: SA-SA-RA-ME), Standard-
     formen auch in Palaikastro (PKZa12, PKZa27); Ost 2/6 vs. Zentral
     2/14 abweichend, p=0,55. *Das revidiert die H1-Randnotiz vom
     „Ostkreta-Cluster": Die Slot-Kongruenz innerhalb eines Dokuments
     bleibt bestehen, die geographische Deutung nicht.*
   - **Datenqualitäts-Fund → systematisches Audit:** Alle 44 plain-ZA-
     Tafeln (ZA1–ZA33) waren in lineara.xyz fälschlich als „Stone
     vessel" geführt. `audit_support.py` leitet den Dokumenttyp aus der
     GORILA-Seriensystematik der IDs ab und korrigiert konservativ
     **53 Einträge** (`data/support_corrections.json`, von
     `corpus_lib.load_inscriptions()` automatisch angewandt; Zd–Zg-
     Serien bewusst ausgenommen, da dort das Material-Feld präziser
     ist als die Serie — KN Zg 57 ist Elfenbein, kein Stein). Alle
     Kernergebnisse überleben die Korrektur; die Zahlen in diesem
     Dokument sind die korrigierten.

   **Stand H5: Dialekt-These verworfen.** Die Daten sprechen für
   **grammatische Differenzierung im Paradigma KU-R-O/-A/-E**:
   -O = abschließende Summenangabe, -A = eröffnende/überschriftliche
   Funktion („Bestand/Soll"?), -E = Rubrik ohne Zahlangabe. Vorhersage
   für Neufunde: KU-RA darf in Kopfposition erscheinen, KU-RO nicht.
8. **H6 (KI-RO als Komplement; Mehrspalten-Arithmetik):** Getestet mit
   `test_kiro_columns.py` (Zeilen als Label→Wert-Spalten; Ergebnisse
   in `kiro_columns_results.txt`).
   - **T1 ✅ Spaltenstruktur bestätigt:** Auf HT123+124a summiert die
     OLIV-Spalte **exakt** (31 + 31½ + 16 + 15 = 93½ = „KU-RO OLIV
     93½"). Die mehrspaltige Buchhaltung ist real und die
     Eintragsliste nachweislich vollständig.
   - **T1 🔶 Bruchzeichen-Gleichung gewonnen:** Die *308-Spalte geht
     bis auf Δ=¼ auf — die Abweichung steckt komplett in zwei
     Klasma-Zeichen mit unsicheren Werten (Eintrag „4 + A701-A" vs.
     Summe „25 + A706-H"). Daraus folgt, unabhängig von den
     Absolutwerten: **A706(H) − A701(A) = ¼**. Direkter Input für die
     geplante Bruchwert-Inferenz (H9).
   - **T2 🔶 Komplement-These nicht haltbar — aber lesungsabhängig
     (Faksimile-Verifikation, s. u.):** Unter der lineara-Lesung
     („KI-RO 6") kann die Schlusszeile nicht die Spaltensumme sein:
     Einträge = 1+X, X, ¾, ¾ ⟹ Σ ≤ 4½ < 6 für jeden Bruchwert X ≤ 1 —
     und da die OLIV-Spalte exakt aufgeht, fehlen keine Einträge.
     **Aber:** Der GORILA-Apparat (Note .9) liest die Schlusszahl als
     unsicher — „IIII et fraction ou IIII[" (4+Bruch oder 4+Kante).
     Bei Lesung „4+f" gälte die Ungleichung nur noch für X < ¾.
     Wahrscheinlich bleibt: Schluss-KI-RO ≠ einfache Spaltensumme;
     bewiesen ist es nur für Lesungen ≥ 5½.
   - *Datenqualität:* lineara.xyz rendert A711 als „.3" und
     A701/A706 pauschal als „≈ ⅙" — die Klasma-Zeichen sind im
     Datensatz nur näherungsweise kodiert (dokumentiert; für H9 muss
     auf die Unicode-Originalzeichen zurückgegriffen werden).
   - **Faksimile-Verifikation (GORILA I, S. 210–211, lokal im Klon):**
     (a) ✓ OLIV-Spalte und Summe 93½ am Original-Faksimile bestätigt
     (∠ = J = ½ durchgängig konsistent); T1 steht. (b) ⚠️ Im
     SA-RU-Eintrag der *308-Spalte zeichnet GORILA „4 ♯[" — dieselbe
     ♯-Form wie das X (A711) der KI-RO-Spalte, mit Bruchkante und
     unsicheren Spuren (Apparat .5); lineara kodiert hier dagegen
     A701 „A". Die Spaltengleichung lautet daher korrekt
     **H − (A oder X) = ¼**. (c) ⚠️ Die Schluss-KI-RO-Zahl ist per
     Apparat .9 unsicher („4+Bruch oder 4+["), nicht hart „6".
     (d) Die Tafel ist ein **Palimpsest** (Apparat 1–9) — erhöhte
     Lesungsunsicherheit generell.
9. **H9 (Bruchwert-Inferenz):** `solve_fractions.py` behandelt die
   Klasma-Werte als Unbekannte und sucht per Max-SAT die Belegung, die
   maximal viele KU-RO-Gleichungen erfüllt (auf Unicode-Originalzeichen;
   Ergebnisse in `fractions_results.txt`).
   - Nur **4 Arithmetik-Constraints** im Korpus enthalten Klasma —
     davon sind zwei die bekannten Fehler-Tafeln: **HT13 ist
     wert-unabhängig unerfüllbar** (2J = J ⟹ Schreiberfehler bewiesen,
     ohne J zu kennen), HT9a verlangt 2J+E=2 (mit keinem plausiblen
     Wertepaar erfüllbar).
   - **Faksimile-Verifikation aller Constraint-Tafeln (GORILA I,
     lokal):**
     - *HT 9a (S. 18–19):* Entry-Werte bestätigt; aber der Apparat
       dokumentiert **Schreiber-Rework in der Totalzeile** („|
       ajouté après ⅍" — Einerstrich nachträglich hinter dem Bruch
       eingefügt) und Zeile .2 über Rasur; GORILA zeigt das Total
       zudem als „31 ⅍" mit zusätzlichem ⁊ — lineara hat zu „31¾"
       geglättet. Die Differenz von ¾ hat damit eine physische
       Korrektur-Geschichte.
     - *HT 13 (S. 26–27):* **Zeilen 4–7 inkl. KU-RO über Rasur**
       („sur ⟦ ⟧"); KU-ZU-NI evtl. 17 statt 18 („doute possible sur
       la quatrième unité … absence de fraction en tout cas");
       RE-ZA = „5[]∠" (Schaden zwischen Zahl und Bruch). Beide
       Zahlvarianten lassen die Gleichung unerfüllbar (2J=J bzw.
       J=1) — die Inkonsistenz ist lesungsstabil, aber die Tafel
       nachweislich überarbeitet.
     - *HT 89 (S. 141):* **vollständig bestätigt** — 23+22+24+13+5 =
       87 = KU-RO 87 exakt; einzige Unsicherheit (4 vs. 5 Striche)
       liegt in der Zeile *nach* dem Total.
     - **Meta-Befund:** Alle arithmetisch scheiternden
       Constraint-Tafeln (HT9a, HT13, HT123a) tragen dokumentierte
       Rasuren/Korrekturen bzw. sind Palimpseste; die exakt
       aufgehende HT89 ist sauber. Die „Schreiberfehler" korrelieren
       mit physischem Rework — das stützt sowohl die Lesung des
       Zahlsystems als auch unsere Outlier-Behandlung. Offene
       Anschlusshypothese: Arithmetik-Abweichungen im Korpus sollten
       bevorzugt auf Palimpsest-Tafeln auftreten (testbar nur durch
       systematisches GORILA-Apparat-Mining, da lineara.xyz
       Rasur-Vermerke nicht kodiert).
   - Verankerter Modus (J=½, E=¼ fix): eindeutig **A732 JE = ¾**
     (konsistent mit dem Ligatur-Axiom JE=J+E); A701/A706 bleiben eine
     einparametrige Familie **H = A + ¼** (aus H6).
   - **Fazit:** Die Methode funktioniert, aber die Constraint-Basis des
     Korpus ist zu dünn für Absolutwerte allein aus KU-RO-Summen.
   - **Abgleich mit Corazza et al. 2021 (JAS 125, Table 8/9) — drei
     Konvergenzen, ein Widerspruch:** (a) Deren JE=¾ reproduziert unser
     Solver-Ergebnis unabhängig. (b) Ihr Ausschluss von X aus dem
     Wertesystem konvergiert mit unserem H6-Befund (A711 verhält sich
     nicht wie ein normaler Bruch). (c) J=½/E=¼ konsistent. ABER:
     ihre als *tentativ* markierten Werte **H=1/16(?), A=1/24(?)**
     ergeben H−A=1/48 und **verletzen unsere HT123-Spaltengleichung
     H−A=¼** (Δ=+0,23). Auflösung, die beides heilt: **A=1/12,
     H=1/3** — erfüllt die Gleichung exakt und füllt zugleich die
     auffällige 1/3-Lücke in Corazzas Optimalsystem (typologisch ist
     ein Bruchsystem ohne 1/3 ungewöhnlich).
     **Nach Faksimile-Verifikation (s. H6) gilt der Vorschlag nur
     bedingt:** GORILAs Umzeichnung legt nahe, dass das Eintrags-
     zeichen X (A711) statt A (A701) sein könnte. Falls X: Die
     Gleichung H − X = ¼ beträfe das von Corazza ausgeschlossene
     Zeichen, und der Widerspruch zu deren H=1/16 bestünde weiter
     (H müsste ≥ ¼ sein), aber der konkrete A-Wert entfiele.
     Prüfbar an der Zg58-Bruchsequenz (PREDICTIONS P-III).
10. **H7 (X ~ X-TE als Positions-/Herkunftssuffix):**
   `test_te_suffix.py`. **10 Alternationspaare gefunden** (6× -TE,
   4× -NE), darunter A-DI-KI-TE ~ **A-DI-KI-TE-TE** (Toponym Dikte +
   TE, auf der Libationsformel PKZa11 — „von/aus Dikte"?) und SI-RU ~
   SI-RU-TE. Positionssignal in der vorhergesagten Richtung: Bei den
   tafel-belegten -TE-Paaren kippt die Position durchgängig
   Listenkörper→Header (DU-RI→DU-RI-TE, KU-NI→KU-NI-TE; gepoolt
   p=0,14, N=7). **🔶 Tendenz, N zu klein** — bei -NE kein Signal
   (p=1,0). Abtrennbarkeit des Suffixes ist damit belegt, die
   Funktionszuweisung braucht mehr Tafeln.
11a. **Anker-Abgleich Linear A ↔ Linear B** (`test_lb_names.py`):
   Die 41 in beiden Schriften identischen Wörter wurden gegen die
   Linear-B-Serienkontexte gestellt (As/Ap/D-Serie = Personen,
   Fp/Fs/Tn = Opfer). Ergebnisse:
   - **Datenlimit dominiert:** 33/41 Anker sind in Linear A selbst
     Hapax/Selten (n<3) — sie tragen LB-Kontext-Information, aber
     keine LA-Distributionsklasse. In LB landen davon 16 in
     Personen-, 3 in Kult-, 14 in sonstigen Kontexten.
   - **PA-DE, der produktive „Fehltreffer":** Unser Lexikon
     klassifiziert PA-DE distributionell als „personenname?" (3×,
     kleine Zahlen, Listenkörper) — in Linear B ist pa-de aber ein
     **Opferempfänger/Gottheit** (KN Fp(1) 1, Fp(1) 48, Fs 8). Falls
     dieselbe Entität: Die PA-DE-Einträge von Haghia Triada wären
     **Opferlisten**, und „Empfänger kleiner Mengen im Listenkörper"
     wäre als Klasse nicht von Personennamen trennbar — eine neue,
     konkrete Hypothese (deckt sich mit der Literaturdebatte um
     pa-de als vorgriechische Gottheit).
   - Methodengrenze dokumentiert: Das LB-Serienkürzel kodiert den
     *Tafelinhalt*, nicht die *Wortrolle* (PA-I-TO erscheint in der
     D-Serie als Ort beim Hirtennamen, nicht als Person).
11. **H8 (Ligatur-Akrophonie): ❌ VERWORFEN** (in der HT31-Form).
   `test_ligatures.py`: Die ligierten Silbenzeichen auf
   Gefäß-Logogrammen (+RU 9×, +L2, +RO, +E, +KE, +A, +SU, +F; n=25)
   treffen die Anfangssilben der HT31-Gefäßnamen nur 1× — bei ~4
   Treffern Zufallserwartung (P(≥1)=0,99, eher *unter* Zufall). Die
   Ligaturzeichen kodieren also nicht den Gefäßtyp-Namen akrophon,
   sondern etwas anderes (Inhalt? Qualität? Kapazität?) — konsistent
   damit, dass das Zepter-Paper sie als Inhalts-/Typangaben *neben*
   selbsterklärenden Gefäßformen beschreibt.

## 5. Realistische Erwartung

Eine *vollständige* Entzifferung (= zusammenhängende Übersetzung) ist ohne
Bilingue oder dramatische Korpuserweiterung nicht erreichbar — bei 84 %
Hapax und ~3.800 Zeichen-Tokens ist das ein mathematisches, kein
methodisches Limit. Erreichbar ist eine **partielle Entzifferung in
Schichten**, von denen die ersten zwei heute schon stehen:

1. ✅ Lesung (Lautwerte, Zahlen, Logogramme) — 94 % der Tokens
2. ✅ Textpragmatik (Buchhaltung verstehen ohne Sprache)
3. 🔶 Morphologie-Skelett (AP2 + Libationsformel) — in Arbeit, hier begonnen
4. 🔶 Funktions- und Namenslexikon (AP3/AP4) — erste Version steht:
   `build_lexicon.py` klassifiziert 67 Wörter regelbasiert nach
   Distributionsvektoren (funktionswort / kultwort / toponym-anker /
   personenname? / header-wort), alle fünf Sanity-Anker korrekt
   (`data/lexicon_classes.json`)
5. ❌ Sprachzuordnung mit Beweiskraft (AP5/AP6) — nur als Wahrscheinlichkeits-
   Ranking erreichbar
6. ❌ Übersetzung zusammenhängender Texte — braucht neue Funde

Der Wert des hier gebauten Werkzeugs: Jede dieser Schichten ist jetzt
**messbar und reproduzierbar** statt anekdotisch — und jede neue Tafel
kann sofort gegen alle Hypothesen getestet werden.

---

## Reproduktion

```bash
node extract.js     # JS-Korpus -> data/*.json
python3 analyze.py  # alle Analysen, Ausgabe wie in report_raw.txt
```

Quellen: GORILA (Godart/Olivier), Transkriptionen J. Younger via
lineara.xyz (github.com/mwenge/lineara.xyz); Forschungsstand: Duhoux,
Schoep, Salgarella (*Aegean Linear Script(s)*, 2020), Luo/Cao/Barzilay
(ACL 2019), SigLA-Datenbank.
