# Class to represent resale flat data as a GeoDataFrame.
# Handles loading data from raw CSV files published by data source,
# raw data processing and outputs.

from pathlib import Path
import pandas as pd
import geopandas

# Local imports.
from resale_flat_prices.csv_data.csv_file_data import CsvFileData
from resale_flat_prices.csv_data.data_processor import DataProcessor


class CsvData:
    def __init__(self, data_dir: Path, wanted_columns = None):
        self.data_dir = data_dir
        self.csv_file_names = []
        self.csv_data_list = []

        self.wanted_columns = wanted_columns
        self.df = geopandas.GeoDataFrame()

        self.data_processor = DataProcessor()

    def load_csv_files(self, data_dir = None):
        if data_dir is None:
            data_dir = self.data_dir
        """Loads raw CSV files published by source."""
        for f in data_dir.iterdir():
            if f.suffix == ".csv":
                csv_data = CsvFileData(file_name = f, wanted_columns = self.wanted_columns)
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

    def get_df(self):
        """Getter for df."""
        return self.df.copy()
    
    def set_df(self, df):
        """"Setter for df."""
        self.df = df.copy()