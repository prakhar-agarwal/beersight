import numpy as np
import xgboost
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
import pickle
import json

from dateutil import parser
import datetime

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

# prepare the Y vectors
Y_unit_sales = np.array([ row["sum_unit_sales"]  for row in data ])
Y_volume_sales = np.array([ row["sum_volume_sales"]  for row in data ])
Y_volume_share = np.array([ row["sum_volume_share_of_category"]  for row in data ])

time_labels = []

data_series = {}

columns = list(data[0].keys())

for row in data:
    timestamp = parser.parse(row['date']).strftime('%s')
    if timestamp not in time_labels:
        time_labels.append(timestamp)
    if row['subsegment'] not in data_series:
        data_series[row['subsegment']] = { 'subsegment': row['subsegment'] }
        for c in columns:
            data_series[row['subsegment']][c] = []
    for c in row.keys():
        data_series[row['subsegment']][c].append(row[c])

# # Input-Output Data Formats
# X = np.array([ [ 
#     row["sum_display_count"],
#     row["sum_display_share"],
#     row["sum_distribution"],
#     row["sum_feature_count"],
#     row["sum_feature_share"],
#     row["avg_price_per_unit"],
#     row["average_of_max_temperaturec"],
# ] for row in data ])
# Y = np.array([ row["sum_unit_sales"]  for row in data ])
# 
# # Load the model
# model = pickle.load('model.data', 'rb')
# 
# # make predictions for test data
# y_pred = model.predict(X_test)
# predictions = [round(value) for value in y_pred]
# print( y_test[0:10] )
# # print( predictions[0:10] )

# ---------------------------------------------------
# Flask app to serve the data, model and predictions
# ---------------------------------------------------

from flask import Flask, render_template, request, url_for, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return jsonify({ "response": "Hello World" })


@app.route('/data')
def get_data():
    return jsonify({'time_labels': time_labels, 'data': data_series})


if __name__ == '__main__':
  app.run( 
        host="0.0.0.0",
        port=8080
  )
