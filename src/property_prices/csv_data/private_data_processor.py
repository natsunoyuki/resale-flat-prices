# Clean and perform feature engineering on the loaded GeoDataFrame.

import re
import geopandas
import numpy as np


numerical_months = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}


class PrivateDataProcessor:
    def __init__(self, df = geopandas.GeoDataFrame()):
        self.df = df.copy()

    def set_df(self, df):
        self.df = df.copy()

    def get_df(self):
        return self.df.copy()

    def process_all_columns(self):
        self.rename_columns()
        self.clean_project_name()
        self.clean_transacted_price()
        self.clean_area_sqft()
        self.clean_unit_price_psf()
        self.clean_sale_date()
        self.clean_street_name()
        self.clean_type_of_sale()
        self.clean_type_of_area()
        self.clean_area_sqm()
        self.clean_unit_price_psm()
        self.clean_nett_price()
        self.clean_property_type()
        self.clean_number_of_units()
        self.clean_tenure()
        self.clean_postal_district()
        self.clean_market_segment()
        self.clean_floor_level()

    def rename_columns(self):
        new_cols = {}
        for col in self.df.columns:
            c = re.sub("[\$\(\)]", "", col).strip()
            c = re.sub(" +", " ", c).lower().replace(" ", "_")
            new_cols[col] = c
        self.df = self.df.rename(columns = new_cols)

    def clean_project_name(self):
        self.df["project_name"] = self.df["project_name"].apply(lambda x: x.upper())

    def clean_transacted_price(self):
        self.df["transacted_price"] = self.df["transacted_price"].apply(lambda x: int(x.replace(",", "")))

    def clean_area_sqft(self):
        self.df["area_sqft"] = self.df["area_sqft"].apply(lambda x: float(x.replace(",", "")))
    
    def clean_unit_price_psf(self):
       self.df["unit_price_psf"] = self.df["unit_price_psf"].apply(lambda x: int(x.replace(",", "")))

    def clean_sale_date(self):
        self.df = self.df.rename(columns={"sale_date": "datetime"})

        self.df["datetime"] = self.df["datetime"].apply(
            lambda x: np.datetime64(
                "20{}-{}".format(
                    x.split("-")[1], numerical_months.get(x.split("-")[0])
                ), "M",
            ),
        )
        
    def clean_street_name(self):
        self.df["street_name"] = self.df["street_name"].apply(lambda x: x.upper())

    def clean_type_of_sale(self):
        self.df["type_of_sale"] = self.df["type_of_sale"].apply(lambda x: x.upper())

    def clean_type_of_area(self):
        self.df["type_of_area"] = self.df["type_of_area"].apply(lambda x: x.upper())
    
    def clean_area_sqm(self):
        self.df["area_sqm"] = self.df["area_sqm"].apply(lambda x: float(x.replace(",", "")))
    
    def clean_unit_price_psm(self):
        self.df["unit_price_psm"] = self.df["unit_price_psm"].apply(lambda x: int(x.replace(",", "")))
    
    def clean_nett_price(self):
        #self.df["nett_price"] = self.df["nett_price"].apply(lambda x: int(x.replace(",", "").replace("-", "")))
        return
        
    def clean_property_type(self):
        self.df["property_type"] = self.df["property_type"].apply(lambda x: x.upper())
    
    def clean_number_of_units(self):
        return

    def clean_tenure(self):
        self.df["tenure"] = self.df["tenure"].apply(lambda x: x.upper())
    
    def clean_postal_district(self):
        return
    
    def clean_market_segment(self):
        self.df["market_segment"] = self.df["market_segment"].apply(lambda x: x.upper())
    
    def clean_floor_level(self):
        #self.df["floor_level"] = self.df["floor_level"].apply(lambda x: int(x.replace(",", "").replace("-", "")))
        return
