import json

from resale_flat_prices.geocode.nominatim_geocoder import NominatimGeocoder


class GeocodedAddresses:
    def __init__(self, geocoder_user_agent = "resale_flat_price_nominatim"):
        self.address_dict = {}
        self.geocoder = NominatimGeocoder(geocoder_user_agent = geocoder_user_agent)

    def to_json(self, output_json_path):
        with open(output_json_path, "w") as f:
            json.dump(self.address_dict, f, indent = 4)
    
    def read_json(self, json_path):
        with open(json_path, "r") as f:
            self.address_dict = json.load(f)

    def update_geocoded_addresses(self, address_list, force_update = False):
        for address in address_list:
            if address not in self.address_dict or (address in self.address_dict and force_update is True):
                gcd = self.geocoder.geocode(address)
                if gcd is not None:
                    self.address_dict[address] = {}
                    self.address_dict[address]["latitude"] = gcd.latitude
                    self.address_dict[address]["longitude"] = gcd.longitude
                    self.address_dict[address]["address"] = gcd.address

    def get_address_dict(self):
        return self.address_dict.copy()
    
    def set_address_dict(self, address_dict):
        self.address_dict = address_dict.copy()