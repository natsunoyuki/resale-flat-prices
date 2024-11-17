# Tool for geocoding addresses to latitudes and longitudes.
# Also utilizes the h3_py library to convert latitudes and longitudes
# to H3 hexagonal cells.

import time
import json
import pandas as pd
import geopandas

# Local imports.
from resale_flat_prices.geocode.nominatim_geocoder import NominatimGeocoder
from resale_flat_prices.geocode.lat_lon_constants import LOCS
from resale_flat_prices.h3_utils.h3_utils import latlon_to_h3, h3_to_geometry


class GeocodedAddresses:
    def __init__(self, geocoder_user_agent = "resale_flat_price_nominatim"):
        self.address_dict = {}
        self.geocoder = NominatimGeocoder(geocoder_user_agent = geocoder_user_agent)

    def to_json(self, output_json_path):
        """Saves the dict of geocoded addresses to a JSON file."""
        with open(output_json_path, "w") as f:
            json.dump(self.address_dict, f, indent = 4)
    
    def read_json(self, json_path):
        """Loads a dict of geocoded addresses from a JSON file."""
        with open(json_path, "r") as f:
            self.address_dict = json.load(f)

        # For some reason, sometimes numericals are saved/loaded as str.
        # Convert to floating point values.
        for k in self.address_dict.keys():
            self.address_dict[k]["latitude"] = float(self.address_dict[k]["latitude"])
            self.address_dict[k]["longitude"] = float(self.address_dict[k]["longitude"])

    def update_geocoded_addresses(self, address_list, force_update = False, sleep = 1):
        """Updates the dict of geocoded addresses with a list of new addresses."""
        error_address_list = []

        for address in address_list:
            if address not in self.address_dict or (address in self.address_dict and force_update is True):
                gcd = self.geocoder.geocode(address)
                if gcd is not None:
                    self.address_dict[address] = {}
                    self.address_dict[address]["latitude"] = gcd.latitude
                    self.address_dict[address]["longitude"] = gcd.longitude
                    self.address_dict[address]["address"] = gcd.address
                else:
                    print("An error occured with geocoding '{}'...".format(address))
                    error_address_list.append(address)

                # Nominatim geocoder only allows 1 geocode query per second.
                # Enforce a sleep of 1 second to prevent over doing the queries.
                time.sleep(sleep)

        return error_address_list

    def verify_geocoded_latitudes_and_longitudes(self, country = "SINGAPORE"):
        """Checks if all the geocoded latitudes and longitudes fall within the
        geographical limits of the specified country."""
        country = LOCS.get(country.upper(), None)
        assert country is not None
        
        lats = country.get("latitude")
        lons = country.get("longitude")

        problem_addresses = {}
        for k, v in self.address_dict.items():
            lat = float(v.get("latitude"))
            lon = float(v.get("longitude"))
            if (lat < lats[0] or lat > lats[1]) or (lon < lons[0] or lon > lons[1]):
                problem_addresses[k] = v.copy()

        return problem_addresses

    def address_dict_to_df(self):
        """Outputs the address dict as a DataFrame."""
        df = pd.DataFrame.from_dict(self.address_dict, orient = "index")
        df = df.reset_index().drop("address", axis = 1)
        df = df.rename(columns = {"index": "address"})
        return df

    def make_h3_geometries(self, resolution = 8, crs = "EPSG:4326"):
        """Processes the latitudes and longitudes to H3 cell geometries as a GeoDataFrame."""
        df = geopandas.GeoDataFrame(self.address_dict_to_df())
        df = latlon_to_h3(df, resolution)
        df = h3_to_geometry(df, crs)
        return df

    def get_address_dict(self):
        """Address dict getter."""
        return self.address_dict.copy()
    
    def set_address_dict(self, address_dict):
        """Address dict setter."""
        self.address_dict = address_dict.copy()

    def get_all_geocoded_addresses(self):
        """Get all unique geocoded addresses."""
        return set([k for k in self.address_dict.keys()])