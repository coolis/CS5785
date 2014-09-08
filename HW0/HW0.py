#!/usr/bin/python
#%pylab inline
import sklearn
import skimage
from matplotlib import *
from numpy import*
import csv

attributes = genfromtxt("/Users/WayneLI/Desktop/CS5785/HW0/iris.data", dtype=[('sepalL','f8'),('sepalW','f8'),
('petalL','f8'), ('petalW','f8'), ('class','S15')], delimiter=',')

xs = numpy.array([1, 2, 3, 4, 5, 6, 7]) 
ys = numpy.array([3, 2, 5, 1, 3, 3, 2]) 
colors = ["r","r","r","b","b","g","g"] 
pyplot(xs, ys, c=colors)

