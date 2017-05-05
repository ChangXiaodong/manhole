# coding=utf-8
import data_reader
import get_parameters
import platform
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
import numpy as np
import pandas

if "Windows" in platform.platform():
    data_path = "E:/Manhole/training data/sql/manhole_database_data.csv"
else:
    data_path = "/Users/xiaoxiami/Manhole/training data/original data/3-6/3/side"

data_dic = pandas.read_csv(data_path)
width = np.array(data_dic["width"])
peak = np.array(data_dic["peakvalue"].apply(lambda x: x >> 9))

train_data = []
for i in range(len(width)):
    train_data.append([width[i], peak[i]])
train_data = np.array(train_data)

k_means_fit = KMeans(n_clusters=3, random_state=150).fit(train_data)
y_pred = k_means_fit.predict(train_data)


fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(len(train_data)):
    if y_pred[i] == 0:
        color = 'r'
        label = u"小型车"
    elif y_pred[i] == 1:
        color = 'g'
        label = u"中型车"
    else:
        color = 'b'
        label = u"大型车"
    ax.plot(train_data[i][0], train_data[i][1], "o", picker=5, c=color)

for x, y in k_means_fit.cluster_centers_:
    ax.plot(x, y, "y*", markersize=24)
ax.set_ylim(0, 130)

plt.show()
