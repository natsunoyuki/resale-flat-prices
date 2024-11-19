# This class represents the processed, geocoded and merged resale flat data, ready for analyses.
import pandas as pd
import geopandas

# Local imports.
from resale_flat_prices.h3_utils.h3_utils import latlon_to_h3, h3_to_geometry


class ResaleFlatData:
    def __init__(self, file_name):
        self.file_name = file_name
        self.df = pd.DataFrame()

    def read_csv(self, file_name = None):
        if file_name is None:
            file_name = self.file_name
        self.df = pd.read_csv(file_name)

    def make_h3_geometries(self, resolution = 8, crs = "EPSG:4326"):
        """Processes the latitudes and longitudes to H3 cell geometries as a GeoDataFrame."""
        df = geopandas.GeoDataFrame(self.df)
        df = latlon_to_h3(df, resolution)
        df = h3_to_geometry(df, crs)
        self.df = df

    def get_df(self):
        return self.df.copy()