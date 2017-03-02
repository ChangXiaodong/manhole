import DBSCAN
import get_parameters
from global_parameters import *

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
        return DBSCAN.DBSCAN_filter(datapath)

    def walk_bicycle_filter(self, data_dic):
        if not data_dic:
            return
        for file, data in data_dic.items():
            pulse_max = get_parameters.pulse_max(data["acc_z"])
            if pulse_max < WALK_BIKE_PULSE_MAX:
                data_dic.pop(file)
        return data_dic


