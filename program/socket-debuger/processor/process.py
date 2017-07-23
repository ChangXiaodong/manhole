# coding=utf-8
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import urllib
import datetime


def res_plot(args):
    data = args[0]
    pred = args[1]
    center = args[2]
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in range(len(data)):
        if pred[i] == 0:
            color = 'g'
        elif pred[i] == 1:
            color = 'b'
        else:
            color = 'r'
        ax.plot(data[i][0], data[i][1], "o", picker=5, c=color)

    for x, y in center:
        ax.plot(x, y, "y*", markersize=24)
    ax.set_ylim(0, 130)

    plt.show()


def post_level(sensor_id, level):
    res = urllib.request.urlopen(
        "http://121.42.213.241/database/post_level?sensor_id={}&level={:.2f}".format(sensor_id, level))
    print(res.status, res.reason)


data_path = "./data/2017-07-22.csv"

sensor_dataframe = pd.read_csv(data_path)
sensor_list = set(sensor_dataframe["sensorid"])
time = sensor_dataframe[["update_time", "sensorid"]]
res = {}
plot_data = {}
res_dataframe = pd.DataFrame()
for sensor_id in sensor_list:
    data = sensor_dataframe[sensor_dataframe.sensorid == sensor_id]
    width = np.array(data["width"])
    peak = np.array(data["peakvalue"].apply(lambda x: x >> 9))

    train_data = []
    for i in range(len(width)):
        train_data.append([width[i], peak[i]])
    train_data = np.array(train_data)

    k_means_fit = KMeans(n_clusters=3, random_state=150).fit(train_data)
    y_pred = k_means_fit.predict(train_data)
    centers = sorted(k_means_fit.cluster_centers_, key=lambda x: x[0])

    # plot_data[sensor_id] = [train_data[:], y_pred, sorted(k_means_fit.cluster_centers_, key=lambda x:x[0])]

    x_index = [k_means_fit.cluster_centers_[0][0], k_means_fit.cluster_centers_[1][0],
               k_means_fit.cluster_centers_[2][0]]
    sorted_pred = []
    sensor_dataframe[sensor_dataframe.sensorid == sensor_id].loc[:"pred"] = y_pred
    # data["pred"] = y_pred
    print(set(data["update_time"]))
    for v in y_pred:
        if x_index[v] == max(x_index):
            sorted_pred.append(2)
        elif x_index[v] == min(x_index):
            sorted_pred.append(0)
        else:
            sorted_pred.append(1)
    y_pred = sorted_pred
    res[sensor_id] = [centers[0][1], y_pred]
    plot_data[sensor_id] = [train_data[:], y_pred, k_means_fit.cluster_centers_]
print("识别结果：")
for id, r in res.items():
    level = r[0]
    pred = r[1]
    light_vehicle_cnt = pred.count(0)
    middle_vehicle_cnt = pred.count(1)
    heavy_vehicle_cnt = pred.count(2)
    print(middle_vehicle_cnt, heavy_vehicle_cnt)
    print("{}号节点,沉降程度为{:.2f}%, 小型车数量为:{},中型车数量为:{},大型车数量为:{}".format(
        id, level, light_vehicle_cnt, middle_vehicle_cnt, heavy_vehicle_cnt))
    # post_level(id, r)

# res_plot(plot_data[10])
