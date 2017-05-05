# coding=utf-8
import filter_function
import math


def peak_width_old(data):
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


def variance(data, mean_value=None):
    if not mean_value:
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
    width = peak_width_old(data)
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


def split_data(data):
    partition = []
    data_filter = filter_function.Filter()
    # data = data_filter.fft_filter(data)
    # 计算原始数据的标准差，并经过一个均值滤波，为后面数据切分做准备
    var = []
    for i in range(len(data) - 3):
        v = int(variance(data[i:i + 3], data[0]) ** 0.5)
        var.append(0 if v < 100 else v)
    var = data_filter.mean_value_filter(var, 20)
    var = data_filter.mean_value_filter(var, 10)
    # var = data_filter.mid_value_filter(var)
    max_var = max(var)
    # 找到第一个波峰和他的斜率
    WIDTH = 20
    split = []
    # 将数据切分，有多少个轮子partition就有多长
    # for i, v in enumerate(var):
    #     print(i, v)
    i = WIDTH

    pass_max_flag = 0
    # 寻找var的波谷进行切分
    while WIDTH <= i < len(var) - WIDTH:
        if var[i] > max_var // 20 or var[i] > 200:
            pass_max_flag = 1
        if pass_max_flag == 1:
            count = 0
            for j in range(i - WIDTH, i + WIDTH):
                # 对 var为0时进行特殊处理。检查左右连边是不是有峰值
                if var[i] <= var[j]:
                    if var[i] != 0:
                        count += 1
                    else:
                        if i - 100 > 0 and i + 100 < len(var):
                            pass_max_flag = 0
                            left_max = max(var[i - 100:i])
                            right_max = max(var[i:i + 100])
                            if left_max > max(var) * 0.3 and right_max > max(var) * 0.3:
                                split.append(i - 4)
                                i += WIDTH
                                count = 0
                                break
            if count >= WIDTH * 2 - 3 and max(var[i - WIDTH:i + WIDTH]) - var[i] > 200:
                split.append(i - 4)
                i += WIDTH
        i += 1
    if len(split) == 1:
        count = 0
        for v in var:
            if v > max_var * 2 // 3:
                count += 1
        if count > 50:
            split = []
    # 波谷切分没有成功，寻找波峰，用两个波峰的中值进行切分
    if not split:
        split = []
        split_buf = []
        WIDTH = WIDTH
        i = WIDTH
        while WIDTH <= i < len(var) - WIDTH:
            count = 0
            for j in range(i - WIDTH, i + WIDTH):
                if var[i] >= var[j] and var[i] > max_var * 0.2:
                    count += 1
            if count > WIDTH * 2 - 2:
                split_buf.append(i - 4)
                i += WIDTH
            i += 1
        for i in range(1, len(split_buf)):
            split.append((split_buf[i] + split_buf[i - 1]) >> 1)
        if len(split_buf) == 1:
            split.append(split_buf[0] - 80)
    mem = 0
    # 切分数据
    for s in split:
        if partition:
            partition.pop()
        partition.append(data[mem:s])
        partition.append(data[s:])
        mem = s

    return partition, var


def get_valid_data(data):
    '''
    :param data: 
    :return:start inedx, end index
     通过斜率找到波形的起始点和结束点
    '''
    WIDTH = 2
    start = 0
    end = 0
    # for i, v in enumerate(data):
    #     print(i, v)
    for i in range(len(data) - WIDTH):
        if abs((data[i + WIDTH] - data[i]) / (WIDTH + 1)) > 200:
            start = i
            break
    for i in range(len(data) - 1, WIDTH, -1):
        if abs((data[i] - data[i - WIDTH]) / (WIDTH + 1)) > 200:
            end = i
            break
    return start, end


def get_peak_width(data, low, high):
    '''
    :param data: 
    :return: width
     目标：
     1.计算出车轮的个数。peak_max_index和peak_min_index的长度为车轮个数。
     2.计算出车轮经过时的峰峰值。一组peak_max_index和peak_min_index对应着最大值最小值的坐标。相减即为峰峰值
     3.计算出车辆经过的起点和终点。用于判断车辆长度，速度等。也可以用来切分不同车辆。low, high为起点和终点
     4.通过var可以整体的判断出标准差，间接反映出井盖震动强弱。
    '''

    partition, var = split_data(data)
    peak_max_index = []
    peak_min_index = []
    base_length = 0
    middle = sum(data[:20]) // 20

    for i, part in enumerate(partition):
        max_buf = -32768
        max_index = -1
        min_buf = 32768
        min_index = -1
        for j, v in enumerate(part):
            if abs(v - middle) > 100:
                if v > max_buf:
                    max_buf = v
                    max_index = j + base_length
                elif v < min_buf:
                    min_buf = v
                    min_index = j + base_length
        if max_index > low and max_index < high and min_index > low and min_index < high:
            # 删除波峰波谷过长的index，这种是识别错误的
            if abs(max_index - min_index) < 70:
                peak_max_index.append(max_index)
                peak_min_index.append(min_index)
        base_length += len(part)
    # 若有四个index，说明有抖动没有滤掉
    # if n == 4:
    #     min_buf = [
    #         (0.8 * peak_min_index[0] + 0.2 * peak_min_index[1]),
    #         (0.8 * peak_min_index[2] + 0.2 * peak_min_index[3]),
    #     ]
    #     max_buf = [
    #         (0.8 * peak_max_index[0] + 0.2 * peak_max_index[1]),
    #         (0.8 * peak_max_index[2] + 0.2 * peak_max_index[3]),
    #     ]
    #     peak_min_index = min_buf[:]
    #     peak_max_index = max_buf[:]

    return peak_max_index, peak_min_index, var


def index():
    if "Windows" in platform.platform():
        # data_path = "E:/Manhole/training data/original data/3-6/3/middle"
        data_path = "E:/Manhole/training data/original data/4-12/2/2017-04-12_16-39-49/"

    else:
        data_path = "/Users/xiaoxiami/Manhole/training data/original data/3-6/3/side"

    data_dic = processor.data_reader.get_data_in_all_dir(data_path)

    fig = {}
    ax = {}

    for title, data in data_dic.items():
        x = range(len(data['acc_x']))
        print(title)
        start, end = get_valid_data(data['acc_z'])
        (max_index, min_index, var) = (get_peak_width(data['acc_z'], start, end))

        fig[title] = plt.figure(figsize=(16, 8))
        ax["acc-" + title] = fig[title].add_subplot(211)
        ax["acc-" + title].set_title(title)
        ax["acc-" + title].plot(x, data['acc_z'])
        ax["acc-" + title].set_ylim([-35000, 35000])
        for i in range(len(max_index)):
            ax["acc-" + title].plot(max_index[i], data['acc_z'][0], 'ro')
            ax["acc-" + title].plot(min_index[i], data['acc_z'][0], 'go')
        ax["acc-" + title].plot(start, data['acc_z'][0], 'yo', alpha=0.5)
        ax["acc-" + title].plot(end, data['acc_z'][0], 'yo', alpha=0.5)
        ax["acc-" + title] = fig[title].add_subplot(212)
        ax["acc-" + title].plot(range(len(var)), var)

    plt.show()


def x_y_info():
    if "Windows" in platform.platform():
        # data_path = "E:/Manhole/training data/original data/3-6/3/middle"
        data_path = "E:/Manhole/training data/2d_plot/"
    else:
        data_path = "/Users/xiaoxiami/Manhole/training data/original data/3-6/3/side"

    data_dic = processor.data_reader.get_data_in_all_dir(data_path)

    fig = {}
    ax = {}

    for title, data in data_dic.items():
        n = len(data['acc_x'])
        x = range(n)
        print(title)
        start, end = get_valid_data(data['acc_z'])
        middle_x = sum(data['acc_x'][:20]) // 20
        middle_y = sum(data['acc_y'][:20]) // 20
        variance_x = int(variance(data['acc_x'][start:end], middle_x) ** 0.5)
        variance_y = int(variance(data['acc_y'][start:end], middle_y) ** 0.5)
        print(variance_x, variance_y)
        fig[title] = plt.figure(figsize=(16, 8))
        ax["acc-" + title] = fig[title].add_subplot(111)
        ax["acc-" + title].set_title(title)
        ax["acc-" + title].plot(x, data['acc_x'])
        ax["acc-" + title].plot(x, data['acc_y'])
        ax["acc-" + title].set_ylim([-35000, 35000])

    plt.show()


if __name__ == "__main__":
    import processor.data_reader
    import matplotlib.pyplot as plt
    import platform
    from mpl_toolkits.mplot3d import Axes3D

    index()
    # x_y_info()
