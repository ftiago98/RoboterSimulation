import sys
sys.path.append('./Model')
sys.path.append('./ViewModel')
sys.path.append('./View')

import time
import threading
from Model.hBot import hBot
from Model.Scara import Scara
from View.Scara import Scara as ScaraView
from View.HBot import HBot as HBotView
from ViewModel.hmi import Hmi


def startHmi1():
    print("Start HMI 1")
    hmiRobot1 = Hmi("Roboter 1")
    while True:
        hmiRobot1.root.update_idletasks()
        hmiRobot1.root.update()
        hmiControl = hmiRobot1.getHmiControl()
        if hmiControl.MoveXPlus:
            robot1Trafo.acsAxis1.Sollposition += 1
        if hmiControl.MoveXNeg:
            robot1Trafo.acsAxis1.Sollposition -= 1
        time.sleep(0.01)

def startHmi2():
    hmiRobot2 = Hmi("Roboter 2")
    hmiRobot2.root.mainloop()

def startHmi3():
    hmiCnc = Hmi("CNC")
    hmiCnc.root.mainloop()


if __name__ == "__main__":
    robot1Trafo = Scara()
    robot2Trafo = Scara()
    CncTrafo = hBot()

    hmiRobot1Thread = threading.Thread(target=startHmi1)
    hmiRobot1Thread.start()

    hmiRobot2Thread = threading.Thread(target=startHmi2)
    hmiRobot2Thread.start()

    hmiCncThread = threading.Thread(target=startHmi3)
    hmiCncThread.start()   

    scaraView1 = ScaraView();
    scaraView1.show();

    #scaraView2 = ScaraView();
    #scaraView2.show();

    #cncView = HBotView()
    #cncView.show()

    while True:
        robot1Trafo.forward()
        scaraView1.update_joints(robot1Trafo.acsAxis1.getSetPosition(),robot1Trafo.acsAxis2.getSetPosition(),robot1Trafo.acsAxis2.getSetPosition(),robot1Trafo.acsAxis4.getSetPosition())
        time.sleep(0.01)

