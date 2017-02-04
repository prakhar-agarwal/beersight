import numpy
import xgboost
from sklearn import model_selection
from sklearn.metrics import accuracy_score

from utils.reader import read_labels, read_data

(X_labels, Y_labels) = read_labels()
(X, Y) = read_data('data/sales_data.csv')

# print(X_labels, Y_labels)
# print(X, Y)
