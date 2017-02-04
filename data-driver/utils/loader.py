import numpy as np
import xgboost
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
from sklearn.metrics import mean_squared_error
from math import sqrt
import pickle

import json

def read_data(input_file):
    data_raw = open(input_file).read()
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
    
    # prepare the Y vectors
    Y_unit_sales = np.array([ row["sum_unit_sales"]  for row in data ])
    Y_volume_sales = np.array([ row["sum_volume_sales"]  for row in data ])
    Y_volume_share = np.array([ row["sum_volume_share_of_category"]  for row in data ])
    
    # return dataset
    return (X, Y_unit_sales, Y_volume_sales, Y_volume_share)
