"""
Make some synthetic FTG data.
"""

import pickle

import pylab
import numpy
from enthought.mayavi import mlab

from fatiando.grav import synthetic, io
from fatiando import utils, vis, geometry

# Get a logger for the script
log = utils.get_logger()

# Set logging to a file
utils.set_logfile('make_data.log')

# Log a header with the current version info
log.info(utils.header())

# Make the prism model
prisms = []
prisms.append(geometry.prism(x1=600, x2=1200, y1=200, y2=4200, z1=100, z2=600,
                             props={'value':1300}))
prisms.append(geometry.prism(x1=3000, x2=4000, y1=1000, y2=2000, z1=200, z2=800,
                             props={'value':1000}))
prisms.append(geometry.prism(x1=2700, x2=3200, y1=3700, y2=4200, z1=0, z2=900,
                             props={'value':1200}))
prisms.append(geometry.prism(x1=1500, x2=4500, y1=2500, y2=3000, z1=100, z2=500,
                             props={'value':1500}))

prisms = numpy.array(prisms)

# Show the model before calculating to make sure it's right
fig = mlab.figure()
fig.scene.background = (1, 1, 1)
dataset = vis.plot_prism_mesh(prisms, style='surface', label='Density kg/cm^3')
axes = mlab.axes(dataset, nb_labels=5, extent=[0,5000,0,5000,-1000,0])
mlab.show()

# Pickle the model so that it can be shown next to the inversion result later
modelfile = open('model.pickle', 'w') 
pickle.dump(prisms, modelfile)
modelfile.close()

# Calculate all the components of the gradient tensor
error = 2

pylab.figure(figsize=(16,8))
pylab.suptitle(r'Synthetic FTG data with %g $E\"otv\"os$ noise' 
               % (error), fontsize=16)
pylab.subplots_adjust(wspace=0.4, hspace=0.3)

for i, field in enumerate(['gxx', 'gxy', 'gxz', 'gyy', 'gyz', 'gzz']):

    data = synthetic.from_prisms(prisms, x1=0, x2=5000, y1=0, y2=5000,
                                 nx=50, ny=50, height=150, field=field)
    
    data['value'], error = utils.contaminate(data['value'], 
                                             stddev=error, 
                                             percent=False, 
                                             return_stddev=True)
    
    data['error'] = error*numpy.ones(len(data['value']))

    io.dump('%s_data.txt' % (field), data)

    pylab.subplot(2, 3, i + 1)
    pylab.axis('scaled')
    pylab.title(field)
    vis.contourf(data, 10)
    vis.contourf(data, 10)
    cb = pylab.colorbar(shrink=0.9)
    cb.set_label(r'$E\"otv\"os$', fontsize=14)
    pylab.xlabel('X [m]')
    pylab.ylabel('Y [m]')

pylab.savefig("data_ftg_raw.pdf")

pylab.show()