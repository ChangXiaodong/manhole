# coding=utf-8
'''
保存csv的格式
'title', 'label','start', "end", "max_index", "min_index", "acc_z_max", "acc_z_min","acc_scale", "gyo_scale","acc_x_var", "acc_y_var", "gyo_x_var", "gyo_y_var", "gyo_z_var","speed", "heavy_vehicle", "light_vehicle"
'''
import csv

csv_path = ""
with open(csv_path) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        pass
