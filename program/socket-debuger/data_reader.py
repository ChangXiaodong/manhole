import xlrd


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

if __name__ == "__main__":
    print get_acc_data_by_excelpath("E:/Manhole/test data/middle_slow/2/data.xlsx")[0]