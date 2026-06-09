import sys
sys.path.append('./Model')
sys.path.append('./ViewModel')
sys.path.append('./View')

import time
import threading
from Model.hBot import hBot
from Model.Scara import Scara
from Model.CncInterpreter import CncInterpreter
from View.Scara import Scara as ScaraView
from View.HBot import HBot as HBotView
from ViewModel.hmi import Hmi
from ViewModel.hmiState import hmiState

class Machine:
    def __init__(self):
        self.robot1Trafo = Scara()
        self.robot1CncControl = CncInterpreter()
        self.interpolated_path = None
        self.robot2Trafo = Scara()
        self.CncTrafo = hBot()

        self.hmiRobot1Thread = threading.Thread(target=self.startHmi1)
        self.hmiRobot1Thread.start()

        self.hmiRobot2Thread = threading.Thread(target=self.startHmi2)
        self.hmiRobot2Thread.start()

        self.hmiCncThread = threading.Thread(target=self.startHmi3)
        self.hmiCncThread.start()   

        self.scaraView1 = ScaraView();
        self.scaraView1.show();
        self.Robot1JointMode = True
        self.Robot1Manual = True

        #self.scaraView2 = ScaraView();
        #self.scaraView2.show();

        #self.cncView = HBotView()
        #self.cncView.show()

    def startHmi1(self):
        print("Start HMI 1")
        hmiRobot1 = Hmi("Roboter 1")
        self.hmi1State = hmiState()

        while True:
            hmiRobot1.root.update_idletasks()
            hmiRobot1.root.update()
            hmiControl = hmiRobot1.getHmiControl()
            self.Robot1Manual = hmiControl.OperationMode == 0
            print(self.Robot1Manual)
            if self.Robot1Manual:
                self.Robot1JointMode = hmiControl.CoordSystem == "Joint"
                if self.Robot1JointMode:
                    if hmiControl.MoveXPlus:
                        self.robot1Trafo.acsAxis1.Sollposition += 1
                    if hmiControl.MoveXNeg:
                        self.robot1Trafo.acsAxis1.Sollposition -= 1
                    if hmiControl.MoveYPlus:
                        self.robot1Trafo.acsAxis2.Sollposition += 1
                    if hmiControl.MoveYNeg:
                        self.robot1Trafo.acsAxis2.Sollposition -= 1
                    if hmiControl.MoveZPlus:
                        self.robot1Trafo.acsAxis3.Sollposition += 1
                    if hmiControl.MoveZNeg:
                        self.robot1Trafo.acsAxis3.Sollposition -= 1
                    if hmiControl.MoveRPlus:
                        self.robot1Trafo.acsAxis4.Sollposition += 1
                    if hmiControl.MoveRNeg:
                        self.robot1Trafo.acsAxis4.Sollposition -= 1

                if not self.Robot1JointMode:
                    if hmiControl.MoveXPlus:
                        self.robot1Trafo.mcsAxisX.Sollposition += 2
                    if hmiControl.MoveXNeg:
                        self.robot1Trafo.mcsAxisX.Sollposition -= 2
                    if hmiControl.MoveYPlus:
                        self.robot1Trafo.mcsAxisY.Sollposition += 2
                    if hmiControl.MoveYNeg:
                        self.robot1Trafo.mcsAxisY.Sollposition -= 2
                    if hmiControl.MoveZPlus:
                        self.robot1Trafo.mcsAxisZ.Sollposition += 2
                    if hmiControl.MoveZNeg:
                        self.robot1Trafo.mcsAxisZ.Sollposition -= 2
                    if hmiControl.MoveRPlus:
                        self.robot1Trafo.mcsAxisR.Sollposition += 2
                    if hmiControl.MoveRNeg:
                        self.robot1Trafo.mcsAxisR.Sollposition -= 2
            else:
                self.Robot1JointMode = False #in Automatic nur Welt
                if hmiControl.Start:
                    self.robot1CncControl.load_from_path("programm.nc")
                    self.interpolated_path = iter(self.robot1CncControl.interpolate_path(step_size=3.0))
                    hmiControl.Start = False # reset the start


            self.hmi1State.axisJ1Position = self.robot1Trafo.acsAxis1.ActualPosition
            self.hmi1State.axisJ2Position = self.robot1Trafo.acsAxis2.ActualPosition
            self.hmi1State.axisJ3Position = self.robot1Trafo.acsAxis3.ActualPosition
            self.hmi1State.axisJ4Position = self.robot1Trafo.acsAxis4.ActualPosition

            self.hmi1State.axisXPosition = self.robot1Trafo.mcsAxisX.ActualPosition
            self.hmi1State.axisYPosition = self.robot1Trafo.mcsAxisY.ActualPosition
            self.hmi1State.axisZPosition = self.robot1Trafo.mcsAxisZ.ActualPosition
            self.hmi1State.axisRPosition = self.robot1Trafo.mcsAxisR.ActualPosition

            hmiRobot1.setHmiState(self.hmi1State)

            time.sleep(0.2)

    def startHmi2(self):
        self.hmiRobot2 = Hmi("Roboter 2")
        self.hmiRobot2.root.mainloop()

    def startHmi3(self):
        self.hmiCnc = Hmi("CNC")
        self.hmiCnc.root.mainloop()


if __name__ == "__main__":
    machine = Machine()

    while True:
        if machine.Robot1JointMode:
            machine.robot1Trafo.forward()
        else:
            machine.robot1Trafo.backward()
        if machine.interpolated_path is not None:
            # Holt den nächsten Punkt. Der Iterator merkt sich, wo er war.
            point = next(machine.path_iterator)
            if point is not None:
                machine.robot1Trafo.mcsAxisX.Sollposition =  point['X']
                machine.robot1Trafo.mcsAxisY.Sollposition =  point['Y']
                machine.robot1Trafo.mcsAxisZ.Sollposition =  point['Z']

        machine.robot1Trafo.cyclic()
        machine.scaraView1.update_joints(machine.robot1Trafo.acsAxis1.getSetPosition(),machine.robot1Trafo.acsAxis2.getSetPosition(),machine.robot1Trafo.acsAxis2.getSetPosition()) #,machine.robot1Trafo.acsAxis4.getSetPosition())
        time.sleep(0.01)

