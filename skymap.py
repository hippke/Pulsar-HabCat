import numpy
import csv
import astropy.coordinates as coord
import matplotlib.pylab as plt
import astropy.units as u
from astropy.io import ascii

def plot_mwd(RA,Dec,org=0,title='Exoplants', projection='mollweide'):
    ''' RA, Dec are arrays of the same length.
    RA takes values in [0,360), Dec in [-90,90],
    which represent angles in degrees.
    org is the origin of the plot, 0 or a multiple of 30 degrees in [0,360).
    title is the title of the figure.
    projection is the kind of projection: 'mollweide', 'aitoff', 'hammer', 'lambert'
    '''
    x = numpy.remainder(RA+360-org,360) # shift RA values
    ind = x>180
    x[ind] -=360    # scale conversion to [-180, 180]
    x=-x    # reverse the scale: East to the left
    tick_labels = numpy.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
    tick_labels = numpy.remainder(tick_labels+360+org,360)
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection=projection, axisbg ='LightCyan')
    ax.scatter(numpy.radians(x),numpy.radians(Dec))  # convert degrees to radians
    ax.set_xticklabels(tick_labels)     # we add the scale on the x axis
    ax.set_title(title)
    ax.title.set_fontsize(15)
    ax.set_xlabel("RA")
    ax.xaxis.label.set_fontsize(12)
    ax.set_ylabel("Dec")
    ax.yaxis.label.set_fontsize(12)
    ax.grid(True)

ra_coord = numpy.array([])
de_coord = numpy.array([])
with open('planet_list.csv', 'r') as csvfile:
    dataset = csv.reader(csvfile, delimiter=',')
    for row in dataset:
        ra = coord.Angle(row[1], unit=u.hour)  # Define as hours
        de = coord.Angle(row[2], unit=u.deg)
        ra_coord = numpy.append(ra_coord, ra.degree)
        de_coord = numpy.append(de_coord, de.degree)

plot_mwd(ra_coord,de_coord, org=90, title ='Exoplanets')
plt.savefig("planets_skymap.pdf", bbox_inches = 'tight')
plt.show()
