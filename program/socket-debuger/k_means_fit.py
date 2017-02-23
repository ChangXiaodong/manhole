import numpy as np
import sys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from mpl_toolkits.mplot3d import Axes3D

import filter
import time
if __name__ == '__main__':

    Filter = filter.Filter()
    data_path = "E:/Manhole/training data/original data/2-16/Data"
    # data_path = "E:/Manhole/training data/original data/2-22/"
    data = np.array(Filter.DBSCAN_filter(data_path))
    if not data.any():
        print("unavailable data")
        sys.exit(0)
    k_means_fit = KMeans(n_clusters=1, max_iter=1000).fit(data)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(data[:, 0], data[:, 1], data[:, 2], 'o', markerfacecolor='b',
            markeredgecolor='k', markersize=6)
    ax.plot(k_means_fit.cluster_centers_[:, 0], k_means_fit.cluster_centers_[:, 1], k_means_fit.cluster_centers_[:, 2],
            '*', markerfacecolor='r',
            markeredgecolor='k', markersize=14)
    ax.set_xlim([-157.4, 3349.4])
    ax.set_ylim([-144.1, 3048.1])
    ax.set_zlim([10, 2044.])
    plt.title("K-Means Center")
    plt.show()
