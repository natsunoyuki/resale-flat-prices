import numpy as np
from sklearn.metrics import r2_score


def r2(d, G, m):
    return r2_score(d, np.dot(G, m))
