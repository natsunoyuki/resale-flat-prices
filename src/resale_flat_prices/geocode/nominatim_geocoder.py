import geopy


class NominatimGeocoder:
    def __init__(self, geocoder_user_agent = "resale_flat_price_nominatim"):
        self.geocoder = geopy.Nominatim(user_agent = geocoder_user_agent)

    def geocode(self, address):
        try:
            gcd = self.geocoder.geocode(address)
        except:
            gcd = None
        return gcd