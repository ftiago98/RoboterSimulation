import tkinter as tk
import tkinter.messagebox
from tkinter import ttk


root = tk.Tk()

root.title("HMI Roboter")
root.configure(background="lightblue")
root.minsize(400, 400)


#Positionen

links = 10
rechts = 250
mitte = 200
oben = 10
unten = 350

#Titel 

Titel = tk.Label(root, text="Roboter Steuerung").pack()

# Knöpfe

button1 = tk.Button(root, text="Stop", activebackground="red", width=25, command=root.destroy)
button1.pack()

button1.place(x=rechts-45, y=unten)

button2 = tk.Button(root, text="Start", activebackground="green", width=25)

button2.pack()

button2.place(x=links, y=unten)


def select(event):
    selected_item = combo_box.get()



# Achse 

combo_box = ttk.Combobox(
    root,
    values=["Welt", "Joint", "Werkzeug"],
    state="readonly"
)
combo_box.pack(pady=5)

combo_box.set("wählen")

combo_box.bind("<<ComboboxSelected>>", select)

combo_box.place(x=links, y= 40)

# Auto / Manuell

combo_box = ttk.Combobox(
    root,
    values=["Hand", "Automatisch"],
    state="readonly"
)
combo_box.pack(pady=5)

combo_box.set("wählen")

combo_box.bind("<<ComboboxSelected>>", select)

combo_box.place(x=rechts, y= 40)

# Achse

Label1 = tk.Label(root, text="X :")
Label2 = tk.Label(root, text="Y :")
Label3 = tk.Label(root, text="Z :")
Label4 = tk.Label(root, text="R :")

Label1.place(x=links, y=100)
Label2.place(x=links, y=125)
Label3.place(x=links, y=150)
Label4.place(x=links, y=175)

# X-Achse
x_label = tk.Label(root, text="0", font=("Arial", 10))
x_label.pack(pady=5)

x_label.place(x=links + 30, y=100)

# Y-Achse
y_label = tk.Label(root, text="0", font=("Arial", 10))
y_label.pack(pady=5)

y_label.place(x=links + 30, y=125)

# Z-Achse
z_label = tk.Label(root, text="0", font=("Arial", 10))
z_label.pack(pady=5)

z_label.place(x=links + 30, y=150)

# R-Achse
r_label = tk.Label(root, text="0", font=("Arial", 10))
r_label.pack(pady=5)

r_label.place(x=links + 30, y=175)

# Beispielwerte setzen
x_label.config(text="000")
y_label.config(text="000")
z_label.config(text="000")
r_label.config(text="000")

tkinter.messagebox.showerror(title="Achtung!", message="Koordinaten überschneiden sich!")

root.mainloop()


