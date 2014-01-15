import pickle

import pylab
from enthought.mayavi import mlab

import fatiando.grav.io as io
import fatiando.inv.gplant as gplant
import fatiando.vis as vis

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

# Unpickle the results
res_file = open("results.pickle")
results = pickle.load(res_file)
res_file.close()

estimate, residuals, misfits, goals = results

adjusted = gplant.adjustment(data, residuals)


# Change the x and y axis so that x points north
for field in ['gxx', 'gxy', 'gxz', 'gyy', 'gyz', 'gzz']:
    tmp =  data[field]['x']*0.001
    data[field]['x'] = data[field]['y']*0.001
    data[field]['y'] = tmp
    tmp =  adjusted[field]['x']*0.001
    adjusted[field]['x'] = adjusted[field]['y']*0.001
    adjusted[field]['y'] = tmp

# Plot the residuals and goal function per iteration
#pylab.figure(figsize=(8,6))
#pylab.suptitle("Inversion results:", fontsize=16)
#pylab.subplots_adjust(hspace=0.4)

#pylab.subplot(2,1,1)
#pylab.title("Residuals")
#vis.residuals_histogram(residuals)
#pylab.xlabel('Eotvos')

#ax = pylab.subplot(2,1,2)
#pylab.title("Goal function and Data misfit")
#pylab.plot(goals, '.-b', label="Goal Function", linewidth=2)
#pylab.plot(misfits, '.-r', label="Misfit", linewidth=2)
#pylab.xlabel("Iteration")
#pylab.legend(loc='upper left', prop={'size':9}, shadow=True)
#ax.set_yscale('log')
#ax.grid()

#pylab.savefig('residuals_raw.pdf')

# Get the adjustment and plot it
pylab.figure(figsize=(16,8))
pylab.suptitle(r'Adjustment [$E\"otv\"os$]', fontsize=16)
pylab.subplots_adjust(hspace=0.3)

nx, ny = 33, 33

for i, field in enumerate(['gxx', 'gxy', 'gxz', 'gyy', 'gyz', 'gzz']):
    
    if field in data:
        
        pylab.subplot(2, 3, i + 1)
        #pylab.figure()
        pylab.title(field)    
        pylab.axis('scaled')
        levels = vis.contour(adjusted[field], levels=5, color='r', label='Adjusted', clabel=False)
        for c in pylab.gca().collections:
            c.set_linestyle('solid')
            c.set_linewidth(1.5)
        vis.contour(data[field], levels=levels, color='k', label='Data')
        for c in pylab.gca().collections[len(levels):]:
            c.set_linestyle('dashed')
            c.set_linewidth(1.5)
        pylab.xlabel('Easting (km)')
        pylab.ylabel('Northing (km)')
        #pylab.savefig("adjustment_%s.pdf" % (field))

pylab.legend(loc='lower left', prop={'size':9}, shadow=True)
#pylab.savefig("comparison_raw.pdf")

pylab.figure(figsize=(16,8))
pylab.subplots_adjust(wspace=0.4, hspace=0.3)

for i, field in enumerate(['gxx', 'gxy', 'gxz', 'gyy', 'gyz', 'gzz']):

    if field in data:

        pylab.subplot(2, 3, i + 1)
        pylab.title(field)
        pylab.axis('scaled')
        levels = vis.contourf(data[field], 10)
        vis.contourf(adjusted[field], levels)
        cb = pylab.colorbar(shrink=0.9)
        cb.set_label(r'$E\"otv\"os$', fontsize=14)
        pylab.xlabel('X [m]')
        pylab.ylabel('Y [m]')

#pylab.savefig("adjusted_raw.pdf")

pylab.figure(figsize=(16,8))
pylab.subplots_adjust(wspace=0.4, hspace=0.3)

for i, field in enumerate(['gxx', 'gxy', 'gxz', 'gyy', 'gyz', 'gzz']):

    if field in data:

        pylab.subplot(2, 3, i + 1)
        pylab.title(field)
        pylab.axis('scaled')
        levels = vis.contourf(data[field], 10)
        vis.contourf(data[field], levels)
        cb = pylab.colorbar(shrink=0.9)
        cb.set_label(r'$E\"otv\"os$', fontsize=14)
        vis.contour(data[field], levels=levels, color='k', clabel=False)
        for c in pylab.gca().collections[len(levels):]:
            c.set_linestyle('solid')
            #c.set_linewidth(1.5)
        pylab.xlabel('Easting (km)')
        pylab.ylabel('Northing (km)')

#pylab.savefig("data_ftg_raw.pdf")

pylab.show()