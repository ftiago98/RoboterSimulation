import math
import Axis

class Scara:
    def __init__(self):
        self.L1 = 225
        self.L2 = 225
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
        self.acsAxis1.Sollposition = axis1
        self.acsAxis2.Sollposition = axis2
        self.acsAxis3.Sollposition = axis3
        self.acsAxis4.Sollposition = axis4

    def forward(self):
        axis1 = math.radians(self.axis1_deg)
        axis2 = math.radians(self.axis2_deg)

        x = self.L1 * math.cos(axis1) + self.L2 *math.cos(axis1 + axis2)
        y = self.L1 * math.sin(axis1) + self.L2 *math.sin(axis1 + axis2)
        z = self.L3 + self.axis3_mm

        r = self.axis1_deg + self.axis2_deg + self.axis4_deg

        return x, y, z, r


robot = Scara()
robot.setAxesJoint(30, 45, 50, 90)
position = robot.forward()
print(position)

   