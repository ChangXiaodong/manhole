from global_parameters import *
import get_parameters


class Filter(object):
    def __init__(self):
        pass

    def mean_value_filter(self, data, filter_length=3):
        length = len(data)
        if length < filter_length:
            return data
        filtered_data = []
        sum_buf = 0
        for i in xrange(length - filter_length):
            if i < filter_length:
                filtered_data.append(data[i])
                sum_buf += data[i]
            else:
                sum_buf -= data[i - filter_length]
                sum_buf += data[i + filter_length]
                filtered_data.append(sum_buf / filter_length)
        return filtered_data

    def DBSCAN_filter(self, datapath):
        import DBSCAN
        return DBSCAN.DBSCAN_filter(datapath)

    def walk_bicycle_filter(self, data_dic):
        if not data_dic:
            return
        for file, data in data_dic.items():
            pulse_max = get_parameters.pulse_max(data["acc_z"])
            if pulse_max < WALK_BIKE_PULSE_MAX:
                data_dic.pop(file)
        return data_dic

    def min_max_filter(self, data):
        n = data.__len__()
        a = 0.6
        rate = []
        rate_r = []
        for i in range(5, n):
            data[i] = float((1 - a) * data[i]) + float(a * data[i - 1])
            r = float((data[i] - data[i - 3]) / 2)
            rate.append(r)
        for i in range(2, rate.__len__()):
            rate_r.append(float((rate[i] - rate[i - 2]) / 2))
        rate = []
        for i in range(2, rate_r.__len__()):
            rate.append(float((rate_r[i] - rate_r[i - 2]) / 2))
        return rate

    def g_h_filter(self, data, dx, g, h, dt=1.):
        x = data[0]
        results = []
        for z in data:
            x_est = x + (dx * dt)
            residual = z - x_est
            dx = dx + h * (residual) / dt
            x = x_est + g * residual
            results.append(x)
        return results


if __name__ == "__main__":
    filter = Filter()
