# Python Code for step 5 of Final Project
# Goal = Given a Data set of n observations, create k clusters of "related" observations

from Lnorm import comp_normalized as l_norm
from findEigen import find_k_vectors
import numpy as np
import mykmeanssp as k_means
from kmeans_pp import k_means_pp


def normal_spectral_clustering(Observations):
    """
    input: Observations
    output: dictionary the holds clusters made by NSC
    """
    laplacian = l_norm(Observations)
    U, k = find_k_vectors(laplacian)
    n = U.shape[0]
    root_of_SOS = np.broadcast_to(np.sqrt(np.sum(U**2, axis=1)).reshape(n, 1), (n, k))
    T = U / root_of_SOS
    Initial_Indexes = k_means_pp(k, n, k, T)
    sent_matrix = np.copy(T).tolist()
    np.set_printoptions(suppress=True)
    list_of_args = [[float(k), float(n), float(k), float(300)], Initial_Indexes] + sent_matrix
    mapping = np.array(k_means.calkmeans(list_of_args))
    clusters_dict = {}
    for j in range(np.min([np.amax(mapping), Observations.shape[0]]) + 1):
        Indexes_of_cluster_j = np.argwhere(mapping == j)
        if len(Indexes_of_cluster_j) != 0:
            clusters_dict[j] = Indexes_of_cluster_j.flatten()
    return clusters_dict, k
