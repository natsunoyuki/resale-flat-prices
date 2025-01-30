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


def minimum_length(G, d):
    """
    Minimum length solution to the underdetermined least squares problem.
    Inputs
        G: array
        d: array
    Outputs
        m: array
    """
    m = np.dot(G.T, np.linalg.inv(np.dot(G, G.T)))
    m = np.dot(m, d)
    return m