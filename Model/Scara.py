import math
import Axis

class Scara:
    def __init__(self):
        self.L1 = 325
        self.L2 = 550
        self.L3 = 0

        self.acsAxis1 = Axis() # Joint axes
        self.acsAxis2 = Axis()
        self.acsAxis3 = Axis()
        self.acsAxis4 = Axis()

        self.mcsAxisX = Axis() #World axes
        self.mcsAxisY = Axis()
        self.mcsAxisZ = Axis()
        self.mcsAxisR = Axis()

    def setAxesJoint(self, axis1, axis2, axis3, axis4):
        self.acsAxisX.Sollposition = axis1
        self.acsAxisY.Sollposition = axis2
        self.acsAxisZ.Sollposition = axis3
        self.acsAxisR.Sollposition = axis4

    def forward(self):
        axisX = math.radians(self.acsAxisX.Sollposition)
        axisY = math.radians(self.acsAxisY.Sollposition)
        axisZ = self.acsAxisZ.Sollposition
        axisR = math.radians(self.acsAxisR.Sollposition)

        x = self.L1 * math.cos(axisX) + self.L2 * math.cos(axisX + axisY)
        y = self.L1 * math.sin(axisX) + self.L2 * math.sin(axisX + axisY)
        z = self.L3 + axisZ
        r = self.acsAxisX.Sollposition + self.acsAxisY.Sollposition + self.acsAxisR.Sollposition

        return x, y, z, r


robot = Scara()
robot.setAxesJoint(30, 45, 50, 90)
position = robot.forward()
print(position)

   