import numpy as np
import data_reader
import get_parameters
from global_parameters import *
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

def DBSCAN_filter(data_path):
    data_dic = data_reader.get_data_in_all_dir(data_path)
    X = []
    for file, data in data_dic.items():
        X.append(get_parameters.peak_value_divide_by_width(data))
    X = np.array(X)
    db = DBSCAN(eps=DBSCAN_eps, min_samples=DBSCAN_min_samples, n_jobs=-1).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    filted_X = []
    for i in db.core_sample_indices_:
        filted_X.append(list(X[i]))
    return filted_X

if __name__ == "__main__":
    # centers = [[1, 1], [-1, -1], [1, -1]]
    # X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
    #                             random_state=0)
    # X = StandardScaler().fit_transform(X)

    data_path = "E:/Manhole/training data/original data/2-16/Data"
    # data_path = "E:/Manhole/training data/original data/2-22/manhole1"
    # data_path = "E:/Manhole/training data/original data/2-22/manhole2"
    # data_path = "E:/Manhole/training data/lebeled data/"
    data_dic = data_reader.get_data_in_all_dir(data_path)
    X = []
    for file, data in data_dic.items():
        X.append(get_parameters.peak_value_divide_by_width(data))
    X = np.array(X)
    db = DBSCAN(eps=DBSCAN_eps, min_samples=DBSCAN_min_samples, n_jobs=-1).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    filted_X = []
    for i in db.core_sample_indices_:
        filted_X.append(X[i])
    filted_X = np.array(filted_X)
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    # print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    # print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    # print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    # print("Adjusted Rand Index: %0.3f"
    #       % metrics.adjusted_rand_score(labels_true, labels))
    # print("Adjusted Mutual Information: %0.3f"
    #       % metrics.adjusted_mutual_info_score(labels_true, labels))
    # print("Silhouette Coefficient: %0.3f"
    #       % metrics.silhouette_score(X, labels))

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)
        xy = X[class_member_mask & core_samples_mask]
        ax.plot(xy[:, 0], xy[:, 1], xy[:, 2], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=6)

        xy = X[class_member_mask & ~core_samples_mask]
        ax.plot(xy[:, 0], xy[:, 1], xy[:, 2], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=6)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    zlim = ax.get_zlim()
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    plt.title('Effective Data:{:.2f}%'.format(float(len(filted_X))/float(len(X))*100))
    print("original length:{}, filtered length:{}".format(len(X), len(filted_X)))
    ax.plot(filted_X[:, 0], filted_X[:, 1], filted_X[:, 2], 'o', markerfacecolor='r',
            markeredgecolor='k')

    # ax.set_xlim(xlim)
    # ax.set_ylim(ylim)
    # ax.set_zlim(zlim)

    plt.show()
