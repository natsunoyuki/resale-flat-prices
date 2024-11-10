import geopy


class NominatimGeocoder:
    def __init__(self, user_agent = "resale_flat_price_nominatim", address_dict = {}):
        self.user_agent = user_agent
        self.address_dict = address_dict
        self.geocoder = geopy.Nominatim(user_agent = user_agent)

    def geocode(self, address):
        try:
            gcd = self.geocoder.geocode(address)
        except:
            print("An error occured with Nominatim geocoding...")
            gcd = None
        return gcd

    def geocode_address(self, address, force_update = False):
        if address not in self.address_dict or (address in self.address_dict and force_update is True):
            gcd = self.geocode(address)
            if gcd is not None:
                self.address_dict[address] = {}
                self.address_dict[address]["latitude"] = gcd.latitude
                self.address_dict[address]["longitude"] = gcd.longitude
                self.address_dict[address]["address"] = gcd.address
        else:
            print("Address '{}' already exists.".format(address))