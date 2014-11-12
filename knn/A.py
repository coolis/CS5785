__author__ = 'aub3'

import matplotlib
import pylab
import numpy as np

from code.utils import *
from config import TRAIN_DATA,EXAMPLE_DATA,F_FIELDS,S_FIELDS,DIR

# fileds
#passenger count, pick up lat, pick up lon, dropp off lat, drop off lon
DATA_FILEDS = [7, 12, 13]
BUCKETS = 1000

rows = [row for row in load_csv_lazy(TRAIN_DATA,[],DATA_FILEDS)] 
    
train_data = []
for i in range(len(rows)):
    if (-75 <= rows[i][1] <= -70 and 40 <= rows[i][2] <= 45):
        train_data.append(rows[i])

train_data = np.asmatrix(train_data)
train_data = outlier_filter(train_data, [1, 2], 3)
data_max = np.amax(train_data, axis=0)
data_min = np.amin(train_data, axis=0)

lon_bucket = (data_max[0 ,1] - data_min[0 ,1])/BUCKETS
lat_bucket = (data_max[0 ,2] - data_min[0 ,2])/BUCKETS
        
passengers_one = np.zeros((BUCKETS, BUCKETS))
passengers_three = np.zeros((BUCKETS, BUCKETS))
total = np.zeros((BUCKETS, BUCKETS))

for i in range(train_data.shape[0]):
    lon = int(round((train_data[i, 1]-data_min[0 ,1])/lon_bucket))-1
    lat = int(round((train_data[i, 2]-data_min[0 ,2])/lat_bucket))-1
    if (train_data[i, 0] == 1):
        passengers_one[lon][lat] += 1
    if (train_data[i, 0] == 3):
        passengers_three[lon][lat] += 1
    total[lon][lat] += 1
    
for i in range(BUCKETS):
    for j in range(BUCKETS):
        if (total[i][j] != 0):
            passengers_one[i][j] /= total[i][j]
            passengers_three[i][j] /= total[i][j]
            

pylab.figure()
pylab.imshow(passengers_one, origin='lower', aspect='auto', interpolation='nearest', norm=matplotlib.colors.Normalize())
pylab.title('Density Estimation of Passenger Count = 1 in 1000 x 1000 parts')
pylab.xlabel('Latitude')
pylab.ylabel('Longtitude')
pylab.savefig(DIR+'/figures/density_1_figure.png')

pylab.figure()
pylab.imshow(passengers_three, origin='lower', aspect='auto', interpolation='nearest', norm=matplotlib.colors.Normalize())
pylab.title('Density Estimation of Passenger Count = 3 in 1000 x 1000 parts')
pylab.xlabel('Latitude')
pylab.ylabel('Longtitude')
pylab.savefig(DIR+'/figures/density_3_figure.png')

