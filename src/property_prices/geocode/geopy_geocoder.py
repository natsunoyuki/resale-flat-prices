# This file wraps several geopy geocoder functions.
# https://geopy.readthedocs.io/en/stable/#module-geopy.geocoders
import geopy


USER_AGENT = "resale_flat_price_nominatim"

COUNTRY_CODES = {
    "sg": "SINGAPORE",
    "jp": "JAPAN",
}


class NominatimGeocoder:
    def __init__(self, geocoder_user_agent=USER_AGENT):
        self.geocoder = geopy.Nominatim(user_agent=geocoder_user_agent)

    def geocode(self, address, **kwargs):
        country_codes = kwargs.get("country_codes", None)
        try:
            gcd = self.geocoder.geocode(address, country_codes=country_codes)
        except:
            gcd = None
        return gcd


class ArcGISGeocoder:
    def __init__(self, geocoder_user_agent=USER_AGENT):
        self.geocoder = geopy.ArcGIS(user_agent=geocoder_user_agent)

    def geocode(self, address, **kwargs):
        try:
            gcd = self.geocoder.geocode(address)
        except:
            gcd = None
        return gcd
    

class PhotonGeocoder:
    def __init__(self, geocoder_user_agent=USER_AGENT):
        self.geocoder = geopy.Photon(user_agent=geocoder_user_agent)

    def geocode(self, address, **kwargs):
        try:
            gcd = self.geocoder.geocode(address)
        except:
            gcd = None
        return gcd
