# HDB building information by merging Excel data from
# https://www.lta.gov.sg/content/ltagov/en/industry_innovations/industry_matters/development_construction_resources/street_works/requirements_for_street_work_proposals/gis_data_hub_collection.html
# and geojson data from
# https://data.gov.sg/collections/2033/view

from pathlib import Path
import json
import geopandas

from property_prices.excel_data.road_name_road_code_excel_data import RoadNameRoadCodeExcel
from property_prices.geojson_data.hdb_existing_building_geojson_data import HDBExistingBuildingGeojson


COUNTRY = "SINGAPORE"


class HDBBuildingInfo:
    def __init__(
        self,
        road_name_road_code_excel_file: Path,
        hdb_existing_building_geojson_file: Path,
    ):
        self.road_name_road_code_excel_file = road_name_road_code_excel_file
        self.hdb_existing_building_geojson_file = hdb_existing_building_geojson_file

        self.road_name_road_code = None
        self.hdb_existing_building = None
        self.df = geopandas.GeoDataFrame()
        self.address_dict = {}


    def load_data(
        self,         
        road_name_road_code_excel_file: Path = None,
        hdb_existing_building_geojson_file: Path = None,
    ):
        """Loads both the road name road code Excel data and the HDB existing building geojson data
        and combines them into a single DataFrame.
        """
        if road_name_road_code_excel_file is None:
            road_name_road_code_excel_file = self.road_name_road_code_excel_file
        if hdb_existing_building_geojson_file is None:
            hdb_existing_building_geojson_file = self.hdb_existing_building_geojson_file

        self.road_name_road_code = RoadNameRoadCodeExcel(road_name_road_code_excel_file)
        self.road_name_road_code.load_excel_file()
        
        self.hdb_existing_building = HDBExistingBuildingGeojson(hdb_existing_building_geojson_file)
        self.hdb_existing_building.load_geojson_file()

        self.df = self.hdb_existing_building.df.copy()
        self.df = self.df.merge(self.road_name_road_code.df.copy(), on="street_code", how="left")

        self.df["address"] = self.df[["block", "street_name"]].apply(
            lambda DF: DF["block"] + " " + DF["street_name"], axis=1,
        )
        self.df["address_postal_code"] = self.df[["address", "postal_code"]].apply(
            lambda DF: DF["address"] + " " + COUNTRY + " " + DF["postal_code"], axis=1,
        )

        self.df["latitude"] = self.df["geometry"].apply(lambda x: x.centroid.coords.xy[1][0])
        self.df["longitude"] = self.df["geometry"].apply(lambda x: x.centroid.coords.xy[0][0])


    def make_address_dict(self):
        """Makes a dict of the addresses from the loaded GeoDataFrame."""
        for i in range(len(self.df)):
            self.address_dict[self.df.iloc[i]["address"]] = {
                "geometry": self.df.iloc[i]["geometry"],
                "longitude": self.df.iloc[i]["geometry"].centroid.coords.xy[0][0],
                "latitude": self.df.iloc[i]["geometry"].centroid.coords.xy[1][0],
            }


    def to_json(self, output_json_path):
        """Saves the dict of geocoded addresses to a JSON file."""
        with open(output_json_path, "w") as f:
            json.dump(self.address_dict, f, indent = 4)

    
    def to_geojson(self, output_json_path):
        """Saves the GeoDataFrame of geocoded addresses to a GEOJSON file."""
        self.df.to_file(output_json_path, driver="GeoJSON") 
