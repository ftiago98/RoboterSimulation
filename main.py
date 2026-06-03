import Model.Scara as Scara
import Model.CoreXY as CNC
import Model.CncInterpreter
import View.Scara as ScaraView
import View.CoreXY as CncView
import ViewModel.HMI as Hmi


if __name__ == "__main__":
    robot1 = Scara()
    robot2 = Scara()
    Cnc = CNC()

    scaraView = ScaraView()
    cncView = CncView()
    hmiRobot1 = Hmi()
    hmiRobot2 = Hmi()
    hmiCnc = Hmi()