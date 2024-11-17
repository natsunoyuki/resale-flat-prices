# This class handles the loading of raw tabular data from individual
# CSV files published by the source.

import pandas as pd

COLUMNS = [
    "month",
    "town", 
    "flat_type", 
    "block", 
    "street_name",
    "storey_range",
    "floor_area_sqm",
    "flat_model",
    "lease_commence_date",
    "resale_price"
]

class CsvFileData:
    def __init__(self, file_name, wanted_columns = None):
        self.file_name = file_name
        self.wanted_columns = wanted_columns
        if self.wanted_columns == "default":
            self.wanted_columns = COLUMNS
        self.df = None

    def load_csv_file(self, file_name = None):
        if file_name is None:
            file_name = self.file_name
        
        self.df = pd.read_csv(file_name)
        if self.wanted_columns is not None:
            self.df = self.df[self.wanted_columns]
    
    def get_df(self):
        assert self.df is not None
        return self.df
    
    def to_csv(self, output_file_name):
        assert self.df is not None
        self.df.to_csv(output_file_name, index = False)
