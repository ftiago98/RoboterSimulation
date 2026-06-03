import os
import pyvista as pv


# ==========================================
# 1. MODEL
# ==========================================
class HBotModel:
    """Hält den aktuellen Zustand des H-Bots."""

    def __init__(self):
        self.x = 0.0
        self.y = 0.0


# ==========================================
# 2. VIEWMODEL
# ==========================================
class HBotViewModel:
    """Verbindet das mathematische Modell mit der PyVista 3D-Ansicht."""

    def __init__(self, model: HBotModel, viewer: "RobotViewer"):
        self._model = model
        self._viewer = viewer

    def move_to(self, target_x: float, target_y: float):
        """Berechnet die lineare Bewegung für die View-Komponenten."""
        # Speichere die Koordinaten im Modell
        self._model.x = target_x
        self._model.y = target_y

        # Übergabe der Verschiebungswerte an die View:
        # - Brücke (H-Bot 2) bewegt sich nur in Y
        # - Schlitten (H-Bot 3) fährt in Y mit der Brücke und in X autark
        self._viewer.update_mesh_positions(x_pos=target_x, y_pos=target_y)


# ==========================================
# 3. VIEW (Angepasst an deine STL-Dateien)
# ==========================================
class RobotViewer:
    """Lädt die 4 spezifischen H-Bot STL-Dateien und steuert deren Bewegung."""

    def __init__(self, data_folder_path=None):
        # 1. Pfade konfigurieren (Standard: Ordner der ausgeführten Datei)
        if data_folder_path is None:
            cwd = os.getcwd()
            data_folder_path = os.path.join(cwd, "View", "H-Bot Modell")

        # Zuordnung deiner hochgeladenen Dateien
        file_base_left = os.path.join(data_folder_path, "H-Bot 5.stl")
        file_base_right = os.path.join(data_folder_path, "H-Bot 1.stl")
        file_bridge = os.path.join(data_folder_path, "H-Bot 2.stl")
        file_tool = os.path.join(data_folder_path, "H-Bot 3.stl")

        # 2. Modelle einlesen
        mesh_base_left = pv.read(file_base_left)
        mesh_base_right = pv.read(file_base_right)
        mesh_bridge = pv.read(file_bridge)
        mesh_tool = pv.read(file_tool)

        # 3. Plotter aufbauen
        self.pl = pv.Plotter()

        # 4. Actors hinzufügen (Da die Teile im CAD matchen, nutzen wir standardmäßig origin=[0,0,0])
        self.base_l_actor = self.pl.add_mesh(
            mesh_base_left, color="lightblue", label="Basis Links"
        )
        self.base_r_actor = self.pl.add_mesh(
            mesh_base_right, color="lightblue", label="Basis Rechts"
        )
        self.bridge_actor = self.pl.add_mesh(
            mesh_bridge, color="orange", label="Y-Brücke"
        )
        self.tool_actor = self.pl.add_mesh(
            mesh_tool, color="green", label="X-Schlitten/Werkzeug"
        )

        # 5. Kamera für die Geometrie optimieren (Zentriert über dem H-Bot, Blick von schräg oben)
        self.pl.camera_position = [
            (375.0, -600.0, 700.0),  # Kameraposition (X zentriert auf 375)
            (375.0, 250.0, 0.0),  # Fokuspunkt (Zentrum des Rahmens)
            (0.0, 0.0, 1.0),  # Z-Achse zeigt nach oben
        ]
        self.pl.add_legend()
        self.pl.add_axes()

    def show(self):
        """Öffnet das Visualisierungsfenster."""
        self.pl.show(interactive_update=True)

    def update_mesh_positions(self, x_pos=0.0, y_pos=0.0):
        """Verschiebt die Komponenten basierend auf der H-Bot Mechanik."""
        # Die Basis-Teile (1 & 5) bleiben fest verankert
        self.base_l_actor.position = [0.0, 0.0, 0.0]
        self.base_r_actor.position = [0.0, 0.0, 0.0]

        # Die Brücke (2) verschiebt sich ausschließlich entlang der Y-Achse
        self.bridge_actor.position = [0.0, y_pos, 0.0]

        # Der Schlitten (3) fährt in Y mit der Brücke mit und bewegt sich in X auf ihr
        self.tool_actor.position = [x_pos, y_pos, 0.0]

        # Szene neu rendern
        self.pl.update()

    def close(self):
        """Schließt das Fenster."""
        self.pl.close()


# ==========================================
# ANWENDUNG STARTEN
# ==========================================
import time
import numpy as np

# ... (Deine Klassen HBotModel, HBotViewModel und RobotViewer bleiben gleich)

# ==========================================
# ANWENDUNG STARTEN MIT BEWEGUNGSSCHLAUFE
# ==========================================
if __name__ == "__main__":
    view = RobotViewer()
    model = HBotModel()
    view_model = HBotViewModel(model, view)

    # Fenster öffnen (interactive_update=True ist wichtig!)
    view.show()

    def animate_move(target_x, target_y, steps=50):
        """Bewegt den Roboter in kleinen Schritten zum Ziel."""
        start_x = view_model._model.x
        start_y = view_model._model.y
        
        # Erzeuge Zwischenschritte mit numpy
        x_path = np.linspace(start_x, target_x, steps)
        y_path = np.linspace(start_y, target_y, steps)
        
        for x, y in zip(x_path, y_path):
            view_model.move_to(x, y)
            time.sleep(0.01) # Kurze Pause für die Optik

    print("Starte Demo-Schlaufe... (Fenster bitte im Vordergrund lassen)")
    
    try:
        # Endlose Demo-Schleife: Der Roboter fährt ein Viereck ab
        while True:
            print("Fahre zu Punkt 1...")
            animate_move(150.0, 100.0)
            
            print("Fahre zu Punkt 2...")
            animate_move(-150.0, 100.0)
            
            print("Fahre zu Punkt 3...")
            animate_move(-150.0, -100.0)
            
            print("Fahre zu Punkt 4 (Ursprung)...")
            animate_move(0.0, 0.0)
            
    except Exception as e:
        print(f"Animation beendet oder Fenster geschlossen: {e}")