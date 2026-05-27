import os
os.environ["VTK_DEFAULT_OPENGL_WINDOW"] = "vtkWin32OpenGLRenderWindow"

import pyvista as pv
import time

cwd = os.getcwd()
BaseMesh     = pv.get_reader(cwd + "\\View\\data\\Base.stl").read()
InnerArmMesh = pv.get_reader(cwd + "\\View\\data\\InnerArm.stl").read()

pl = pv.Plotter(lighting="none")
pl.renderer.SetUseDepthPeeling(False)
pl.renderer.SetMaximumNumberOfPeels(0)

base  = pl.add_mesh(BaseMesh,     color="lightgray")
actor = pl.add_mesh(InnerArmMesh, color="orange")

# ✅ Drehpunkt = Gelenk wo Arm mit Basis verbunden ist
# → Werte aus dem print() oben anpassen!
gelenk_x = 0    # <-- anpassen
gelenk_y = 0    # <-- anpassen
gelenk_z = 0    # <-- anpassen
actor.SetOrigin(gelenk_x, gelenk_y, gelenk_z)

cpos = [
    (0.0, -2500.0, 1200.0),
    (500.0,  1000.0,  100.0),
    (0.0,     1.0,    0.0)
]

max_steps  = 200
duration_s = 3.0

pl.show(cpos=cpos, interactive_update=True, auto_close=False)

for step in range(max_steps + 1):
    t     = step / max_steps
    angle = 90 * t  # 90° Rotation — nach Bedarf anpassen

    actor.SetOrientation(0, 0, angle)  # Achse nach Bedarf anpassen

    pl.update()
    time.sleep(duration_s / max_steps)

pl.show()