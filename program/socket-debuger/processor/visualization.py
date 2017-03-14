'''
Show all different interpolation methods for imshow
'''

import matplotlib.pyplot as plt
import numpy as np
import data_reader

methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
           'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
           'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

# np.random.seed(0)
# grid = [
#     [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]],
#     [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
#     [[0, 0, 1.0], [0, 0, 1.0], [0, 0, 1.0], [0, 0, 1.0], [0, 0, 1.0], [0, 0, 1.0]]
# ]
# import matplotlib.cbook as cbook
#
# image_file = cbook.get_sample_data('ada.png')
# image = plt.imread(image_file)

dir_path = "E:/Manhole/training data/original data/3-6/2/middle/1"
data_dic = data_reader.get_data_in_all_dir(dir_path, data_bit=8)
column = 1000
row_step = 1000 / len(data_dic)
row = 0

image = [
    [[0, 0, 0] for _ in range(column)] for _ in range(row_step * len(data_dic))
    ]
for filename, item in data_dic.items():
    for i in range(column):
        n = len(item["acc_x"])
        for j in range(row_step):
            if i >= n:
                image[row + j][i] = [1, 1, 1]
            else:
                image[row + j][i] = [
                    item["acc_x"][i],
                    item["acc_y"][i],
                    item["acc_z"][i]
                ]
    row += row_step
fig, axes = plt.subplots(figsize=(12, 6),
                         subplot_kw={'xticks': [], 'yticks': []})

# for ax, interp_method in zip(axes.flat, methods):
#     ax.imshow(image, interpolation=interp_method)
#     ax.set_title(interp_method)
surf = axes.imshow(image, cmap="brg")
fig.colorbar(surf, shrink=1, aspect=5)
plt.show()
