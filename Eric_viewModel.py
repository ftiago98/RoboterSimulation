import pyvista as pv
import os

cwd = os.getcwd()

BaseMesh = pv.get_reader(cwd + "\\View\\data\\Base.stl").read()
InnerArmMesh = pv.get_reader(cwd + "\\View\\data\\InnerArm.stl").read()

pl = pv.Plotter()
base  = pl.add_mesh(BaseMesh,     color="lightgray")
actor = pl.add_mesh(InnerArmMesh, color="orange")

ziel_x, ziel_y, ziel_z = 1000, 2000, 100
max_steps = 200

def callback(step):
    base.SetPosition(0, 0, 0)
    t = step / max_steps
    actor.SetPosition(ziel_x * t, ziel_y * t, ziel_z * t)
    pl.render()

pl.add_timer_event(max_steps=max_steps, duration=3000, callback=callback)

cpos = [
    (0.0, -2500.0, 1200.0),
    (500.0,  1000.0,  100.0),
    (0.0,     1.0,    0.0)
]

pl.show(cpos=cpos)