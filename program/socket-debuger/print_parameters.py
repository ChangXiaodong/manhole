import get_parameters
import data_reader
import os


def get_data_in_all_dir(dir_path=""):
    dir_path = dir_path.replace("\\", "/")
    dir_list = []
    file_list = []
    if dir_path[-1] != "/":
        dir_path += "/"

    dir_list.append(dir_path)
    while dir_list:
        current_dir = dir_list.pop()
        for fileordir in os.listdir(current_dir):
            temp_path = current_dir + fileordir
            if os.path.isdir(temp_path):
                if temp_path[-1] != "/":
                    temp_path += "/"
                dir_list.append(temp_path)
            elif temp_path.endswith(".csv"):
                file_list.append(temp_path)

    data_dic = {}
    for file in file_list:
        acc_x, acc_y, acc_z, gyo_x, gyo_y, gyo_z = data_reader.get_data_by_csvpath(file)
        data_dic[str(file).split("/")[-1].split(".")[0]] = {
            "acc_x": acc_x,
            "acc_y": acc_y,
            "acc_z": acc_z,
            "gyo_x": gyo_x,
            "gyo_y": gyo_y,
            "gyo_z": gyo_z
        }
    return data_dic


if __name__ == "__main__":
    data_dic = get_data_in_all_dir("E:/Manhole/test data/1-13")
    for filename, data in data_dic.items():
        print "{}->peak width:{} peak value:{} pulse max:{}".format(
            filename,
            get_parameters.peak_width(data[0],1000),
            get_parameters.peak_value(data[0]),
            get_parameters.pulse_max(data[0])
        )
