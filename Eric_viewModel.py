import os
os.environ["VTK_DEFAULT_OPENGL_WINDOW"] = "vtkWin32OpenGLRenderWindow"

import pyvista as pv
import vtk #Matrizenrechnen
import time


class RobotViewer:

    def __init__(self, data_folder_path=None):
        if data_folder_path is None:
            cwd = os.getcwd()
            data_folder_path = os.path.join(cwd, "View", "data")

        base_mesh      = pv.read(os.path.join(data_folder_path, "Base.stl"))
        inner_arm_mesh = pv.read(os.path.join(data_folder_path, "InnerArm.stl"))
        outer_arm_mesh = pv.read(os.path.join(data_folder_path, "OuterArm.stl"))
        spindle_mesh   = pv.read(os.path.join(data_folder_path, "Spindle.stl"))

        self.pl = pv.Plotter(lighting="none")
        self.pl.renderer.SetUseDepthPeeling(False)
        self.pl.renderer.SetMaximumNumberOfPeels(0)

        self.base_actor      = self.pl.add_mesh(base_mesh,      color="lightblue")
        self.inner_arm_actor = self.pl.add_mesh(inner_arm_mesh, color="orange")
        self.outer_arm_actor = self.pl.add_mesh(outer_arm_mesh, color="green")
        self.spindle_actor   = self.pl.add_mesh(spindle_mesh,   color="gray")

        self.shoulder = (0,   0, 0)   # <-- anpassen
        self.elbow    = (0, -500, 0)   # <-- anpassen
        self.tip      = (0, 900, 0)   # <-- anpassen

        # InnerArm dreht einfach um die Schulter
        self.inner_arm_actor.SetOrigin(*self.shoulder)

        # OuterArm und Spindle bekommen keinen SetOrigin mehr –
        # deren Transform wird in update_joints komplett neu berechnet.

        self.pl.camera_position = [
            (0.0, -1500.0, 850.0),
            (0.0,    0.0,   0.0),
            (0.0,    1.0,   0.0),
        ]

    # ------------------------------------------------------------------

    @staticmethod
    def _build_transform(own_angle, own_pivot, parent_angle, parent_pivot):
        """
        Baut einen vtkTransform, der:
          1. das Teil um sein eigenes Gelenk (own_pivot) dreht
          2. dann mit dem Elternteil um dessen Gelenk (parent_pivot) mitdreht
        """
        ox, oy, oz = own_pivot
        px, py, pz = parent_pivot

        t = vtk.vtkTransform()
        t.PostMultiply()

        # Schritt 1 – Eigenrotation um own_pivot
        t.Translate(-ox, -oy, -oz)
        t.RotateZ(own_angle)
        t.Translate(ox, oy, oz)

        # Schritt 2 – Mitdrehen mit Elternteil um parent_pivot
        t.Translate(-px, -py, -pz)
        t.RotateZ(parent_angle)
        t.Translate(px, py, pz)

        return t

    def show(self):
        self.pl.show(interactive_update=True, auto_close=False)

    def update_joints(self, inner_angle=0, outer_angle=0, spindle_angle=0):
        # InnerArm: einfache Rotation um Schulter
        self.inner_arm_actor.SetOrientation(0, 0, inner_angle)

        # OuterArm: erst eigene Rotation um Ellbogen, dann mit InnerArm mitdrehen
        t_outer = self._build_transform(
            own_angle=outer_angle,   own_pivot=self.elbow,
            parent_angle=inner_angle, parent_pivot=self.shoulder,
        )
        self.outer_arm_actor.SetUserTransform(t_outer)

        # Spindel: erst eigene Rotation um Handgelenk,
        # dann mit OuterArm (der schon inner_angle trägt) mitdrehen.
        # Da OuterArm bereits die kombinierte Bewegung enthält, addieren wir
        # inner_angle + outer_angle als effektiven Elternwinkel.
        t_spindle = self._build_transform(
            own_angle=spindle_angle, own_pivot=self.tip,
            parent_angle=inner_angle + outer_angle, parent_pivot=self.shoulder,
        )
        self.spindle_actor.SetUserTransform(t_spindle)

        self.pl.update()

    def animate(self, target_inner=90, target_outer=0, target_spindle=0,
                max_steps=200, duration_s=3.0):
        for step in range(max_steps + 1):
            t = step / max_steps
            self.update_joints(
                inner_angle   = target_inner   * t,
                outer_angle   = target_outer   * t,
                spindle_angle = target_spindle * t,
            )
            time.sleep(duration_s / max_steps)

    def close(self):
        self.pl.close()


robot = RobotViewer()
robot.show()
robot.animate(target_inner=90)
robot.pl.show()