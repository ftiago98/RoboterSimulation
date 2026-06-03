import math
import Axis

class Scara:
    def __init__(self):
        self.L1 = 325
        self.L2 = 550
        self.L3 = 0

        # Gelenkachsen (ACS)
        self.acsAxis1 = Axis() # Gelenk 1
        self.acsAxis2 = Axis() # Gelenk 2
        self.acsAxis3 = Axis() # Hubachse
        self.acsAxis4 = Axis() # Werkzeugdrehachse

        # Kartesische Achsen (MCS)
        self.mcsAxisX = Axis() # X Achse
        self.mcsAxisY = Axis() # Y Achse
        self.mcsAxisZ = Axis() # Z Achse
        self.mcsAxisR = Axis() # Rotationsachse

    def setAxesJoint(self, axis1, axis2, axis3, axis4): # Gelenkwinkel und Hubhöhe setzen
        self.acsAxis1.Sollposition = axis1
        self.acsAxis2.Sollposition = axis2
        self.acsAxis3.Sollposition = axis3
        self.acsAxis4.Sollposition = axis4

    def forward(self): # Vorwärtskinematik berechnen # Winkel von Grad in Bogenmaß umrechnen
        axis1 = math.radians(self.acsAxis1.Sollposition)
        axis2 = math.radians(self.acsAxis2.Sollposition)
        axis3 = self.acsAxis3.Sollposition # Lineare Bewegung
        axis4 = math.radians(self.acsAxis4.Sollposition)

        x = self.L1 * math.cos(axis1) + self.L2 * math.cos(axis1 + axis2) # Berechnung der X-Koordinate
        y = self.L1 * math.sin(axis1) + self.L2 * math.sin(axis1 + axis2) # Berechnung der Y-Koordinate
        z = self.L3 + axis3 # Berechnung der Z-Koordinate
        r = self.acsAxis1.Sollposition + self.acsAxis2.Sollposition + self.acsAxis4.Sollposition # Berechnung der Rotationsachse

        return x, y, z, r

if __name__ == "__main__":
    robot = Scara()
    robot.setAxesJoint(30, 45, 50, 90)
    position = robot.forward()
    print(position)

   