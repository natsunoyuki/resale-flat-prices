import numpy as np


def least_squares(G, d):
    """
    Linear least squares linear inversion.
    Inputs
        G: array
        d: array
    Outputs
        m: array
    """
    m = np.dot(np.linalg.inv(np.dot(G.T, G)), G.T)
    m = np.dot(m, d)
    return m
