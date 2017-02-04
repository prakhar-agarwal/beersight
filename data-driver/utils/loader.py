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
    input_file = '/home/ubuntu/data/sales_data_all_subsegment_rollup.json'
    data_raw = open(input_file).read()
    data = json.loads(data_raw)
        
    # get all the subsegments possible
    subsegments = []
    dates = []
    for row in data:
        if( row['ab_subsegment_value'] not in subsegments ):
            subsegments.append(row['ab_subsegment_value'])
        if( row['date'] not in dates ):
            dates.append(row['date'])
        
    subsegments_idx = {}
    for (subsegment, idx) in zip(subsegments, range(0,len(subsegments))):
        subsegments_idx[subsegment] = idx
     
    removal = ['date']
    targets = ['sum_unit_sales', 'sum_volume_sales', 'sum_volume_share_of_category']
        
    # get all the feature columns possible
    columns = []
    for key in data[0].keys():
        if( key not in columns and key not in removal ):
            columns.append(key)
    
    # prepare the X and Y vectors
    X = np.zeros((len(subsegments), len(dates), len(columns)), dtype=np.float)
    Y_unit_sales = np.zeros((len(subsegments), len(dates)), dtype=np.float)
    Y_volume_sales = np.zeros((len(subsegments), len(dates)), dtype=np.float)
    Y_volume_share = np.zeros((len(subsegments), len(dates)), dtype=np.float)
    for (subsegment, s) in zip(subsegments, range(0, len(subsegments))):
        i = 0
        for row in data:
            if( row['ab_subsegment_value'] == subsegment ):
                for (column, j) in zip(columns, range(0, len(columns))):
                    if( column == 'ab_subsegment_value' ):
                      continue
                    if( column == 'sum_unit_sales' ):
                      Y_unit_sales[s][i] = row['sum_unit_sales']
                      continue
                    if( column == 'sum_volume_sales' ):
                      Y_volume_sales[s][i] = row['sum_volume_sales']
                      continue
                    if( column == 'sum_volume_share_of_category' ):
                      Y_volume_share[s][i] = row['sum_volume_share_of_category']
                      continue
                    X[s][i][j] = row[column]
                i += 1
        
    return (subsegments, dates, columns, X, Y_unit_sales, Y_volume_sales, Y_volume_share)
    
