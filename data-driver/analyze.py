import numpy as np
import xgboost
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn import cross_validation, linear_model
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import Imputer
from math import sqrt

import json

def get_model(name='xgb'):
    """TODO: Docstring for function.

    :arg1: TODO
    :returns: TODO

    """
    if name == 'xgb':
        return xgboost.XGBRegressor(max_depth=10, n_estimators=500)
    elif name == 'linearreg':
        return linear_model.LinearRegression()

data_raw = open('/home/ubuntu/data/sales_data_all_subsegment_rollup.json').read()
data = json.loads(data_raw)

# get all the subsegments possible
subsegments = []
for row in data:
    if( row['ab_subsegment_value'] not in subsegments ):
        subsegments.append(row['ab_subsegment_value'])

removal = ['ab_subsegment_value', 'date', 'sum_unit_sales', 'sum_volume_sales', 'sum_volume_share_of_category']

# get all the feature columns possible
columns = []
for key in data[0].keys():
    if( key not in columns and key not in removal ):
        columns.append(key)

# prepare the X vector
X = np.zeros((len(data), len(columns)), dtype=np.float)
i = 0
for row in data:
    j = 0
    for column in columns:
        X[i][j] = row[column]
        j += 1
    i += 1    

imputer = Imputer()
X = imputer.fit_transform(X)
# prepare the Y vectors
Y_unit_sales = np.array([ row["sum_unit_sales"]  for row in data ])
Y_volume_sales = np.array([ row["sum_volume_sales"]  for row in data ])
Y_volume_share = np.array([ row["sum_volume_share_of_category"]  for row in data ])

seed = 7
test_size = 0.10

# model UNIT SALES information
X_train, X_test, y_train_unit_sales, y_test_unit_sales = cross_validation.train_test_split(X, Y_unit_sales, test_size=test_size, random_state=seed)
model_unit_sales = get_model('xgb')
model_unit_sales.fit(X_train, y_train_unit_sales)

# model VOLUME SALES information
X_train, X_test, y_train_volume_sales, y_test_volume_sales = cross_validation.train_test_split(X, Y_volume_sales, test_size=test_size, random_state=seed)
model_volume_sales = get_model('xgb')
model_volume_sales.fit(X_train, y_train_volume_sales)

# model VOLUME SHARE information
X_train, X_test, y_train_volume_share, y_test_volume_share = cross_validation.train_test_split(X, Y_volume_share, test_size=test_size, random_state=seed)
model_volume_share = get_model('xgb')
model_volume_share.fit(X_train, y_train_volume_share)

# make predictions to evalute model on test data
predictions_unit_sales = model_unit_sales.predict(X_test)
predictions_volume_sales = model_volume_sales.predict(X_test)
predictions_volume_share = model_volume_share.predict(X_test)

rms_unit_sales = sqrt(mean_squared_error(y_test_unit_sales[:20], predictions_unit_sales[:20]))
rms_volume_sales = sqrt(mean_squared_error(y_test_volume_sales[:20], predictions_volume_sales[:20]))
rms_volume_share = sqrt(mean_squared_error(y_test_volume_share[:20], predictions_volume_share[:20]))
print('Unit Sales error', rms_unit_sales/np.mean( y_train_unit_sales ))
print('Volume Sales error', rms_volume_sales/np.mean( y_train_volume_sales ))
print('Volume Shares error', rms_volume_share/np.mean( y_train_volume_share ))

