import sys
sys.path.append('../ViewModel')

import tkinter as tk
from tkinter import ttk
from hmiControl import hmiControl

class Hmi:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HMI Roboter")
        self.root.configure(background="lightblue")
        self.root.minsize(400, 400)

        # Instanz der Steuerung
        self.hmiControl = hmiControl()

        # Achsenwerte
        self.x_value = 0
        self.y_value = 0
        self.z_value = 0
        self.r_value = 0

        # Layout
        links = 10
        rechts = 250
        unten = 350

        # ---------------- EVENTS ----------------

        def on_coord_changed(event):
            selected = combo_axis.get()
            self.hmiControl.CoordSystem = selected
            print(f"Koordinatensystem geändert auf: {selected}")

        def on_mode_changed(event):
            selected = combo_mode.get()

            if selected == "Hand":
                self.hmiControl.OperationMode = 0
            elif selected == "Automatisch":
                self.hmiControl.OperationMode = 1

            print(f"Betriebsmodus geändert auf: {selected}")

        def on_start_click():
            self.hmiControl.Start = True
            self.hmiControl.Stop = False
            print("Start")

        def on_stop_click():
            self.hmiControl.Start = False
            self.hmiControl.Stop = True
            print("Stop")
            self.root.destroy()

        # ---------------- ACHSEN ----------------

        def x_plus():
            self.x_value += 1
            self.x_label.config(text=str(self.x_value))

        def x_minus():
            self.x_value -= 1
            self.x_label.config(text=str(self.x_value))

        def y_plus():
            self.y_value += 1
            self.y_label.config(text=str(self.y_value))

        def y_minus():
            self.y_value -= 1
            self.y_label.config(text=str(self.y_value))

        def z_plus():
            self.z_value += 1
            self.z_label.config(text=str(self.z_value))

        def z_minus():
            self.z_value -= 1
            self.z_label.config(text=str(self.z_value))

        def r_plus():
            self.r_value += 1
            self.r_label.config(text=str(self.r_value))

        def r_minus():
            self.r_value -= 1
            self.r_label.config(text=str(self.r_value))

        # ---------------- UI ----------------

        titel = tk.Label(
            self.root,
            text="Roboter Steuerung",
            bg="lightblue",
            font=("Arial", 12, "bold")
        )
        titel.pack(pady=5)

        button_start = tk.Button(
            self.root,
            text="Start",
            width=15,
            command=on_start_click
        )
        button_start.place(x=links, y=unten)

        button_stop = tk.Button(
            self.root,
            text="Stop",
            width=15,
            command=on_stop_click
        )
        button_stop.place(x=rechts, y=unten)

        # Koordinatensystem
        combo_axis = ttk.Combobox(
            self.root,
            values=["Welt", "Joint", "Werkzeug"],
            state="readonly"
        )
        combo_axis.set("wählen")
        combo_axis.bind("<<ComboboxSelected>>", on_coord_changed)
        combo_axis.place(x=links, y=40)

        # Betriebsart
        combo_mode = ttk.Combobox(
            self.root,
            values=["Hand", "Automatisch"],
            state="readonly"
        )
        combo_mode.set("wählen")
        combo_mode.bind("<<ComboboxSelected>>", on_mode_changed)
        combo_mode.place(x=rechts, y=40)

        # Beschriftungen
        tk.Label(self.root, text="X :", bg="lightblue").place(x=10, y=100)
        tk.Label(self.root, text="Y :", bg="lightblue").place(x=10, y=130)
        tk.Label(self.root, text="Z :", bg="lightblue").place(x=10, y=160)
        tk.Label(self.root, text="R :", bg="lightblue").place(x=10, y=190)

        # X
        self.x_label = tk.Label(self.root, text="0", bg="lightblue")
        self.x_label.place(x=40, y=100)

        tk.Button(self.root, text="+", width=3, command=x_plus).place(x=80, y=95)
        tk.Button(self.root, text="-", width=3, command=x_minus).place(x=120, y=95)

        # Y
        self.y_label = tk.Label(self.root, text="0", bg="lightblue")
        self.y_label.place(x=40, y=130)

        tk.Button(self.root, text="+", width=3, command=y_plus).place(x=80, y=125)
        tk.Button(self.root, text="-", width=3, command=y_minus).place(x=120, y=125)

        # Z
        self.z_label = tk.Label(self.root, text="0", bg="lightblue")
        self.z_label.place(x=40, y=160)

        tk.Button(self.root, text="+", width=3, command=z_plus).place(x=80, y=155)
        tk.Button(self.root, text="-", width=3, command=z_minus).place(x=120, y=155)

        # R
        self.r_label = tk.Label(self.root, text="0", bg="lightblue")
        self.r_label.place(x=40, y=190)

        tk.Button(self.root, text="+", width=3, command=r_plus).place(x=80, y=185)
        tk.Button(self.root, text="-", width=3, command=r_minus).place(x=120, y=185)


if __name__ == "__main__":
    hmi = Hmi()
    hmi.root.mainloop()

    print(
        f"Letzter Betriebsmodus: "
        f"{hmi.hmiControl.OperationMode}"
    )