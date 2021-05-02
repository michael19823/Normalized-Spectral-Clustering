# Main module to run the code with one run_code function

from RandomDataGeneration import create_random_data
from SpectralClustering import normal_spectral_clustering
from k_means_clustering import k_means_clustering
from Output import output_all
from OutputText import start_print
import time


# function to run entire code
def run_code(k, n, rand):
    """
    param: k = number of groups
    param: n = number of points
    param: rand = boolean of whether to use k and n or to randomize
    output: 3 files with data and clustering
    """
    if rand:
        Observations, Labels, Original = create_random_data(True, n, k)
        k = 0
        start_print()
    else:
        if k <= 0 or n <= 0:
            print("k and n must be positive integers")
            return
        if k >= n:
            print("n must be bigger than k")
            return
        start_print()
        Observations, Labels, Original = create_random_data(False, n, k)
    spectral_clusters, algo_k = normal_spectral_clustering(Observations)
    k_means_clusters = k_means_clustering(Observations, algo_k)
    output_all(spectral_clusters, k_means_clusters, Observations, Labels, Original)
    return