# Python Code for steps 6.5 and 6.6 of Final Project
# Goal = Given the clustered data, create 3 output files as requested

import matplotlib.pyplot as plt
import numpy as np
import random
from OutputText import data_output, clusters_output
from ComputeJaccard import find_jaccard


def visualize_results(observations, spectral_clusters, kmeans_clusters, original_clusters):
    """
    input: observations and 3 clusters (spectral, k-means, original)
    output: pdf file with graphs and details of clusters made by algorithm
    """
    n = observations.shape[0]
    k_algo = len(spectral_clusters.keys())
    k_original = len(original_clusters.keys())
    d = observations[0].shape[0]
    if d == 3:
        fig, axs = plt.subplots(2, 3, subplot_kw={'projection': "3d"})
    else:
        fig, axs = plt.subplots(2, 3)
    plt.tick_params(axis='both', which='major', labelsize=6)
    colors = []

    for i in spectral_clusters:
        r = random.random()
        g = random.random()
        b = random.random()
        rgb = [r, g, b]
        colors.append(rgb)
        arr = observations[spectral_clusters[i]]
        if d == 2:
            axs[0, 0].scatter(arr[:, 0], arr[:, 1], c=[rgb])
        else:
            axs[0, 0].scatter(arr[:, 0], arr[:, 1], arr[:, 2], c=[rgb])
    axs[0, 0].set_title("Normalized Spectral Clustering")
    axs[1, 0].set_axis_off()
    axs[1, 1].set_axis_off()
    axs[0, 1].set_axis_off()
    axs[1, 2].set_axis_off()
    t = 0

    for i in kmeans_clusters:
        arr = observations[kmeans_clusters[i]]
        if d == 2:
            axs[0, 2].scatter(arr[:, 0], arr[:, 1], c=[colors[t]])
        else:
            axs[0, 2].scatter(arr[:, 0], arr[:, 1], arr[:, 2], c=[colors[t]])
        t += 1
        if t == len(colors):
            r = random.random()
            g = random.random()
            b = random.random()
            rgb = [r, g, b]
            colors.append(rgb)
    axs[0, 2].set_title("K-means")

    # decisions considering size of details in graph to optimize visualization
    axs[0, 0].set_xticks(np.arange(-10, 12, 2))
    axs[0, 0].set_yticks(np.arange(-10, 12, 2))
    axs[0, 2].set_xticks(np.arange(-10, 12, 2))
    axs[0, 2].set_yticks(np.arange(-10, 12, 2))
    axs[0, 0].tick_params(axis='x', labelsize=5.5)
    axs[0, 2].tick_params(axis='x', labelsize=5.5)
    axs[0, 0].tick_params(axis='y', labelsize=5.5)
    axs[0, 2].tick_params(axis='y', labelsize=5.5)

    J_cluster = find_jaccard(spectral_clusters, original_clusters)
    J_Means = find_jaccard(kmeans_clusters, original_clusters)
    s1 = 'Data was generated from the values:'
    s2 = 'n = ' + str(n) + ' , k = ' + str(k_original)
    s3 = 'the k that was used for both algorithms was ' + str(k_algo)
    s4 = 'The Jaccard measure for Spectral Clustering: ' + str(np.around(J_cluster, 3))
    s5 = 'The Jaccard measure for K-Means: ' + str(np.around(J_Means, 3))
    if d == 3:
        # decisions considering size of details in graph to optimize visualization
        axs[0, 0].tick_params(axis='x', labelsize=4.5, labelrotation=30)
        axs[0, 2].tick_params(axis='x', labelsize=4.5, labelrotation=30)
        axs[0, 0].tick_params(axis='y', labelsize=4.5)
        axs[0, 2].tick_params(axis='y', labelsize=4.5)
        axs[0, 0].set_xticks(np.arange(-10, 10, 2.5))
        axs[0, 0].set_yticks(np.arange(-10, 10, 2.5))
        axs[0, 2].set_xticks(np.arange(-10, 10, 2.5))
        axs[0, 2].set_yticks(np.arange(-10, 10, 2.5))
        axs[0, 0].set_zticks(np.arange(-10, 10, 2.5))
        axs[0, 2].set_zticks(np.arange(-10, 10, 2.5))
        axs[0, 0].tick_params(axis='z', labelsize=4.5)
        axs[0, 2].tick_params(axis='z', labelsize=4.5)
        axs[1, 1].text(0.5, 0.5, 0.5, s=s1, ha='center', va='center', fontsize=6)
        axs[1, 1].text(0.5, 0.4, 0.3, s=s2, ha='center', va='center', fontsize=6)
        axs[1, 1].text(0.6, 0.3, 0.1, s=s3, ha='center', va='center', fontsize=6)
        axs[1, 1].text(0.6, 0.2, -0.1, s=s4, ha='center', va='center', fontsize=6)
        axs[1, 1].text(0.7, 0.1, -0.3, s=s5, ha='center', va='center', fontsize=6)
    else:
        axs[1, 1].text(0.5, 0.5, s=s1, ha='center', fontsize=9)
        axs[1, 1].text(0.5, 0.4, s=s2, ha='center', fontsize=9)
        axs[1, 1].text(0.5, 0.3, s=s3, ha='center', fontsize=9)
        axs[1, 1].text(0.5, 0.2, s=s4, ha='center', fontsize=9)
        axs[1, 1].text(0.5, 0.1, s=s5, ha='center', fontsize=9)
    fig.savefig("clusters.pdf")
    return


# function to be called from main. outputs 3 requested files
def output_all(spectral, k_means, Observations, Labels, Original):
    """
    input: clusters, observations, labels
    output: 2 text files and 1 pdf file with entire data needed
    """
    data_output(Observations, Labels)
    algo_k = len(spectral.keys())
    clusters_output(algo_k, spectral, k_means)
    visualize_results(Observations, spectral, k_means, Original)
    return
