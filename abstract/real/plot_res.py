import pickle
import numpy
from enthought.mayavi import mlab
from fatiando import vis

f = open("mesh.pickle")
mesh = pickle.load(f)
f.close()

f = open("seeds.pickle")
seeds = pickle.load(f)
f.close()

seed_mesh = numpy.array([seed['cell'] for seed in seeds])

fig = mlab.figure()
fig.scene.camera.yaw(230)
fig.scene.background = (1, 1, 1)
vis.plot_prism_mesh(mesh, opacity=0.2)
plot = vis.plot_prism_mesh(mesh)
vis.plot_prism_mesh(seed_mesh)
axes = mlab.axes(plot, nb_labels=5)

mlab.show()