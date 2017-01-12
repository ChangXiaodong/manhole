import data_reader


def peak_width(data, threshold):
    length = len(data)
    index = []
    for i in xrange(length - 1):
        if abs(data[i] - data[i + 1]) > threshold:
            index.append(i)
    return index[-1] - index[0]


def peak_value(data):
    return abs(max(data) - min(data))


def mean(data):
    return sum(data) / len(data)


def variance(data):
    mean_value = mean(data)
    sum_buf = 0
    for v in data:
        sum_buf += (v - mean_value) ** 2
    return sum_buf / len(data)


def pulse_max(data):
    stable_value = mean(data[:5])
    max_value = 0
    for i in xrange(len(data)):
        max_value = max(max_value, abs(data[i] - stable_value))
    return max_value


if __name__ == "__main__":
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt


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
    acc_pulse_buf, gyo_pulse_buf = get_pulse("E:/Manhole/test data/middle_fast/1/middle_fast_1.csv", acc_pulse_buf,
                                             gyo_pulse_buf)
    acc_pulse_buf, gyo_pulse_buf = get_pulse("E:/Manhole/test data/middle_fast/2/middle_fast_2.csv", acc_pulse_buf,
                                             gyo_pulse_buf)
    # acc_pulse_buf, gyo_pulse_buf = get_pulse("E:/Manhole/test data/middle_middle/1/middle_middle_1.csv", acc_pulse_buf,
    #                                          gyo_pulse_buf)
    # acc_pulse_buf, gyo_pulse_buf = get_pulse("E:/Manhole/test data/middle_middle/2/middle_middle_2.csv", acc_pulse_buf,
    #                                          gyo_pulse_buf)
    # acc_pulse_buf, gyo_pulse_buf = get_pulse("E:/Manhole/test data/middle_middle/3/middle_middle_3.csv", acc_pulse_buf,
    #                                          gyo_pulse_buf)
    acc_pulse_buf, gyo_pulse_buf = get_pulse("E:/Manhole/test data/middle_slow/1/middle_slow_1.csv", acc_pulse_buf,
                                             gyo_pulse_buf)
    acc_pulse_buf, gyo_pulse_buf = get_pulse("E:/Manhole/test data/middle_slow/2/middle_slow_2.csv", acc_pulse_buf,
                                             gyo_pulse_buf)
    acc_pulse_buf, gyo_pulse_buf = get_pulse("E:/Manhole/test data/middle_slow/3/middle_slow_3.csv", acc_pulse_buf,
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
