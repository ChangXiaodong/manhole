from global_parameters import *
import get_parameters
import numpy as np


class Filter(object):
    def __init__(self):
        pass

    def mean_value_filter(self, data, filter_length=3):
        length = len(data)
        if length < filter_length:
            return data
        filtered_data = []
        sum_buf = 0
        for i in range(length - filter_length):
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

    def fft_filter(self, data, width=600, dir="out"):
        transformed = np.fft.fft(data)
        shifted = np.fft.fftshift(transformed)
        center = list(shifted).index(max(shifted))
        new_fft = []
        for i, v in enumerate(shifted):
            if dir == "out":
                if center - width // 2 < i < center + width // 2:
                    new_fft.append(0)
                else:
                    new_fft.append(v)
            elif dir == "in":
                if center - width // 2 < i < center + width // 2:
                    new_fft.append(v)
                else:
                    new_fft.append(0)
        shifted = np.fft.ifftshift(new_fft)
        transformed = np.fft.ifft(shifted)
        return transformed

    def mid_value_filter(self, data, width=3):
        i = 0
        while i < len(data) - width:
            mid = sorted(data[i:i + width])[width // 2]
            data[i:i + width] = [mid for _ in range(width)]
            i += width
        return data

    def linearSooth3(self, data):
        n = len(data)
        res = [0 for _ in range(n)]
        if n < 3:
            for i in range(n):
                res[i] = data[i]
        else:
            res[0] = (5.0 * data[0] + 2.0 * data[1] - data[2]) // 6.0
            for i in range(1, n - 2):
                res[i] = (data[i - 1] + data[i] + data[i + 1]) // 3.0
            res[n - 1] = (5.0 * data[n - 1] + 2 * data[n - 2] - data[n - 3]) // 6.0
        return res

    def linearSooth5(self, data):
        n = len(data)
        res = [0 for _ in range(n)]
        if n < 5:
            for i in range(n):
                res[i] = data[i]
        else:
            res[0] = (3.0 * data[0] + 2.0 * data[1] + data[2] - data[4]) // 5.0
            res[1] = (4.0 * data[0] + 3.0 * data[1] + 2 * data[2] + data[3]) // 10.0
            for i in range(2, n - 4):
                res[i] = (data[i - 2] + data[i - 1] + data[i] + data[i + 1] + data[i + 2]) // 5.0
            res[n - 2] = (4.0 * data[n - 1] + 3.0 * data[n - 2] + 2 * data[n - 3] + data[n - 4]) // 10
            res[n - 1] = (3.0 * data[n - 1] + 2.0 * data[n - 2] + data[n - 3] - data[n - 5]) // 5.0
        return res

    def linearSooth7(self, data):
        n = len(data)
        res = [0 for _ in range(n)]
        if n < 7:
            for i in range(n):
                res[i] = data[i]
        else:
            res[0] = (13.0 * data[0] + 10.0 * data[1] + 7.0 * data[2] + 4.0 * data[3] +
                      data[4] - 2.0 * data[5] - 5.0 * data[6]) / 28.0
            res[1] = (5.0 * data[0] + 4.0 * data[1] + 3 * data[2] + 2 * data[3] +
                      data[4] - data[6]) / 14.0

            res[2] = (7.0 * data[0] + 6.0 * data[1] + 5.0 * data[2] + 4.0 * data[3] +
                      3.0 * data[4] + 2.0 * data[5] + data[6]) / 28.0

            for i in range(3, n - 5):
                res[i] = (data[i - 3] + data[i - 2] + data[i - 1] + data[i] + data[i + 1] + data[i + 2] + data[
                    i + 3]) / 7.0
            res[n - 3] = (7.0 * data[n - 1] + 6.0 * data[n - 2] + 5.0 * data[n - 3] +
                          4.0 * data[n - 4] + 3.0 * data[n - 5] + 2.0 * data[n - 6] + data[n - 7]) / 28.0

            res[n - 2] = (5.0 * data[n - 1] + 4.0 * data[n - 2] + 3.0 * data[n - 3] +
                          2.0 * data[n - 4] + data[n - 5] - data[n - 7]) / 14.0

            res[n - 1] = (13.0 * data[n - 1] + 10.0 * data[n - 2] + 7.0 * data[n - 3] +
                          4 * data[n - 4] + data[n - 5] - 2 * data[n - 6] - 5 * data[n - 7]) / 28.0
        return res


if __name__ == "__main__":
    filter = Filter()
