import DBSCAN


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
