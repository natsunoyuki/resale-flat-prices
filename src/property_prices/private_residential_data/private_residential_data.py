import pandas as pd
import geopandas
import numpy as np

# Local imports.
from property_prices.resale_flat_data.flat_data_base import FlatDataBase 
from property_prices.h3_utils.h3_utils import point_to_h3, h3_to_geometry


COLUMNS = [
    'project_name', 'transacted_price', 'area_sqft', 'unit_price_psf',
    'datetime', 'street_name', 'type_of_sale', 'type_of_area', 'area_sqm',
    'unit_price_psm', 'nett_price', 'property_type', 'number_of_units',
    'tenure', 'postal_district', 'market_segment', 'floor_level',
    'geometry',
]


class PrivateResidentialData(FlatDataBase):
    def __init__(self, file_name, wanted_columns = None):
        super().__init__(file_name, wanted_columns)

        if wanted_columns == "default":
            self.wanted_columns = COLUMNS
        else:
            self.wanted_columns = wanted_columns
