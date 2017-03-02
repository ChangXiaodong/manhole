import matplotlib.pyplot as plt
import data_reader
import numpy as np

dir_path = "E:/Manhole/training data/plot"
data_dic = data_reader.get_data_in_all_dir(dir_path)
fig = {}
ax = {}

for title, value in data_dic.items():
    fig[title] = plt.figure(figsize=(16, 8))
    ax["acc-" + title] = fig[title].add_subplot(311)
    ax["acc-" + title].set_title(title)
    x = range(len(value['gyo_z']))
    acc_x_line, = ax["acc-" + title].plot(x, value['acc_x'])
    acc_y_line, = ax["acc-" + title].plot(x, value['acc_y'])
    acc_z_line, = ax["acc-" + title].plot(x, value['acc_z'])
    ax["acc-" + title].set_ylim([-35000, 35000])
    ax["gyo-" + title] = fig[title].add_subplot(312)
    gyo_x_line, = ax["gyo-" + title].plot(x, value['gyo_x'])
    gyo_y_line, = ax["gyo-" + title].plot(x, value['gyo_y'])
    gyo_z_line, = ax["gyo-" + title].plot(x, value['gyo_z'])
    ax["gyo-" + title].set_ylim([-35000, 35000])
plt.show()
