import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import data_reader
import platform

if "Windows" in platform.platform():
    data_path = "E:/Manhole/training data/original data/3-15/10"
else:
    data_path = "/Users/xiaoxiami/Manhole/training data/original data/3-6/"
data_dic = data_reader.get_data_in_all_dir(data_path)

fig = {}
ax = {}
for title, value in data_dic.items():
    fig[title] = plt.figure(figsize=(12, 5))
    ax["acc-" + title] = fig[title].add_subplot(121, projection='3d')
    ax["acc-" + title].set_title("acc: " + title)
    ax["acc-" + title].plot(value['acc_x'], value['acc_y'], value['acc_z'])

    ax["gyo-" + title] = fig[title].add_subplot(122, projection='3d')
    ax["gyo-" + title].set_title("gyo: " + title)
    ax["gyo-" + title].plot(value['gyo_x'], value['gyo_y'], value['gyo_z'])

plt.tight_layout()
plt.show()
