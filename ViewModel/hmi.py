import tkinter as tk

root = tk.Tk()

root.title("HMI Roboter")
root.configure(background="lightblue")
root.minsize(200, 200)
root.maxsize(500, 500)
root.geometry("300x300+50+50")

tk.Label(root, text="Roboter Steuerung").pack()

widgets = [
    tk.Button,
]

for widget in widgets:
    try:
        widget = widget(root, text=widget.__name__)
    except tk.TclError:
        widget = widget(root)
    widget.pack(padx=5, pady=5, fill="x")



root.mainloop()


