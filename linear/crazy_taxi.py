#!/usr/bin/env python
__author__ = 'wenli'


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
big_data_1 = "trip_data_1.csv"
big_data_2 = "trip_data_2.csv"
small_data = "example_data.csv"

#get the distance between long, lat of two points
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

#outlier filter. It counts the distance of the data to the mean or median,
#and compare it with the standard deviation
#@param: data, the numpy matrix
#        index, a list of index where you want to apply the filter
#        quantile: the criteria of the filter
#@return: a numpy matrix of the filtered data
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
        for j in index:
            if math.fabs(d[0, j] - mean[0, j]) > quantile * std[0, j]:
                list_index.append(i)
                break
    return numpy.delete(data, list_index, 0)

#@parameter numpy array, integer
#@return: numpy array, numpy array
def split_data(data, index):
    train = data[0,:]
    test = data[index-1, :]
    for i,d in enumerate(data):
        if (i+1) % index == 0:
             test = numpy.concatenate((test, d), axis=0)
        else:
            train = numpy.concatenate((train, d), axis=0)
    return (numpy.asmatrix(train), numpy.asmatrix(test))

#normalize the data by using (x - mean) / std
#@param: numpy matrix of the data
#@return: numpy matrix of the normalized data
def normalization_g(data):
    mean = numpy.mean(data, axis=0)
    std = numpy.std(data, axis=0)
    data = (data - mean) / std
    return data

#normalize the data by using x / mean
#@param: numpy matrix of the data
#@return: numpy matrix of the normalized data
def normalization_m(data):
    mean = numpy.mean(data, axis=0)
    data = data / mean
    return data

#normalize the data by using x / norm(x)
#@param: numpy matrix of the data
#@return: numpy matrix of the normalized data
def normalization_d(data):
    norm_d = numpy.linalg.norm(data, axis=0)
    return data / norm_d

#read the data file and return a numpy matrix
#@param: file_name, the name of the file. The file must be in the same directory as this
#@return: a numpy matrix of the data
def readData(file_name):
    trips = []
    error_count  = 0
    header = True;
    for line in file(os.path.join(dir, file_name)):
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
            #ptime = datetime.strptime(line[5], "%Y-%m-%d %H:%M:%S").weekday()
            #trip time in secs
            ttime = float(line[8])
            #trip distance
            tdistance = float(line[9])
            #absolute displacement
            distance = get_distance(plat,plong,dlat,dlong)
            trip = (ttime, ptime, tdistance, distance, plong, plat, dlong, dlat)
            trips.append(trip)
        except:
            error_count += 1
            print ptime,ttime,tdistance,plong,plat,dlong,dlat
            print error_count
    return numpy.asmatrix(trips), error_count

if __name__ == '__main__':

    #dimensions to consider
    train_col = [1, 2, 3, 4, 5, 6, 7]

    #read the data and return a numpy matrix
    train_data, error_count = readData(small_data)
    test_data, error_count = readData(small_data)
    print "max distance", numpy.matrix.max(train_data[:, 3])
    print "min distance", numpy.matrix.min(train_data[:, 3])
    print "file read completed!"

    #outlier filter, the it provides two ways of filtering,
    #1. filter the outlier by comparing the distance of the outlier
    #   to the mean
    #2. filter the outlier by comparing the distance of the outlier
    #   to the median
    train_data = outlier_filter_simple(train_data, [1, 2, 3], 1)
    test_data = outlier_filter_simple(test_data, [1, 2, 3], 1)
    print "outlier filter completed!"

    #normalize the data. Three option provide,
    #1. normalization_g = (x - mean) / std
    #2. normalization_m = x / mean
    #3. normalization_d = x / norm(x)
    train_data = normalization_g(train_data)
    test_data = normalization_g(test_data)
    print "normalization completed!"

    #split the data into test and train set by every fourth data is test,
    #the others are the train data.
    #(train_data, test_data) = split_data(train_data, 4)

    #linear regression on the test data
    clf = linear_model.LinearRegression()
    clf.fit(train_data[:, train_col], train_data[:, 0])

    #the mean of the ordinary least squares
    ols = numpy.mean(numpy.asarray(clf.predict(test_data[:, train_col])-test_data[:, 0]) ** 2)
    #the mean of the total least squares
    tls = ols / (numpy.sum(clf.coef_ * clf.coef_.T) + 1)

    print ("Coefficients: ", clf.coef_)
    print ("OLS", ols)
    print ("TLS", tls)

    #create the plot panel
    #figure 1, the plot on all the training data
    pyplot.figure(1)
    pyplot.title("Plot using training set")
    pyplot.subplot(3, 1, 1)
    pyplot.plot(train_data[:,1], train_data[:,0], 'ro')
    pyplot.ylabel("trip time")
    pyplot.xlabel("pick-up time")
    pyplot.xlim([-1, 7])
    pyplot.subplot(3, 1, 2)
    pyplot.plot(train_data[:,2], train_data[:,0], 'bo')
    pyplot.ylabel("trip time")
    pyplot.xlabel("trip distance")
    pyplot.subplot(3, 1, 3)
    pyplot.plot(train_data[:,3], train_data[:,0], 'go')
    pyplot.ylabel("trip time")
    pyplot.xlabel("distance between pickup and dropof")
    pyplot.tight_layout()

    #figure 2, the model and the testing data
    pyplot.figure(2)
    pyplot.subplot(3, 1, 1)
    pyplot.plot(test_data[:, 1], test_data[:, 0], 'ro', test_data[:, 1], clf.predict(test_data[:, train_col]), '-')
    pyplot.subplot(3, 1, 2)
    pyplot.plot(test_data[:, 2], test_data[:, 0], 'bo', test_data[:, 2], clf.predict(test_data[:, train_col]), '-')
    pyplot.subplot(3, 1, 3)
    pyplot.plot(test_data[:, 3], test_data[:, 0], 'go', test_data[:, 3], clf.predict(test_data[:, train_col]), '-')
    pyplot.tight_layout()
    pyplot.show()
