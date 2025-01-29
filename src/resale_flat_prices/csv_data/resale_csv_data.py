# Class to represent resale flat data as a GeoDataFrame.
# Handles loading data from raw CSV files published by data source,
# raw data processing and outputs.

from pathlib import Path
import pandas as pd
import geopandas
import numpy as np

# Local imports.
from resale_flat_prices.csv_data.resale_csv_file_data import ResaleCsvFileData
from resale_flat_prices.csv_data.data_processor import ResaleDataProcessor


# HDB resale data records start from 1990.
START_YEAR = np.datetime64("1990-01")

COLUMNS = [
    'datetime', 'town', 'flat_type', 'block', 'street_name', 'address',
    'storey_range', 'floor_area_sqm', 'flat_model', 'lease_commence_date', 
    'resale_price', 'price_per_sqft'
]


class ResaleCsvData:
    def __init__(self, data_dir: Path, wanted_columns = "default"):
        self.data_dir = data_dir
        self.csv_file_names = []
        self.csv_data_list = []

        self.wanted_columns = wanted_columns
        if self.wanted_columns is not None and self.wanted_columns == "default":
            self.wanted_columns = COLUMNS

        self.df = geopandas.GeoDataFrame()

        self.data_processor = ResaleDataProcessor()


    def load_csv_files(self, data_dir = None, wanted_csv_columns = None):
        if data_dir is None:
            data_dir = self.data_dir
        """Loads raw CSV files published by source."""
        for f in data_dir.iterdir():
            if f.suffix == ".csv":
                csv_data = ResaleCsvFileData(file_name = f, wanted_columns = wanted_csv_columns)
                csv_data.load_csv_file()
                self.csv_data_list.append(csv_data)


    def compile_csv_data(self):
        """Compiles loaded CSV files into a single GeoDataFrame."""
        df = pd.DataFrame()
        for c in self.csv_data_list:
            _df = c.df.copy()
            df = pd.concat([df, _df])
        self.df = geopandas.GeoDataFrame(df)


    def process_csv_data(self):
        """"Processes data in an existing GeoDataFrame."""
        self.data_processor.set_df(self.df)
        self.data_processor.process_all_columns()
        self.df = self.data_processor.get_df()

        if self.wanted_columns is not None:
            self.df = self.df[self.wanted_columns]


    def check_and_repair_datetimes(self, column = "datetime"):
        """Checks if the transaction datetimes are valid. 
        HDB has a record of providing erroneous dates.
        If erroneous dates are discovered, they are forward filled."""
        want = np.where(self.df[column] < START_YEAR)[0]
        self.df.loc[want, column] = np.nan
        self.df = self.df.infer_objects().ffill()
        return want


    def get_df(self):
        """Getter for df."""
        return self.df.copy()
    

    def set_df(self, df):
        """"Setter for df."""
        self.df = df.copy()
