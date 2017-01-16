from get_parameters import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os
import pyperclip
import tkMessageBox as msg
import time

class PlotTools(object):
    def __init__(self):
        self.fig = []

    def plot_3d(self, x, y, z, color='b', marker='o'):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        for i, item in enumerate(x):
            xs = x[i]
            ys = y[i]
            zs = z[i]
            ax.scatter(xs, ys, zs, c=color, marker=marker)
        plt.show()

    def plot_3d_browser(self, x, y, z, filename_dic, title, color='b', marker='o'):
        def onpick(event):
            if event.artist != line:
                return True
            N = len(event.ind)
            if not N:
                return True
            # the click locations
            dataind = event.ind[0]
            name = "{}{}{}".format(x[dataind], y[dataind], z[dataind])
            pyperclip.copy(str(filename_dic[name]).split("/")[-1])
            if msg.askyesno("open file directory?",
                            "open file directory ?\nx:{}\ny:{}\nz:{}".format(x[dataind], y[dataind], z[dataind])):
                os.startfile(filename_dic[name])


        self.fig.append(plt.figure())
        ax = self.fig[-1].add_subplot(111, projection='3d')
        ax.set_title(title)
        line, = ax.plot(x, y, z, marker, c=color, picker=5)  # 5 points tolerance
        self.fig[-1].canvas.mpl_connect('pick_event', onpick)

    def plot_show(self):
        plt.show()


if __name__ == "__main__":
    def get_pulse(path, acc_pulse_buf, gyo_pulse_buf):
        acc_x, acc_y, acc_z, gyo_x, gyo_y, gyo_z = data_reader.get_data_by_csvpath(path)
        pulse_max_acc_x = pulse_max(acc_x)
        pulse_max_acc_y = pulse_max(acc_y)
        pulse_max_acc_z = pulse_max(acc_z)
        pulse_max_gyo_x = pulse_max(gyo_x)
        pulse_max_gyo_y = pulse_max(gyo_y)
        pulse_max_gyo_z = pulse_max(gyo_z)
        print "{} pulse max acc x:{} y:{} z:{} gyo x:{} y:{} z:{}".format(
            path.split("/")[-1],
            pulse_max_acc_x,
            pulse_max_acc_y,
            pulse_max_acc_z,
            pulse_max_gyo_x,
            pulse_max_gyo_y,
            pulse_max_gyo_z
        )

        acc_pulse_buf.append([pulse_max_acc_x, pulse_max_acc_y, pulse_max_acc_z])
        gyo_pulse_buf.append([pulse_max_gyo_x, pulse_max_gyo_y, pulse_max_gyo_z])
        return acc_pulse_buf, gyo_pulse_buf


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    acc_pulse_buf = []
    gyo_pulse_buf = []
    acc_pulse_buf, gyo_pulse_buf = get_pulse("/Users/xiaoxiami/Manhole/test data/middle_fast/1/middle_fast_1.csv",
                                             acc_pulse_buf,
                                             gyo_pulse_buf)
    acc_pulse_buf, gyo_pulse_buf = get_pulse("/Users/xiaoxiami/Manhole/test data/middle_fast/2/middle_fast_2.csv",
                                             acc_pulse_buf,
                                             gyo_pulse_buf)
    # acc_pulse_buf, gyo_pulse_buf = get_pulse("/Users/xiaoxiami/Manhole/test data/middle_middle/1/middle_middle_1.csv", acc_pulse_buf,
    #                                          gyo_pulse_buf)
    # acc_pulse_buf, gyo_pulse_buf = get_pulse("/Users/xiaoxiami/Manhole/test data/middle_middle/2/middle_middle_2.csv", acc_pulse_buf,
    #                                          gyo_pulse_buf)
    # acc_pulse_buf, gyo_pulse_buf = get_pulse("/Users/xiaoxiami/Manhole/test data/middle_middle/3/middle_middle_3.csv", acc_pulse_buf,
    #                                          gyo_pulse_buf)
    acc_pulse_buf, gyo_pulse_buf = get_pulse("/Users/xiaoxiami/Manhole/test data/middle_slow/1/middle_slow_1.csv",
                                             acc_pulse_buf,
                                             gyo_pulse_buf)
    acc_pulse_buf, gyo_pulse_buf = get_pulse("/Users/xiaoxiami/Manhole/test data/middle_slow/2/middle_slow_2.csv",
                                             acc_pulse_buf,
                                             gyo_pulse_buf)
    acc_pulse_buf, gyo_pulse_buf = get_pulse("/Users/xiaoxiami/Manhole/test data/middle_slow/3/middle_slow_3.csv",
                                             acc_pulse_buf,
                                             gyo_pulse_buf)

    # for i, item in enumerate(acc_pulse_buf):
    #     xs = acc_pulse_buf[i][0]
    #     ys = acc_pulse_buf[i][1]
    #     zs = acc_pulse_buf[i][2]
    #     ax.scatter(xs, ys, zs, c='r', marker='^')
    for i, item in enumerate(gyo_pulse_buf):
        xs = gyo_pulse_buf[i][0]
        ys = gyo_pulse_buf[i][1]
        zs = gyo_pulse_buf[i][2]
        ax.scatter(xs, ys, zs, c='b', marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()
