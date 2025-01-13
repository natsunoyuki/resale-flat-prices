# This class represents the processed, geocoded and merged rent flat data, ready for analyses.
import pandas as pd
import geopandas

# Local imports.
from resale_flat_prices.h3_utils.h3_utils import latlon_to_h3, h3_to_geometry


COLUMNS = [
    'year', 'month', 'year_month', "datetime",
    'town', 'town_cleaned', 'block', 'street_name', 'street_name_cleaned', 'address',
    'flat_type', 'flat_type_num', 
    'latitude', 'longitude',
    'monthly_rent',
]


class RentPricesData:
    def __init__(self, file_name, wanted_columns = "default"):
        self.file_name = file_name
        self.df = geopandas.GeoDataFrame()

        if wanted_columns == "default":
            self.wanted_columns = COLUMNS
        else:
            self.wanted_columns = wanted_columns

    def read_csv(self, file_name = None):
        if file_name is None:
            file_name = self.file_name
        self.df = pd.read_csv(file_name)
        self.df = geopandas.GeoDataFrame(self.df)
        
        if self.wanted_columns is not None:
            self.df = self.df[self.wanted_columns]

    def make_h3_geometries(self, resolution = 8, crs = "EPSG:4326"):
        """Processes the latitudes and longitudes to H3 cell geometries as a GeoDataFrame."""
        if not isinstance(self.df, geopandas.GeoDataFrame):
            df = geopandas.GeoDataFrame(self.df)
        else:
            df = self.df.copy()
        df = latlon_to_h3(df, resolution)
        df = h3_to_geometry(df, crs)
        self.df = df

    def make_point_geometries(self, crs = "EPSG:4326"):
        """Processes the latitudes and longitudes to point geometries as a GeoDataFrame."""
        if not isinstance(self.df, geopandas.GeoDataFrame):
            df = geopandas.GeoDataFrame(self.df)
        else:
            df = self.df.copy()
        geometry = geopandas.points_from_xy(df["longitude"], df["latitude"], crs = crs)
        df = df.set_geometry(geometry)
        self.df = df.copy()

    def get_df(self):
        return self.df.copy()
