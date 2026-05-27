import pyvista as pv
import os

cwd = os.getcwd()
filename = cwd+"\\View\\data\\Base.stl"
reader = pv.get_reader(filename)
mesh = reader.read()

filename = cwd+"\\View\\data\\InnerArm.stl"
reader = pv.get_reader(filename)
InnerArmMesh = reader.read()

totalMesh = pv.merge([mesh,InnerArmMesh])
totalMesh.plot()

