import numpy,math,datetime,logging
import matplotlib.pyplot as pyplot
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from distance import get_distance

# logging.basicConfig(filename='logs/utils.log',level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def metrics(model,x,y):
    """
    compute ols and rmse
    :param y:
    :param yhat:
    :return ols and rmse:
    """
    yhat = model.predict(x)
    ols = sum(numpy.square((y-yhat)))
    rmse = (ols/len(y))**0.5
    corr = numpy.corrcoef(y,yhat)
    return ols,rmse,corr

def evaluate(model_list,x,y):
    for description,model in model_list:
        print "\t",description,"OLS, RMSE and Correlation coefficient",metrics(model,x,y),"Model",model.coef_,model.intercept_


def split(target, features, row, x, y, x_test=None, y_test=None, i= None, nth = None):
    """
    :param target: index of expected
    :param features: list of indexes
    :param row:
    :param x:
    :param y:
    :param x_test:
    :param y_test:
    :param i:
    :param nth:
    """

    if nth and i % nth == 0:
        x_test.append([row[feature] for feature in features])
        y_test.append(row[target])
    else:
        x.append([row[feature] for feature in features])
        y.append(row[target])


def tls(model,x,y):
    pass


def linear_regression(x,y):
    """
    :param x:
    :param y:
    :return linear regression model object:
    """
    model = linear_model.LinearRegression()
    model.fit(x, y)
    return model


def itransformer(row):
    """
    identity transformer returns same
    :param row:
    :return True:
    """
    return row

def ifilter(row):
    """
    identity filter always returns True
    :param row:
    :return True:
    """
    
    return True


def load_csv_lazy(fname,str_fields,float_fields,exclude_first=True,row_filter=ifilter,row_tranformer=itransformer):
    """
    np.genfromtxt is a good alternative, not sure if it can act as a generator. pandas frames are also a good alternative.
    :param fname:
    :param exclude_first:
    :return:
    """
    error_count = 0
    excluded_count = 0
    for count,line in enumerate(file(fname)):
        if not exclude_first:
            try:
                if count and count % 10**6 == 0:
                    logging.debug("Loaded "+str(count))
                    logging.debug("error_count : "+str(error_count))
                    logging.debug("excluded_count : "+str(excluded_count))
                entries = line.strip().split(',')
                row = [entries[f] for f in str_fields] + [float(entries[f]) for f in float_fields]
                if row_filter(row):
                    row = row_tranformer(row)
                    yield row
                else:
                    excluded_count += 1
            except:
                error_count += 1
        else:
            exclude_first = False
    logging.debug("count : "+str(count))
    logging.debug("error_count : "+str(error_count))
    logging.debug("excluded_count : "+str(excluded_count))
    
#outlier filter. It counts the distance of the data to the mean or median,
#and compare it with the standard deviation
#@param: data, the numpy matrix
#        index, a list of index where you want to apply the filter
#        quantile: the criteria of the filter
#@return: a numpy matrix of the filtered data
def outlier_filter(data, index, quantile):
    #filt outlier by remove all the points larger than the quantile
    list_index = []
    #mean of the data by column
    mean = numpy.mean(data, axis=0)
    #standard deviation of the data by column
    std = numpy.std(data, axis=0)

    for i,d in enumerate(data):
        #if the distance to the mean is bigger than quantile times the standard deviation, the outlier marked
        for j in index:
            if math.fabs(d[0, j] - mean[0, j]) > quantile * std[0, j]:
                list_index.append(i)
                break
    return numpy.delete(data, list_index, 0)
    
def scores(model, x, y):
    yhat = model.predict(x)
    ols = sum(numpy.square((y-yhat)))
    rmse = numpy.sqrt(mean_squared_error(y, yhat))
    mae = mean_absolute_error(y, yhat)
    corr = numpy.corrcoef(y.T, yhat.T)
    print "=========================Evaluation==========================="
    print "Training Data: Train_Data.csv    Test Data: Top 10000 lines of Trip_Data_1.csv" 
    print "Root Mean Square Error: "
    print rmse
    print "Mean Absolute Error: "
    print mae
    print "Correlation Coefficient: "
    print corr
    return ols,rmse,mae,corr
    
