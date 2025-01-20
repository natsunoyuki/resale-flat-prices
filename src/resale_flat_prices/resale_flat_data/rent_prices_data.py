# This class represents the processed, geocoded and merged rent flat data, ready for analyses.

# Local imports.
from resale_flat_prices.resale_flat_data.flat_data_base import FlatDataBase 


COLUMNS = [
    'month', 'datetime', 'town', 'block', 'street_name', 'address',
    'flat_type', 'monthly_rent', 'geometry',
]


class RentPricesData(FlatDataBase):
    def __init__(self, file_name, wanted_columns = None):
        super().__init__(file_name, wanted_columns)

        if wanted_columns == "default":
            self.wanted_columns = COLUMNS
        else:
            self.wanted_columns = wanted_columns
