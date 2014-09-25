#!/usr/bin/env python
__author__ = 'aub3'


# code taken from
import math
import os
import time
import numpy
import matplotlib.pyplot as pyplot
from pprint import pprint
from datetime import datetime

dir = os.path.dirname(__file__)

test = numpy.matrix([[1,2],[3,4]])

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

def outlier_filter_simple(data, index, quantile):
    #filt outlier by remove all the points larger than the quantile
    list_index = []
    
    for i,d in enumerate(data):
        if d.item(index) > quantile:
            list_index.append(i)
    return numpy.delete(data, list_index, 0)
    

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
            distance = get_distance(plat,plong,dlat,dlong)
            trip = (ttime, ptime, tdistance, distance)
            trips.append(trip)
        except:
            error_count += 1
            print plong,plat,dlong,dlat
            print error_count        
        
    print error_count
    
    data = numpy.asmatrix(trips)
    data = outlier_filter_simple(data, 3, 50)
    
    #create the plot panel
    fig = pyplot.figure()
    ax = fig.add_subplot(3, 1, 1)
    ax.scatter(data[:,0], data[:,1], c=['r'] * data.shape[0])
    ax = fig.add_subplot(3, 1, 2)
    ax.scatter(data[:,0], data[:,2], c=['g'] * data.shape[0])
    ax = fig.add_subplot(3, 1, 3)
    ax.scatter(data[:,0], data[:,3], c=['b'] * data.shape[0])
    pyplot.show()

