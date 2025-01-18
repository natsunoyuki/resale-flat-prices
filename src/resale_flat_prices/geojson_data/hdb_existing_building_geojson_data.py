# This code handles the HDB existing building geojson data downloaded from:
# https://data.gov.sg/datasets/d_16b157c52ed637edd6ba1232e026258d/view

from pathlib import Path
import io
import pandas as pd
import geopandas


WANTED_RAW_COLS = ["Description", "geometry"]


class HDBExistingBuildingGeojson:
    def __init__(self, file_name: Path):
        self.file_name = file_name
        self.df = geopandas.GeoDataFrame()

    
    def load_geojson_file(self, file_name = None):
        if file_name is None:
            file_name = self.file_name

        df = geopandas.read_file(file_name)
        df = df[WANTED_RAW_COLS]

        _Description_df = df[WANTED_RAW_COLS[0]].apply(parse_html_description_to_dict)

        df["block"] = _Description_df.apply(lambda x: x.get("BLK_NO", None))
        df["street_code"] = _Description_df.apply(lambda x: x.get("ST_COD", None))
        df["entity_id"] = _Description_df.apply(lambda x: x.get("ENTITYID", None))
        df["postal_code"] = _Description_df.apply(lambda x: x.get("POSTAL_COD", None))
        df["inc_crc"] = _Description_df.apply(lambda x: x.get("INC_CRC", None))
        df["fmel_upd_d"] = _Description_df.apply(lambda x: x.get("FMEL_UPD_D", None))

        df.drop(WANTED_RAW_COLS[0], axis=1, inplace=True)

        self.df = df


    def get_df(self):
        """Getter for df."""
        return self.df.copy()


    def set_df(self, df):
        """"Setter for df."""
        self.df = df.copy()


def parse_html_description_to_dict(html):
    _df = pd.read_html(io.StringIO(html))[0].T
    new_header = _df.iloc[0]
    _df = _df[1:]
    _df.columns = new_header
    return _df.reset_index(drop=True).iloc[0].to_dict()
