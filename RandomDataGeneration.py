# Python Code for step 6.3 of Final Project
# Goal = Given n, k, d generate n d-dimensional points with k centers

import sklearn.datasets as skl
import numpy as np
from constants import maximumCapacity_k_2, maximumCapacity_n_2, maximumCapacity_k_3, maximumCapacity_n_3


def create_random_data(randomize, n, k):
    """
    param: randomize = boolean. whether to random n and k
    param: n = number of observations
    param: k = number of groups
    return: the generated data
    """
    d = np.random.choice([2, 3])
    if d == 3:
        maximumCapacity_n = maximumCapacity_n_2
        maximumCapacity_k = maximumCapacity_k_2
    else:
        maximumCapacity_n = maximumCapacity_n_3
        maximumCapacity_k = maximumCapacity_k_3

    if randomize:
        n = np.random.randint(maximumCapacity_n / 2, maximumCapacity_n + 1, size=1)[0]
        k = np.random.randint(maximumCapacity_k / 2, maximumCapacity_k + 1, size=1)[0]
        while n <= k:
            n = np.random.randint(maximumCapacity_n / 2, maximumCapacity_n + 1, size=1)[0]
            k = np.random.randint(maximumCapacity_k / 2, maximumCapacity_k + 1, size=1)[0]

    Observations, Cluster_Labels = skl.make_blobs(n_samples=n, centers=k, n_features=d)

    # create dictionary that holds the original clustering
    Original_Clusters = {}
    for i in range(len(Cluster_Labels)):
        if Cluster_Labels[i] in Original_Clusters:
            Original_Clusters[Cluster_Labels[i]] += [i]
        else:
            Original_Clusters[Cluster_Labels[i]] = [i]
    for i in Original_Clusters:
        Original_Clusters[i] = np.array(Original_Clusters[i])
    return Observations, Cluster_Labels, Original_Clusters
