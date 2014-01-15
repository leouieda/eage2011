import pickle

import numpy
from enthought.mayavi import mlab
mlab.options.backend = 'envisage'

from fatiando import vis
import fatiando.mesh

f = open("mesh.pickle")
mesh = pickle.load(f)
f.close()
f = open("seeds.pickle")
seeds = pickle.load(f)
f.close()

seed_mesh = numpy.array([seed['cell'] for seed in seeds])
corpo = fatiando.mesh.vfilter(mesh, 1, 1000)

# Plot the resulting model
fig = mlab.figure()
fig.scene.background = (1, 1, 1)
vis.plot_prism_mesh(seed_mesh, style='surface', xy2ne=True)
plot = vis.plot_prism_mesh(corpo, style='surface', xy2ne=True)
plot = vis.plot_prism_mesh(mesh, style='surface', opacity=0.2, xy2ne=True)
axes = mlab.axes(plot, nb_labels=5, color=(0,0,0))
axes.label_text_property.color = (0,0,0)
axes.title_text_property.color = (0,0,0)
axes.axes.label_format = "%-.2f"
mlab.outline(color=(0,0,0))
mlab.show()
