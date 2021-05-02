# Python Code for K-Means Clustering

import mykmeanssp as k_means
from kmeans_pp import k_means_pp
import numpy as np


# 6.3 function to cluster Observations with K-means
def k_means_clustering(Observations, algo_k):
    """
    input: Observations
    output: algo_k = number of clusters
    return: dictionary that holds the k clusters
    """
    n = Observations.shape[0]
    d = Observations.shape[1]
    Initial_Indexes = k_means_pp(algo_k, n, d, Observations)
    sent_matrix = np.copy(Observations).tolist()
    list_of_args = [[float(algo_k), float(n), float(d), float(300)], Initial_Indexes] + sent_matrix
    mapping = np.array(k_means.calkmeans(list_of_args))
    k_means_clusters = {}
    for j in range(np.min([np.amax(mapping), Observations.shape[0]]) + 1):
        Indexes_of_cluster_j = np.argwhere(mapping == j)
        if len(Indexes_of_cluster_j) != 0:
            k_means_clusters[j] = Indexes_of_cluster_j.flatten()
    return k_means_clusters
