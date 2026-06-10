import sys
sys.path.append('./Model')
sys.path.append('./ViewModel')
sys.path.append('./View')

import time
import threading
import pyvista as pv

from Model.hBot import hBot
from Model.Scara import Scara
from Model.CncInterpreter import CncInterpreter

from View.Scara import Scara as ScaraView
from View.HBot import HBot as HBotView

from ViewModel.hmi import Hmi
from ViewModel.hmiState import hmiState


class Machine:
    def __init__(self):
        # ========================================================
        # MODELLE
        # ========================================================
        self.robot1Trafo = Scara()
        self.robot2Trafo = Scara()

        self.robot1CncControl = CncInterpreter()
        self.interpolated_path = None

        self.CncTrafo = hBot()

        # H-Bot Positionen
        self.hbotX = 0.0
        self.hbotY = 0.0

        # ========================================================
        # MODI ROBOTER 1
        # ========================================================
        self.Robot1JointMode = True
        self.Robot1Manual = True

        # ========================================================
        # MODI ROBOTER 2
        # ========================================================
        self.Robot2JointMode = True
        self.Robot2Manual = True

        # ========================================================
        # HMI STATES
        # ========================================================
        self.hmi1State = hmiState()
        self.hmi2State = hmiState()
        self.hmiCncState = hmiState()

        # ========================================================
        # GEMEINSAMES PYVISTA-FENSTER
        # ========================================================
        self.sharedPlotter = pv.Plotter()

        # Reihenfolge:
        # SCARA 1 links
        self.scaraView1 = ScaraView(
            pl=self.sharedPlotter,
            position=(-1000, 250, 0)
        )

        # H-Bot in der Mitte
        self.cncView = HBotView(
            pl=self.sharedPlotter,
            position=(0, 0, 0)
        )

        # SCARA 2 rechts
        self.scaraView2 = ScaraView(
            pl=self.sharedPlotter,
            position=(1300, 250, 0)
        )

        # Kamera / Ansicht
        self.sharedPlotter.show_axes()

        self.sharedPlotter.camera_position = [
            (400.0, -2700.0, 1600.0),  # Kamera
            (250.0, 250.0, 0.0),       # Fokuspunkt
            (0.0, 0.0, 1.0)            # Oben-Richtung
        ]

        self.sharedPlotter.show(
            interactive_update=True,
            auto_close=False
        )

        # ========================================================
        # HMI THREADS STARTEN
        # ========================================================
        self.hmiRobot1Thread = threading.Thread(
            target=self.startHmi1,
            daemon=True
        )
        self.hmiRobot1Thread.start()

        self.hmiRobot2Thread = threading.Thread(
            target=self.startHmi2,
            daemon=True
        )
        self.hmiRobot2Thread.start()

        self.hmiCncThread = threading.Thread(
            target=self.startHmi3,
            daemon=True
        )
        self.hmiCncThread.start()

    # ============================================================
    # ALLGEMEINE STEUERUNG FÜR SCARA
    # ============================================================
    def handle_scara_manual_control(self, robotTrafo, hmiControl, step_joint=1, step_world=2):
        """
        Steuert einen SCARA-Roboter im Joint- oder Weltkoordinatensystem.
        """

        joint_mode = hmiControl.CoordSystem == "Joint"

        if joint_mode:
            # Joint-Modus
            if hmiControl.MoveXPlus:
                robotTrafo.acsAxis1.Sollposition += step_joint
            if hmiControl.MoveXNeg:
                robotTrafo.acsAxis1.Sollposition -= step_joint

            if hmiControl.MoveYPlus:
                robotTrafo.acsAxis2.Sollposition += step_joint
            if hmiControl.MoveYNeg:
                robotTrafo.acsAxis2.Sollposition -= step_joint

            if hmiControl.MoveZPlus:
                robotTrafo.acsAxis3.Sollposition += step_joint
            if hmiControl.MoveZNeg:
                robotTrafo.acsAxis3.Sollposition -= step_joint

            if hmiControl.MoveRPlus:
                robotTrafo.acsAxis4.Sollposition += step_joint
            if hmiControl.MoveRNeg:
                robotTrafo.acsAxis4.Sollposition -= step_joint

        else:
            # Weltkoordinaten-Modus
            if hmiControl.MoveXPlus:
                robotTrafo.mcsAxisX.Sollposition += step_world
            if hmiControl.MoveXNeg:
                robotTrafo.mcsAxisX.Sollposition -= step_world

            if hmiControl.MoveYPlus:
                robotTrafo.mcsAxisY.Sollposition += step_world
            if hmiControl.MoveYNeg:
                robotTrafo.mcsAxisY.Sollposition -= step_world

            if hmiControl.MoveZPlus:
                robotTrafo.mcsAxisZ.Sollposition += step_world
            if hmiControl.MoveZNeg:
                robotTrafo.mcsAxisZ.Sollposition -= step_world

            if hmiControl.MoveRPlus:
                robotTrafo.mcsAxisR.Sollposition += step_world
            if hmiControl.MoveRNeg:
                robotTrafo.mcsAxisR.Sollposition -= step_world

        return joint_mode

    # ============================================================
    # HMI STATUS FÜR SCARA
    # ============================================================
    def update_scara_hmi_state(self, robotTrafo, state):
        """
        Aktualisiert die Anzeige im HMI.
        """

        state.axisJ1Position = robotTrafo.acsAxis1.ActualPosition
        state.axisJ2Position = robotTrafo.acsAxis2.ActualPosition
        state.axisJ3Position = robotTrafo.acsAxis3.ActualPosition
        state.axisJ4Position = robotTrafo.acsAxis4.ActualPosition

        state.axisXPosition = robotTrafo.mcsAxisX.ActualPosition
        state.axisYPosition = robotTrafo.mcsAxisY.ActualPosition
        state.axisZPosition = robotTrafo.mcsAxisZ.ActualPosition
        state.axisRPosition = robotTrafo.mcsAxisR.ActualPosition

    # ============================================================
    # HMI ROBOTER 1
    # ============================================================
    def startHmi1(self):
        print("Start HMI Roboter 1")

        hmiRobot1 = Hmi("Roboter 1")

        while True:
            hmiRobot1.root.update_idletasks()
            hmiRobot1.root.update()

            hmiControl = hmiRobot1.getHmiControl()

            self.Robot1Manual = hmiControl.OperationMode == 0

            if self.Robot1Manual:
                self.Robot1JointMode = self.handle_scara_manual_control(
                    self.robot1Trafo,
                    hmiControl
                )

            else:
                # Automatik nur in Weltkoordinaten
                self.Robot1JointMode = False

                if hmiControl.Start:
                    self.robot1CncControl.load_from_path("Model\\programm.nc")
                    self.interpolated_path = iter(
                        self.robot1CncControl.interpolate_path(step_size=3.0)
                    )

                    hmiControl.Start = False

            self.update_scara_hmi_state(
                self.robot1Trafo,
                self.hmi1State
            )

            hmiRobot1.setHmiState(self.hmi1State)

            time.sleep(0.2)

    # ============================================================
    # HMI ROBOTER 2
    # ============================================================
    def startHmi2(self):
        print("Start HMI Roboter 2")

        hmiRobot2 = Hmi("Roboter 2")

        while True:
            hmiRobot2.root.update_idletasks()
            hmiRobot2.root.update()

            hmiControl = hmiRobot2.getHmiControl()

            self.Robot2Manual = hmiControl.OperationMode == 0

            if self.Robot2Manual:
                self.Robot2JointMode = self.handle_scara_manual_control(
                    self.robot2Trafo,
                    hmiControl
                )

            else:
                # Roboter 2 aktuell ohne CNC-Automatik
                self.Robot2JointMode = False

            self.update_scara_hmi_state(
                self.robot2Trafo,
                self.hmi2State
            )

            hmiRobot2.setHmiState(self.hmi2State)

            time.sleep(0.2)

    # ============================================================
    # HMI CNC / H-BOT
    # ============================================================
    def startHmi3(self):
        print("Start HMI CNC / H-Bot")

        hmiCnc = Hmi("CNC / H-Bot")

        while True:
            hmiCnc.root.update_idletasks()
            hmiCnc.root.update()

            hmiControl = hmiCnc.getHmiControl()

            # H-Bot Steuerung:
            # X+ / X- bewegt den Schlitten
            # Y+ / Y- bewegt die Brücke
            if hmiControl.MoveXPlus:
                self.hbotX += 5
            if hmiControl.MoveXNeg:
                self.hbotX -= 5

            if hmiControl.MoveYPlus:
                self.hbotY += 5
            if hmiControl.MoveYNeg:
                self.hbotY -= 5

            # Begrenzung, damit H-Bot nicht zu weit wegfährt
            if self.hbotX > 300:
                self.hbotX = 300
            if self.hbotX < -300:
                self.hbotX = -300

            if self.hbotY > 300:
                self.hbotY = 300
            if self.hbotY < -300:
                self.hbotY = -300

            # HMI Anzeige aktualisieren
            self.hmiCncState.axisXPosition = self.hbotX
            self.hmiCncState.axisYPosition = self.hbotY
            self.hmiCncState.axisZPosition = 0.0
            self.hmiCncState.axisRPosition = 0.0

            hmiCnc.setHmiState(self.hmiCncState)

            time.sleep(0.2)


# ================================================================
# HAUPTPROGRAMM
# ================================================================
if __name__ == "__main__":
    machine = Machine()

    while True:
        # ========================================================
        # ROBOTER 1 CNC-POSITION AKTUALISIEREN
        # ========================================================
        machine.robot1CncControl.position = {
            "X": machine.robot1Trafo.mcsAxisX.ActualPosition,
            "Y": machine.robot1Trafo.mcsAxisY.ActualPosition,
            "Z": machine.robot1Trafo.mcsAxisZ.ActualPosition
        }

        # ========================================================
        # ROBOTER 1 KINEMATIK
        # ========================================================
        try:
            if machine.Robot1JointMode:
                machine.robot1Trafo.forward()
            else:
                machine.robot1Trafo.backward()

        except ValueError as e:
            print("Roboter 1 Fehler:", e)

            machine.robot1Trafo.mcsAxisX.Sollposition = machine.robot1Trafo.mcsAxisX.ActualPosition
            machine.robot1Trafo.mcsAxisY.Sollposition = machine.robot1Trafo.mcsAxisY.ActualPosition
            machine.robot1Trafo.mcsAxisZ.Sollposition = machine.robot1Trafo.mcsAxisZ.ActualPosition
            machine.robot1Trafo.mcsAxisR.Sollposition = machine.robot1Trafo.mcsAxisR.ActualPosition

        # ========================================================
        # ROBOTER 1 CNC-PFAD
        # ========================================================
        if machine.interpolated_path is not None:
            point = next(machine.interpolated_path, None)

            if point is not None:
                machine.robot1Trafo.mcsAxisX.Sollposition = point["X"]
                machine.robot1Trafo.mcsAxisY.Sollposition = point["Y"]
                machine.robot1Trafo.mcsAxisZ.Sollposition = point["Z"]

        machine.robot1Trafo.cyclic()

        # ========================================================
        # ROBOTER 2 KINEMATIK
        # ========================================================
        try:
            if machine.Robot2JointMode:
                machine.robot2Trafo.forward()
            else:
                machine.robot2Trafo.backward()

        except ValueError as e:
            print("Roboter 2 Fehler:", e)

            machine.robot2Trafo.mcsAxisX.Sollposition = machine.robot2Trafo.mcsAxisX.ActualPosition
            machine.robot2Trafo.mcsAxisY.Sollposition = machine.robot2Trafo.mcsAxisY.ActualPosition
            machine.robot2Trafo.mcsAxisZ.Sollposition = machine.robot2Trafo.mcsAxisZ.ActualPosition
            machine.robot2Trafo.mcsAxisR.Sollposition = machine.robot2Trafo.mcsAxisR.ActualPosition

        machine.robot2Trafo.cyclic()

        # ========================================================
        # 3D-VIEW ROBOTER 1 AKTUALISIEREN
        # ========================================================
        machine.scaraView1.update_joints(
            machine.robot1Trafo.acsAxis1.getSetPosition(),
            machine.robot1Trafo.acsAxis2.getSetPosition(),
            machine.robot1Trafo.acsAxis4.getSetPosition()
        )

        # ========================================================
        # 3D-VIEW H-BOT AKTUALISIEREN
        # ========================================================
        machine.cncView.update_mesh_positions(
            x_pos=machine.hbotX,
            y_pos=machine.hbotY
        )

        # ========================================================
        # 3D-VIEW ROBOTER 2 AKTUALISIEREN
        # ========================================================
        machine.scaraView2.update_joints(
            machine.robot2Trafo.acsAxis1.getSetPosition(),
            machine.robot2Trafo.acsAxis2.getSetPosition(),
            machine.robot2Trafo.acsAxis4.getSetPosition()
        )

        time.sleep(0.01)