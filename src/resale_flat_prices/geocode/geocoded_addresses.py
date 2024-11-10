import json


class GeocodedAddresses:
    def __init__(self):
        self.address_dict = {}

    def to_json(self, output_json_path):
        with open(output_json_path, "w") as f:
            json.dump(self.address_dict, f, indent = 4)
    
    def read_json(self, json_path):
        with open(json_path, "r") as f:
            self.address_dict = json.load(f)