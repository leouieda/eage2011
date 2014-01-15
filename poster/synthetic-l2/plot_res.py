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

f = open("model.pickle")
model = pickle.load(f)
f.close()

seed_mesh = numpy.array([seed['cell'] for seed in seeds])

fig = mlab.figure()
fig.scene.camera.yaw(230)
fig.scene.background = (1, 1, 1)
vis.plot_prism_mesh(model, style='wireframe', xy2ne=True)
plot = vis.plot_prism_mesh(mesh, xy2ne=True)
vis.plot_prism_mesh(seed_mesh, xy2ne=True)
axes = mlab.axes(plot, nb_labels=5, color=(0,0,0))
axes.label_text_property.color = (0,0,0)
axes.title_text_property.color = (0,0,0)
axes.axes.label_format = "%-#.0f"
mlab.outline(color=(0,0,0))

mlab.show()