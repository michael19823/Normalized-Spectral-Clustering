# Python code for HW.2 - K-Means++

import numpy as np


# function K-Means-pp
def k_means_pp(k, n, v_size, data_matrix):
    """
    param: k = number of clusters
    param: n = number of vectors in data
    param: v_size = size of a single vector
    param: data_matrix = matrix of vectors to cluster
    return: the k initial vectors to use
    """
    np.random.seed(0)
    centroids = np.zeros((k, v_size))
    centroid_indexes = []
    dists = np.zeros((1, n))
    for j in range(0, k):
        if j > 1:
            dist_from_last = np.power((data_matrix - centroids[j-1]), 2).sum(axis=1)
            dists = np.minimum(dists, dist_from_last)
            probabilities = np.array(dists / sum(dists))
            chosen_index = np.random.choice(n, p=probabilities.tolist())
        if j == 1:
            dists = np.power((data_matrix - centroids[j - 1]), 2).sum(axis=1)
            probabilities = np.array(dists / sum(dists))
            chosen_index = np.random.choice(n, p=probabilities.tolist())
        if j == 0:
            chosen_index = np.random.choice(n)
        new_u = data_matrix[chosen_index]
        centroids[j] = new_u
        centroid_indexes.append(float(chosen_index))
    return centroid_indexes
