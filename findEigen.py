# Python Code for step 4 of Final Project
# Goal a = finding the number k of clusters, using eigen values
# Goal b = determining the k eigen vectors for the normalized spectral clustering

import numpy as np
from constants import epsilon


# 4.1 The Modified Gram-Schmidt Algorithm
def gram_schmidt(A_matrix):
    """
    input: A_matrix: matrix with NxN dimensions
    output: matrices Q,R which holds (Q^T)Q = I and QR = I
    """
    n = A_matrix.shape[0]                 # Define n as the number of rows in A_matrix
    U = np.copy(A_matrix).astype(np.float32)   # deep copy so that original matrix isn't impaired
    U = U
    R = np.zeros((n, n), dtype=np.float32)                   # Initialize R to matrix of zeros
    Q = np.zeros((n, n), dtype=np.float32)                   # Initialize Q to matrix of zeros
    for i in range(n):
        R[i][i] = np.linalg.norm(U[:, [i]])
        if R[i][i] != 0:
            Q[:, [i]] = np.divide(U[:, [i]], R[i][i])
        else:
            Q[:, [i]] = 0
        if i < n:
            R[[i], i+1:] = np.matmul(np.transpose(Q[:, [i]]), U[:, i+1:])
            # Simultaneously compute all scalars of row i in R.
            # row i consists of n-i values which are
            # computed using np.matmul which multiplies
            # the transposed i'th column of Q by each column of U independently
            # specifically columns i+1 to n of U.
            # since dimensions of column and row are (1xn) and (nx1)
            # product of each multiplication is a scalar, so we get n-i scalars.

            U[:, i+1:] = np.subtract(U[:, i+1:], np.multiply((R[[i], i+1:]), Q[:, [i]]))
            # np.multiply multiplies dimensions (1xn) (nx1) element-wise so that
            # column i of Q is multiplied once by each scalar of R[i] and the product is
            # nxn matrix which comes from n multiplications of n values each
    return Q, R


# 4.2 The QR Iteration Algorithm
def qr_iteration(A_matrix):
    """
    input:  A_matrix
    output: matrix A_hat which holds approximation for eigen values of A_matrix
            matrix Q_hat which holds approximation for eigen vectors of A_matrix
    """
    A_hat = np.copy(A_matrix)
    Q_hat = np.eye(A_matrix.shape[0], dtype='float32')
    for i in range(A_matrix.shape[0]):
        Q, R = gram_schmidt(A_hat)
        A_hat = np.dot(R, Q)
        Q_multi = np.dot(Q_hat, Q)
        Distance = np.abs(np.subtract(np.abs(Q_hat), np.abs(Q_multi)))
        if np.all(Distance < epsilon):
            return A_hat, Q_hat
        Q_hat = Q_multi
    return A_hat, Q_hat


# 4.3 The Eigen-gap Heuristic
def eigen_gap(A_hat, Q_hat):
    """
    input:  eigen values matrix A_hat
            eigen vectors matrix Q_hat
    output: matrix with chosen vectors for clustering as columns
            k value for number of clusters
    """
    eigen_values = np.array(A_hat[np.diag_indices_from(A_hat)])
    sorted_indexes = np.argsort(eigen_values)
    sorted_vals = eigen_values[sorted_indexes]
    n = eigen_values.shape[0]
    sorted_vectors = np.transpose(Q_hat)[sorted_indexes]
    k = np.argmax(np.abs(sorted_vals[0:int(n/2)] - sorted_vals[1:int(n/2+1)])) + 1
    chosen_vectors = sorted_vectors[:k, :]
    return np.transpose(chosen_vectors), k


# A simple function to glue the whole module
def find_k_vectors(A_matrix):
    A_hat, Q_hat = qr_iteration(A_matrix)
    eigen_vectors, k = eigen_gap(A_hat, Q_hat)
    return eigen_vectors, k
