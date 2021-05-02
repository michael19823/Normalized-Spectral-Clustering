# Python code for step 3 of Final Project
# Goal: create a matrix of full rank from the generated observations

import numpy as np


# computes Lnorm from a given observations 2darray
def comp_normalized(observations):
    a = dist_matrix(observations)
    b = diag_mat(a)
    c = l_norm(a, b)
    return c


def compute_distance(a, a1, a2):
    mat = 2*np.matmul(a, a.transpose())
    return -mat+a1+a2


# compute w from a given observations 2darray, using linear algebra attributes for efficiency
def dist_matrix(obs):
    d = obs.shape[0]
    a = np.power(obs, 2)
    b = np.sum(a, 1).reshape(d, 1)
    c = compute_distance(obs, b, b.transpose())
    c[np.diag_indices_from(c)] = 0
    ret = np.e ** (-((np.sqrt(c)) / 2))
    to_ret = np.asarray(ret)
    to_ret[np.diag_indices_from(to_ret)] = 0
    return to_ret


# computes d from given w
def diag_mat(a):
    sum_arr = np.asarray(np.sum(a, axis=0))
    sum_arr = np.power(sum_arr, (-0.5))
    b = np.asarray(np.diag(sum_arr))
    return b


# computes l_norm from given w, d
def l_norm(w, d):
    n = len(d)
    id_mat = np.identity(n)
    to_ret = id_mat - np.dot(np.dot(d, w), d)
    return to_ret
