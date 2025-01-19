import sys
sys.dont_write_bytecode = True

from pathlib import Path
import yaml
import numpy as np
import geopandas
import pandas as pd


#from resale_flat_prices.excel_data.road_name_road_code_excel_data import RoadNameRoadCodeExcel
#from resale_flat_prices.geojson_data.hdb_existing_building_geojson_data import HDBExistingBuildingGeojson
from resale_flat_prices.hdb_building_info.hdb_building_info import HDBBuildingInfo


CONFIG_FILE = "hdb_addresses.yml"


if __name__ == "__main__":
    tools_dir = Path(__file__).parent
    main_dir = tools_dir.parent

    with open(tools_dir / CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    # Data directories.
    # Directory containing the road name road code Excel file.
    road_name_road_code_data_dir =  Path(config.get("road_name_road_code_data_dir", "data/RoadNameRoadCode/"))
    # Excel file containing the road name and road code data.
    road_name_road_code_excel_file = config.get("road_name_road_code_excel_file", "road_name_road_code_jan2024.xlsx")

    # Directory containing the HDB existing building geojson file.
    hdb_existing_building_data_dir = Path(config.get("hdb_existing_building_data_dir", "data/HDBExistingBuilding"))
    # Geojson file containing the HDB existing building data.
    hdb_existing_building_geojson_file = config.get("hdb_existing_building_geojson_file", "HDBExistingBuilding.geojson")

    # Directory containing the processed data (e.g. geocoded addresses etc.)
    processed_data_dir = Path(config.get("processed_data_dir", "data/processed_data/"))
    # (Pre-made) GEOJSON file containing the geocoded addresses.
    hdb_addresses_json_file = config.get("hdb_addresses_json_file", "hdb_addresses.json")


    # Load and process the road name road code Excel data and the HDB existing building information, and
    # combine them.
    print("Loading the following HDB building and road name information:")
    print("i. Road name road code information from {}.".format(
        road_name_road_code_data_dir / road_name_road_code_excel_file))
    print("ii. HDB existing building information from {}.".format(
        hdb_existing_building_data_dir / hdb_existing_building_geojson_file))
    hdb_building_info = HDBBuildingInfo(
        road_name_road_code_data_dir / road_name_road_code_excel_file, 
        hdb_existing_building_data_dir / hdb_existing_building_geojson_file
    )

    hdb_building_info.load_data()
    hdb_building_info_df = hdb_building_info.df[["geometry", "address", "address_postal_code", "latitude", "longitude"]]
    hdb_building_info_df = hdb_building_info_df.rename(columns = {"address_postal_code": "geocoded_address"})
    hdb_building_info_df["geocoded_address"] = hdb_building_info_df["geocoded_address"].apply(lambda x: x.upper())
    print("Loaded and compiled HDB building information with shape: {}.".format(hdb_building_info.df.shape))


    # Load the pre-existing GEOJSON file containing geocoded addresses.
    print("Loading geocoded HDB addresses from {}.".format(processed_data_dir / hdb_addresses_json_file))
    hdb_addresses_df = geopandas.read_file(processed_data_dir / hdb_addresses_json_file)
    print("Loaded geocoded HDB addresses with shape: {}.".format(hdb_addresses_df.shape))

    # Combine both pieces of information together by overwriting the geocoded addresses.
    print("Building the updated geocoded addresses with the loaded HDB building information.")
    df = hdb_building_info.df[["geometry", "address", "address_postal_code", "latitude", "longitude"]]
    df = df.rename(columns = {"address_postal_code": "geocoded_address"})

    df = pd.concat(
        [
            df, 
            hdb_addresses_df[np.logical_not(hdb_addresses_df["address"].isin(df["address"].unique()))]
        ]
    )
    print("Updated HDB address DataFrame shape: {}.".format(df.shape))


    # Output combined information to disk.
    print("Saving updated HDB addresses to {}.".format(processed_data_dir / hdb_addresses_json_file))
    df.to_file(processed_data_dir / hdb_addresses_json_file, driver="GeoJSON") 
