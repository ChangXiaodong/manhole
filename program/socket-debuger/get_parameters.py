import data_reader


def peak_width(data, threshold):
    length = len(data)
    index = []
    for i in xrange(length - 1):
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
    for i in xrange(len(data)):
        max_value = max(max_value, abs(data[i] - stable_value))
    return max_value



