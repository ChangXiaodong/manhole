def peak_width(data):
    def get_width(data_buf):
        n = data_buf.__len__()
        start_index = 0
        end_index = n
        for i in range(n - 5):
            if start_index == 0 and abs(data_buf[i] - data_buf[i + 2]) > 500 and abs(
                            data_buf[i] - data_buf[i + 5]) > 1000:
                start_index = i
                break
        for i in range(n - 1, 5, -1):
            if end_index == n and abs(data_buf[i] - data_buf[i - 2]) > 500 and abs(
                            data_buf[i] - data_buf[i - 5]) > 1000:
                end_index = i
                break
        return end_index - start_index

    acc_x = get_width(data["acc_x"])
    acc_y = get_width(data["acc_y"])
    acc_z = get_width(data["acc_z"])
    return sum([acc_x, acc_y, acc_z]) / 3 + 1


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
    width = peak_width(data)
    x_peak_value = peak_value(data["acc_x"])
    y_peak_value = peak_value(data["acc_y"])
    z_peak_value = peak_value(data["acc_z"])
    x_peak_value_divide_by_width = int(x_peak_value / width)
    y_peak_value_divide_by_width = int(y_peak_value / width)
    z_peak_value_divide_by_width = int(z_peak_value / width)
    return [x_peak_value_divide_by_width, y_peak_value_divide_by_width, z_peak_value_divide_by_width]

if __name__ == "__main__":
    import data_reader

    data_path = "E:/Manhole/training data/original data/2-22/manhole1"
    data_dic = data_reader.get_data_in_all_dir(data_path)
    for file, data in data_dic.items():
        print("file:{} width:{}".format(file, peak_width(data)))
