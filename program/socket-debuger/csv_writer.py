# coding=utf-8
import csv
import os
import time


def write(data, path="test_csv"):
    if os.path.exists("./data/") != True:
        os.makedirs("./data/")
    os.makedirs("./data/" + path)

    csv_path = "./data/" + path + "/" + path + ".csv"
    with open(csv_path, 'wb') as csvfile:
        filed_names = ['time', 'acc_x', 'acc_y', 'acc_z', "gyo_x", "gyo_y", "gyo_z"]
        writer = csv.DictWriter(csvfile, filed_names)
        writer.writeheader()
        for i in xrange(len(data["time"])):
            writer.writerow(
                {
                    "time": data['time'][i],
                    "acc_x": data["acc_x"][i], "acc_y": data["acc_y"][i], "acc_z": data["acc_z"][i],
                    "gyo_x": data["gyo_x"][i], "gyo_y": data["gyo_y"][i], "gyo_z": data["gyo_z"][i]
                })


if __name__ == "__main__":
    write([])