# Python Code for steps 6.6 of Final Project
# Goal = Given Clusters of Spectral Clustering and K-Means, find Jaccard measure

from math import *
import numpy as np


# function to count pairs from all clusters, for calculation A ∪ B
def count_pairs(clusters):
    """
    input: clusters: dictionary, each key is a cluster
    output: sum of pairs from all clusters taken separately
    """
    pairs = 0
    for i in clusters:
        n = len(clusters[i])
        if n > 1:
            denominator = 2*np.math.factorial(n-2)
            pairs += np.math.factorial(n) / denominator

            # numbers of pairs is given by mathematical combination formula
    return int(pairs)


# function to count intersected pairs from two cluster arrays, for calculation A ∩ B
def count_mutual_pairs(clusters_a, clusters_b):
    """
    input: clusters_a,clusters_b:
    output: sum of intersected pairs
    """
    couples_a = set([])
    couples_b = set([])
    for i in clusters_a:
        for j in range(len(clusters_a[i])):
            for k in range(j + 1, len(clusters_a[i])):
                couple = np.sort((clusters_a[i][j], clusters_a[i][k]))
                couples_a.add(tuple(couple.tolist()))

                # create new array which holds a
                # tuple for i j if i and j are in the same cluster

    for i in clusters_b:
        for j in range(len(clusters_b[i])):
            for k in range(j + 1, len(clusters_b[i])):
                couple = np.sort((clusters_b[i][j], clusters_b[i][k]))
                couples_b.add(tuple(couple.tolist()))

                # create new array which holds a
                # tuple for i j if i and j are in the same cluster

    return len(couples_a & couples_b)


# function to calculate jaccard measure using the above methods
def find_jaccard(clusters, original_clusters):
    """
    input: clusters, original_clusters:
    output: jaccard measure for resemblance of clusters to the original
    """
    mutual_pairs = count_mutual_pairs(clusters, original_clusters)
    spectral_pairs = count_pairs(clusters)
    original_pairs = count_pairs(original_clusters)
    return mutual_pairs / (spectral_pairs + original_pairs - mutual_pairs)
