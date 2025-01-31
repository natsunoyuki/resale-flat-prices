from pathlib import Path
import numpy as np
import pandas as pd
import geopandas

# Local imports.
from property_prices.csv_data.private_data_processor import PrivateDataProcessor


COLUMNS = [
    'project_name', 'transacted_price', 'area_sqft', 'unit_price_psf',
    'datetime', 'street_name', 'type_of_sale', 'type_of_area', 'area_sqm',
    'unit_price_psm', 'nett_price', 'property_type', 'number_of_units',
    'tenure', 'postal_district', 'market_segment', 'floor_level'
]


class PrivateCsvData:
    def __init__(self, data_dir: Path, file_name: Path = None, wanted_columns = "default"):
        self.data_dir = data_dir
        self.file_name = file_name

        self.csv_data_list = []

        self.wanted_columns = wanted_columns
        if self.wanted_columns is not None and self.wanted_columns == "default":
            self.wanted_columns = COLUMNS

        self.df = geopandas.GeoDataFrame()
        self.data_processor = PrivateDataProcessor()


    def load_csv_files(self, data_dir: Path=None):
        if data_dir is None:
            data_dir = self.data_dir

        for f in data_dir.iterdir():
            if f.suffix == ".csv":
                try:
                    self.csv_data_list.append(pd.read_csv(f))
                except UnicodeDecodeError:
                    self.csv_data_list.append(pd.read_csv(f, encoding="ISO-8859-1"))

        self.df = geopandas.GeoDataFrame(pd.concat(self.csv_data_list))


    def load_csv_file(self, file_name=None):
        if file_name is None:
            file_name = self.file_name

        self.df = pd.read_csv(file_name)
        self.df = geopandas.GeoDataFrame(self.df)


    def process_csv_data(self):
        """"Processes data in an existing GeoDataFrame."""
        self.data_processor.set_df(self.df)
        self.data_processor.process_all_columns()
        self.df = self.data_processor.get_df()

        if self.wanted_columns is not None:
            self.df = self.df[self.wanted_columns]


    def get_df(self):
        """Getter for df."""
        return self.df.copy()
    

    def set_df(self, df):
        """"Setter for df."""
        self.df = df.copy()
