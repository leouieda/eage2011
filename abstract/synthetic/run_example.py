import pickle

import pylab
import numpy
from enthought.mayavi import mlab

import fatiando.inv.gplant as gplant
import fatiando.grav.io as io
import fatiando.mesh
import fatiando.utils
import fatiando.vis as vis

# Get a logger
log = fatiando.utils.get_logger()

# Set logging to a file
fatiando.utils.set_logfile('synthetic_run.log')

# Log a header with the current version info
log.info(fatiando.utils.header())

# Load the synthetic data
gzz = io.load('gzz_data.txt')
gxx = io.load('gxx_data.txt')
gxy = io.load('gxy_data.txt')
gxz = io.load('gxz_data.txt')
gyy = io.load('gyy_data.txt')
gyz = io.load('gyz_data.txt')

data = {}
data['gzz'] = gzz
data['gxx'] = gxx
data['gxy'] = gxy
data['gxz'] = gxz
data['gyy'] = gyy
data['gyz'] = gyz

# Load the synthetic model for comparison
synth_file = open('model.pickle')
synthetic = pickle.load(synth_file)
synth_file.close()

# Generate a model space mesh
x1, x2 = 0, 5000
y1, y2 = 0, 5000
z1, z2 = 0, 1000
mesh = fatiando.mesh.prism_mesh(x1=x1, x2=x2, y1=y1, y2=y2, z1=z1, z2=z2, 
                                nx=50, ny=50, nz=10)

# Set the seeds and save them for later use
log.info("Getting seeds from mesh:")

seedpoints = []
seedpoints.append(((3701, 1201, 501), 1000))
seedpoints.append(((3201, 1201, 501), 1000))
seedpoints.append(((3701, 1701, 501), 1000))
seedpoints.append(((3201, 1701, 501), 1000))
seedpoints.append(((901, 701, 301), 1300))
seedpoints.append(((901, 1201, 301), 1300))
seedpoints.append(((901, 1701, 301), 1300))
seedpoints.append(((901, 2201, 301), 1300))
seedpoints.append(((901, 2701, 301), 1300))
seedpoints.append(((901, 3201, 301), 1300))
seedpoints.append(((901, 3701, 301), 1300))
seedpoints.append(((2951, 3951, 301), 1200))
seedpoints.append(((2951, 3951, 701), 1200))
seedpoints.append(((2001, 2751, 301), 1500))
seedpoints.append(((2501, 2751, 301), 1500))
seedpoints.append(((3001, 2751, 301), 1500))
seedpoints.append(((3501, 2751, 301), 1500))
seedpoints.append(((4001, 2751, 301), 1500))

seeds = [gplant.get_seed(point, dens, mesh) for point, dens in seedpoints]

# Make a mesh for the seeds to plot them
seed_mesh = numpy.array([seed['cell'] for seed in seeds])

# Plot the seeds ontop of the data
pylab.figure()
#pylab.title()
pylab.axis('scaled')
vis.contourf(data['gzz'], 10)
cb = pylab.colorbar()
cb.set_label(r'$E\"otv\"os$', fontsize=14)
xs = []
ys = []
for p, dens in seedpoints:
    xs.append(p[0])
    ys.append(p[1])
pylab.plot(xs, ys, '*k', markersize=9, label='Seeds')
pylab.xlabel('X [m]')
pylab.ylabel('Y [m]')
pylab.legend(shadow=True, loc='lower right')
pylab.savefig('seeds_raw.pdf')

#pylab.show()

# Show the seeds first to confirm that they are right
fig = mlab.figure()
fig.scene.background = (1, 1, 1)
vis.plot_prism_mesh(synthetic, style='wireframe')
plot = vis.plot_prism_mesh(seed_mesh, style='surface')
axes = mlab.axes(plot, nb_labels=5, extent=[x1, x2, y1, y2, -z2, -z1])
mlab.show()

# Run the inversion
results = gplant.grow(data, mesh, seeds, compactness=10**(15), power=5,
                      threshold=5*10**(-4), norm=2, neighbor_type='reduced',
                      jacobian_file=None, distance_type='radial')

estimate, residuals, misfits, goals = results

adjusted = gplant.adjustment(data, residuals)

fatiando.mesh.fill(estimate, mesh)

log.info("Pickling results")

# Save the results
output = open('mesh.pickle', 'w')
pickle.dump(mesh, output)
output.close()

seed_file = open("seeds.pickle", 'w')
pickle.dump(seeds, seed_file)
seed_file.close()

res_file = open("results.pickle", 'w')
pickle.dump(results, res_file)
res_file.close()

log.info("Plotting")

# Plot the residuals and goal function per iteration
pylab.figure(figsize=(8,6))
pylab.suptitle("Inversion results:", fontsize=16)
pylab.subplots_adjust(hspace=0.4)

pylab.subplot(2,1,1)
pylab.title("Residuals")
vis.residuals_histogram(residuals)
pylab.xlabel('Eotvos')

ax = pylab.subplot(2,1,2)
pylab.title("Goal function and Data misfit")
pylab.plot(goals, '.-b', label="Goal Function", linewidth=2)
pylab.plot(misfits, '.-r', label="Misfit", linewidth=2)
pylab.xlabel("Iteration")
pylab.legend(loc='upper left', prop={'size':9}, shadow=True)
ax.set_yscale('log')
ax.grid()

pylab.savefig('residuals_raw.pdf')

# Get the adjustment and plot it
pylab.figure(figsize=(16,8))
pylab.suptitle(r'Adjustment [$E\"otv\"os$]', fontsize=16)

for i, field in enumerate(['gxx', 'gxy', 'gxz', 'gyy', 'gyz', 'gzz']):
    
    if field in data:
        
        pylab.subplot(2, 3, i + 1)    
        pylab.title(field)    
        pylab.axis('scaled')    
        levels = vis.contour(data[field], levels=5, color='b', label='Data')
        vis.contour(adjusted[field], levels=levels, color='r', label='Adjusted')
        #pylab.legend(loc='lower left', prop={'size':9}, shadow=True)
        pylab.xlabel('X [m]')
        pylab.ylabel('Y [m]')

pylab.savefig("adjustment_raw.pdf")

pylab.show()

# Plot the adjusted model plus the skeleton of the synthetic model
fig = mlab.figure()
fig.scene.background = (1, 1, 1)
vis.plot_prism_mesh(synthetic, style='wireframe')
vis.plot_prism_mesh(seed_mesh, style='surface')
plot = vis.plot_prism_mesh(mesh, style='surface')
axes = mlab.axes(plot, nb_labels=5, extent=[x1, x2, y1, y2, -z2, -z1])

mlab.show()
