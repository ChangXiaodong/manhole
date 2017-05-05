import xlrd
import csv
import os


def get_acc_data_by_excelpath(path=""):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    x = []
    y = []
    z = []
    for rows in xrange(nrows):
        x.append(table.cell(rows, 0).value)
        y.append(table.cell(rows, 1).value)
        z.append(table.cell(rows, 2).value)
    return x, y, z


def get_gyo_data_by_excelpath(path=""):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    x = []
    y = []
    z = []
    for rows in xrange(nrows):
        x.append(table.cell(rows, 3).value)
        y.append(table.cell(rows, 4).value)
        z.append(table.cell(rows, 5).value)
    return x, y, z


def get_data_by_csvpath(path=""):
    acc_x = []
    acc_y = []
    acc_z = []
    gyo_x = []
    gyo_y = []
    gyo_z = []
    acc_scale = []
    gyo_scale = []
    with open(path) as csvfile:
        # reader = csv.DictReader(csvfile)
        reader = csv.reader(csvfile)
        for row in reader:
            acc_x.append(int(row[1]))
            acc_y.append(int(row[2]))
            acc_z.append(int(row[3]))
            gyo_x.append(int(row[4]))
            gyo_y.append(int(row[5]))
            gyo_z.append(int(row[6]))
            acc_scale.append(int(row[7]))
            gyo_scale.append(int(row[8]))
    return acc_x, acc_y, acc_z, gyo_x, gyo_y, gyo_z, acc_scale, gyo_scale


def get_data_by_csvpath_8bit(path=""):
    acc_x = []
    acc_y = []
    acc_z = []
    gyo_x = []
    gyo_y = []
    gyo_z = []
    count = 0
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            acc_x.append(float(int(row[1]) + 32767) / 65535)
            acc_y.append(float(int(row[2]) + 32767) / 65535)
            acc_z.append(float(int(row[3]) + 32767) / 65535)
            gyo_x.append(float(int(row[4]) + 32767) / 65535)
            gyo_y.append(float(int(row[5]) + 32767) / 65535)
            gyo_z.append(float(int(row[6]) + 32767) / 65535)
            count += 1
            if count == 10:
                break
    middle_acc_x = sum(acc_x) / 10
    middle_acc_y = sum(acc_y) / 10
    middle_acc_z = sum(acc_z) / 10
    middle_gyo_x = sum(gyo_x) / 10
    middle_gyo_y = sum(gyo_y) / 10
    middle_gyo_z = sum(gyo_z) / 10
    acc_x = []
    acc_y = []
    acc_z = []
    gyo_x = []
    gyo_y = []
    gyo_z = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            acc_x.append(float(int(row[1]) - middle_acc_x + 32767) / 65535)
            acc_y.append(float(int(row[2]) - middle_acc_y + 32767) / 65535)
            acc_z.append(float(int(row[3]) - middle_acc_z + 32767) / 65535)
            gyo_x.append(float(int(row[4]) - middle_gyo_x + 32767) / 65535)
            gyo_y.append(float(int(row[5]) - middle_gyo_y + 32767) / 65535)
            gyo_z.append(float(int(row[6]) - middle_gyo_z + 32767) / 65535)
    return acc_x, acc_y, acc_z, gyo_x, gyo_y, gyo_z


def dir_path_check(dir_path):
    dir_path = dir_path.replace("\\", "/")
    if dir_path[-1] != "/":
        dir_path += "/"
    return dir_path


def get_file_recursive(dir_path=""):
    dir_path = dir_path_check(dir_path)
    file_list = []
    dir_list = []
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
    return file_list


def get_data_in_all_dir(dir_path=""):
    dir_path = dir_path_check(dir_path)
    file_list = get_file_recursive(dir_path)
    data_dic = {}
    for file in file_list:
        acc_x, acc_y, acc_z, gyo_x, gyo_y, gyo_z, acc_scale, gyo_scale = get_data_by_csvpath(file)
        data_dic[str(file).split("/")[-1].split(".")[0]] = {
            "acc_x": acc_x,
            "acc_y": acc_y,
            "acc_z": acc_z,
            "gyo_x": gyo_x,
            "gyo_y": gyo_y,
            "gyo_z": gyo_z,
            "acc_scale": acc_scale,
            "gyo_scale": gyo_scale
        }
    return data_dic

if __name__ == "__main__":
    print(get_data_by_csvpath("E:\Manhole\\test data\middle_fast\\2\middle_fast_2.csv"))
