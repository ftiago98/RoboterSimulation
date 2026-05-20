import pyvista as pv
from pyvista import examples

# Kitchen CFD simulation: grid with a velocity field
# and furniture meshes as a separate dataset
mesh = examples.download_kitchen()
furniture = examples.download_kitchen(split=True)

# Trace streamlines from above the stove
source = pv.Line((0.08, 2.5, 0.71), (0.08, 4.5, 0.71), resolution=15)
streamlines = mesh.streamlines_from_source(source, max_length=200)

# Compose the scene
pl = pv.Plotter()
pl.add_mesh(furniture, color='slategray')
pl.add_mesh(streamlines.tube(radius=0.02))
pl.show()