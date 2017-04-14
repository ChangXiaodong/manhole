import data_reader
import get_parameters
import csv
import time
csv_path = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
data_path = "E:/Manhole/training data/original data/extract"

data_dic = data_reader.get_data_in_all_dir(data_path)
dir_path = data_reader.get_file_recursive(data_path)

csvfile = open(data_path + csv_path + ".csv", 'ab')
filed_names = ['title', 'label',
               'start', "end", "max_index", "min_index", "acc_z_max", "acc_z_min",
               "acc_scale", "gyo_scale",
               "acc_x_var", "acc_y_var", "gyo_x_var", "gyo_y_var", "gyo_z_var",
               "speed", "heavy_vehicle", "light_vehicle"
               ]
writer = csv.DictWriter(csvfile, filed_names)
# writer.writeheader()
total = len(dir_path)
i = 0
for p in dir_path:
    i += 1
    print("process:{}/{}".format(i, total))
    title = str(p).split("/")[-1].split(".")[0]
    acc_x, acc_y, acc_z, gyo_x, gyo_y, gyo_z, acc_scale, gyo_scale = data_reader.get_data_by_csvpath(p)
    new_p = "/".join(p.split("/")[:-2]) + "/params.txt"
    with open(new_p, "r") as params_file:
        lines = params_file.readlines()
    start, end = get_parameters.get_valid_data(acc_z)
    (max_index, min_index, _) = (get_parameters.get_peak_width(acc_z, start, end))
    max_index = str(max_index)
    max_index = max_index.replace("[", "").replace("]", "")
    min_index = str(min_index)
    min_index = min_index.replace("[", "").replace("]", "")

    acc_z_max = max(acc_z)
    acc_z_min = min(acc_z)
    acc_scale = acc_scale[0]
    gyo_scale = gyo_scale[0]
    mean_value = sum(acc_x[:20]) / 20
    try:
        acc_x_var = int(get_parameters.variance(acc_x[start:end], mean_value) ** 0.5)
    except:
        print(title)
    mean_value = sum(acc_y[:20]) / 20
    acc_y_var = int(get_parameters.variance(acc_y[start:end], mean_value) ** 0.5)
    mean_value = sum(gyo_x[:20]) / 20
    gyo_x_var = int(get_parameters.variance(gyo_x[start:end], mean_value) ** 0.5)
    mean_value = sum(gyo_y[:20]) / 20
    gyo_y_var = int(get_parameters.variance(gyo_y[start:end], mean_value) ** 0.5)
    mean_value = sum(gyo_z[:20]) / 20
    gyo_z_var = int(get_parameters.variance(gyo_z[start:end], mean_value) ** 0.5)
    label = lines[0].split(":")[1]
    speed = lines[1].split(":")[1]
    heavy_vehicle = lines[2].split(":")[1]
    light_vehicle = lines[3].split(":")[1]

    writer.writerow(
        {
            "title": title, "label": int(label),
            "start": int(start), "end": int(end), "max_index": max_index, "min_index": (min_index),
            "acc_z_max": int(acc_z_max),
            "acc_z_min": int(acc_z_min),
            "acc_scale": int(acc_scale), "gyo_scale": int(gyo_scale),
            "acc_x_var": int(acc_x_var), "acc_y_var": int(acc_y_var), "gyo_x_var": int(gyo_x_var),
            "gyo_y_var": int(gyo_y_var),
            "gyo_z_var": int(gyo_z_var),
            "speed": int(speed), "heavy_vehicle": int(heavy_vehicle), "light_vehicle": int(light_vehicle)
        })
csvfile.close()

import tkMessageBox

tkMessageBox.showinfo("Finished", "Extract Finished")
