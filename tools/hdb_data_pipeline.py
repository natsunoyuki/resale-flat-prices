import sys
sys.dont_write_bytecode = True

import yaml

from pathlib import Path
import pandas as pd
import geopandas


# Local imports.
from property_prices.csv_data.resale_csv_data import ResaleCsvData
from property_prices.csv_data.rent_csv_data import RentCsvData
from property_prices.geocode.hdb_addresses import HDBAddresses


CONFIG_FILE = "hdb_data_pipeline.yml"


if __name__ == "__main__":
    tools_dir = Path(__file__).parent
    main_dir = tools_dir.parent

    with open(tools_dir / CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)


    # Load user configurations.
    csv_data_dir = Path(config.get("resale_data_csv_data_dir", main_dir / "data/ResaleFlatPrices/"))

    rent_data_csv_file = config.get("rent_data_csv_file", None)
    if rent_data_csv_file is not None:
        rent_data_csv_file = Path(rent_data_csv_file)

    processed_data_dir = Path(config.get("processed_data_dir", main_dir / "data/processed_data/"))
    hdb_addresses_json_file = Path(config.get("hdb_addresses_json_file", "hdb_addresses.json"))
    
    output_resale_flat_prices_file = Path(config.get("output_resale_flat_prices_file", "resale-flat-prices.parquet"))
    output_rent_prices_file = Path(config.get("output_rent_prices_file", "rent-prices.parquet"))

    convert_polygons_to_centroids = config.get("convert_polygons_to_centroids", True)

    parquet_compression = config.get("parquet_compression", "brotli")


    # Load and process resale flat prices CSV files published on https://data.gov.sg/collections/189/view.
    print("Loading resale flat prices CSV data from {}.".format(csv_data_dir))
    csv_data = ResaleCsvData(csv_data_dir, wanted_columns = "default")
    csv_data.load_csv_files()
    csv_data.compile_csv_data()
    csv_data.process_csv_data()
    repaired_rows = csv_data.check_and_repair_datetimes()
    if len(repaired_rows) > 0:
        print("    Repaired datetimes at rows {}.".format(repaired_rows))
    print("    Loaded and compiled resale flat prices CSV data with shape {}.".format(csv_data.df.shape))

    # Optional: load and process rent CSV data published on:
    # https://data.gov.sg/datasets/d_c9f57187485a850908655db0e8cfe651/view
    if rent_data_csv_file is not None:
        print("Loading rent data CSV data from {}.".format(rent_data_csv_file))
        rent_csv_data = RentCsvData(rent_data_csv_file)
        rent_csv_data.load_csv_file()
        rent_csv_data.process_csv_data()
        repaired_rows = rent_csv_data.check_and_repair_datetimes()
        if len(repaired_rows) > 0:
            print("    Repaired datetimes at rows {}.".format(repaired_rows))
        print("    Loaded and compiled rent CSV data with shape {}.".format(rent_csv_data.df.shape))


    # Load geocoded addresses.
    print("Loading geocoded HDB addresses from {}.".format(processed_data_dir / hdb_addresses_json_file))
    hdb_addresses = HDBAddresses()
    hdb_addresses.read_json(processed_data_dir / hdb_addresses_json_file)
    print("    Loaded {} existing geocoded addresses.".format(len(hdb_addresses.df)))

    # Check for new addresses to be geocoded.
    all_unique_addresses = set(csv_data.df["address"].unique())
    if rent_data_csv_file is not None:
        all_unique_addresses.update(set(rent_csv_data.df["address"].unique()))
    all_unique_geocoded_addresses = hdb_addresses.get_all_geocoded_addresses()

    # Update new geocoded addresses.
    missing_addresses = all_unique_addresses.difference(all_unique_geocoded_addresses)
    print("Found {} new addresses to be geocoded in the CSV data.".format(len(missing_addresses)))
    if len(missing_addresses) > 0:
        for ma in missing_addresses:
            print("    {}".format(ma))

        hdb_addresses.update_geocoded_addresses(missing_addresses, country_codes = ["sg"])
        hdb_addresses.to_json(processed_data_dir / hdb_addresses_json_file)
        print("    Updated {} new geocoded HDB addresses.".format(len(missing_addresses)))

    # Check for problematic geocodes.
    problem_addresses = hdb_addresses.verify_geocoded_latitudes_and_longitudes(country = "SINGAPORE")
    if len(problem_addresses) > 0:
        print("Warning - the following {} addresses do not seem to have been geocoded correctly.".format(
            len(problem_addresses))
        )
        for i, p in enumerate(problem_addresses):
            print("    {:05d}: {}.".format(i, p))


    # Merge geocoded addresses with the resale flat prices CSV data.
    geocode_df = hdb_addresses.df[["address", "geometry"]]
    csv_df = csv_data.get_df()
    processed_data_df = pd.merge(
        left=csv_df, right=geocode_df, left_on="address", right_on="address", how="left")
    processed_data_df = geopandas.GeoDataFrame(processed_data_df)
    processed_data_df.crs = geocode_df.crs
    
    if convert_polygons_to_centroids is True:
        processed_data_df["geometry"] = processed_data_df["geometry"].apply(lambda x: x.centroid)

    # Merge geocoded addresses with the rent CSV data.
    if rent_data_csv_file is not None:
        rent_csv_df = rent_csv_data.get_df()
        processed_rent_data_df = pd.merge(
            left=rent_csv_df, right=geocode_df, left_on="address", right_on="address", how="left")
        processed_rent_data_df = geopandas.GeoDataFrame(processed_rent_data_df)
        processed_rent_data_df.crs = geocode_df.crs

        if convert_polygons_to_centroids is True:
            processed_rent_data_df["geometry"] = processed_rent_data_df["geometry"].apply(lambda x: x.centroid)


    # Output the merged processed resale flat prices data to disk.
    out_path = processed_data_dir / output_resale_flat_prices_file
    print("Saving processed resale flat prices data to {}.".format(out_path))
    if out_path.suffix == ".zip":
        processed_data_df.to_csv(out_path, index=False, compression="zip")
    elif out_path.suffix == ".json":
        processed_data_df.to_file(out_path, driver="GeoJSON")
    elif out_path.suffix == ".parquet":
        processed_data_df.to_parquet(out_path, index=False, compression=parquet_compression)

    # Optional: output the merged processed rent data to disk:
    if rent_data_csv_file is not None:
        out_path = processed_data_dir / output_rent_prices_file
        print("Saving processed rent data to {}.".format(out_path))
        if out_path.suffix == ".zip":
            processed_rent_data_df.to_csv(out_path, index=False, compression="zip")
        elif out_path.suffix == ".json":
            processed_rent_data_df.to_file(out_path, driver="GeoJSON")
        elif out_path.suffix == ".parquet":
            processed_rent_data_df.to_parquet(out_path, index=False, compression=parquet_compression)
