import numpy as np
import xgboost
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
import pickle
import json

from dateutil import parser
import datetime

from utils.loader import read_data

# load dataset
(subsegments, time_labels, columns, X, Y_unit_sales, Y_volume_sales, Y_volume_share) = read_data('/home/ubuntu/data/sales_data_all_subsegment_rollup.json')

# load the model
models = pickle.load(open('models.dat', 'rb'))

print(models)
print(time_labels)
print(columns)
print(X.shape)
print(subsegments)

data_series = {}

for (timestamp, x) in zip(time_labels, X):
    
    timestamp = parser.parse(row['date']).strftime('%s')
    if timestamp not in time_labels:
        time_labels.append(timestamp)
    if row['subsegment'] not in data_series:
        data_series[row['subsegment']] = { 'subsegment': row['subsegment'] }
        for c in columns:
            data_series[row['subsegment']][c] = []
    for c in row.keys():
        data_series[row['subsegment']][c].append(row[c])


# make predictions for test data
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]
print( y_test[0:10] )
print( predictions[0:10] )

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
