import math
import Axis

class Scara:
    def __init__(self):
        self.L1 = 325
        self.L2 = 550
        self.L3 = 0

        self.acsAxis1 = Axis() # Gelenk 1
        self.acsAxis2 = Axis() # Gelenk 2
        self.acsAxis3 = Axis() # Hubachse
        self.acsAxis4 = Axis() # Werkzeugdrehachse

        self.mcsAxisX = Axis() # X Achse
        self.mcsAxisY = Axis() # Y Achse
        self.mcsAxisZ = Axis() # Z Achse
        self.mcsAxisR = Axis() # Rotationsachse

    def setAxesJoint(self, axis1, axis2, axis3, axis4): # Gelenkwinkel und Hubhöhe setzen
        self.acsAxisX.Sollposition = axis1
        self.acsAxisY.Sollposition = axis2
        self.acsAxisZ.Sollposition = axis3
        self.acsAxisR.Sollposition = axis4

    def forward(self): # Vorwärtskinematik berechnen # Winkel von Grad in Bogenmaß umrechnen
        axisX = math.radians(self.acsAxisX.Sollposition)
        axisY = math.radians(self.acsAxisY.Sollposition)
        axisZ = self.acsAxisZ.Sollposition # Lineare Bewegung
        axisR = math.radians(self.acsAxisR.Sollposition)

        x = self.L1 * math.cos(axisX) + self.L2 * math.cos(axisX + axisY) # Berechnung der X-Koordinate
        y = self.L1 * math.sin(axisX) + self.L2 * math.sin(axisX + axisY) # Berechnung der Y-Koordinate
        z = self.L3 + axisZ # Berechnung der Z-Koordinate
        r = self.acsAxisX.Sollposition + self.acsAxisY.Sollposition + self.acsAxisR.Sollposition # Berechnung der Rotationsachse

        return x, y, z, r


robot = Scara()
robot.setAxesJoint(30, 45, 50, 90)
position = robot.forward()
print(position)

   