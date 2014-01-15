Code, expanded abstract and poster presented at the 2011 73th EAGE Conference
and Exhibition incorporating SPE EUROPEC in Viena, Austria

Results were generated using open-source software [Fatiando a
Terra](http://fatiando.org)

Poster is available on figshare:
[doi:10.6084/m9.figshare.91511](http://dx.doi.org/10.6084/m9.figshare.91511)

A PDF version of the expanded abstract is available from
[my personal page](http://fatiando.org/people/uieda/)

Citation:

Uieda, L., and V. C. F. Barbosa (2011), 3D gravity gradient inversion by
planting density anomalies, 73th EAGE Conference & Exhibition incorporating SPE
EUROPEC, pp. 1-5.

# 3D gravity gradient inversion by planting density anomalies

**Leonardo Uieda and Valéria C. F. Barbosa**

We present a new gravity gradient tensor inversion for estimating a 3D
density-contrast distribution defined on a user-specified grid of prisms. Our
method consists of an iterative algorithm that does not require the solution of
large equation system. Instead, the solution grows systematically around
user-specified prismatic elements called “seeds”. Each seed can have a different
density contrast, allowing the interpretation of multiples bodies with different
density contrasts. The compactness of the solution is imposed by means of a
regularizing function that favors compact bodies closest to the priorly
specified seeds. The solution grows by accreting neighboring prisms of the
current solution. The prisms for the accretion are chosen by systematically
searching the set of current neighboring prisms. Therefore, this approach allows
that the columns of the Jacobian matrix be calculated on demand. This is a known
technique from computer science called “lazy evaluation”, which greatly reduces
the demand of computer memory and processing time. Test on synthetic data from
multiple buried sources at different depths and on real data collected over iron
deposits located in the Quadrilátero Ferrífero, southeastern region of Brazil,
confirmed the ability of our method in detecting sharp and compact bodies.
