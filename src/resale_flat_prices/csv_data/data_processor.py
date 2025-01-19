# Clean and perform feature engineering on the loaded resale price GeoDataFrame.

from datetime import datetime
import geopandas

# Local imports.
from resale_flat_prices.csv_data.data_processing_utils import (
    clean_month, get_price_per_sqft, get_price_per_sqm, clean_town, clean_flat_model, clean_flat_type, 
    clean_floor_area_sqm, clean_storey_range, clean_street_name, make_address, get_age_from_lease_commence_date,
    clean_rent_approval_date
)

# Fixed constants.
CURRENT_YEAR = datetime.today().year


class ResaleDataProcessor:
    def __init__(self, df = geopandas.GeoDataFrame()):
        self.df = df.copy()

    def set_df(self, df):
        self.df = df.copy()

    def get_df(self):
        return self.df.copy()

    def process_all_columns(self):
        self.clean_month()
        #self.get_price_per_sqm()
        self.get_price_per_sqft()
        self.clean_town()
        self.clean_street_name()
        self.make_address()
        self.clean_flat_type()
        #self.clean_storey_range()
        self.clean_flat_model()
        #self.clean_floor_area_sqm()
        #self.calculate_age()

    def clean_month(self):
        self.df = clean_month(self.df)

    def get_price_per_sqft(self):
        self.df = get_price_per_sqft(self.df)

    def get_price_per_sqm(self):
        self.df = get_price_per_sqm(self.df)

    def clean_town(self):
        self.df = clean_town(self.df)

    def clean_street_name(self):
        self.df = clean_street_name(self.df)

    def make_address(self):
        self.df = make_address(self.df)

    def clean_flat_type(self):
        self.df = clean_flat_type(self.df)

    def clean_storey_range(self):
        self.df = clean_storey_range(self.df)

    def clean_flat_model(self):
        self.df = clean_flat_model(self.df)

    def clean_floor_area_sqm(self):
        self.df = clean_floor_area_sqm(self.df)
    
    def calculate_age(self):
        self.df = get_age_from_lease_commence_date(self.df, CURRENT_YEAR)


class RentDataProcessor(ResaleDataProcessor):
    def __init__(self, df = geopandas.GeoDataFrame()):
        super().__init__(df = df)

    def process_all_columns(self):
        self.clean_rent_approval_date()
        self.clean_town()
        self.clean_street_name()
        self.make_address()
        self.clean_flat_type()

    def clean_rent_approval_date(self):
        self.df = clean_rent_approval_date(self.df)