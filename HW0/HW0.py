#************************************************************
# Copyright @ Siyi Fan and Wen Li
#
# Instruction on running the program:
# 1. Change the data path to where you locate your iris.data
# 2. Remove and blank line at the end of iris.data
# 3. Please run the program in Enthought python environment
#    with matplolib and numpy library installed
#
# Note: no input validation and error checking implemented,
#       please carefully follow the instruction
#
#************************************************************
#!/usr/bin/python
#%pylab inline
import matplotlib.pyplot as pyplot
from numpy import *

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

#change the path to where you put your data file
data = "/Users/WayneLI/Desktop/CS5785/HW0/iris.data"

#read the length and width of each sample and push to a N x p dimentional matrix
attributes = genfromtxt(data, usecols=(0,1,2,3) ,delimiter=',')
#read the species and push to a p dimentional vector
species = genfromtxt(data, dtype="|S15", usecols=(4) ,delimiter=',')

#create the plot panel
fig = pyplot.figure()
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
pyplot.show()

