from collections import deque


class ManholeAlgorithm(object):
    def __init__(self):
        self.MAX_QUENE_LENGTH = 100
        self.acc_x = deque(maxlen=self.MAX_QUENE_LENGTH)
        self.acc_y = deque(maxlen=self.MAX_QUENE_LENGTH)
        self.acc_z = deque(maxlen=self.MAX_QUENE_LENGTH)
        self.gyo_x = deque(maxlen=self.MAX_QUENE_LENGTH)
        self.gyo_y = deque(maxlen=self.MAX_QUENE_LENGTH)
        self.gyo_z = deque(maxlen=self.MAX_QUENE_LENGTH)
        self.leans_count = 0

    def get_mean_value(self, data):
        sum = 0
        for v in data:
            sum += v
        return sum / len(data)

    def get_variance_value(self, data):
        mean_value = self.get_mean_value(data)
        sum = 0
        for v in data:
            sum += (v - mean_value) ** 2
        return sum / len(data)

    def variance_identify(self, data_dict):
        self.acc_x.append(data_dict["acc_x"])
        self.acc_y.append(data_dict["acc_y"])
        self.acc_z.append(data_dict["acc_z"])
        self.gyo_x.append(data_dict["gyo_x"])
        self.gyo_y.append(data_dict["gyo_y"])
        self.gyo_z.append(data_dict["gyo_z"])
        if abs(data_dict["acc_x"]+abs(data_dict["acc_y"]))>1000:
            self.leans_count += 1
        else:
            self.leans_count = 0
        if self.leans_count > 300:
            print "Lean"
            return 1

        settlement_activate = 0
        if self.get_variance_value(self.acc_z) > 10000:
            print "Z"
            settlement_activate += 1
        if self.get_variance_value(self.acc_x)> 10000:
            print "X"
            settlement_activate += 1
        if self.get_variance_value(self.acc_y) > 7000:
            print "Y"
            settlement_activate += 1
        if settlement_activate>2:
            print "Settlement"
            return 2
        return 0

