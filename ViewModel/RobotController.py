"""
Module: RobotController
Purpose: Per-robot orchestration layer that bridges HMI input, kinematics, and 3D view.
Responsibilities: Process HMI commands each tick, run forward/inverse kinematics, advance CNC
                  path with override, update 3D view, surface fault state to HMI status label.
Inputs:  hmiControl flags (from Hmi), kinematics model (Scara), view (View.Scara), hmiState.
Outputs: Updated axis positions, actor transforms, hmiState, HMI status display.
Dependencies: ViewModel.hmiControl, ViewModel.hmiState, Model.Scara, View.Scara, Model.RobotConfig
"""

import math
from Model.RobotConfig import SCARA_HOME


class RobotController:
    def __init__(self, robot_trafo, robot_view, hmi, hmi_state,
                 cnc_control=None, cnc_program_path=None):
        self.robot_trafo = robot_trafo
        self.robot_view = robot_view
        self.hmi = hmi
        self.hmi_state = hmi_state
        self.cnc_control = cnc_control
        self.cnc_program_path = cnc_program_path

        self._gripper_closed = False
        self._joint_mode = True
        self._manual_mode = True
        self._interpolated_path = None
        self._fault = False
        self._override_tick = 0

        if hasattr(self.robot_view, "set_gripper"):
            self.robot_view.set_gripper(closed=self._gripper_closed)

    def update_hmi(self):
        hmi_ctrl = self.hmi.getHmiControl()

        # Reset: clear fault and drive all axes to home position
        if getattr(hmi_ctrl, "Reset", False):
            self._fault = False
            self.robot_trafo.acsAxis1.Sollposition = SCARA_HOME["acsAxis1"]
            self.robot_trafo.acsAxis2.Sollposition = SCARA_HOME["acsAxis2"]
            self.robot_trafo.acsAxis3.Sollposition = SCARA_HOME["acsAxis3"]
            self.robot_trafo.acsAxis4.Sollposition = SCARA_HOME["acsAxis4"]
            hmi_ctrl.Reset = False  # consume pulse

        # Update status display every tick
        if self._fault:
            self.hmi.setStatus("STÖRUNG — Reset drücken", "red")
        elif self._any_at_limit():
            self.hmi.setStatus("Achse an Grenzwert", "orange")
        else:
            self.hmi.setStatus("Bereit", "lightgreen")

        if self._fault:
            self._update_hmi_state()
            self.hmi.setHmiState(self.hmi_state)
            return

        self._manual_mode = hmi_ctrl.OperationMode == 0

        if self._manual_mode:
            self._joint_mode = self._handle_manual_control(hmi_ctrl)
            self._handle_gripper(hmi_ctrl)
        else:
            self._joint_mode = False
            if self.cnc_control is not None and getattr(hmi_ctrl, "Start", False):
                self.cnc_control.load_from_path(self.cnc_program_path)
                self._interpolated_path = iter(
                    self.cnc_control.interpolate_path(step_size=3.0)
                )
                hmi_ctrl.Start = False

        self._update_hmi_state()
        self.hmi.setHmiState(self.hmi_state)

    def update_kinematics(self):
        try:
            if self._joint_mode:
                self.robot_trafo.forward()
            else:
                self.robot_trafo.backward()
        except ValueError as e:
            print(f"Kinematik Fehler: {e}")
            for axis in [
                self.robot_trafo.acsAxis1, self.robot_trafo.acsAxis2,
                self.robot_trafo.acsAxis3, self.robot_trafo.acsAxis4,
                self.robot_trafo.mcsAxisX, self.robot_trafo.mcsAxisY,
                self.robot_trafo.mcsAxisZ, self.robot_trafo.mcsAxisR,
            ]:
                axis.Sollposition = axis.ActualPosition
            self._fault = True

    def update_cnc_path(self):
        if self.cnc_control is None or self._interpolated_path is None:
            return

        # Speed override: 100% = 1 waypoint/tick, 50% = 1 per 2 ticks, etc.
        override = getattr(self.hmi.getHmiControl(), "OverridePercent", 100)
        ticks_per_step = max(1, round(100 / max(1, override)))
        self._override_tick += 1
        if self._override_tick < ticks_per_step:
            return
        self._override_tick = 0

        self.cnc_control.position = {
            "X": self.robot_trafo.mcsAxisX.ActualPosition,
            "Y": self.robot_trafo.mcsAxisY.ActualPosition,
            "Z": self.robot_trafo.mcsAxisZ.ActualPosition,
        }

        point = next(self._interpolated_path, None)
        if point is not None:
            self.robot_trafo.mcsAxisX.Sollposition = point["X"]
            self.robot_trafo.mcsAxisY.Sollposition = point["Y"]
            self.robot_trafo.mcsAxisZ.Sollposition = point["Z"]

    def update_view(self):
        self.robot_view.update_joints(
            self.robot_trafo.acsAxis1.getSetPosition(),
            self.robot_trafo.acsAxis2.getSetPosition(),
            self.robot_trafo.acsAxis4.getSetPosition(),
            z_height=self.robot_trafo.acsAxis3.getSetPosition()
        )

    # ============================================================
    # PRIVATE HELPERS
    # ============================================================
    def _any_at_limit(self):
        return any(a.is_at_limit() for a in [
            self.robot_trafo.acsAxis1, self.robot_trafo.acsAxis2,
            self.robot_trafo.acsAxis3, self.robot_trafo.acsAxis4,
        ])

    def _handle_manual_control(self, hmi_ctrl, step_joint=1, step_world=2):
        coord_system = getattr(hmi_ctrl, "CoordSystem", "Joint")
        if coord_system not in ["Joint", "Welt", "Werkzeug"]:
            coord_system = "Joint"

        if coord_system == "Joint":
            # Each button directly moves one joint / one axis
            # X→J1, Y→J2, Z→Hubachse (linear), R→Werkzeugdrehachse
            if hmi_ctrl.MoveXPlus: self.robot_trafo.acsAxis1.Sollposition += step_joint
            if hmi_ctrl.MoveXNeg:  self.robot_trafo.acsAxis1.Sollposition -= step_joint
            if hmi_ctrl.MoveYPlus: self.robot_trafo.acsAxis2.Sollposition += step_joint
            if hmi_ctrl.MoveYNeg:  self.robot_trafo.acsAxis2.Sollposition -= step_joint
            if hmi_ctrl.MoveZPlus: self.robot_trafo.acsAxis3.Sollposition += step_joint
            if hmi_ctrl.MoveZNeg:  self.robot_trafo.acsAxis3.Sollposition -= step_joint
            if hmi_ctrl.MoveRPlus: self.robot_trafo.acsAxis4.Sollposition += step_joint
            if hmi_ctrl.MoveRNeg:  self.robot_trafo.acsAxis4.Sollposition -= step_joint
            return True  # → forward() in update_kinematics

        elif coord_system == "Welt":
            # Buttons move TCP in the robot base (world) coordinate frame
            if hmi_ctrl.MoveXPlus: self.robot_trafo.mcsAxisX.Sollposition += step_world
            if hmi_ctrl.MoveXNeg:  self.robot_trafo.mcsAxisX.Sollposition -= step_world
            if hmi_ctrl.MoveYPlus: self.robot_trafo.mcsAxisY.Sollposition += step_world
            if hmi_ctrl.MoveYNeg:  self.robot_trafo.mcsAxisY.Sollposition -= step_world
            if hmi_ctrl.MoveZPlus: self.robot_trafo.mcsAxisZ.Sollposition += step_world
            if hmi_ctrl.MoveZNeg:  self.robot_trafo.mcsAxisZ.Sollposition -= step_world
            if hmi_ctrl.MoveRPlus: self.robot_trafo.mcsAxisR.Sollposition += step_world
            if hmi_ctrl.MoveRNeg:  self.robot_trafo.mcsAxisR.Sollposition -= step_world
            return False  # → backward() in update_kinematics

        else:  # Werkzeug — jog along/across the tool flange axes
            # X/Y jog is rotated by the current absolute flange angle (mcsAxisR).
            # For a flat SCARA, tool Z is always parallel to world Z → Z/R unchanged.
            r_rad = math.radians(self.robot_trafo.mcsAxisR.ActualPosition)
            cos_r = math.cos(r_rad)
            sin_r = math.sin(r_rad)

            tool_dx = 0.0
            tool_dy = 0.0
            if hmi_ctrl.MoveXPlus: tool_dx += step_world
            if hmi_ctrl.MoveXNeg:  tool_dx -= step_world
            if hmi_ctrl.MoveYPlus: tool_dy += step_world
            if hmi_ctrl.MoveYNeg:  tool_dy -= step_world

            # Rotate tool-frame vector into world frame
            self.robot_trafo.mcsAxisX.Sollposition += tool_dx * cos_r - tool_dy * sin_r
            self.robot_trafo.mcsAxisY.Sollposition += tool_dx * sin_r + tool_dy * cos_r

            if hmi_ctrl.MoveZPlus: self.robot_trafo.mcsAxisZ.Sollposition += step_world
            if hmi_ctrl.MoveZNeg:  self.robot_trafo.mcsAxisZ.Sollposition -= step_world
            if hmi_ctrl.MoveRPlus: self.robot_trafo.mcsAxisR.Sollposition += step_world
            if hmi_ctrl.MoveRNeg:  self.robot_trafo.mcsAxisR.Sollposition -= step_world
            return False  # → backward() in update_kinematics

    def _handle_gripper(self, hmi_ctrl):
        if getattr(hmi_ctrl, "Start", False):
            self._gripper_closed = True
        if getattr(hmi_ctrl, "Stop", False):
            self._gripper_closed = False
        if hasattr(self.robot_view, "set_gripper"):
            self.robot_view.set_gripper(closed=self._gripper_closed)
        if hasattr(self.robot_view, "attach_part"):
            self.robot_view.attach_part(self._gripper_closed)

    def _update_hmi_state(self):
        self.hmi_state.axisJ1Position = self.robot_trafo.acsAxis1.ActualPosition
        self.hmi_state.axisJ2Position = self.robot_trafo.acsAxis2.ActualPosition
        self.hmi_state.axisJ3Position = self.robot_trafo.acsAxis3.ActualPosition
        self.hmi_state.axisJ4Position = self.robot_trafo.acsAxis4.ActualPosition
        self.hmi_state.axisXPosition = self.robot_trafo.mcsAxisX.ActualPosition
        self.hmi_state.axisYPosition = self.robot_trafo.mcsAxisY.ActualPosition
        self.hmi_state.axisZPosition = self.robot_trafo.mcsAxisZ.ActualPosition
        self.hmi_state.axisRPosition = self.robot_trafo.mcsAxisR.ActualPosition
