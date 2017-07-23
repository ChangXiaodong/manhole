# coding=utf-8
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import urllib
import datetime
import pymysql

db = pymysql.connect("121.42.213.241", "root", "123", "parkinfo")
select_latest = "SELECT * FROM manhole_database_data WHERE TO_DAYS(NOW()) - TO_DAYS(update_time) < 2"
select_all = "SELECT * FROM manhole_database_data"
latest_dataframe = pd.read_sql(select_latest, db)
all_dataframe = pd.read_sql(select_all, db)
all_dataframe.to_csv('data/{}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d')))


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


def post_level(sensor_id, level, light_vehicle_cnt, middle_vehicle_cnt, heavy_vehicle_cnt, total_vehicle_cnt):
    res = urllib.request.urlopen(
        "http://121.42.213.241/database/post_level?"
        "sensor_id={}&level={:.2f}&"
        "light_vehicle_cnt={}&"
        "middle_vehicle_cnt={}&"
        "heavy_vehicle_cnt={}&"
        "total_vehicle_cnt={}".format(sensor_id, level,
                                      light_vehicle_cnt, middle_vehicle_cnt,
                                      heavy_vehicle_cnt, total_vehicle_cnt))
    print(res.status, res.reason)


sensor_list = set(latest_dataframe["sensorid"])
res = {}
plot_data = {}
res_dataframe = pd.DataFrame()
for sensor_id in sensor_list:
    data = all_dataframe[all_dataframe.sensorid == sensor_id]
    width = np.array(data["width"])
    peak = np.array(data["peakvalue"].apply(lambda x: x >> 9))
    train_data = []
    for i in range(len(width)):
        train_data.append([width[i], peak[i]])
    train_data = np.array(train_data)

    k_means_fit = KMeans(n_clusters=3, random_state=150).fit(train_data)
    y_pred = k_means_fit.predict(train_data)
    centers = sorted(k_means_fit.cluster_centers_, key=lambda x: x[0])

    x_index = [k_means_fit.cluster_centers_[0][0], k_means_fit.cluster_centers_[1][0],
               k_means_fit.cluster_centers_[2][0]]
    sorted_pred = []
    for v in y_pred:
        if x_index[v] == max(x_index):
            sorted_pred.append(2)
        elif x_index[v] == min(x_index):
            sorted_pred.append(0)
        else:
            sorted_pred.append(1)
    y_pred = sorted_pred

    plot_data[sensor_id] = [train_data[:], y_pred, k_means_fit.cluster_centers_]

    vehicle_cnt_data = latest_dataframe[latest_dataframe.sensorid == sensor_id]
    width = np.array(vehicle_cnt_data["width"])
    peak = np.array(vehicle_cnt_data["peakvalue"].apply(lambda x: x >> 9))
    vehicle_cnt_train_data = []
    for i in range(len(width)):
        vehicle_cnt_train_data.append([width[i], peak[i]])
    vehicle_cnt_train_data = np.array(vehicle_cnt_train_data)

    vehicle_cnt_fit = KMeans(n_clusters=3, random_state=150).fit(vehicle_cnt_train_data)
    vehicle_cnt_y_pred = vehicle_cnt_fit.predict(vehicle_cnt_train_data)
    vehicle_cnt_x_index = [vehicle_cnt_fit.cluster_centers_[0][0], vehicle_cnt_fit.cluster_centers_[1][0],
                           vehicle_cnt_fit.cluster_centers_[2][0]]
    vehicle_cnt_sorted_pred = []
    for v in vehicle_cnt_y_pred:
        if vehicle_cnt_x_index[v] == max(vehicle_cnt_x_index):
            vehicle_cnt_sorted_pred.append(2)
        elif vehicle_cnt_x_index[v] == min(vehicle_cnt_x_index):
            vehicle_cnt_sorted_pred.append(0)
        else:
            vehicle_cnt_sorted_pred.append(1)
    vehicle_cnt_y_pred = vehicle_cnt_sorted_pred

    res[sensor_id] = [centers[0][1], vehicle_cnt_y_pred, len(data)]

print("识别结果：")
for id, args in res.items():
    level = args[0]
    pred = args[1]
    total_vehicle_cnt = args[2]
    light_vehicle_cnt = pred.count(0)
    middle_vehicle_cnt = pred.count(1)
    heavy_vehicle_cnt = pred.count(2)
    print("{}号节点,沉降程度为{:.2f}%, 最近一小时内，小型车数量为:{},中型车数量为:{},大型车数量为:{} 经过车辆总数为:{}".format(
        id, level, light_vehicle_cnt, middle_vehicle_cnt, heavy_vehicle_cnt, total_vehicle_cnt))
    post_level(id, level, light_vehicle_cnt, middle_vehicle_cnt, heavy_vehicle_cnt, total_vehicle_cnt)

res_plot(plot_data["7"])
