import os

class Axis:
    def __init__(self):
        self.ActualPosition = 10
        self.Sollposition = 0
    
    def getActualPosition(self):
        return self.ActualPosition


testaxis = Axis()
print (testaxis.getActualPosition())

