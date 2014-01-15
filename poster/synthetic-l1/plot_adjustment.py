import pylab
import fatiando.grav.io as io
import fatiando.vis as vis

# Load the synthetic data
data = {}
data['gzz'] = io.load('gzz.txt')
data['gyy'] = io.load('gyz.txt')
data['gyz'] = io.load('gyy.txt')
adjusted = {}
adjusted['gzz'] = io.load('gzz_adj.txt')
adjusted['gyy'] = io.load('gyz_adj.txt')
adjusted['gyz'] = io.load('gyy_adj.txt')
posdata = {}
posdata['gzz'] = io.load('gzz_pos.txt')
posdata['gyy'] = io.load('gyz_pos.txt')
posdata['gyz'] = io.load('gyy_pos.txt')

fields = ['gyy', 'gyz', 'gzz']
# Change the x and y axis so that x points north
for field in fields:
    tmp =  data[field]['x']*0.001
    data[field]['x'] = data[field]['y']*0.001
    data[field]['y'] = tmp
    tmp =  posdata[field]['x']*0.001
    posdata[field]['x'] = posdata[field]['y']*0.001
    posdata[field]['y'] = tmp
    tmp =  adjusted[field]['x']*0.001
    adjusted[field]['x'] = adjusted[field]['y']*0.001
    adjusted[field]['y'] = tmp

# Get the adjustment and plot it
pylab.figure(figsize=(16,8))
pylab.subplots_adjust(hspace=0.3)
for i, field in enumerate(fields):
    pylab.subplot(2, 3, i + 1)
    pylab.title(field)
    pylab.axis('scaled')
    levels = vis.contour(data[field], levels=5, color='k', label='Data')
    for c in pylab.gca().collections:
        c.set_linestyle('dashed')
        c.set_linewidth(1.5)
    vis.contour(adjusted[field], levels=levels, color='r', label='Adjusted', clabel=False)
    for c in pylab.gca().collections[len(levels):]:
        c.set_linestyle('solid')
        c.set_linewidth(1.5)
    pylab.xlabel("Easting (km)")
    pylab.ylabel("Northing (km)")
for i, field in enumerate(fields):
    pylab.subplot(2, 3, i + 4)
    pylab.title(field)
    pylab.axis('scaled')
    levels = vis.contour(posdata[field], levels=5, color='k', label='Data')
    for c in pylab.gca().collections:
        c.set_linestyle('dashed')
        c.set_linewidth(1.5)
    vis.contour(adjusted[field], levels=levels, color='r', label='Adjusted', clabel=False)
    for c in pylab.gca().collections[len(levels):]:
        c.set_linestyle('solid')
        c.set_linewidth(1.5)
    pylab.xlabel("Easting (km)")
    pylab.ylabel("Northing (km)")
pylab.legend(loc='lower left', prop={'size':9}, shadow=True)
pylab.show()
