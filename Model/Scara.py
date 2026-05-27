import math
import Axis

class Scara:
    def __init__(self):
        self.L1 = 225
        self.L2 = 225
        self.L3 = 0

        self.axis1 = Axis()
        self.axis2 = Axis()
        self.axis3 = Axis()
        self.axis4 = Axis()

        self.axis1_deg = 0
        self.axis2_deg = 0
        self.axis3_mm = 0
        self.axis4_deg = 0

    def setAxes(self, axis1, axis2, axis3, axis4):
        self.axis1_deg = axis1
        self.axis2_deg = axis2
        self.axis3_mm = axis3
        self.axis4_deg = axis4

    def forward(self):
        axis1 = math.radians(self.axis1_deg)
        axis2 = math.radians(self.axis2_deg)

        x = self.L1 * math.cos(axis1) + self.L2 *math.cos(axis1 + axis2)
        y = self.L1 * math.sin(axis1) + self.L2 *math.sin(axis1 + axis2)
        z = self.L3 + self.axis3_mm

        r = self.axis1_deg + self.axis2_deg + self.axis4_deg

        return x, y, z, r


robot = Scara()
robot.setAxes(30, 45, 50, 90)
position = robot.forward()
print(position)

   
