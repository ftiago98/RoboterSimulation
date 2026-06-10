# SCARA Robot – Kinematik- und Transformationsproblem (Critical Issue)

## 🧠 Problemübersicht

Im aktuellen System ist die manuelle Verfahrfunktion im Koordinaten-/World-Modus nicht korrekt implementiert.

Das Verhalten deutet auf grundlegende Fehler in der Kinematik- oder Transformationslogik hin.

---

## ❌ Beobachtetes Fehlverhalten

- Wenn nur die X-Koordinate erhöht wird (X+),
  verändert sich gleichzeitig auch die Y-Koordinate.
- Der TCP bewegt sich nicht linear, sondern auf einer Bogenbahn.
- Tool Mode und World/Coordinate Mode verhalten sich nahezu identisch.

---

## ✅ Erwartetes Verhalten (Industrie-Standard)

### 🌍 World / Koordinaten-Modus

- X+ verändert ausschließlich X
- Y bleibt konstant
- TCP bewegt sich linear im kartesischen Raum
- Werkzeugorientierung beeinflusst die Richtung nicht

---

### 🛠 Tool / TCP-Modus

- Bewegung erfolgt entlang der Werkzeugachse
- TCP bewegt sich linear im Raum
- Tool-Orientierung beeinflusst Bewegungsrichtung im Weltkoordinatensystem

---

### 🤖 Joint-Modus

- Direkte Achsbewegung
- Keine kartesische Linearität erforderlich
- TCP ergibt sich nur aus FK

---

## 🚨 Vermutete Hauptursachen

### ❌ 1. Falsche Transformationsreihenfolge

Z- und Positionsbewegungen werden im rotierten Koordinatensystem angewendet:

```python
t_spindle.Concatenate(t_outer)
t_spindle.Translate(0.0, 0.0, z_height)
```

### ❌ 2. Vermischung von Frames ohne klare Struktur

Aktuell existieren keine klare Trennung zwischen:

- Base Frame
- Joint Frame
- Tool Frame

Ergebnis:
Bewegung in X beeinflussen automatisch Y

### ❌ 3. Verkettung ohne kontrolliertes Kinematikmodell

Aktuell wird verwendet:

```python
Concatenate(t_inner)
Concatenate(t_outer)
```

ohne definierte kinematische Struktur.
Unkontrollierte Abhängigkeiten zwischen Gelenken.

### ❌ 4. Tool und World Mode sind faktisch identisch

Beide Modi nutzen dieselbe Transformationslogik.
Ergebnis:

- Kein Unterschied zwischen Tool- und World-Bewegung
- Fehlende Frame-Trennung

### 1.Fix

# FALSCH:

t_spindle.Translate(0, 0, z)

# RICHTIG:

Z-Bewegung muss im World/Base Frame berechnet werden
und darf nicht nach Rotation angewendet werden

### 2.Fix

klare, hierarchische Kinematik-Struktur einführen

# kritisch vermeiden:

Concatenate(t_inner)
Concatenate(t_outer)

### 3.Fix

Das System muss in klar getrennte Frames strukturiert werden:

BaseFrame
├── Joint1Frame
├── Joint2Frame
├── ZFrame
└── ToolFrame (TCP)
