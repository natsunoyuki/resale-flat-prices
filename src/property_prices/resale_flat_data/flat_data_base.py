# Base class for both resale flat prices and rent prices data.
import pandas as pd
import geopandas
import numpy as np


# Local imports.
from property_prices.h3_utils.h3_utils import point_to_h3, h3_to_geometry


class FlatDataBase:
    def __init__(self, file_name, wanted_columns = None):
        self.file_name = file_name
        self.df = geopandas.GeoDataFrame()
        self.wanted_columns = wanted_columns


    def read_parquet(self, file_name = None):
        """Reads the resale flat prices data from a parquet file."""
        if file_name is None:
            file_name = self.file_name

        self.df = geopandas.read_parquet(file_name)
        self.set_wanted_columns()
        self.format_datetime()


    def read_json(self, file_name = None):
        """Reads the resale flat prices data from a geojson file."""
        if file_name is None:
            file_name = self.file_name

        self.df = geopandas.read_file(file_name)
        self.set_wanted_columns()
        self.format_datetime()


    def read_csv(self, file_name = None):
        """Reads the resale flat prices data from a CSV file."""
        if file_name is None:
            file_name = self.file_name
            
        self.df = pd.read_csv(file_name)
        self.df = geopandas.GeoDataFrame(self.df)
        self.set_wanted_columns()
        self.format_datetime()


    def set_wanted_columns(self, wanted_columns = None):
        if wanted_columns is None:
            wanted_columns = self.wanted_columns

        if wanted_columns is not None:
            self.df = self.df[wanted_columns]


    def format_datetime(self, format = 'datetime64[M]'):
        if "datetime" in self.df.columns:
            self.df["datetime"] = self.df["datetime"].apply(lambda x: np.datetime64(x).astype(format))


    def make_h3_geometries(self, resolution = 8, crs = "EPSG:4326"):
        """Processes the latitudes and longitudes to H3 cell geometries as a GeoDataFrame."""
        if not isinstance(self.df, geopandas.GeoDataFrame):
            df = geopandas.GeoDataFrame(self.df)
        else:
            df = self.df.copy()

        df = point_to_h3(df, resolution)
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
    

    def set_df(self, df):
        self.df = df.copy()
