import numpy as np
import xgboost
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn import cross_validation

import json
import pickle

from dateutil import parser
import datetime

data_raw = open('/home/ubuntu/data/sales_data_subsegment_all.json').read()
data = json.loads(data_raw)

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
