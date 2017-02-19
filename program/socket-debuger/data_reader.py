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
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            acc_x.append(int(row["acc_x"]))
            acc_y.append(int(row["acc_y"]))
            acc_z.append(int(row["acc_z"]))
            gyo_x.append(int(row["gyo_x"]))
            gyo_y.append(int(row["gyo_y"]))
            gyo_z.append(int(row["gyo_z"]))
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
        acc_x, acc_y, acc_z, gyo_x, gyo_y, gyo_z = get_data_by_csvpath(file)
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

    print(get_data_by_csvpath("E:\Manhole\\test data\middle_fast\\2\middle_fast_2.csv"))
