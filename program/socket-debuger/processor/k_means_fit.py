import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

import filter_function

if __name__ == '__main__':

    Filter = filter_function.Filter()
    # data_path = "E:/Manhole/training data/original data/2-16/Data"
    # data_path = "E:/Manhole/training data/original data/2-22/"
    # data_path = "E:/Manhole/training data/original data/2-24"
    # data_path = "E:/Manhole/training data/original data/2-28/"
    data_path = "..//training data/scale/good/"
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
    plt.title("K-Means Center")
    plt.show()
