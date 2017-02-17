import matplotlib.pyplot as plt
import data_reader

dir_path = "E:/Manhole/test data/plot"
data_dic = data_reader.get_data_in_all_dir(dir_path)
fig = {}
ax = {}

for title, value in data_dic.items():
    fig[title] = plt.figure()
    ax[title] = fig[title].add_subplot(111)
    ax[title].set_title(title)
    x = range(len(value['gyo_z']))
    acc_x_line, = ax[title].plot(x, value['acc_x'])
    acc_y_line, = ax[title].plot(x, value['acc_y'])
    acc_z_line, = ax[title].plot(x, value['acc_z'])

plt.show()
