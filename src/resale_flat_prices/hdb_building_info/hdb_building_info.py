# HDB building information by merging Excel data from
# https://www.lta.gov.sg/content/ltagov/en/industry_innovations/industry_matters/development_construction_resources/street_works/requirements_for_street_work_proposals/gis_data_hub_collection.html
# and geojson data from
# https://data.gov.sg/collections/2033/view

from pathlib import Path
import geopandas

from resale_flat_prices.excel_data.road_name_road_code_excel_data import RoadNameRoadCodeExcel
from resale_flat_prices.geojson_data.hdb_existing_building_geojson_data import HDBExistingBuildingGeojson


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


    def load_data(
        self,         
        road_name_road_code_excel_file: Path = None,
        hdb_existing_building_geojson_file: Path = None,
    ):
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

        self.df["address"] = self.df[["block", "street_name_cleaned"]].apply(
            lambda DF: DF["block"] + " " + DF["street_name_cleaned"], axis=1,
        )

        self.df = self.df[["address", "geometry"]]

    