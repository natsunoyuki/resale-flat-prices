# https://data.gov.sg/datasets?topics=housing&page=1&query=Renting+Out+of+Flats&resultId=d_c9f57187485a850908655db0e8cfe651

from pathlib import Path
import pandas as pd
import geopandas

# Local imports.
from resale_flat_prices.csv_data.data_processor import RentDataProcessor


COLUMNS = ['rent_approval_date', 'town', 'block', 'street_name', 'flat_type', 'monthly_rent']


class RentCsvData:
    def __init__(self, file_name: Path, wanted_columns = None):
        self.file_name = file_name
        self.wanted_columns = wanted_columns
        if wanted_columns == "default":
            wanted_columns = COLUMNS

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

    def get_df(self):
        """Getter for df."""
        return self.df.copy()
    
    def set_df(self, df):
        """"Setter for df."""
        self.df = df.copy()