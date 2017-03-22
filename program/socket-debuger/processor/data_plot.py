import platform
import matplotlib.pyplot as plt
import data_reader
from processor import filter_function

def gh_plot(fig, ax, title, value):
    filter = filter_function.Filter()
    fig[title] = plt.figure(figsize=(16, 8))
    ax["acc-" + title] = fig[title].add_subplot(411)
    ax["acc-" + title].set_title(title)
    x = range(len(value['gyo_z']))
    ax["acc-" + title].plot(x, value['acc_x'])
    ax["acc-" + title].plot(x, value['acc_y'])
    ax["acc-" + title].plot(x, value['acc_z'])
    ax["acc-" + title].set_ylim([-35000, 35000])
    ax["acc-" + title] = fig[title].add_subplot(412)
    ax["acc-" + title].plot(filter.g_h_filter(data=value['acc_x'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    ax["acc-" + title].plot(filter.g_h_filter(data=value['acc_y'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    ax["acc-" + title].plot(filter.g_h_filter(data=value['acc_z'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    ax["acc-" + title] = fig[title].add_subplot(413)
    ax["acc-" + title].plot(x, value['gyo_x'])
    ax["acc-" + title].plot(x, value['gyo_y'])
    ax["acc-" + title].plot(x, value['gyo_z'])
    ax["acc-" + title] = fig[title].add_subplot(414)
    ax["acc-" + title].plot(filter.g_h_filter(data=value['gyo_x'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    ax["acc-" + title].plot(filter.g_h_filter(data=value['gyo_y'], dx=1, g=1. / 10, h=1. / 3, dt=1.))
    ax["acc-" + title].plot(filter.g_h_filter(data=value['gyo_z'], dx=1, g=1. / 10, h=1. / 3, dt=1.))

def none_plot(fig, ax, title, value):
    fig[title] = plt.figure(figsize=(16, 8))
    ax["acc-" + title] = fig[title].add_subplot(211)
    ax["acc-" + title].set_title(title)
    x = range(len(value['gyo_z']))
    ax["acc-" + title].plot(x, value['acc_x'])
    ax["acc-" + title].plot(x, value['acc_y'])
    ax["acc-" + title].plot(x, value['acc_z'])
    ax["acc-" + title].set_ylim([-35000, 35000])
    ax["acc-" + title] = fig[title].add_subplot(212)
    ax["acc-" + title].plot(x, value['gyo_x'])
    ax["acc-" + title].plot(x, value['gyo_y'])
    ax["acc-" + title].plot(x, value['gyo_z'])


def plot_2d(filter_type=None):
    if "Windows" in platform.platform():
        dir_path = "E:/Manhole/training data/2d_plot"
    else:
        dir_path = "/Users/xiaoxiami/Manhole/training data/2d_plot"
    data_dic = data_reader.get_data_in_all_dir(dir_path)
    fig = {}
    ax = {}

    for title, value in data_dic.items():
        if filter_type == "gh":
            gh_plot(fig, ax, title, value)
        elif filter_type is None:
            none_plot(fig, ax, title, value)
    plt.show()

if __name__ == "__main__":
    plot_2d()

