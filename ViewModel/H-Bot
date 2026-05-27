class HBotModel:
    """Hält den realen Zustand des Roboters."""
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.motor1 = 0.0
        self.motor2 = 0.0

class HBotViewModel:
    """Verbindet die GUI/UI-Logik mit der H-Bot-Kinematik."""
    def __init__(self, model: HBotModel):
        self._model = model
        
    # --- Getters für die UI ---
    @property
    def current_position(self):
        return {"X": self._model.x, "Y": self._model.y}
    
    @property
    def motor_steps(self):
        return {"Motor1": self._model.motor1, "Motor2": self._model.motor2}
    
    # --- Befehle (Commands) für die UI ---
    def move_to_target(self, target_x: float, target_y: float):
        """Berechnet die benötigten Motorschritte für eine Zielkoordinate (Inverskinematik)."""
        # In einem echten MVVM-Szenario würde man hier ggf. auch Validierungen durchführen
        # (z.B. ob die Zielkoordinaten außerhalb des Arbeitsraums liegen).
        
        # Berechnung der Delta-Schritte basierend auf der H-Bot Formel
        self._model.motor1 = target_x + target_y
        self._model.motor2 = target_x - target_y
        
        # Aktualisiere die aktuelle Position im Modell
        self._model.x = target_x
        self._model.y = target_y
        
        print(f"[ViewModel] Ziel erreicht: X={self._model.x}, Y={self._model.y}")
        print(f"[ViewModel] Berechnete Motorpositionen -> M1: {self._model.motor1}, M2: {self._model.motor2}")

    def update_from_motors(self, m1_steps: float, m2_steps: float):
        """Berechnet die X/Y Position basierend auf den Motorschritten (Vorwärtskinematik)."""
        self._model.motor1 = m1_steps
        self._model.motor2 = m2_steps
        
        # Vorwärtskinematik anwenden
        self._model.x = (m1_steps + m2_steps) / 2
        self._model.y = (m1_steps - m2_steps) / 2


# --- TEST DES VIEWMODELS (Simulierter UI-Aufruf) ---
if __name__ == "__main__":
    # 1. Model und ViewModel instanziieren
    robot_model = HBotModel()
    view_model = HBotViewModel(robot_model)
    
    print("--- Befehl: Fahre zu X=50, Y=20 ---")
    view_model.move_to_target(50, 20)
    
    print("\n--- Befehl: Motoren haben sich bewegt (M1=100, M2=0) ---")
    view_model.update_from_motors(100, 0)
    print(f"UI Anzeige aktuelle Position: {view_model.current_position}")