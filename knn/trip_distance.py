__author__ = 'wenli'

import numpy as np
from sklearn.neighbors import KNeighborsRegressor

from code.utils import *
from config import TRAIN_DATA,EXAMPLE_DATA,TRIP_DATA_1,F_FIELDS,S_FIELDS

DATA_FILEDS = [8, 10, 11, 12, 13]
    
if __name__ == '__main__':
    rows = [row for row in load_csv_lazy(TRAIN_DATA,[],DATA_FILEDS)]
    train_data = np.asmatrix(rows)
    train_data = outlier_filter(train_data, [1,2,3,4], 1)
    rows = [row for row in load_csv_lazy(TRIP_DATA_1,[],DATA_FILEDS)]
    test_data = np.asmatrix(rows[:10000])
    
    neigh = KNeighborsRegressor(n_neighbors=1)
    neigh.fit(train_data[:, [1,2,3,4]], train_data[:,0])
    
    ols,rmse,mae,corr = scores(neigh, test_data[:, [1,2,3,4]], test_data[:,0])