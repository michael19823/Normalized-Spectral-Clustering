# Python Code for steps 6.5 and 6.6 of Final Project
# Goal = Given the clustered data, create 3 output files as requested

import numpy as np
from constants import *


# the print on start of the code
def start_print():
    print("max capacities for d=2: k = {k} and n = {n}".format(k=maximumCapacity_k_2, n=maximumCapacity_n_2))
    print("max capacities for d=3: k = {k} and n = {n}".format(k=maximumCapacity_k_3, n=maximumCapacity_n_3))
    return


# function to create text file with Observations and labels
def data_output(Observations, labels):
    Obs = np.concatenate((Observations, labels.reshape(labels.shape[0], 1)), axis=1)
    data_file = open('data.txt', 'w')
    for line in Obs:
        for index in range(line.shape[0]):
            if index < line.shape[0] - 1:
                number = np.around(line[index], 8)
                data_file.write(number.astype(str))
                data_file.write(',')
            else:
                number = int(line[index])
                data_file.write(str(number))
                data_file.write('\n')
    data_file.close()
    return


# function to create text file with clusters made by algorithm
def clusters_output(k, spectral_clusters, kmeans_clusters):
    clusters_file = open('clusters.txt', 'w')
    clusters_file.write(str(k))
    clusters_file.write('\n')
    for key in spectral_clusters:
        cur = np.array(spectral_clusters[key])
        for index in range(cur.shape[0]):
            clusters_file.write(str(cur[index]))
            if index < cur.shape[0] - 1:
                clusters_file.write(',')
            else:
                clusters_file.write('\n')
    for key in kmeans_clusters:
        cur = np.array(kmeans_clusters[key])
        for index in range(cur.shape[0]):
            clusters_file.write(str(cur[index]))
            if index < cur.shape[0] - 1:
                clusters_file.write(',')
            else:
                clusters_file.write('\n')
    clusters_file.close()
    return
