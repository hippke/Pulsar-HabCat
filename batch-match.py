"""Compare Pulsar and HabCat coordinates"""
import csv
import astropy.units as u
from astropy.coordinates import SkyCoord, Angle
from astropy import coordinates as coord


def flipra(coordinate):
    """Flips RA coordinates by 180 degrees"""    
    coordinate = coordinate + 180
    if coordinate > 360:
        coordinate = coordinate - 360
    return coordinate    

def flipde(coordinate):
    """Flips RA coordinates by 90 degrees""" 
    return coordinate * (-1.)


# Load HabCat
habcat_id = []
habcat_ra = []
habcat_de = []
with open('habcat.csv', 'rb') as csvfile:
    dataset = csv.reader(csvfile, delimiter=';')
    for row in dataset:
        habcat_id.append(row[0])
        ra = coord.Angle(row[1], unit=u.hour)  # Define as hours
        habcat_ra.append(ra.degree)  # Convert to degree
        de = coord.Angle(row[2], unit=u.deg)
        habcat_de.append(de.degree)
print len(habcat_id), 'HabCat datalines loaded'

# Load Pulsar catalogue
pulsar_id = []
pulsar_ra = []
pulsar_de = []
pulsar_period = []
with open('pulsar_16msec.csv', 'rb') as csvfile:
    dataset = csv.reader(csvfile, delimiter=';')
    for row in dataset:
        pulsar_id.append(row[0])
        ra = coord.Angle(row[1], unit=u.hour)  # Define as hours
        pulsar_ra.append(ra.degree)  # Convert to degree
        de = coord.Angle(row[2], unit=u.deg)
        pulsar_de.append(de.degree)
        pulsar_period.append(row[3])
print len(pulsar_id), 'Pulsar datalines loaded'

# Nested loop through all Pulsars to find closest 180deg HabCat for each
for currentpulsar in range(len(pulsar_id)):  # Pulsar loop
    shortest_distance = 180 * 60 # set to max, in arcminutes
    for currenthabcat in range(len(habcat_id)):  # HabCat loop
        habcat_coordinate = SkyCoord(
            habcat_ra[currenthabcat], 
            habcat_de[currenthabcat], 
            unit="deg")
        pulsar_coordinate_flipped = SkyCoord(  # flip pulsar coordinates
            flipra(pulsar_ra[currentpulsar]), 
            flipde(pulsar_de[currentpulsar]), 
            unit="deg")
        distance = pulsar_coordinate_flipped.separation(habcat_coordinate)
        if distance.arcminute < shortest_distance:
            shortest_distance = distance.arcminute  # New best found
            bestfit_pulsar_id = pulsar_id[currentpulsar]
            bestfit_habcat_id = habcat_id[currenthabcat]
    print bestfit_pulsar_id, bestfit_habcat_id, shortest_distance / 60.  # deg

    with open('result.csv', 'a') as fp:  # Append each result to CSV
        a = csv.writer(fp, delimiter=';')
        a.writerow([
            bestfit_pulsar_id, 
            bestfit_habcat_id, 
            shortest_distance / 60.])  # degrees

print 'Done.'
