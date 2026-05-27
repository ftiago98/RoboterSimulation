import pyvista as pv
import os

class RobotViewer:
    """
    Diese Klasse lädt die 3D-Modelle des Roboters und stellt ein Fenster
    zur Verfügung, um den Roboter von außen zu steuern.
    """
    
    def __init__(self, data_folder_path=None):
        # 1. Pfade konfigurieren
        # Wenn kein Pfad übergeben wird, nutze den Standardpfad (cwd/View/data)
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

        # Wir speichern die 'Actors' als Attribute der Klasse (self.xyz), 
        # damit wir später in anderen Methoden darauf zugreifen können.
        self.base_actor = self.pl.add_mesh(base_mesh, color="lightblue")
        self.inner_arm_actor = self.pl.add_mesh(inner_arm_mesh, color="orange")
        self.outer_arm_actor = self.pl.add_mesh(outer_arm_mesh, color="green")
        self.spindle_actor = self.pl.add_mesh(spindle_mesh, color="gray")


        # 4. Verschiebungen zu Koordinatien 0
        self.inner_arm_actor.origin = (0.0, 100.0, 50.0)
        self.outer_arm_actor.origin = (-325.0, 0.0, 0.0)
        self.spindle_actor.origin = (-550, 0.0, 0.0)

        # 5. Kamera einstellen
        self.pl.camera_position = [
            (0.0, -1500.0, 850.0),  # Position der Kamera
            (0.0, 0.0, 0.0),        # Fokuspunkt
            (0.0, 1.0, 0.0)         # Oben-Vektor
        ]

    def show(self):
        """
        Öffnet das Fenster im interaktiven Modus.
        """
        self.pl.show(interactive_update=True)

    def update_joints(self, inner_angle=0, outer_angle=0, spindle_angle=0):
        """
        Aktualisiert die Position der Roboterarme und zeichnet das Bild neu.
        
        Parameter:
        - inner_angle: Drehung des inneren Arms (Z-Achse)
        - outer_angle: Drehung des äußeren Arms (Z-Achse)
        - spindle_angle: Drehung der Spindel (Z-Achse)
        """
        # Setze die Orientierung [X, Y, Z] für die jeweiligen Bauteile
        self.inner_arm_actor.orientation = [0, 0, inner_angle]
        self.outer_arm_actor.orientation = [0, 0, outer_angle]
        self.spindle_actor.orientation = [0, 0, spindle_angle]
        

        # Zwingt PyVista, das Bild mit der neuen Position neu zu zeichnen
        self.pl.update()
        
    def close(self):
        """
        Schließt das PyVista Fenster sauber.
        """
        self.pl.close()


robot = RobotViewer()
robot.show()     
