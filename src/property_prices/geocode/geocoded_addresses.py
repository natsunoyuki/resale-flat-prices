import time
from pathlib import Path
import pandas as pd
import geopandas
from shapely import Point


# Local imports.
from property_prices.geocode.geopy_geocoder import NominatimGeocoder
from property_prices.geocode.lat_lon_constants import LOCS


GEOCODING_COUNTRY_CODES = {
    "SINGAPORE" : "sg",
    "JAPAN" : "jp",
}


class GeocodedAddresses:
    def __init__(self, geocoder_user_agent="resale_flat_price_nominatim", crs="EPSG:4326"):
        self.geocoder = NominatimGeocoder(geocoder_user_agent = geocoder_user_agent)
        self.df = geopandas.GeoDataFrame(
            {"address": [], "geocoded_address": [], "latitude": [], "longitude": [], "geometry": []},
            crs=crs,
        )


    def to_json(self, output_json_path: Path):
        """Saves the dict of geocoded addresses to a GeoJSON file."""
        self.df.to_file(output_json_path, driver="GeoJSON")
    

    def read_json(self, json_path:Path):
        """Loads a dict of geocoded addresses from a GeoJSON file."""
        self.df = geopandas.read_file(json_path)

        self.df["latitude"] = self.df["latitude"].apply(lambda x: float(x))
        self.df["longitude"] = self.df["longitude"].apply(lambda x: float(x))


    def update_geocoded_addresses(self, address_list, country_codes=None, force_update=False, sleep=1):
        """Updates the dict of geocoded addresses with a list of new addresses."""
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


    def verify_geocoded_latitudes_and_longitudes(self, country = "SINGAPORE"):
        """Checks if all the geocoded latitudes and longitudes fall within the
        geographical limits of the specified country."""
        country = LOCS.get(country.upper(), None)
        assert country is not None
        
        lats = country.get("latitude")
        lons = country.get("longitude")

        problem_addresses = {}
        for i in range(len(self.df)):
            lat = self.df.iloc[i]["latitude"]
            lon = self.df.iloc[i]["longitude"]
            if (lat < lats[0] or lat > lats[1]) or (lon < lons[0] or lon > lons[1]):
                problem_addresses[self.df.iloc[i]["address"]] = self.df.iloc[i]

        return problem_addresses


    def get_all_geocoded_addresses(self):
        """Returns all unique geocoded addresses in the GeoDataFrame."""
        return set(self.df["address"].unique())


    def manually_update_geocoded_address(
        self, 
        address_dict={
            "address": None, "geocoded_address": None, "latitude": None, "longitude": None, "geometry": None,
        },
        force_update=False,
    ):
        address = address_dict.get("address", None)
        if address is not None:
            if address not in self.df["address"] or (address in self.df["address"] and force_update is True):
                _df = geopandas.GeoDataFrame(
                    {
                        "address": [address_dict.get("address")],
                        "geocoded_address": [address_dict.get("geocoded_address")],
                        "latitude": [address_dict.get("latitude")],
                        "longitude": [address_dict.get("longitude")],
                        "geometry": [address_dict.get("geometry")],
                    }, 
                    crs=self.df.crs
                )
                self.df = pd.concat([self.df, _df]).reset_index(drop=True)
