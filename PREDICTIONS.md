# PREDICTIONS — registrierte Vorhersagen (Stand: 10. Juni 2026)

**Zweck:** Out-of-sample-Tests. Alle Vorhersagen hier sind *vor*
Publikation der jeweiligen Daten formuliert und durch die Git-Historie
dieses Repos zeitgestempelt. Zu jeder Vorhersage gehört ein explizites
Fehlschlag-Kriterium — eine Vorhersage, die nicht scheitern kann, zählt
nicht. Grundlage: die getesteten Hypothesen in `ANSATZ.md` (H1, H4b,
H4c, H5, H6).

Der wichtigste anstehende Testfall ist die zeichengenaue Edition des
Elfenbein-Zepters von Knossos (KN Zg 57–58) in *Anetaki II* (Kanta ed.,
forthcoming) — ein Text, der existiert, aber noch nicht publiziert ist.

---

## P-I — Ring KN Zg 57: Kult-Register-Morphologie (aus H4b)

Der Ring ist ein Kultobjekt. Die -E-Suffixe {-NE, -ME, -TE, -RE, -SE}
sind im Kult-Register fast doppelt so häufig wie in der Verwaltung
(30,6 % vs. 17,5 % wortfinal).

**Vorhersage:** Unter den lesbaren phonetischen Zeichengruppen des
Rings (≥6 auf Face B, ≥9 auf Face C) enden **≥ 25 %** auf eines der
fünf Zeichen {NE, ME, TE, RE, SE}.

**Fehlschlag:** < 18 % (= Verwaltungsniveau oder darunter).

## P-II — Griff KN Zg 58: Positionssyntax des KU-R-Paradigmas (aus H5)

**Vorhersage:** Falls auf dem Griff (Wirtschaftstext) eine KU-R-/
KI-R-Form erscheint: KU-RO/KI-RO stehen nur listen-final unmittelbar
vor einer Zahl; eine KU-RA/KI-RA-Form darf dagegen eröffnend/
überschriftlich stehen.

**Fehlschlag:** KU-RO eröffnet eine Liste, oder KU-RA steht listen-final
als arithmetisch exakte Spaltensumme.

## P-III — Zg 58, Face δ: Bruchzeichen-Sequenz (aus H6)

Aus der *308-Spalte von HT123+124a folgt die Gleichung
**A706 (H) − A701 (A) = ¼**, unabhängig von den Absolutwerten.

**Vorhersage (verschärft nach H9 + Corazza-Abgleich, 10.06.2026):**
Die auf Face δ dokumentierte Sequenz von sechs Bruchzeichen ist mit
H = A + ¼ kompatibel; konkret favorisieren wir **A701(A) = 1/12 und
A706(H) = 1/3** — gegen die tentativen Werte H=1/16(?), A=1/24(?) von
Corazza et al. 2021 (Table 8), deren Differenz (1/48) unsere
HT123-Spaltengleichung verletzt. Unser Vorschlag füllt zugleich die
1/3-Lücke in deren Optimalsystem.

**Fehlschlag:** Die publizierte Werteordnung von Zg 58 (oder eine
verifizierte Neukollation von HT 123a) widerspricht H = A + ¼ bzw.
ordnet H unterhalb von E (=¼) ein.

## P-IV — Neue Libationsinschriften: Slot-Kongruenz (aus H1)

Bisher kovariieren die Formel-Slot-Varianten perfekt (S3=-TI ⟺
S4=-MI-NA ⟺ S1=-WA-E), aber N=3–5.

**Vorhersage:** Unter den nächsten 10 neu publizierten
Libationsformel-Texten mit ≥ 2 ausgefüllten Slots ist **höchstens ein**
inkongruentes Dokument.

**Fehlschlag:** ≥ 2 inkongruente Dokumente (dann ist die
Kongruenz-These tot und die Varianten sind freie Variation).

## P-V — Neue Verwaltungstafeln, beliebiger Fundort (aus H4b/H6)

**Vorhersage (Replikation):**
1. -NE/-TE-finale Wörter haben einen Headeranteil > 40 %
   (globaler Headeranteil ≈ 29 %).
2. Bei unbeschädigten, einspaltigen Summenformeln geht die Mehrheit
   (> 50 %) exakt auf; mehrspaltige Tafeln summieren spaltenweise
   (wie HT123+124a OLIV).

**Fehlschlag:** -NE/-TE-Headeranteil ≤ 30 %, oder systematisch
nicht-aufgehende intakte Summen.

---

*Methodik: exakte Fisher-Tests bzw. Arithmetik-Checks wie in den
test_*.py-Skripten dieses Repos; Auswertung erfolgt mit denselben
Skripten gegen die dann publizierten Transkriptionen.*
