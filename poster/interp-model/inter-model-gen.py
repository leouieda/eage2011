import pylab
import numpy
from enthought.mayavi import mlab

import fatiando.inv.gplant as gplant
import fatiando.grav.synthetic as synthetic
import fatiando.mesh
import fatiando.utils as utils
import fatiando.vis as vis

# Get a logger
log = utils.get_logger()
# Set logging to a file
utils.set_logfile('interp-model-gen.log')
# Log a header with the current version info
log.info(utils.header())

# GENERATE SYNTHETIC DATA
################################################################################
# Make the prism model
model = []
model.append({'x1':1000, 'x2':2000, 'y1':1000, 'y2':2000, 'z1':1000, 'z2':2000,
               'value':1000})
model = numpy.array(model)

x1, x2 = 0, 3000
y1, y2 = 0, 3000
z1, z2 = 0, 3000
extent = [x1, x2, y1, y2, -z2, -z1]

# Now calculate all the components of the gradient tensor and contaminate the
# data with gaussian noise
error = 0.5
data = {}
for i, field in enumerate(['gzz']):
    data[field] = synthetic.from_prisms(model, x1=0, x2=3000, y1=0, y2=3000,
                                        nx=30, ny=30, height=150, field=field)
    data[field]['value'], error = utils.contaminate(data[field]['value'],
                                                    stddev=error,
                                                    percent=False,
                                                    return_stddev=True)
    data[field]['error'] = error*numpy.ones(len(data[field]['value']))

# PERFORM THE INVERSION
################################################################################
# Generate a prism mesh
mesh = fatiando.mesh.prism_mesh(x1=x1, x2=x2, y1=y1, y2=y2, z1=z1, z2=z2,
                                nx=30, ny=30, nz=30)

# Set the seeds and save them for later use
log.info("Setting seeds in mesh:")
seeds = []
seeds.append(gplant.get_seed((1501, 1501, 1501), 1000, mesh))

# Make a mesh for the seeds to plot them
seed_mesh = numpy.array([seed['cell'] for seed in seeds])

# Run the inversion
results = gplant.grow(data, mesh, seeds, compactness=10**(4), power=3,
                      threshold=10**(-3), norm=2, neighbor_type='reduced',
                      jacobian_file=None, distance_type='radial')

# Unpack the results and calculate the adjusted data
estimate, residuals, misfits, goals = results
fatiando.mesh.fill(estimate, mesh)
adjusted = gplant.adjustment(data, residuals)

# PLOT THE INVERSION RESULTS
################################################################################
log.info("Plotting")

# Plot the adjusted model plus the skeleton of the synthetic model
fig = mlab.figure()
fig.scene.background = (1, 1, 1)
plot = vis.plot_prism_mesh(seed_mesh, style='surface', label='Density')
plot = vis.plot_prism_mesh(mesh, style='surface', label='Density')
plot = vis.plot_prism_mesh(mesh, style='surface', label='Density')
axes = mlab.axes(plot, nb_labels=5, extent=extent, color=(0,0,0))
axes.label_text_property.color = (0,0,0)
axes.title_text_property.color = (0,0,0)
axes.axes.label_format = "%-#.0f"
mlab.outline(color=(0,0,0), extent=extent)
Y, X, Z = utils.extract_matrices(data['gzz'])
mlab.surf(X, Y, Z)
mlab.show()
