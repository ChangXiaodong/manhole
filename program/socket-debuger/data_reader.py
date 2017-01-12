import xlrd
import csv


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


if __name__ == "__main__":

    print get_data_by_csvpath("E:\Manhole\\test data\middle_fast\\2\middle_fast_2.csv")
