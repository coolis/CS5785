#!/usr/bin/python
#%pylab inline
import sklearn
import skimage
from matplotlib import *
from numpy import*
import matplotlib.pyplot as plt
import csv

attributes = genfromtxt("/Users/WayneLI/Desktop/CS5785/HW0/iris.data", usecols=(0,1,2,3) ,delimiter=',')
species = genfromtxt("/Users/WayneLI/Desktop/CS5785/HW0/iris.data", dtype="|S15", usecols=(4) ,delimiter=',')

fig = plt.figure()
colorR = ["r"]*50
colorB = ["b"]*50
colorG = ["g"]*50
colors = numpy.concatenate((colorR, colorB, colorG))

for i in range(0, 4):
    xs = attributes[:,i]
    for j in range(0, 4):
        if i == j:
            continue
        else:
            ys = attributes[:,j]
            ax = fig.add_subplot(4, 4, i*4+j+1)
            ax.scatter(xs, ys, c=colors)
            
plt.show()




