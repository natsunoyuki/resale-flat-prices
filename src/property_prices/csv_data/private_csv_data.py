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
    def __init__(self, file_name: Path, wanted_columns = "default"):
        self.file_name = file_name

        self.wanted_columns = wanted_columns
        if self.wanted_columns is not None and self.wanted_columns == "default":
            self.wanted_columns = COLUMNS

        self.df = geopandas.GeoDataFrame()
        self.data_processor = PrivateDataProcessor()


    def load_csv_file(self, file_name = None):
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