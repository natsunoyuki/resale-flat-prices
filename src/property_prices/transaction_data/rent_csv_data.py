# https://data.gov.sg/datasets?topics=housing&page=1&query=Renting+Out+of+Flats&resultId=d_c9f57187485a850908655db0e8cfe651

from pathlib import Path
import pandas as pd
import geopandas
import numpy as np

# Local imports.
from property_prices.transaction_data.data_processor import RentDataProcessor

# HDB rent data records start from 2021.
START_YEAR = np.datetime64("2021-01")

COLUMNS = [
    'datetime', 'town', 'block', 'street_name', 'flat_type', 'address', 'monthly_rent',
]


class RentCsvData:
    def __init__(self, file_name: Path, wanted_columns = "default"):
        self.file_name = file_name

        self.wanted_columns = wanted_columns
        if self.wanted_columns is not None and self.wanted_columns == "default":
            self.wanted_columns = COLUMNS

        self.df = geopandas.GeoDataFrame()
        self.data_processor = RentDataProcessor()


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
