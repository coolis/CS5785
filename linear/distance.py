#!/usr/bin/env python
__author__ = 'wenli'


# code taken from
import math
import os
import time
import numpy
import matplotlib.pyplot as pyplot
from pprint import pprint
from datetime import datetime

dir = os.path.dirname(__file__)

def get_distance(lat1, long1, lat2, long2):
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    # MODIFIED TO return distance in miles
    return arc*3960.0

if __name__ == '__main__':
    trips = []
    error_count  = 0
    for line in file(os.path.join(dir, 'example_data_no_header.csv')):
        line = line.strip().split(',')
        plong,plat,dlong,dlat=line[-4:]
        plong = float(plong)
        plat = float(plat)
        dlong = float(dlong)
        dlat = float(dlat)

        #pick up time
        ptime = float(time.mktime(datetime.strptime(line[5], "%Y-%m-%d %H:%M:%S").timetuple()))
        #trip time in secs
        ttime = float(line[8])
        #trip distance
        tdistance = float(line[9])
        try:
            #absolute displacement
            trip = (ttime, ptime, tdistance, get_distance(plat,plong,dlat,dlong))
            trips.append(trip)
        except:
            error_count += 1
            print plong,plat,dlong,dlat
            print error_count

    print error_count

    data = numpy.asmatrix(trips)

    data[:,3].sort()
    #print "number of distances","maximum distance","minimum distance"
    print len(data[:,3]),max(data[:,3]),min(data[:,3]) # distance is measured in miles
    #"Top 50 distances, obvious outliers"
    #pprint(trips[:50])


    color = ['r'] * data.shape[0]
    #create the plot panel
    fig = pyplot.figure()
    ax = fig.add_subplot(3, 1, 1)
    ax.scatter(data[:,0], data[:,1], c=color)
    ax = fig.add_subplot(3, 1, 2)
    ax.scatter(data[:,0], data[:,2], c=color)
    ax = fig.add_subplot(3, 1, 3)
    ax.scatter(data[:,0], data[:,3], c=color)
    pyplot.show()

