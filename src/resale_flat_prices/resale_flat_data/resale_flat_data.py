import pandas as pd
from pathlib import Path

# Local imports.
from resale_flat_prices.resale_flat_data.csv_data import CsvData
from resale_flat_prices.data_preprocessing.data_processor import DataProcessor


class ResaleFlatData:
    def __init__(self, data_dir: Path, wanted_columns = None):
        self.data_dir = data_dir
        self.csv_file_names = []
        self.csv_data_list = []
        self.wanted_columns = wanted_columns
        self.df = pd.DataFrame()
        self.data_processor = DataProcessor()

    def load_csv_files(self):
        for f in self.data_dir.iterdir():
            if f.suffix == ".csv":
                csv_data = CsvData(file_name = f, wanted_columns = self.wanted_columns)
                csv_data.load_csv_file()
                self.csv_data_list.append(csv_data)

    def compile_data(self):
        for c in self.csv_data_list:
            _df = c.df.copy()
            self.df = pd.concat([self.df, _df])

    def process_data(self):
        self.data_processor.set_df(self.df)
        self.data_processor.process_all_columns()
        self.df = self.data_processor.get_df()

    def get_df(self):
        return self.df.copy()
    
    def set_df(self, df):
        self.df = df.copy()