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
(subsegments, time_labels, columns, X_full, Y_unit_sales_full, Y_volume_sales_full, Y_volume_share_full) = read_data('/home/ubuntu/data/sales_data_all_subsegment_rollup.json')

# load the model
models = pickle.load(open('models.dat', 'rb'))

data_raw = open('/home/ubuntu/data/sales_data_all_subsegment_rollup.json').read()
# data_raw = open('/home/ubuntu/data/sales_data_subsegment_all.json').read()
data = json.loads(data_raw)

time_labels = []
data_series = {}

columns = list(data[0].keys())

for row in data:
    timestamp = parser.parse(row['date']).strftime('%s')
    if timestamp not in time_labels:
        time_labels.append(timestamp)
    if row['ab_subsegment_value'] not in data_series:
        data_series[row['ab_subsegment_value']] = { 'subsegment': row['ab_subsegment_value'] }
        for c in columns:
            if c == 'ab_subsegment_value' :
                data_series[row['ab_subsegment_value']]['subsegment_value'] = []
                continue
            data_series[row['ab_subsegment_value']][c] = []
    for c in row.keys():
        if c == 'ab_subsegment_value' :
            data_series[row['ab_subsegment_value']]['subsegment_value'].append(row[c])
            continue
        data_series[row['ab_subsegment_value']][c].append(row[c])

# make predictions for the last 8 weeks for back-tested data
backtest = -16
for (subsegment, s) in zip(subsegments, range(0, len(subsegments))):
     model_unit_sales = models[subsegment]['unit_sales']
     model_volume_sales = models[subsegment]['volume_sales']
     model_volume_share = models[subsegment]['volume_share']
     X_test = X_full[s][-16:]
     y_unit_sales_test = Y_unit_sales_full[s][-16:]
     y_volume_sales_test = Y_volume_sales_full[s][-16:]
     y_volume_share_test = Y_volume_share_full[s][-16:]
     predictions_unit_sales = model_unit_sales.predict(X_test)
     predictions_volume_sales = model_volume_sales.predict(X_test)
     predictions_volume_share = model_volume_share.predict(X_test)
     data_series[subsegment]['predicted_unit_sales'] = predictions_unit_sales.tolist()
     data_series[subsegment]['predicted_volume_sales'] = predictions_volume_sales.tolist()
     data_series[subsegment]['predicted_volume_share_of_category'] = predictions_volume_share.tolist()


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

# @app.route('/predict', methods = ['POST'])
# def predict_data():
#     body = request.get_json(force=True, silent=True)
#     subsegment = body['subsegment']
#     return jsonify({ 'error' : 'Invalid json.' })


if __name__ == '__main__':
   app.run( 
        host="0.0.0.0",
        port=8081
  )
