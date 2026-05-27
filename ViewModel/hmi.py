import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.title("HMI Roboter")
root.configure(background="lightblue")
root.minsize(400, 400)


#Positionen

links = 10
rechts = 250
mitte = 200
unten= 350

tk.Label(root, text="Roboter Steuerung").pack()


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

tk.Label(root, text="X")
tk.Label(root, text="Y")
tk.Label(root, text="Z")
tk.Label(root, text="R")









root.mainloop()


