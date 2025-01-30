# This class represents the processed, geocoded and merged resale flat data, ready for analyses.

# Local imports.
from property_prices.resale_flat_data.flat_data_base import FlatDataBase 


COLUMNS = [
    'datetime', 'month', 'town', 'flat_type', 'block', 'street_name', 'address',
    'storey_range', 'floor_area_sqm', 'flat_model', 'lease_commence_date', 
    'resale_price', 'price_per_sqft', 'geometry',
]


class ResaleFlatData(FlatDataBase):
    def __init__(self, file_name, wanted_columns = None):
        super().__init__(file_name, wanted_columns)

        if wanted_columns == "default":
            self.wanted_columns = COLUMNS
        else:
            self.wanted_columns = wanted_columns
