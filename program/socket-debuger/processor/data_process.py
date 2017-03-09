# coding=utf-8
from processor.get_parameters import *

path = raw_input("input excel data path:")
path = path.replace("\\", "/")
acc_x, acc_y, acc_z = data_reader.get_acc_data_by_excelpath(path)
gyo_x, gyo_y, gyo_z = data_reader.get_gyo_data_by_excelpath(path)
print "peak width:{}".format(peak_width(acc_x, 1000))
print "peak value:{}".format(peak_value(acc_x))
print "mean:{}".format(mean(acc_x))
print "variance:{}".format(variance(acc_x))
print "pulse_max:{}".format(pulse_max(acc_x))
print "-------------------------------------"
print "peak width:{}".format(peak_width(gyo_x, 200))
print "peak value:{}".format(peak_value(gyo_x))
print "mean:{}".format(mean(gyo_x))
print "variance:{}".format(variance(gyo_x))
print "pulse_max:{}".format(pulse_max(gyo_x))
