import numpy as np

# Local imports.
from property_prices.linear_inversion.least_squares import least_squares, minimum_length
from property_prices.linear_inversion.l1_norm_inversion import l1_norm_inversion


class LinearInversion:
    def __init__(self, error_type = "l2", vander_order = 2):
        self.model = None
        
        self.error_type = error_type.lower()
        if self.error_type == "l2":
            self.model = least_squares
        elif self.error_type == "l1":
            self.model = l1_norm_inversion
        
        self.m = None
        self.vander_order = vander_order


    def fit(self, X, y, sd = None, vander_order = None):
        assert self.model is not None

        self.m = None
        G = self.make_data_kernel(X, vander_order)
        
        try:
            if self.error_type == "l2":
                self.m = self.model(G, y)
            elif self.error_type == "l1":
                self.m = self.model(G, y, sd)
        except np.linalg.LinAlgError:
            self.m = minimum_length(G, y)

        return self.m


    def predict(self, X, vander_order = None):
        assert self.m is not None

        G = self.make_data_kernel(X, vander_order)
        return np.dot(G, self.m.reshape(-1, 1))


    def make_data_kernel(self, X, vander_order = None):
        if vander_order is None:
            vander_order = self.vander_order

        if len(X.shape) > 1:
            if X.shape[1] == 1:
                X = X.reshape(-1)

        return np.vander(X, vander_order)
