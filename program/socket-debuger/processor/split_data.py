import processor.data_reader
import matplotlib.pyplot as plt
import platform
import filter_function
import get_parameters
import filter_function
import numpy as np

def split_data_by_slop_and_time(data):
    split_data = []
    WIDTH = 2
    MAX_CNT = 500
    start = -1
    end = 0
    max_value = 0
    buf = []
    count = MAX_CNT
    stable_cnt = 0
    end_flag = 0
    index = []
    for i in range(len(data) - WIDTH):
        slop = abs((data[i + WIDTH] - data[i]) / (WIDTH + 1))
        if start == -1 and slop > 400:
            if i > 100 and i - end > 100:
                start = i - 100
                buf.append([data[start:i]])
            else:
                buf.append([data[end:i]])
                start = (end + i) // 2
            count = MAX_CNT
            stable_cnt = 0
            index.append(start)
        if start != -1:
            if data[i] > 0 and data[i] > max_value:
                max_value = data[i]
                if count < MAX_CNT // 2:
                    count = MAX_CNT
            elif data[i] > 0 and data[i] > max_value * 0.75:
                count = int(count * 1.2)
            count -= 1
            if count == 0:
                end_flag = 1
            if slop < 400:
                stable_cnt += 1
            else:
                stable_cnt = 0
            if stable_cnt > 100:
                if count < MAX_CNT // 2:
                    end_flag = 1
            if end_flag == 1:
                buf.append(buf.pop().append(data[start:i]))
                start = -1
                end = i
                end_flag = 0
                count = MAX_CNT
                stable_cnt = 0
                index.append(end)
    return split_data, index


if "Windows" in platform.platform():
    data_path = "E:/Manhole/training data/split_error/"
    new_path = "E:/Manhole/training data/split_correct/"
else:
    data_path = "/Users/xiaoxiami/Manhole/training data/original data/3-6/3/side"

data_dic = processor.data_reader.get_data_in_all_dir(data_path)

fig = {}
ax = {}

for title, data in data_dic.items():
    print(title)
    data_filter = filter_function.Filter()
    n = len(data['acc_z'])
    x = range(n)
    _, index = split_data_by_slop_and_time(data['acc_z'])
    fig[title] = plt.figure(figsize=(16, 8))
    ax["acc-" + title] = fig[title].add_subplot(111)
    ax["acc-" + title].set_ylim([-35000, 35000])
    ax["acc-" + title].plot(data['acc_z'])
    ax["acc-" + title].plot(index, [data['acc_z'][0] for _ in range(len(index))], 'ro')
    ax["acc-" + title].set_title(title)
plt.show()
