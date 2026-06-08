"""
Modul zur 3D-Visualisierung und kinematischen Steuerung eines Roboterarms.

Dieses Modul nutzt `pyvista` und `vtk`, um die STL-Modelle eines mehrgliedrigen 
Roboters (Basis, innerer Arm, äusserer Arm, Spindel) zu laden, grafisch darzustellen 
und durch Vorwärtskinematik hierarchisch zu animieren.
"""
import sys
sys.path.append('../View')

import pyvista as pv
import os
import vtk

class Scara:
    """
    Lädt die 3D-Modelle des Roboters und stellt eine interaktive Umgebung zur Steuerung bereit.

    Die Klasse baut eine Szene mit PyVista auf und verknüpft die einzelnen Roboterbauteile 
    hierarchisch (Basis -> Innerer Arm -> Äusserer Arm -> Spindel). Dadurch übertragen sich 
    die Bewegungen der übergeordneten Glieder automatisch auf die untergeordneten.

    Args:
        data_folder_path (str, optional): Der absolute oder relative Dateipfad zum Verzeichnis 
            mit den STL-Dateien ('Base.stl', 'InnerArm.stl', 'OuterArm.stl', 'Spindle.stl'). 
            Wird `None` übergeben, sucht das Skript standardmässig in './View/data'.

    Attributes:
        pl (pyvista.Plotter): Das PyVista-Plotter-Objekt für die 3D-Szene.
        origin_inner (tuple): Der (x, y, z)-Rotationsursprung des inneren Arms.
        origin_outer (tuple): Der (x, y, z)-Rotationsursprung des äusseren Arms.
        origin_spindle (tuple): Der (x, y, z)-Rotationsursprung der Spindel.
    """
    
    def __init__(self, data_folder_path=None):
        """Initialisiert den viewScadaRoboter, lädt die Meshes und konfiguriert die Kamera."""
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

        # 3. Plotter und Szene aufbauen
        self.pl = pv.Plotter()

        self.base_actor = self.pl.add_mesh(base_mesh, color="lightblue")
        self.inner_arm_actor = self.pl.add_mesh(inner_arm_mesh, color="orange")
        self.outer_arm_actor = self.pl.add_mesh(outer_arm_mesh, color="green")
        self.spindle_actor = self.pl.add_mesh(spindle_mesh, color="gray")

        # 4. Koordinaten der Drehpunkte aus dem CAD-Programm
        self.origin_inner = (0.0, 0, 0)
        self.origin_outer = (-325.0, 0.0, 0.0)
        self.origin_spindle = (-550.0, 0.0, 0.0)

        # Setze die PyVista Origins (unterstützt die korrekte visuelle Darstellung)
        self.inner_arm_actor.origin = self.origin_inner
        self.outer_arm_actor.origin = self.origin_outer
        self.spindle_actor.origin = self.origin_spindle

        # 5. Kamera einstellen
        self.pl.camera_position = [
            (0.0, -1500.0, 850.0),  # Position der Kamera
            (0.0, 0.0, 0.0),        # Fokuspunkt
            (0.0, 1.0, 0.0)         # Oben-Vektor
        ]

    def _create_rotation(self, origin, angle):
        """
        Hilfsmethode: Erstellt eine VTK-Transformation für die Rotation um die Z-Achse.

        Die Transformation verschiebt das Objekt zunächst in den Nullpunkt, führt die 
        Rotation aus und schiebt es anschliessend wieder an den ursprünglichen Ort zurück.

        Args:
            origin (tuple): Die (x, y, z)-Koordinaten des gewünschten Drehpunkts.
            angle (float): Der Rotationswinkel in Grad.

        Returns:
            vtk.vtkTransform: Das konfigurierte VTK-Transformationsobjekt.
        """
        transform = vtk.vtkTransform()
        transform.PostMultiply()
        
        # Verschieben zum Nullpunkt -> Drehen -> Zurückschieben
        transform.Translate(-origin[0], -origin[1], -origin[2])
        transform.RotateZ(angle) 
        transform.Translate(origin[0], origin[1], origin[2])
        
        return transform

    def show(self):
        """Öffnet das 3D-Fenster im interaktiven Modus, sodass Positionsupdates sichtbar werden."""
        self.pl.show(interactive_update=True)

    def update_joints(self, inner_angle=0, outer_angle=0, spindle_angle=0):
        """
        Aktualisiert die Gelenkwinkel und berechnet die neue Position der Roboterarme.

        Die Methode wendet Vorwärtskinematik an, indem sie die VTK-Transformationen 
        verkettet. Der äussere Arm erbt die Rotation des inneren Arms, und die Spindel 
        erbt die Rotationen beider übergeordneten Arme.

        Args:
            inner_angle (float, optional): Der Rotationswinkel des inneren Arms in Grad. Standard ist 0.
            outer_angle (float, optional): Der relative Rotationswinkel des äusseren Arms in Grad. Standard ist 0.
            spindle_angle (float, optional): Der relative Rotationswinkel der Spindel in Grad. Standard ist 0.
        """
        # --- 1. Innerer Arm ---
        t_inner = self._create_rotation(self.origin_inner, inner_angle)
        self.inner_arm_actor.SetUserTransform(t_inner)

        # --- 2. Äusserer Arm (Kind vom inneren Arm) ---
        t_outer = vtk.vtkTransform()
        t_outer.PostMultiply()
        t_outer.Concatenate(self._create_rotation(self.origin_outer, outer_angle))
        t_outer.Concatenate(t_inner) # Hier wird die Bewegung verknüpft!
        self.outer_arm_actor.SetUserTransform(t_outer)

        # --- 3. Spindel (Kind vom äusseren Arm) ---
        t_spindle = vtk.vtkTransform()
        t_spindle.PostMultiply()
        t_spindle.Concatenate(self._create_rotation(self.origin_spindle, spindle_angle))
        t_spindle.Concatenate(t_outer) # Verknüpfung mit dem äusseren Arm
        self.spindle_actor.SetUserTransform(t_spindle)

        # Zwingt PyVista, das Bild neu zu zeichnen
        self.pl.update()
        
    def close(self):
        """Schliesst das PyVista-Darstellungsfenster sauber und gibt die Ressourcen frei."""
        self.pl.close()


# --- Test-Aufruf ---
if __name__ == "__main__":
    import time
    robot = Scara()
    robot.show()
    
    # Kurzer Test, um zu sehen, ob die Spindel mitfährt
    print("Starte kurzen Bewegungstest...")
    for i in range(500):
        # Drehe den inneren Arm und den äusseren Arm gleichzeitig
        robot.update_joints(inner_angle=i, outer_angle=-i*0.5, spindle_angle=i*2)
        time.sleep(0.05)
        
    print("Test beendet.")