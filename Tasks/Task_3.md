# Task: Überarbeitung und Korrektur der manuellen Verfahrmodi (Werkzeug, Koordinaten, Joint)

## Hintergrund

Bei der manuellen Bedienung des Roboters scheint die Implementierung der Verfahrmodi aktuell nicht dem Verhalten zu entsprechen, das in der industriellen Robotik üblich ist.

Folgendes Verhalten wurde beobachtet:

- HMI → **Manuell**
- HMI → **Werkzeug**
- Button **X-**

Erwartetes Verhalten:

Der TCP (Tool Center Point) sollte sich geradlinig entlang der negativen X-Achse des Werkzeugs bewegen.

Aktuelles Verhalten:

Der Roboter bewegt sich auf einer Bogenbahn zurück. Dies deutet darauf hin, dass entweder:

- die Transformationen zwischen den Koordinatensystemen nicht korrekt berechnet werden,
- die Verfahrbefehle im falschen Bezugssystem ausgeführt werden,
- die inverse Kinematik nicht korrekt angewendet wird,
- oder die Modi „Werkzeug“ und „Koordinaten“ aktuell nicht sauber voneinander getrennt sind.

Zusätzlich scheint sich der Roboter im Modus **Koordinaten** und **Werkzeug** nahezu identisch zu verhalten, obwohl diese Modi in der Robotik unterschiedliche Bedeutungen haben.

---

## Ziel

Analysiere die aktuelle Implementierung der manuellen Verfahrfunktionen und erarbeite ein Konzept, das sich an etablierten Robotik-Standards orientiert.

Falls die bestehende Architektur unnötig komplex oder konzeptionell falsch aufgebaut ist, darf eine umfassende Überarbeitung oder ein kompletter Neuaufbau der betroffenen Bereiche vorgeschlagen werden.

Ziel ist eine saubere, verständliche und mathematisch korrekte Lösung.

---

## Untersuchungsumfang

Analysiere die komplette Befehlskette:

- HMI
- Manuelle Bedienung
- Jog-Funktionen
- Robot Controller
- Vorwärtskinematik
- Inverse Kinematik
- Transformationsberechnungen
- TCP-Verwaltung
- Bewegungsplanung
- 3D-Simulation

Verfolge den Weg eines Tastendrucks vom HMI bis zur tatsächlichen Roboterbewegung.

---

# Fachliches Zielbild

Erarbeite ein Konzept basierend auf den Standards industrieller Robotersysteme wie:

- ABB
- KUKA
- FANUC
- Yaskawa
- Universal Robots

---

## 1. Joint-Modus

Im Joint-Modus werden die einzelnen Achsen direkt verfahren.

Eigenschaften:

- Jede Achse wird unabhängig bewegt.
- Die TCP-Bewegung ergibt sich aus der Kinematik.
- Es wird keine kartesische Bahn garantiert.
- Es findet keine direkte Steuerung des TCP statt.

Beispiele:

- Achse 1 +
- Achse 1 -
- Achse 2 +
- Achse 2 -
- Z +
- Z -

Erwartetes Verhalten:

- Direkte Achsbewegung
- Keine lineare TCP-Bahn erforderlich

---

## 2. Koordinaten-Modus

Prüfe, ob die aktuelle Bezeichnung „Koordinaten“ sinnvoll ist.

Mögliche Alternativen:

- Welt
- Basis
- Kartesisch
- World
- Base

Eigenschaften:

- Bewegungen erfolgen relativ zum Basiskoordinatensystem des Roboters.
- X+, X-, Y+, Y-, Z+, Z- beziehen sich immer auf die festen Weltachsen.
- Die Werkzeugausrichtung beeinflusst die Bewegungsrichtung nicht.
- Der TCP muss sich linear bewegen.

Beispiel:

Wird X+ gedrückt, bewegt sich der TCP immer entlang der positiven Welt-X-Achse, unabhängig von der aktuellen Werkzeugausrichtung.

---

## 3. Werkzeug-Modus

Im Werkzeug-Modus erfolgen Bewegungen relativ zum TCP-Koordinatensystem.

Eigenschaften:

- Bewegungen beziehen sich auf die lokale Werkzeugorientierung.
- Die aktuelle TCP-Ausrichtung bestimmt die Bewegungsrichtung.
- Der TCP muss sich trotzdem linear bewegen.
- Die resultierende Weltbewegung kann je nach Werkzeugausrichtung unterschiedlich sein.

Beispiel:

Ist das Werkzeug um 90° gedreht, muss sich X+ entlang der lokalen Werkzeug-X-Achse bewegen und nicht entlang der Welt-X-Achse.

---

# Analyseaufgaben

## 1. Ist-Analyse

Dokumentiere:

- Wie Joint aktuell implementiert ist.
- Wie Koordinaten aktuell implementiert ist.
- Wie Werkzeug aktuell implementiert ist.
- Welche Transformationen verwendet werden.
- Welche Koordinatensysteme existieren.
- Wo die aktuelle Implementierung von den Robotik-Standards abweicht.

---

## 2. Ursachenanalyse

Finde die genaue Ursache dafür, dass:

- sich der TCP im Werkzeugmodus auf einer Bogenbahn bewegt,
- Werkzeug und Koordinaten nahezu identisch reagieren,
- die Transformationen möglicherweise fehlerhaft sind.

Identifiziere die verantwortlichen:

- Dateien
- Klassen
- Module
- Funktionen

und dokumentiere deren aktuelle Arbeitsweise.

---

## 3. Architekturvorschlag

Entwirf eine saubere Architektur für alle Verfahrmodi.

Anforderungen:

- Klare Trennung zwischen Joint, Koordinaten und Werkzeug.
- Einheitliche Transformationslogik.
- Keine doppelte Berechnung in mehreren Modulen.
- Korrekte TCP-Verwaltung.
- Erweiterbar für zukünftige Robotertypen.

---

## 4. Überprüfung der Begrifflichkeiten

Bewerte die aktuelle Benennung der Modi.

Prüfe, ob folgende Bezeichnungen verständlicher wären:

| Aktuell     | Vorschlag |
| ----------- | --------- |
| Koordinaten | Welt      |
| Koordinaten | Basis     |
| Werkzeug    | TCP       |
| Joint       | Achsen    |

Begründe die Empfehlung anhand gängiger Robotik-Standards.

---

## 5. Refactoring-Konzept

Falls die aktuelle Architektur grundlegende Schwächen aufweist:

- Erstelle einen Vorschlag für eine vollständige Überarbeitung.
- Vereinfache die Logik.
- Reduziere technische Schulden.
- Schaffe eine langfristig wartbare Lösung.

Ein größerer Umbau ist ausdrücklich erlaubt, wenn dadurch die Verständlichkeit und Korrektheit verbessert werden.

---

# Test- und Validierungskonzept

Definiere konkrete Tests für jeden Modus.

## Joint

- Einzelne Achsen verfahren
- Achsbewegungen überprüfen
- TCP-Verhalten dokumentieren

## Koordinaten

- Lineare Bewegung entlang Weltachsen
- Werkzeugorientierung darf Bewegungsrichtung nicht beeinflussen

## Werkzeug

- Lineare Bewegung entlang Werkzeugachsen
- Werkzeugorientierung muss Bewegungsrichtung beeinflussen
- Keine Bogenbahnen bei einfachen Verfahrbefehlen

## Sonderfälle

- Moduswechsel während der Bedienung
- Große Werkzeugrotationen
- Achsgrenzen
- Singularitäten
- HMI-Overrides

---

# Erwartete Ergebnisse

1. Analyse der aktuellen Implementierung.
2. Identifikation der Ursache für das Fehlverhalten.
3. Empfehlung eines Robotik-konformen Konzepts für Joint-, Koordinaten- und Werkzeugmodus.
4. Architekturvorschlag.
5. Refactoring-Plan.
6. Test- und Validierungskonzept.
7. Empfehlung für eine bessere Benennung der Modi im HMI.

## Arbeitsanweisung

Bitte nicht sofort mit Codeänderungen beginnen.

Analysiere zuerst die gesamte Architektur, die Transformationsketten, die Kinematik sowie die aktuelle Implementierung der Verfahrmodi.

Vergleiche das bestehende Verhalten mit den Standards industrieller Robotersysteme und schlage anschließend die einfachste, mathematisch korrekte und langfristig wartbare Lösung vor.
