#!/usr/bin/env python3
"""H10 — Rasur-Hypothese: Arithmetik-Abweichungen korrelieren mit
physischem Rework (GORILA-Apparat-Mining).

Datengrundlage: data/gorila_apparatus.json — manuell aus dem kritischen
Apparat von GORILA Vol. I gelesen (alle 11 einspaltig prüfbaren
KU-RO-Tafeln: 8 exakt aufgehende, 3 knapp abweichende mit Δ ≤ 1).

Zwei Tests:
T1  Rasur irgendwo auf der Tafelseite (präregistrierte Grobfassung)
T2  Rasur/Korrektur in zahltragender Zeile oder Totalzeile
    (verfeinerte Fassung — ACHTUNG: post hoc nach Sichtung der Daten
    formuliert; als präregistriertes Kriterium für die Ausweitung auf
    weitere Tafeln zu verwenden)
"""
import json
from corpus_lib import DATA, fisher2x2

app = {k: v for k, v in json.load(open(DATA / "gorila_apparatus.json")).items()
       if not k.startswith("_")}

print("=" * 78)
print("H10 — Rasuren (GORILA-Apparat) vs. Arithmetik-Status")
print("=" * 78)
print(f"{'Tafel':<9} {'Status':<7} {'Rasur':<7} {'Rasur-numerisch':<16} Apparat")
for n, e in sorted(app.items(), key=lambda kv: (kv[1]['status'], kv[0])):
    print(f"{n:<9} {e['status']:<7} {'ja' if e['rework'] else '—':<7} "
          f"{'ja' if e['rework_numerisch'] else '—':<16} {e['apparat'][:70]}")

for label, key in (("T1: Rasur irgendwo", "rework"),
                   ("T2: Rasur in Zahl-/Totalzeile", "rework_numerisch")):
    a = sum(1 for e in app.values() if e["status"] == "NAH" and e[key])
    b = sum(1 for e in app.values() if e["status"] == "NAH" and not e[key])
    c = sum(1 for e in app.values() if e["status"] == "EXAKT" and e[key])
    d = sum(1 for e in app.values() if e["status"] == "EXAKT" and not e[key])
    p = fisher2x2(a, b, c, d)
    print(f"\n{label}:")
    print(f"   Abweichler {a}/{a+b} mit Rasur  vs.  Exakte {c}/{c+d} mit Rasur"
          f"   ->  Fisher p={p:.4f}" + ("  ***" if p < 0.05 else ""))

print("""
Lesart: Rasuren kommen auch auf exakt summierenden Tafeln vor (HT104,
HT117a) — dort aber peripher (leere Rasur am Zeilenende, Kopf-/Namens-
zeilen) und die Rechnung geht auf: vollendete Korrekturen. Auf allen
drei Abweichler-Tafeln sitzt das Rework dagegen in den zahltragenden
Zeilen bzw. der Totalzeile selbst (HT9a: Strich in der Totalzeile
nachgetragen; HT13: Zeilen 4-7 inkl. KU-RO über Rasur; HT94a: zwei
getilgte Einerstriche im Eintrag). Die 'Schreiberfehler' des Korpus
sind Residuen unvollständig nachgeführter Korrekturen.
Kontext: auch HT123a (mehrspaltiger Abweichler) ist Palimpsest mit
spaeteren Rasuren — konsistent mit dem Muster.""")
