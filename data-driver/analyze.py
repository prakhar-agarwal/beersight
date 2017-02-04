import numpy as np
import xgboost
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
import pickle

import json

from utils.loader import read_data

# load dataset
(X, Y_unit_sales, Y_volume_sales, Y_volume_share) = read_data('/home/ubuntu/data/sales_data_all_subsegment_rollup.json')

# prepare training/test split
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
model_unit_sales = xgboost.XGBRegressor(max_depth=10, n_estimators=500)
model_unit_sales.fit(X_train, y_train_unit_sales)

# model VOLUME SALES information
model_volume_sales = xgboost.XGBRegressor(max_depth=10, n_estimators=500)
model_volume_sales.fit(X_train, y_train_volume_sales)

# model VOLUME SHARE information
model_volume_share = xgboost.XGBRegressor(max_depth=10, n_estimators=500)
model_volume_share.fit(X_train, y_train_volume_share)

# make predictions to evalute model on test data
predictions_unit_sales = model_unit_sales.predict(X_test)
predictions_volume_sales = model_volume_sales.predict(X_test)
predictions_volume_share = model_volume_share.predict(X_test)

# calculate RMS / r2 errors
rms_unit_sales = sqrt(mean_squared_error(y_test_unit_sales[:20], predictions_unit_sales[:20]))
rms_volume_sales = sqrt(mean_squared_error(y_test_volume_sales[:20], predictions_volume_sales[:20]))
rms_volume_share = sqrt(mean_squared_error(y_test_volume_share[:20], predictions_volume_share[:20]))
print('Unit Sales  r_squared', r2_score(y_test_unit_sales, predictions_unit_sales))
print('Volume Sales  r_squared', r2_score(y_test_volume_sales, predictions_volume_sales))
print('Volume Shares  r_squared', r2_score(y_test_volume_share, predictions_volume_share))

models = {
    'unit_sales': model_unit_sales,
    'unit_sales': model_volume_sales,
    'unit_sales': model_volume_share
}

print('Saving models')
pickle.dump(models, open('models.dat', 'wb'))

