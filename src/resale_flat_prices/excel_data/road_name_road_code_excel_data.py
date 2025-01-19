# This code handles road name road code excel sheets downloaded from:
# https://www.lta.gov.sg/content/ltagov/en/industry_innovations/industry_matters/development_construction_resources/street_works/requirements_for_street_work_proposals/gis_data_hub_collection.html

from pathlib import Path
import pandas as pd


WANTED_RAW_COLS = ["Unnamed: 4", "Unnamed: 8"]
COLUMN_MAP = {"Domain Value": "street_code", "Description": "street_name"}


class RoadNameRoadCodeExcel:
    def __init__(self, file_name: Path):
        self.file_name = file_name
        self.df = pd.DataFrame()


    def load_excel_file(self, file_name = None):
        if file_name is None:
            file_name = self.file_name

        df = pd.read_excel(file_name)

        df = df[WANTED_RAW_COLS]
        df = df.dropna(how="all").reset_index(drop=True)
        new_header = df.iloc[0]
        df = df.iloc[1:]
        df.columns = new_header
        self.df = df.rename(columns = COLUMN_MAP)


    def get_df(self):
        """Getter for df."""
        return self.df.copy()


    def set_df(self, df):
        """"Setter for df."""
        self.df = df.copy()
