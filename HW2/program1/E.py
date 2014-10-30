__author__ = 'aub3'

import numpy as np
import dateutil.parser
from datetime import datetime
from sklearn.neighbors import KNeighborsRegressor

from code.utils import *
from code.distance import *
from config import TRAIN_DATA,EXAMPLE_DATA,TRIP_DATA_1,F_FIELDS,S_FIELDS

#pick up lon, pick up lat, drop off lon, drop off lat
FLOAT_FILEDS = [8, 10, 11, 12, 13]
#pick up time
STRING_FILEDS = [5]

def E():
    rows = [row for row in load_csv_lazy(TRAIN_DATA,STRING_FILEDS,FLOAT_FILEDS)]   
    train_data = []
    for row in rows:
        pdate = dateutil.parser.parse(row[0])
        ptime = pdate.hour*3600 + pdate.minute*60 + pdate.second
        tdistance = get_distance(row[3], row[2], row[5], row[4])
        plat = row[3]
        plon = row[2]
        dlat = row[5]
        dlon = row[4]
        ttime = row[1]
        train_data.append([ttime, ptime, tdistance, plat, plon, dlat, dlon])  
    train_data = np.asmatrix(train_data)
    train_data = outlier_filter(train_data, [1,2,3,4,5,6], 2)
    mean = numpy.mean(train_data[:,[1,2,3,4,5,6]], axis=0)
    std = numpy.std(train_data[:,[1,2,3,4,5,6]], axis=0)
    train_data[:,[1,2,3,4,5,6]] = (train_data[:,[1,2,3,4,5,6]] - mean) / std
    rows = [row for row in load_csv_lazy(TRIP_DATA_1,STRING_FILEDS,FLOAT_FILEDS)] 
    test_data = []
    for row in rows[:10000]:
        pdate = dateutil.parser.parse(row[0])
        ptime = pdate.hour*3600 + pdate.minute*60 + pdate.second
        tdistance = get_distance(row[3], row[2], row[5], row[4])
        plat = row[3]
        plon = row[2]
        dlat = row[5]
        dlon = row[4]
        ttime = row[1]
        test_data.append([ttime, ptime, tdistance, plat, plon, dlat, dlon])  
    test_data = np.asmatrix(test_data)
    test_data[:,[1,2,3,4,5,6]] = (test_data[:,[1,2,3,4,5,6]] - mean) / std
    
    optimal_k = 0
    optimal = 0
    for k in range(5, 21):
        neigh = KNeighborsRegressor(n_neighbors=k)
        neigh.fit(train_data[:,[1,2,3,4,5,6]], train_data[:,0])
        dist, ind = neigh.kneighbors(test_data[:, [1,2,3,4,5,6]])
        result = []
        for row in range(ind.shape[0]):
            e = []
            for i in range(ind.shape[1]):
                e.append(train_data[ind[row,i], 0])
            result.append(e)
        result = np.asmatrix(result)
        median = np.median(result, axis=1)
        mae = mean_absolute_error(median, test_data[:,0])
        print mae
        if mae > optimal:
            optimal_k = k
    print optimal_k

if __name__ == '__main__':
    E()