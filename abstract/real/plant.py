"""
Example script for doing the inversion of synthetic FTG data using grow
"""

import pickle

import pylab
import numpy
from enthought.mayavi import mlab

from fatiando.inv import gplant
from fatiando.grav import io
import fatiando.mesh
from fatiando import utils, vis

# Get a logger
log = utils.get_logger()

# Set logging to a file
utils.set_logfile('plant.log')

# Log a header with the current version info
log.info(utils.header())

# Load the synthetic data
gzz = io.load('gzz.txt')
#gxx = io.load('gxx.txt')
#gxy = io.load('gxy.txt')
#gxz = io.load('gxz.txt')
#gyy = io.load('gyy.txt')
#gyz = io.load('gyz.txt')

topo = io.load_topo('topo.txt')

data = {}
data['gzz'] = gzz
#data['gxx'] = gxx
#data['gxy'] = gxy
#data['gxz'] = gxz
#data['gyy'] = gyy
#data['gyz'] = gyz

xmin, xmax = 1.0*topo['x'].min(), 0.995*topo['x'].max()
ymin, ymax = 1.005*topo['y'].min(), 0.987*topo['y'].max()
#xmin, xmax = topo['x'].min(), topo['x'].max()
#ymin, ymax = topo['y'].min(), topo['y'].max()
zmin, zmax = -topo['h'].max(), -400

# Generate a model space mesh
mesh = fatiando.mesh.prism_mesh(x1=xmin, x2=xmax, y1=ymin, y2=ymax, z1=zmin,
                                z2=zmax, nx=50, ny=50, nz=30, topo=topo)

# Fill it with zeros so that I can plot the mesh with the seeds
fatiando.mesh.fill(numpy.zeros(mesh.size), mesh, fillNone=False)

# Set the seeds and save them for later use
log.info("Getting seeds from mesh:")
spoints = []
sdens = []
# Upper
spoints.append((11000, 16230, -950))
sdens.append(830)
spoints.append((11300, 16620, -950))
sdens.append(830)
spoints.append((11525, 16880, -950))
sdens.append(830)
# Lower
spoints.append((11290, 15570, -900))
sdens.append(830)
#spoints.append((11575, 15460, -900))
#sdens.append(830)
spoints.append((11650, 16200, -900))
sdens.append(830)
spoints.append((11760, 16540, -900))
sdens.append(830)
# Negative
spoints.append((11210, 16175, -950))
sdens.append(-400)
spoints.append((10950, 15810, -950))
sdens.append(-400)
spoints.append((10825, 15510, -950))
sdens.append(-400)
spoints.append((11000, 16900, -900))
sdens.append(-400)
spoints.append((11920, 16070, -950))
sdens.append(-400)
spoints.append((11670, 15225, -900))
sdens.append(-400)

seeds = [gplant.get_seed(p, dens, mesh) for p, dens in zip(spoints, sdens)]

# Make a mesh for the seeds to plot them
seed_mesh = numpy.array([seed['cell'] for seed in seeds])

# Show the seeds before starting
pylab.figure()
pylab.axis('scaled')
l = vis.contourf(data['gzz'], 10, nx=40, ny=60)
vis.contour(data['gzz'], l, nx=40, ny=60)
for p in spoints:
    pylab.plot(p[0], p[1], '*k', markersize=9)
labels = pylab.gca().get_xticklabels()
for label in labels:
    label.set_rotation(30)
pylab.savefig('seeds.pdf')
pylab.xlabel('Northing [m]')
pylab.ylabel('Easting [m]')

pylab.show()

fig = mlab.figure()
fig.scene.background = (1, 1, 1)
fig.scene.camera.yaw(230)
plot = vis.plot_prism_mesh(mesh, opacity=0.4)
plot = vis.plot_prism_mesh(seed_mesh)
axes = mlab.axes(plot, nb_labels=5, extent=[xmin,xmax,ymin,ymax,-zmax,-zmin])

mlab.show()

# Run the inversion
results = gplant.grow(data, mesh, seeds, compactness=10**(5), power=5, norm=1,
                      threshold=5*10**(-5), jacobian_file=None,
                      distance_type='radial')

estimate, residuals, misfits, goals = results

adjusted = gplant.adjustment(data, residuals)

fatiando.mesh.fill(estimate, mesh, fillNone=False)

log.info("Pickling results")

output = open('mesh.pickle', 'w')
pickle.dump(mesh, output)
output.close()

seed_file = open("seeds.pickle", 'w')
pickle.dump(seeds, seed_file)
seed_file.close()

res_file = open("results.pickle", 'w')
pickle.dump(results, res_file)
res_file.close()

log.info("Plotting results")

pylab.figure(figsize=(8,6))
pylab.suptitle("Inversion results:", fontsize=16)
pylab.subplots_adjust(hspace=0.4)

# Plot the residuals
pylab.subplot(2,1,1)
pylab.title("Residuals")
vis.residuals_histogram(residuals)
pylab.xlabel('Eotvos')

# Plot the misfit and goal function per iteration
ax = pylab.subplot(2,1,2)
pylab.title("Goal function and misfit")
pylab.plot(goals, '-b', label="Goal Function")
pylab.plot(misfits, '-r', label="Misfit")
pylab.xlabel("Iteration")
pylab.legend(loc='lower left', prop={'size':10}, shadow=True)
ax.set_yscale('log')
ax.grid()
pylab.savefig('residuals.pdf')

# Plot the adjustment of all components
angle = 40.
nx = 40
ny = 60

for i, field in enumerate(['gxx', 'gxy', 'gxz', 'gyy', 'gyz', 'gzz']):

    if field in data:
        

        pylab.figure(figsize=(14,8))
        pylab.subplots_adjust(hspace=0.3)

        ax = pylab.subplot(1,3,1)
        pylab.title("Comparison")
        pylab.axis('scaled')
        levels = vis.contour(data[field], 10, color='b', label='Data', nx=nx,
                             ny=ny)
        vis.contour(adjusted[field], levels, color='r', label='Adjusted', nx=nx,
                    ny=ny)
        #pylab.legend(loc='lower right', prop={'size':10}, shadow=True)
        labels = ax.get_xticklabels()
        for label in labels:
            label.set_rotation(angle)
        pylab.xlabel('Northing [m]')
        pylab.ylabel('Easting [m]')

        ax = pylab.subplot(1,3,2)
        pylab.title("Adjusted")
        pylab.axis('scaled')
        vis.contourf(adjusted[field], levels, nx=nx, ny=ny)
        vis.contour(adjusted[field], levels, nx=nx, ny=ny)
        labels = ax.get_xticklabels()
        for label in labels:
            label.set_rotation(angle)
        pylab.xlabel('Northing [m]')
        pylab.ylabel('Easting [m]')

        ax = pylab.subplot(1,3,3)
        pylab.title("Data")
        pylab.axis('scaled')
        vis.contourf(data[field], levels, nx=nx, ny=ny)
        vis.contour(data[field], levels, nx=nx, ny=ny)
        labels = ax.get_xticklabels()
        for label in labels:
            label.set_rotation(angle)
        pylab.xlabel('Northing [m]')
        pylab.ylabel('Easting [m]')

        pylab.savefig("adjustment_%s.pdf" % (field))

pylab.show()

# Plot the resulting model
fig = mlab.figure()
fig.scene.background = (1, 1, 1)
#fig.scene.camera.yaw(230)
vis.plot_prism_mesh(seed_mesh, style='surface')
plot = vis.plot_prism_mesh(mesh, style='surface', opacity=0.2)
plot = vis.plot_prism_mesh(mesh, style='surface', )
axes = mlab.axes(plot, nb_labels=5, extent=[ymin,ymax,xmin,xmax,-zmax,-zmin])

mlab.show()
