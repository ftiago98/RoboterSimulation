import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import hmiControl

class Hmi:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HMI Roboter")
        self.root.configure(background="lightblue")
        self.root.minsize(400, 400)

        # Instanz der Steuerung
        self.hmiControl = hmiControl.hmiControl()

        # Layout-Positionen
        links = 10
        rechts = 250
        unten = 350

        # --- EVENT HANDLER (BINDINGS) ---
        
        def on_coord_changed(event):
            # Holt den aktuellen Text aus der ersten Combobox
            selected = combo_axis.get()
            self.hmiControl.CoordSystem = selected
            print(f"Koordinatensystem geändert auf: {selected}")

        def on_mode_changed(event):
            # Holt den aktuellen Text aus der Modus-Combobox
            selected = combo_mode.get()
            if selected == "Hand":
                self.hmiControl.OperationMode = 0
            elif selected == "Automatisch":
                self.hmiControl.OperationMode = 1
            print(f"Betriebsmodus geändert auf: {selected} (Wert: {self.hmiControl.OperationMode})")

        def on_start_click():
            self.hmiControl.Start = True
            self.hmiControl.Stop = False
            print("Roboter gestartet (Start=True)")

        def on_stop_click():
            self.hmiControl.Start = False
            self.hmiControl.Stop = True
            print("Roboter gestoppt (Stop=True)")
            self.root.destroy()

        # --- UI ELEMENTE ---

        # Titel
        titel = tk.Label(self.root, text="Roboter Steuerung", bg="lightblue", font=("Arial", 12, "bold"))
        titel.pack(pady=5)

        # Knöpfe
        button_stop = tk.Button(self.root, text="Stop", activebackground="red", width=15, command=on_stop_click)
        button_stop.place(x=rechts, y=unten)

        button_start = tk.Button(self.root, text="Start", activebackground="green", width=15, command=on_start_click)
        button_start.place(x=links, y=unten)

        # Combobox: Achse / Koordinatensystem
        combo_axis = ttk.Combobox(
            self.root,
            values=["Welt", "Joint", "Werkzeug"],
            state="readonly"
        )
        combo_axis.set("wählen")
        combo_axis.bind("<<ComboboxSelected>>", on_coord_changed)
        combo_axis.place(x=links, y=40)

        # Combobox: Auto / Manuell
        combo_mode = ttk.Combobox(
            self.root,
            values=["Hand", "Automatisch"],
            state="readonly"
        )
        combo_mode.set("wählen")
        combo_mode.bind("<<ComboboxSelected>>", on_mode_changed)
        combo_mode.place(x=rechts, y=40)

        # Achsen-Labels
        labels = ["X :", "Y :", "Z :", "R :"]
        for i, text in enumerate(labels):
            lbl = tk.Label(self.root, text=text, bg="lightblue")
            lbl.place(x=links, y=100 + (i * 25))

        # Werte-Labels (X, Y, Z, R)
        self.x_label = tk.Label(self.root, text="000", font=("Arial", 10), bg="lightblue")
        self.x_label.place(x=links + 30, y=100)

        self.y_label = tk.Label(self.root, text="000", font=("Arial", 10), bg="lightblue")
        self.y_label.place(x=links + 30, y=125)

        self.z_label = tk.Label(self.root, text="000", font=("Arial", 10), bg="lightblue")
        self.z_label.place(x=links + 30, y=150)

        self.r_label = tk.Label(self.root, text="000", font=("Arial", 10), bg="lightblue")
        self.r_label.place(x=links + 30, y=175)


# --- Test-Aufruf ---
if __name__ == "__main__":
    hmi = Hmi()
    hmi.root.mainloop()
    
    # Zeigt nach dem Schließen den letzten Zustand des Modus an
    print(f"Letzter Betriebsmodus im Control-Objekt: {hmi.hmiControl.OperationMode}")