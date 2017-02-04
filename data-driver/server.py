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
metadata = {}

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
     maxs = np.nanmax(X_full[s], axis=0)
     mins = np.nanmin(X_full[s], axis=0)
     means = np.nanmean(X_full[s], axis=0)
     stds = np.nanstd(X_full[s], axis=0)
     metadata[s] = {}
     metadata[s]['knobs'] = {
         'sum_feature_count': {
             'lower_limit': mins[15],
             'upper_limit': maxs[15],
             'mean': means[15],
             'std': stds[15]
         },
         'sum_display_count': {
             'lower_limit': mins[10],
             'upper_limit': maxs[10],
             'mean': means[10],
             'std': stds[10]
         },
         'price_per_unit': {
             'lower_limit': mins[0],
             'upper_limit': maxs[0],
             'mean': means[0],
             'std': stds[0]
         }
     }
     data_series[subsegment]['knobs'] = metadata[s]['knobs']



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

@app.route('/predict', methods = ['GET', 'POST'])
def predict_data():
    look_forward = 12
    body = request.get_json(force=True, silent=True)
    subsegment = body['subsegment']
    model_unit_sales = models[subsegment]['unit_sales']
    model_volume_sales = models[subsegment]['volume_sales']
    model_volume_share = models[subsegment]['volume_share']
    s = subsegments.index(subsegment)
    X_test = X_full[s][-4*look_forward::4]
    for record in X_test:
        if( 'sum_feature_count' in body ):
            record[15] = body['sum_feature_count']
        if( 'sum_display_count' in body ):
            record[10] = body['sum_display_count']
        if( 'price_per_unit' in body ):
            record[0] = body['price_per_unit']
    # show the previous value again for visual continuity
    X_test[0] = X_full[s][-1]
    predictions_unit_sales = model_unit_sales.predict(X_test)
    predictions_volume_sales = model_volume_sales.predict(X_test)
    predictions_volume_share = model_volume_share.predict(X_test)
    predictions_unit_sales = model_unit_sales.predict(X_test)
    predictions_volume_sales = model_volume_sales.predict(X_test)
    predictions_volume_share = model_volume_share.predict(X_test)
    response = {}
    response['forecasted_unit_sales'] = predictions_unit_sales.tolist()
    response['forecasted_volume_sales'] = predictions_volume_sales.tolist()
    response['forecasted_volume_share_of_category'] = predictions_volume_share.tolist()
    return jsonify({ 'data': response } )


if __name__ == '__main__':
   app.run( 
        host="0.0.0.0",
        port=8081
  )
