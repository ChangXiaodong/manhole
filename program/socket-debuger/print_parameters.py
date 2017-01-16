import get_parameters
import data_reader
import os
import plot_3d


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
    data_dic = get_data_in_all_dir("E:/Manhole/test data/1-13/")

    acc_x_peak_width = []
    acc_x_peak_value = []
    acc_x_pulse_max = []
    acc_y_peak_width = []
    acc_y_peak_value = []
    acc_y_pulse_max = []
    acc_z_peak_width = []
    acc_z_peak_value = []
    acc_z_pulse_max = []

    gyo_x_peak_width = []
    gyo_x_peak_value = []
    gyo_x_pulse_max = []
    gyo_y_peak_width = []
    gyo_y_peak_value = []
    gyo_y_pulse_max = []
    gyo_z_peak_width = []
    gyo_z_peak_value = []
    gyo_z_pulse_max = []

    for filename, data in data_dic.items():
        print "file name                     peak width  peak value   pulse max"
        acc_x_peak_width.append(get_parameters.peak_width(data["acc_x"], 1000))
        acc_x_peak_value.append(get_parameters.peak_value(data["acc_x"]))
        acc_x_pulse_max.append(get_parameters.pulse_max(data["acc_x"]))
        print "{}  acc_x->     {}        {}       {}".format(
            filename,
            acc_x_peak_width[-1],
            acc_x_peak_value[-1],
            acc_x_pulse_max[-1]
        )
        acc_y_peak_width.append(get_parameters.peak_width(data["acc_y"], 1000))
        acc_y_peak_value.append(get_parameters.peak_value(data["acc_y"]))
        acc_y_pulse_max.append(get_parameters.pulse_max(data["acc_y"]))
        print "{}  acc_y->     {}        {}       {}".format(
            filename,
            acc_y_peak_width[-1],
            acc_y_peak_value[-1],
            acc_y_pulse_max[-1]
        )
        acc_z_peak_width.append(get_parameters.peak_width(data["acc_z"], 1000))
        acc_z_peak_value.append(get_parameters.peak_value(data["acc_z"]))
        acc_z_pulse_max.append(get_parameters.pulse_max(data["acc_z"]))
        print "{}  acc_z->     {}        {}       {}".format(
            filename,
            acc_z_peak_width[-1],
            acc_z_peak_value[-1],
            acc_z_pulse_max[-1]
        )

        gyo_x_peak_width.append(get_parameters.peak_width(data["gyo_x"], 1000))
        gyo_x_peak_value.append(get_parameters.peak_value(data["gyo_x"]))
        gyo_x_pulse_max.append(get_parameters.pulse_max(data["gyo_x"]))
        print "{}  gyo_x->     {}        {}       {}".format(
            filename,
            gyo_x_peak_width[-1],
            gyo_x_peak_value[-1],
            gyo_x_pulse_max[-1]
        )
        gyo_y_peak_width.append(get_parameters.peak_width(data["gyo_y"], 1000))
        gyo_y_peak_value.append(get_parameters.peak_value(   data["gyo_y"]))
        gyo_y_pulse_max.append(get_parameters.pulse_max(data["gyo_y"]))
        print "{}  gyo_y->     {}        {}       {}".format(
            filename,
            gyo_y_peak_width[-1],
            gyo_y_peak_value[-1],
            gyo_y_pulse_max[-1]
        )
        gyo_z_peak_width.append(get_parameters.peak_width(data["gyo_z"], 1000))
        gyo_z_peak_value.append(get_parameters.peak_value(data["gyo_z"]))
        gyo_z_pulse_max.append(get_parameters.pulse_max(data["gyo_z"]))
        print "{}  gyo_z->     {}        {}       {}".format(
            filename,
            gyo_z_peak_width[-1],
            gyo_z_peak_value[-1],
            gyo_z_pulse_max[-1]
        )
    plot_3d.plot_3d(acc_x_peak_value, acc_y_peak_value, acc_z_peak_value)
    plot_3d.plot_3d(acc_x_pulse_max, acc_y_pulse_max, acc_z_pulse_max, color='r', marker='*')
    plot_3d.plot_3d(acc_x_peak_width, acc_y_peak_width, acc_z_peak_width, color='y',marker='+')

    plot_3d.plot_3d(gyo_x_peak_value, gyo_y_peak_value, gyo_z_peak_value)
    plot_3d.plot_3d(gyo_x_pulse_max, gyo_y_pulse_max, gyo_z_pulse_max, color='r', marker='*')
    plot_3d.plot_3d(gyo_x_peak_width, gyo_y_peak_width, gyo_z_peak_width, color='y', marker='+')

