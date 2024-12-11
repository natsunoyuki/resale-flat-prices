import geopy


class NominatimGeocoder:
    def __init__(self, geocoder_user_agent = "resale_flat_price_nominatim"):
        self.geocoder = geopy.Nominatim(user_agent = geocoder_user_agent)

    def geocode(self, address, country_codes = None):
        try:
            gcd = self.geocoder.geocode(address, country_codes = country_codes)
        except:
            gcd = None
        return gcd