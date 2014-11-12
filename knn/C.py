# -*- coding: utf-8 -*-
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

def C():
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

    neigh = KNeighborsRegressor(n_neighbors=1)
    neigh.fit(train_data[:,[1,2,3,4,5,6]], train_data[:,0])

    ols,rmse,mae,corr = scores(neigh, test_data[:,[1,2,3,4,5,6]], test_data[:,0])

if __name__ == '__main__':
    C()
