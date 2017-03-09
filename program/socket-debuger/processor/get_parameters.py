import filter_function
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

def variance(data):
    mean_value = mean(data)
    sum_buf = 0
    for v in data:
        sum_buf += (v - mean_value) ** 2
    return sum_buf / len(data)

def mean(data):
    return sum(data) / len(data)

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


def get_width_index(data):
    '''
    :param data:
    :return: (index1 to index8)

            index1:start index of the wavelet
            index2:end index of the first stable part of the wavelet
            index3:start index of the middle flat wavelet
            index4:end index of the middle flat wavelet
            index5:end index of the second part of the wavelet
            index6:end index of the second stable part of the wavelet
            index7:first part peak value index
            index8:second park peak value index
    '''
    n = data.__len__()
    if n < 50:
        return
    index1 = 0
    index2 = 0
    index3 = 0
    index4 = 0
    buf_index3 = 0
    buf_index4 = 0
    index5 = 0
    index6 = 0
    index7 = 0
    index8 = 0
    var_list = []
    sqr_data = []
    VARIANCE_WIDTH = 8
    for v in data:
        sqr_data.append((v + abs(min(data))) ** 0.5)
    for i in range(VARIANCE_WIDTH, n):
        var = variance(sqr_data[i - VARIANCE_WIDTH:i])
        var_list.append(var)

    for i in range(var_list.__len__())[::-1]:
        if var_list[i] > 50:
            index6 = i
            break
    for i in range(var_list.__len__())[::-1]:
        if var_list[i] > 1:
            index5 = i
            break

    for i in range(var_list.__len__()):
        if var_list[i] > 1:
            index1 = i
            break
    for i in range(var_list.__len__()):
        if var_list[i] > 50:
            index2 = i
            break
    find_flag = 0
    for i in range(index2, index5):
        flat_flag = True
        for j in range(10):
            if var_list[i + j] > 150:
                flat_flag = False
                break
        if flat_flag and i > index2 + 50:
            if find_flag == 0:
                buf_index3 = i
                find_flag = 1
            if find_flag == 1:
                buf_index4 = i
        else:
            if find_flag == 1 and buf_index4 - buf_index3 > index4 - index3:
                unstable_flag = False
                for v in var_list[buf_index3:buf_index4]:
                    if v > 1000:
                        unstable_flag = True
                        break
                if unstable_flag:
                    continue
                index4 = buf_index4
                index3 = buf_index3
                find_flag = 0
    if index2 * index3 * index4 * index5 != 0:
        index7 = data.index(max(data[index2:index3]))
        index8 = data.index(max(data[index4:index5]))
    return (index1, index2, index3, index4, index5, index6, index7, index8)
    # print(index1, index2, index3, index4, index5, index6, index7, index8)
    # plt.subplot(2, 1, 1)
    # plt.plot(var_list)
    # plt.plot(index1, 100, 'o')
    # plt.plot(index2, 100, 'o')
    # plt.plot(index3, 100, 'o')
    # plt.plot(index4, 100, 'o')
    # plt.plot(index5, 100, 'o')
    # plt.plot(index6, 100, 'o')
    # plt.subplot(2, 1, 2)
    # plt.plot(data)
    # plt.plot(index1, 100, 'o')
    # plt.plot(index2, 100, 'o')
    # plt.plot(index3, 100, 'o')
    # plt.plot(index4, 100, 'o')
    # plt.plot(index5, 100, 'o')
    # plt.plot(index6, 100, 'o')
    # plt.plot(index7, data[index7], 'o')
    # plt.plot(index8, data[index8], 'o')
    # plt.show()


if __name__ == "__main__":
    import processor.data_reader
    import matplotlib.pyplot as plt
    import platform
    from mpl_toolkits.mplot3d import Axes3D

    filter = filter_function.Filter()
    # data_path = "E:/Manhole/training data/plot"
    if "Windows" in platform.platform():
        data_path = "E:/Manhole/training data/original data/3-6/3/middle"
    else:
        data_path = "/Users/xiaoxiami/Manhole/training data/original data/3-6/3/side"

    data_dic = processor.data_reader.get_data_in_all_dir(data_path)
    index_x = []
    index_y = []
    index_z = []

    for title, data in data_dic.items():
        filtered_data_x = filter.g_h_filter(data=data['acc_x'], dx=1, g=1. / 10, h=1. / 3, dt=1.)
        filtered_data_y = filter.g_h_filter(data=data['acc_y'], dx=1, g=1. / 10, h=1. / 3, dt=1.)
        filtered_data_z = filter.g_h_filter(data=data['acc_z'], dx=1, g=1. / 10, h=1. / 3, dt=1.)
        index_x.append(get_width_index(filtered_data_x))
        index_y.append(get_width_index(filtered_data_y))
        index_z.append(get_width_index(filtered_data_z))
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []
    for i in range(index_x.__len__()):
        item_x = index_x[i]
        item_y = index_y[i]
        item_z = index_z[i]
        x.append(item_x[5] - item_x[3])
        y.append(item_y[5] - item_y[3])
        z.append(item_z[5] - item_z[3])
        # ax.plot(item[2] - item[0], 100, "bo")
    ax.plot(x, y, z, "bo")

    if "Windows" in platform.platform():
        data_path = "E:/Manhole/training data/original data/3-6/3/middle"
    else:
        data_path = "/Users/xiaoxiami/Manhole/training data/original data/3-6/3/middle"
    data_dic = processor.data_reader.get_data_in_all_dir(data_path)
    index_x = []
    index_y = []
    index_z = []
    for title, data in data_dic.items():
        filtered_data_x = filter.g_h_filter(data=data['acc_x'], dx=1, g=1. / 10, h=1. / 3, dt=1.)
        filtered_data_y = filter.g_h_filter(data=data['acc_y'], dx=1, g=1. / 10, h=1. / 3, dt=1.)
        filtered_data_z = filter.g_h_filter(data=data['acc_z'], dx=1, g=1. / 10, h=1. / 3, dt=1.)
        index_x.append(get_width_index(filtered_data_x))
        index_y.append(get_width_index(filtered_data_y))
        index_z.append(get_width_index(filtered_data_z))
    x = []
    y = []
    z = []
    for i in range(index_x.__len__()):
        item_x = index_x[i]
        item_y = index_y[i]
        item_z = index_z[i]
        # ax.plot(item[2] - item[0], 100, "o")
        x.append(item_x[5] - item_x[3])
        y.append(item_y[5] - item_y[3])
        z.append(item_z[5] - item_z[3])
    ax.plot(x, y, z, "ro")

    plt.show()
