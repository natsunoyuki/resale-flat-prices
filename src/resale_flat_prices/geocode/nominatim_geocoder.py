import geopy


class NominatimGeocoder:
    def __init__(self, geocoder_user_agent = "resale_flat_price_nominatim"):
        self.geocoder = geopy.Nominatim(user_agent = geocoder_user_agent)

    def geocode(self, address):
        try:
            gcd = self.geocoder.geocode(address)
        except:
            print("An error occured with geocoding '{}'...".format(address))
            gcd = None
        return gcd