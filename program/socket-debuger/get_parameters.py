import data_reader


def peak_width(data, threshold):
    length = len(data)
    index = []
    for i in range(length - 1):
        if abs(data[i] - data[i + 1]) > threshold:
            index.append(i)
    if not index:
        return 0
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
    for i in range(len(data)):
        max_value = max(max_value, abs(data[i] - stable_value))
    return max_value


def peak_value_divide_by_width(data):
    gyo_x_peak_width = peak_width(data["gyo_x"], 1000)
    gyo_y_peak_width = peak_width(data["gyo_y"], 1000)
    gyo_z_peak_width = peak_width(data["gyo_z"], 1000)
    acc_x_peak_width = peak_width(data["acc_x"], 1000)
    acc_y_peak_width = peak_width(data["acc_y"], 1000)
    acc_z_peak_width = peak_width(data["acc_z"], 1000)
    width = max(gyo_x_peak_width, gyo_y_peak_width, gyo_z_peak_width,
                     acc_x_peak_width, acc_y_peak_width, acc_z_peak_width) / 3 + 1
    x_peak_value = peak_value(data["acc_x"])
    y_peak_value = peak_value(data["acc_y"])
    z_peak_value = peak_value(data["acc_z"])
    x_peak_value_divide_by_width = int(x_peak_value / width)
    y_peak_value_divide_by_width = int(y_peak_value / width)
    z_peak_value_divide_by_width = int(z_peak_value / width)
    return [x_peak_value_divide_by_width, y_peak_value_divide_by_width, z_peak_value_divide_by_width]
