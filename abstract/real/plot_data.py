import pylab

from fatiando.grav import io
from fatiando import utils, vis, grid

pylab.figure(figsize=(15,10))
pylab.subplots_adjust(hspace=0.4, wspace=0.3)
levels = 12
angle = 40
nx, ny = 40, 60

for i, field in enumerate(['gxx', 'gxy', 'gxz', 'gyy', 'gyz', 'gzz']):

    data = io.load('%s.txt' % (field))

    ax = pylab.subplot(2, 3, i + 1)
    pylab.title(field)
    pylab.axis('scaled')
    #pylab.plot(data['x'], data['y'], '.k')
    vis.contourf(data, levels, nx=nx, ny=ny)
    vis.contourf(data, levels, nx=nx, ny=ny)
    cb = pylab.colorbar()
    cb.set_label(r'$E\"otv\"os$', fontsize=14)
    labels = ax.get_xticklabels()
    for label in labels:
        label.set_rotation(angle)
    pylab.xlabel('Northing [m]')
    pylab.ylabel('Easting [m]')

pylab.savefig("ftg_data_raw.pdf")

datatopo = io.load_topo('topo.txt')

pylab.figure(figsize=(8,10))
pylab.title("Topography [m]")
pylab.axis('scaled')
levelslist = vis.contourf(datatopo, levels, vkey='h', nx=nx, ny=ny)
vis.contour(datatopo, levelslist, vkey='h', nx=nx, ny=ny)
labels = pylab.gca().get_xticklabels()
for label in labels:
    label.set_rotation(angle)
pylab.xlabel('Northing [m]')
pylab.ylabel('Easting [m]')

pylab.savefig("topo_raw.pdf")

pylab.show()