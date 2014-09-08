#!/usr/bin/python
#%pylab inline
import sklearn
import skimage
from matplotlib import *
from numpy import*
import matplotlib.pyplot as plt
import csv

#initialize the colors for each species
def initColors(species):
    colors = []
    for s in species:
        if s == 'Iris-setosa':
            colors.append('r')
        elif s == 'Iris-versicolor':
            colors.append('b')
        elif s == 'Iris-virginica':
            colors.append('g')
    return colors

#read the length and width of each sample and push to a N x p dimentional matrix
attributes = genfromtxt("/Users/WayneLI/Desktop/CS5785/HW0/iris.data", usecols=(0,1,2,3) ,delimiter=',')
#read the species and push to a p dimentional vector
species = genfromtxt("/Users/WayneLI/Desktop/CS5785/HW0/iris.data", dtype="|S15", usecols=(4) ,delimiter=',')

#create the plot panel
fig = plt.figure()  
#initialize the color for each species   
colors = initColors(species)  

#plot each attribute against the other
for i in range(0, 4):
    #x axis value
    xs = attributes[:,i]
    for j in range(0, 4):
        if i == j:
            continue
        else:
            #y axis value
            ys = attributes[:,j]
            #plot the graph on the plot panel
            ax = fig.add_subplot(4, 4, i*4+j+1)
            ax.scatter(xs, ys, c=colors)

#set the layout and show    
fig.tight_layout()        
plt.show()

