import matplotlib.pyplot as plt
import data_reader
import numpy as np
import filter_function
import platform

if platform.platform() == "Windows":
    dir_path = "E:/Manhole/training data/plot"
else:
    dir_path = "/Users/xiaoxiami/Manhole/training data/plot"
data_dic = data_reader.get_data_in_all_dir(dir_path)
fig = {}
ax = {}
filter = filter_function.Filter()
for title, value in data_dic.items():
    fig[title] = plt.figure(figsize=(16, 8))
    ax["acc-" + title] = fig[title].add_subplot(411)
    ax["acc-" + title].set_title(title)
    x = range(len(value['gyo_z']))
    acc_x_line, = ax["acc-" + title].plot(x, value['acc_x'])
    acc_y_line, = ax["acc-" + title].plot(x, value['acc_y'])
    acc_z_line, = ax["acc-" + title].plot(x, value['acc_z'])
    ax["acc-" + title].set_ylim([-35000, 35000])
    ax["acc-" + title] = fig[title].add_subplot(412)
    acc_line1, = ax["acc-" + title].plot(filter.g_h_filter(data=value['acc_x'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    acc_line2, = ax["acc-" + title].plot(filter.g_h_filter(data=value['acc_y'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    acc_line3, = ax["acc-" + title].plot(filter.g_h_filter(data=value['acc_z'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    ax["acc-" + title] = fig[title].add_subplot(413)
    gyo_x_line, = ax["acc-" + title].plot(x, value['gyo_x'])
    gyo_y_line, = ax["acc-" + title].plot(x, value['gyo_y'])
    gyo_z_line, = ax["acc-" + title].plot(x, value['gyo_z'])
    ax["acc-" + title] = fig[title].add_subplot(414)
    gyo_line1, = ax["acc-" + title].plot(filter.g_h_filter(data=value['gyo_x'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    gyo_line2, = ax["acc-" + title].plot(filter.g_h_filter(data=value['gyo_y'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    gyo_line3, = ax["acc-" + title].plot(filter.g_h_filter(data=value['gyo_z'], dx=1, g=1. / 10, h=1. / 3, dt=1.))


plt.show()
