import data_reader
import get_parameters
import platform
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
import numpy as np

if "Windows" in platform.platform():
    data_path = "E:/Manhole/training data/original data/3-29/1"
    # data_path = "E:/Manhole/training data/2d_plot"
else:
    data_path = "/Users/xiaoxiami/Manhole/training data/original data/3-6/3/side"

data_dic = data_reader.get_data_in_all_dir(data_path)
peak_value = []
width = []
start_q = {}
end_q = {}
max_index_q = {}
min_index_q = {}
var_q = {}
data_q = {}
quary = {}
new = True
if os.path.isfile(data_path + "/.bin") and not new:
    train_data = np.fromfile(data_path + "/.bin", dtype=np.int32)
    train_data = train_data.reshape(len(train_data) / 2, 2)
else:
    for title, data in data_dic.items():
        start, end = get_parameters.get_valid_data(data['acc_z'])
        data_q[title] = data['acc_z']
        start_q[title] = start
        end_q[title] = end
        (max_index, min_index, var) = (get_parameters.get_peak_width(data['acc_z'], start, end))
        max_index_q[title] = max_index
        min_index_q[title] = min_index
        var_q[title] = var
        buf = []
        if len(max_index) > 1:
            for i in range(len(max_index)):
                buf.append(abs(data['acc_z'][int(max_index[i])] - data['acc_z'][int(min_index[i])]))
            x = ((max_index[-1] + min_index[-1]) // 2) - ((max_index[0] + min_index[0]) // 2)
            y = max(buf) >> 9
            width.append(x)
            peak_value.append(y)
            quary[str(x)+str(y)] = title
            # middle_x = sum(data['acc_x'][:20]) // 20
            # middle_y = sum(data['acc_y'][:20]) // 20
            # variance_x = int(get_parameters.variance(data['acc_x'][start:end], middle_x) ** 0.5)
            # variance_y = int(get_parameters.variance(data['acc_y'][start:end], middle_y) ** 0.5)
    train_data = []
    for i in range(len(width)):
        train_data.append([width[i], peak_value[i]])
    train_data = np.array(train_data)
    train_data.tofile(data_path + "/.bin")

fig = plt.figure()
ax = fig.add_subplot(111)
k_means_fit = KMeans(n_clusters=3, random_state=150).fit(train_data)
y_pred = k_means_fit.predict(train_data)
for i in range(len(train_data)):
    if y_pred[i] == 0:
        color = 'r'
    elif y_pred[i] == 1:
        color = 'g'
    else:
        color = 'b'
    ax.plot(train_data[i][0], train_data[i][1], "o", picker=5, c=color)

for x, y in k_means_fit.cluster_centers_:
    ax.plot(x, y, "y*", markersize=24)

def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()

    N = len(event.ind)
    if not N:
        return True

    figi = {}
    ax = {}
    for i in range(len(xdata)):
        figi[i] = plt.figure(figsize=(16, 8))
        title = quary[str(xdata[i])+str(ydata[i])]
        ax[i] = figi[i].add_subplot(211)
        x = range(len(data_q[title]))
        ax[i].set_title(title)
        ax[i].plot(x, data_q[title])
        ax[i].set_ylim([-35000, 35000])
        for j in range(len(max_index_q[title])):
            ax[i].plot(max_index_q[title][j], data_q[title][0], 'ro')
            ax[i].plot(min_index_q[title][j], data_q[title][0], 'go')
        ax[i].plot(start_q[title], data_q[title][0], 'yo', alpha=0.5)
        ax[i].plot(end_q[title], data_q[title][0], 'yo', alpha=0.5)
        ax[i] = figi[i].add_subplot(212)
        ax[i].plot(range(len(var_q[title])), var_q[title])
        path = data_path + "/{}".format(title)
        os.startfile(str(path))
    for v in figi.values():
        v.show()
    return True


fig.canvas.mpl_connect('pick_event', onpick)
plt.show()
