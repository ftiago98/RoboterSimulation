import threading
import Model.Scara as Scara
import Model.CoreXY as CNC

import View.Scara as Scara
import View.CoreXY as CncView
import ViewModel.HMI as Hmi


def startHmi1():
    hmiRobot1 = Hmi()
def startHmi2():
    hmiRobot2 = Hmi()
def startHmi3():
    hmiCnc = Hmi()


if __name__ == "__main__":
    robot1Trafo = Scara()
    robot2Trafo = Scara()
    CncTrafo = CNC()

    scaraView = ScaraView()
    cncView = CncView()

    hmiRobot1Thread = threading.Thread(target=startHmi1, args=("A", 3))
    hmiRobot1Thread.start()

    hmiRobot2Thread = threading.Thread(target=startHmi1, args=("A", 3))
    hmiRobot2Thread.start()

    hmiCncThread = threading.Thread(target=startHmi3, args=("A", 3))
    hmiCncThread.start()   
