"""
Modul zur 3D-Visualisierung und kinematischen Steuerung eines Roboterarms.
"""

import sys
sys.path.append('../View')

import pyvista as pv
import os
import vtk


class Scara:
    """
    Lädt die 3D-Modelle des Roboters und stellt eine interaktive Umgebung zur Steuerung bereit.
    """

    def __init__(self, data_folder_path=None, pl=None, position=(0, 0, 0)):
        """
        Initialisiert den SCARA-Roboter.

        Args:
            data_folder_path (str, optional): Pfad zum STL-Ordner.
            pl (pyvista.Plotter, optional): Gemeinsames PyVista-Fenster.
            position (tuple): Verschiebung des ganzen Roboters, z.B. (0, 800, 0)
        """

        # Position / Offset des ganzen Roboters
        self.position = position

        # 1. Pfade konfigurieren
        if data_folder_path is None:
            cwd = os.getcwd()
            data_folder_path = os.path.join(cwd, "View", "data")

        base_file = os.path.join(data_folder_path, "Base.stl")
        inner_arm_file = os.path.join(data_folder_path, "InnerArm.stl")
        outer_arm_file = os.path.join(data_folder_path, "OuterArm.stl")
        spindle_file = os.path.join(data_folder_path, "Spindle.stl")

        # 2. Modelle einlesen
        base_mesh = pv.read(base_file)
        inner_arm_mesh = pv.read(inner_arm_file)
        outer_arm_mesh = pv.read(outer_arm_file)
        spindle_mesh = pv.read(spindle_file)

        # 3. Ganzen Roboter verschieben
        # Wichtig: Die Meshes UND die Drehpunkte werden verschoben,
        # damit die Rotation weiterhin korrekt funktioniert.
        base_mesh.translate(self.position, inplace=True)
        inner_arm_mesh.translate(self.position, inplace=True)
        outer_arm_mesh.translate(self.position, inplace=True)
        spindle_mesh.translate(self.position, inplace=True)

        # 4. Plotter verwenden oder eigenen erstellen
        if pl is None:
            self.pl = pv.Plotter()
        else:
            self.pl = pl

        # 5. Meshes in die Szene einfügen
        self.base_actor = self.pl.add_mesh(base_mesh, color="lightblue")
        self.inner_arm_actor = self.pl.add_mesh(inner_arm_mesh, color="orange")
        self.outer_arm_actor = self.pl.add_mesh(outer_arm_mesh, color="green")
        self.spindle_actor = self.pl.add_mesh(spindle_mesh, color="gray")

        # 6. Original-Drehpunkte aus dem CAD
        original_origin_inner = (0.0, 0.0, 0.0)
        original_origin_outer = (-325.0, 0.0, 0.0)
        original_origin_spindle = (-550.0, 0.0, 0.0)

        # 7. Drehpunkte auch verschieben
        self.origin_inner = (
            original_origin_inner[0] + self.position[0],
            original_origin_inner[1] + self.position[1],
            original_origin_inner[2] + self.position[2]
        )

        self.origin_outer = (
            original_origin_outer[0] + self.position[0],
            original_origin_outer[1] + self.position[1],
            original_origin_outer[2] + self.position[2]
        )

        self.origin_spindle = (
            original_origin_spindle[0] + self.position[0],
            original_origin_spindle[1] + self.position[1],
            original_origin_spindle[2] + self.position[2]
        )

        # PyVista Origins setzen
        self.inner_arm_actor.origin = self.origin_inner
        self.outer_arm_actor.origin = self.origin_outer
        self.spindle_actor.origin = self.origin_spindle

        # 8. Kamera einstellen
        self.pl.camera_position = [
            (200.0, -1800.0, 1000.0),  # Position der Kamera
            (0.0, 400.0, 0.0),         # Fokuspunkt ungefähr zwischen beiden Robotern
            (0.0, 0.0, 1.0)            # Oben-Vektor
        ]

    def _create_rotation(self, origin, angle):
        """
        Erstellt eine Rotation um die Z-Achse um einen bestimmten Drehpunkt.
        """

        transform = vtk.vtkTransform()
        transform.PostMultiply()

        # Zum Drehpunkt verschieben -> rotieren -> zurück
        transform.Translate(-origin[0], -origin[1], -origin[2])
        transform.RotateZ(angle)
        transform.Translate(origin[0], origin[1], origin[2])

        return transform

    def show(self):
        """
        Öffnet das 3D-Fenster.
        """
        self.pl.show(interactive_update=True, auto_close=False)

    def update_joints(self, inner_angle=0, outer_angle=0, spindle_angle=0):
        """
        Aktualisiert die Gelenkwinkel des Roboters.
        """

        # 1. Innerer Arm
        t_inner = self._create_rotation(self.origin_inner, inner_angle)
        self.inner_arm_actor.SetUserTransform(t_inner)

        # 2. Äusserer Arm folgt dem inneren Arm
        t_outer = vtk.vtkTransform()
        t_outer.PostMultiply()
        t_outer.Concatenate(self._create_rotation(self.origin_outer, outer_angle))
        t_outer.Concatenate(t_inner)
        self.outer_arm_actor.SetUserTransform(t_outer)

        # 3. Spindel folgt äusserem und innerem Arm
        t_spindle = vtk.vtkTransform()
        t_spindle.PostMultiply()
        t_spindle.Concatenate(self._create_rotation(self.origin_spindle, spindle_angle))
        t_spindle.Concatenate(t_outer)
        self.spindle_actor.SetUserTransform(t_spindle)

        # Fenster aktualisieren
        self.pl.update()

    def close(self):
        """
        Schliesst das PyVista-Fenster.
        """
        self.pl.close()


# --- Test-Aufruf ---
if __name__ == "__main__":
    import time

    # Gemeinsames Fenster
    plotter = pv.Plotter()

    # Roboter 1 bleibt an Originalposition
    robot1 = Scara(pl=plotter, position=(0, 0, 0))

    # Roboter 2 wird 800 mm in Y-Richtung verschoben
    # Falls sie immer noch zu nahe sind: 800 auf 1000 oder 1200 erhöhen.
    robot2 = Scara(pl=plotter, position=(0, 800, 0))

    plotter.show_axes()
    plotter.show(interactive_update=True, auto_close=False)

    print("Starte kurzen Bewegungstest...")

    for i in range(500):
        robot1.update_joints(
            inner_angle=i,
            outer_angle=-i * 0.5,
            spindle_angle=i * 2
        )

        robot2.update_joints(
            inner_angle=i + 80,
            outer_angle=-i * 0.5 + 60,
            spindle_angle=i * 2
        )

        time.sleep(0.05)

    print("Test beendet.")