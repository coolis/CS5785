#!/usr/bin/python
#%pylab inline
import sklearn
import skimage
from matplotlib import *
from numpy import*
import matplotlib.pyplot as plt
import csv

attributes = genfromtxt("/Users/WayneLI/Desktop/CS5785/HW0/iris.data", usecols=(0,1,2,3) ,delimiter=',')

xs = numpy.array([1, 2, 3, 4, 5, 6, 7]) 
ys = numpy.array([3, 2, 5, 1, 3, 3, 2]) 
colors = ["r","b","g"] 
plt.scatter(xs, ys, c=colors)
plt.show()



