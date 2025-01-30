import time
import pandas as pd
import geopandas
from shapely import Point

# Local imports.
from property_prices.geocode.hdb_addresses import HDBAddresses


class LandedAddresses(HDBAddresses):
    def __init__(self, geocoder_user_agent = "resale_flat_price_nominatim"):
        super().__init__(geocoder_user_agent=geocoder_user_agent)


    def update_landed_addresses(self, address_list, country_codes=None, force_update=False, sleep=1):
        """Updates the dict of geocoded landed addresses with a list of new addresses."""
        error_address_list = []

        for address in address_list:
            address = address.upper()
            if address not in self.df["address"] or (address in self.df["address"] and force_update is True):
                gcd = self.geocoder.geocode(address, country_codes=country_codes)
                if gcd is not None:
                    _df = geopandas.GeoDataFrame(
                        {
                            "address": [address], 
                            "geocoded_address": [gcd.address.upper()], 
                            "latitude": [gcd.latitude], 
                            "longitude": [gcd.longitude], 
                            "geometry": [Point(gcd.longitude, gcd.latitude)],
                        },
                        crs=self.df.crs,
                    )
                    self.df = pd.concat([self.df, _df]).reset_index(drop=True)
                else:
                    print("An error occured with geocoding '{}'...".format(address))
                    error_address_list.append(address)

                # Nominatim geocoder only allows 1 geocode query per second.
                # Enforce a sleep of 1 second to prevent over doing the queries.
                time.sleep(sleep)

        return error_address_list
