import pylab


xs = range(0, 21, 1)
ys = range(0, 21, 1)

pylab.axis('scaled')
for x in xs:
    pylab.plot([x, x], [ys[0], ys[-1]], '-k')

for y in ys:
    pylab.plot([xs[0], xs[-1]], [y, y], '-k')

pylab.xlim(0,20)
pylab.ylim(20,0)
pylab.show()