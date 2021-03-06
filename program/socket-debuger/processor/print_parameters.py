import data_reader
from collector import plot_3d
from processor import get_parameters

if __name__ == "__main__":
    # data_path = "E:/Manhole/training data/original data/2-16/Data"
    # data_path = "E:/Manhole/training data/original data/2-22/manhole1"
    # data_path = "E:/Manhole/test data/special vehicle/walk"
    # data_path = "E:/Manhole/training data/plot"
    # data_path = "E:/Manhole/training data/original data/2-28/Data1"
    # data_path = "E:/Manhole/training data/scale/good/"
    data_path = "E:/Manhole/training data/plot"
    data_dic = data_reader.get_data_in_all_dir(data_path)
    acc_x_peak_value = []
    acc_x_pulse_max = []
    acc_y_peak_value = []
    acc_y_pulse_max = []
    acc_z_peak_value = []
    acc_z_pulse_max = []

    gyo_x_peak_value = []
    gyo_x_pulse_max = []
    gyo_y_peak_value = []
    gyo_y_pulse_max = []
    peak_width = []
    gyo_z_peak_value = []
    gyo_z_pulse_max = []
    filename_dic = {}
    filename_data_base = {}
    acc_x_peak_value_divide_by_gyo_peak_width = []
    acc_y_peak_value_divide_by_gyo_peak_width = []
    acc_z_peak_value_divide_by_gyo_peak_width = []

    for filename, data in data_dic.items():
        width = get_parameters.peak_width(data)

        acc_x_peak_value.append(get_parameters.peak_value(data["acc_x"]))
        acc_x_pulse_max.append(get_parameters.pulse_max(data["acc_x"]))

        acc_y_peak_value.append(get_parameters.peak_value(data["acc_y"]))
        acc_y_pulse_max.append(get_parameters.pulse_max(data["acc_y"]))

        acc_z_peak_value.append(get_parameters.peak_value(data["acc_z"]))
        acc_z_pulse_max.append(get_parameters.pulse_max(data["acc_z"]))

        gyo_x_peak_value.append(get_parameters.peak_value(data["gyo_x"]))
        gyo_x_pulse_max.append(get_parameters.pulse_max(data["gyo_x"]))

        gyo_y_peak_value.append(get_parameters.peak_value(data["gyo_y"]))
        gyo_y_pulse_max.append(get_parameters.pulse_max(data["gyo_y"]))

        gyo_z_peak_value.append(get_parameters.peak_value(data["gyo_z"]))
        gyo_z_pulse_max.append(get_parameters.pulse_max(data["gyo_z"]))

        acc_x_peak_value_divide_by_gyo_peak_width.append(acc_x_peak_value[-1] * width)
        acc_y_peak_value_divide_by_gyo_peak_width.append(acc_y_peak_value[-1] * width)
        acc_z_peak_value_divide_by_gyo_peak_width.append(acc_z_peak_value[-1] * width)
        name = "{}{}{}".format(gyo_x_peak_value[-1], gyo_y_peak_value[-1], gyo_z_peak_value[-1])
        filename_dic[name] = filename
        name = "{}{}{}".format(gyo_x_pulse_max[-1], gyo_y_pulse_max[-1], gyo_z_pulse_max[-1])
        filename_dic[name] = filename

        filename_dic[name] = filename
        name = "{}{}{}".format(acc_x_peak_value[-1], acc_y_peak_value[-1], acc_z_peak_value[-1])
        filename_dic[name] = filename
        name = "{}{}{}".format(acc_x_pulse_max[-1], acc_y_pulse_max[-1], acc_z_pulse_max[-1])
        filename_dic[name] = filename
        name = "{}{}{}".format(acc_x_peak_value_divide_by_gyo_peak_width[-1],
                               acc_y_peak_value_divide_by_gyo_peak_width[-1],
                               acc_z_peak_value_divide_by_gyo_peak_width[-1])
        filename_dic[name] = filename

        filename_data_base["{}_acc_peak_value".format(filename)] = [acc_x_peak_value[-1], acc_y_peak_value[-1],
                                                                    acc_z_peak_value[-1]]
        filename_data_base["{}_acc_pulse_max".format(filename)] = [acc_x_pulse_max[-1], acc_y_pulse_max[-1],
                                                                   acc_z_pulse_max[-1]]
        filename_data_base["{}_gyo_peak_value".format(filename)] = [gyo_x_peak_value[-1], gyo_y_peak_value[-1],
                                                                    gyo_z_peak_value[-1]]
        filename_data_base["{}_gyo_pulse_max".format(filename)] = [gyo_x_pulse_max[-1], gyo_y_pulse_max[-1],
                                                                   gyo_z_pulse_max[-1]]

        filename_data_base["{}_acc_peak_value_divide_by_gyo_peak_width".format(filename)] = [
            acc_x_peak_value_divide_by_gyo_peak_width[-1],
            acc_y_peak_value_divide_by_gyo_peak_width[-1],
            acc_z_peak_value_divide_by_gyo_peak_width[-1]
        ]
        filename_data_base["{}_width".format(filename)] = width
    plot_browser = plot_3d.PlotTools(filename_data_base)
    plot_browser.plot_3d_browser(acc_x_peak_value, acc_y_peak_value, acc_z_peak_value, filename_dic, "ACC Peak Value")
    plot_browser.plot_3d_browser(acc_x_pulse_max, acc_y_pulse_max, acc_z_pulse_max, filename_dic, "ACC Pulse Max",
                                 color='r',
                                 marker='*')

    plot_browser.plot_3d_browser(gyo_x_peak_value, gyo_y_peak_value, gyo_z_peak_value, filename_dic, "GYO Peak Value")
    plot_browser.plot_3d_browser(gyo_x_pulse_max, gyo_y_pulse_max, gyo_z_pulse_max, filename_dic, "GYO Pulse Max",
                                 color='r',
                                 marker='*')

    plot_browser.plot_3d_browser(acc_x_peak_value_divide_by_gyo_peak_width,
                                 acc_y_peak_value_divide_by_gyo_peak_width,
                                 acc_z_peak_value_divide_by_gyo_peak_width, filename_dic,
                                 "ACC Peak Value/Width",
                                 color='g', marker='o')
    plot_browser.plot_show()
