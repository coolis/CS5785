#!/usr/bin/env python
__author__ = 'aub3'


# code taken from
import math
import os
import time
import numpy
import matplotlib.pyplot as pyplot
from sklearn import linear_model
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

def outlier_filter_simple(data, index, quantile):
    #filt outlier by remove all the points larger than the quantile
    list_index = []
    #mean of the data by column
    mean = numpy.mean(data, axis=0)
    #median of the data by column
    median = numpy.median(data, axis=0)
    #standard deviation of the data by column
    std = numpy.std(data, axis=0)

    for i,d in enumerate(data):
        #if the distance to the mean is bigger than quantile times the standard deviation, the outlier marked
        if math.fabs(d[0, index] - median[0, index]) > quantile * std[0, index]:
            list_index.append(i)
    return numpy.delete(data, list_index, 0)

#@parameter numpy array, integer
#@return: numpy array, numpy array
def split_data(data, index):
    train = []
    test = []
    for i,d in enumerate(data):
        if (i+1) % index == 0:
             test.append(d)
        else:
            train.append(d)
    return (numpy.asmatrix(train), numpy.asmatrix(test))


if __name__ == '__main__':
    trips = []
    error_count  = 0
    header = True;
    for line in file(os.path.join(dir, 'trip_data_2.csv')):
        if header:
            header = False
            continue
        try:
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
            #absolute displacement
            distance = get_distance(plat,plong,dlat,dlong)
            trip = (ttime, ptime, tdistance, distance)
            trips.append(trip)
        except:
            error_count += 1
            print ptime,ttime,tdistance,plong,plat,dlong,dlat
            print error_count

    print error_count

    data = numpy.asmatrix(trips)
    #outlier filter
    data = outlier_filter_simple(data, 3, 1)
    data = outlier_filter_simple(data, 3, 1)

    #linear regresion, given trip distance, predicts trip time
    (xTrain, xTest) = split_data(numpy.asarray(data[:, 2]), 4)
    (yTrain, yTest) = split_data(numpy.asarray(data[:, 0]), 4)

    clf = linear_model.LinearRegression()
    clf.fit(xTrain, yTrain)
    ols = numpy.sum(numpy.asarray(clf.predict(xTest)-yTest) ** 2)
    tls = ols / (numpy.sum(clf.coef_ * clf.coef_.T) + 1)
    print ("Coefficients: ", clf.coef_)
    print ("OLS", ols)
    print ("TLS", tls)

    pyplot.plot(xTest, yTest, 'co', xTest, clf.predict(xTest), '-')

    #create the plot panel
    #fig = pyplot.figure()
    #ax = fig.add_subplot(3, 1, 1)
    #ax.scatter(data[:,0], data[:,1], c=['r'] * data.shape[0])
    #ax = fig.add_subplot(3, 1, 2)
    #ax.scatter(data[:,0], data[:,2], c=['g'] * data.shape[0])
    #ax = fig.add_subplot(3, 1, 3)
    #ax.scatter(data[:,0], data[:,3], c=['b'] * data.shape[0])
    pyplot.show()
