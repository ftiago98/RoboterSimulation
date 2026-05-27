import pyvista as pv
import os
import time

# 1. Sichere Pfaderstellung
cwd = os.getcwd()
base_file = os.path.join(cwd, "View", "data", "Base.stl")
inner_arm_file = os.path.join(cwd, "View", "data", "InnerArm.stl")
outer_arm_file = os.path.join(cwd, "View", "data", "OuterArm.stl")
Spindle_file = os.path.join(cwd, "View", "data", "Spindle.stl")

# 2. Modelle einlesen
base_mesh = pv.read(base_file)
inner_arm_mesh = pv.read(inner_arm_file)
outer_arm_mesh = pv.read(outer_arm_file)
Spindle_mesh = pv.read(Spindle_file)

# 3. Plotter und Szene aufbauen
pl = pv.Plotter()

# Optional: Farben hinzugefügt, um die Bauteile besser unterscheiden zu können
base_actor = pl.add_mesh(base_mesh, color="lightblue")
inner_arm_actor = pl.add_mesh(inner_arm_mesh, color="orange")
outer_arm_actor = pl.add_mesh(outer_arm_mesh, color="green")
Spindle_actor = pl.add_mesh(Spindle_mesh, color="gray")

# 4. Kamera einstellen
pl.camera_position = [
    (0.0, -1500.0, 850.0),  # Position der Kamera
    (0.0, 0.0, 0.0),        # Punkt, auf den die Kamera schaut (Fokus)
    (0.0, 1.0, 0.0)         # Oben-Vektor (View up)
]

# 5. Fenster im Hintergrund öffnen
# interactive_update=True sorgt dafür, dass das Skript hier nicht stehen bleibt,
# sondern zur for-Schleife übergeht.
pl.show(interactive_update=True)

# 6. Manuelle Animationsschleife
print("Starte Animation...")

for step in range(5000):
    # Position des inneren Arms aktualisieren
    inner_arm_actor.orientation = [0, 0, step]
    
    # Position in der VS Code Konsole ausgeben
    print(f"Schritt: {step} | Arm Position: {inner_arm_actor.orientation}")
    
    # Zwingt PyVista, das Bild mit der neuen Position neu zu zeichnen
    pl.update()
    
    # 0.2 Sekunden (200 Millisekunden) warten, bevor der nächste Schritt berechnet wird
    time.sleep(0.2)

print("Animation beendet.")