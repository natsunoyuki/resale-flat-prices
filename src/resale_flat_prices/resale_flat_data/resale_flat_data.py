import pandas as pd
from pathlib import Path

# Local imports.
from resale_flat_prices.resale_flat_data.csv_data import CsvData


class ResaleFlatData:
    def __init__(self, data_dir: Path, wanted_columns = None):
        self.data_dir = data_dir
        self.csv_file_names = []
        self.csv_data_list = []
        self.wanted_columns = wanted_columns
        self.df = pd.DataFrame()

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

    def process_month(self):
        self.df["year"] = self.df["month"].apply(lambda x: x.split("-")[0])
        self.df["month"] = self.df["month"].apply(lambda x: x.split("-")[1])

    def get_df(self):
        return self.df