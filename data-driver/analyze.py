import numpy as np
import xgboost
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn import cross_validation, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
import pickle

import json

from utils.loader import read_data

def get_model(name='xgb'):
    """TODO: Docstring for function.

    :arg1: TODO
    :returns: TODO

    """
    if name == 'xgb':
        return xgboost.XGBRegressor(max_depth=10, n_estimators=500)
    elif name == 'linearreg':
        return linear_model.LinearRegression()

# load dataset
(subsegments, dates, columns, X_full, Y_unit_sales_full, Y_volume_sales_full, Y_volume_share_full) = read_data('/home/ubuntu/data/sales_data_all_subsegment_rollup.json')

# prepare training/test split
models = {}
for (subsegment, s) in zip(subsegments, list(range(0, len(subsegments)))):
    print('---')
    print('Training for subsegment', subsegment)
    X = X_full[s]
    Y_unit_sales = Y_unit_sales_full[s]
    Y_volume_sales = Y_volume_sales_full[s]
    Y_volume_share = Y_volume_share_full[s]
    seed = 7
    test_size = 0.1
    split_point = round(len(X)*(1-test_size))
    X_train = X[:split_point]
    X_test = X[split_point:]
    y_train_unit_sales = Y_unit_sales[:split_point]
    y_test_unit_sales = Y_unit_sales[split_point:]
    y_train_volume_sales = Y_volume_sales[:split_point]
    y_test_volume_sales = Y_volume_sales[split_point:]
    y_train_volume_share = Y_volume_share[:split_point]
    y_test_volume_share = Y_volume_share[split_point:]
    
    # model UNIT SALES information
    model_unit_sales = get_model('xgb')
    model_unit_sales.fit(X_train, y_train_unit_sales)
    
    # model VOLUME SALES information
    model_volume_sales = get_model('xgb')
    model_volume_sales.fit(X_train, y_train_volume_sales)
    
    # model VOLUME SHARE information
    model_volume_share = get_model('xgb')
    model_volume_share.fit(X_train, y_train_volume_share)
    
    # make predictions to evalute model on test data
    predictions_unit_sales = model_unit_sales.predict(X_test)
    predictions_volume_sales = model_volume_sales.predict(X_test)
    predictions_volume_share = model_volume_share.predict(X_test)
    
    # calculate RMS / r2 errors
    rms_unit_sales = sqrt(mean_squared_error(y_test_unit_sales[:10], predictions_unit_sales[:10]))/np.mean(y_test_unit_sales)
    rms_volume_sales = sqrt(mean_squared_error(y_test_volume_sales[:10], predictions_volume_sales[:10]))/np.mean(y_test_volume_sales)
    rms_volume_share = sqrt(mean_squared_error(y_test_volume_share[:10], predictions_volume_share[:10]))/np.mean(y_test_volume_share)
    print('Unit Sales  rms', rms_unit_sales)
    print('Volume Sales  rms', rms_volume_sales)
    print('Volume Shares rms', rms_volume_share)
    
    model = {
        'unit_sales': model_unit_sales,
        'volume_sales': model_volume_sales,
        'volume_share': model_volume_share
    }

    models[subsegment] = model

pickle.dump(models, open('models.dat', 'wb'))
    
if len(sys.argv) > 2:
    if sys.argv[2] == 'save':
        print('Saving models')
        pickle.dump(models, open('models.dat', 'wb'))
