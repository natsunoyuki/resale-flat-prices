import sys
sys.dont_write_bytecode = True

import yaml

from pathlib import Path
import pandas as pd


# Local imports.
from resale_flat_prices.csv_data.resale_csv_data import ResaleCsvData
from resale_flat_prices.csv_data.rent_csv_data import RentCsvData
from resale_flat_prices.geocode.geocoded_addresses import GeocodedAddresses


if __name__ == "__main__":
    tools_dir = Path(__file__).parent
    main_dir = tools_dir.parent

    with open(tools_dir / "data_pipeline.yml", "r") as f:
        config = yaml.safe_load(f)

    # Data directories.
    csv_data_dir = Path(config.get("resale_data_csv_data_dir", main_dir / "data/ResaleFlatPrices/"))

    rent_data_csv_file = config.get("rent_data_csv_file", None)
    if rent_data_csv_file is not None:
        rent_data_csv_file = Path(rent_data_csv_file)

    processed_data_dir = Path(config.get("processed_data_dir", main_dir / "data/processed_data/"))
    geocoded_addresses_json_file = config.get("geocoded_addresses_json_file", "geocoded_addresses.json")
    
    output_csv_file = config.get("output_csv_file", "resale-flat-prices.csv.zip")
    output_rent_csv_file = config.get("output_rent_csv_file", "rent-prices.csv.zip")


    # Load and process resale flat prices CSV files published on https://data.gov.sg/collections/189/view.
    print("Loading resale flat prices CSV data from {}.".format(csv_data_dir))
    csv_data = ResaleCsvData(csv_data_dir, wanted_columns = "default")
    csv_data.load_csv_files()
    csv_data.compile_csv_data()
    csv_data.process_csv_data()
    print("    Loaded and compiled resale flat prices CSV data with shape {}.".format(csv_data.df.shape))

    # Optional: load and process rent CSV data published on:
    # https://data.gov.sg/datasets/d_c9f57187485a850908655db0e8cfe651/view
    if rent_data_csv_file is not None:
        print("Loading rent data CSV data from {}.".format(rent_data_csv_file))
        rent_csv_data = RentCsvData(rent_data_csv_file)
        rent_csv_data.load_csv_file()
        rent_csv_data.process_csv_data()
        print("    Loaded and compiled rent CSV data with shape {}.".format(rent_csv_data.df.shape))

    # Load geocoded addresses.
    print("Loading geocoded addresses from {}.".format(processed_data_dir / geocoded_addresses_json_file))
    geocoded_addresses = GeocodedAddresses()
    geocoded_addresses.read_json(processed_data_dir / geocoded_addresses_json_file)
    print("    Loaded {} existing geocoded addresses.".format(len(geocoded_addresses.address_dict)))

    # Check for new addresses to be geocoded.
    all_unique_addresses = set(csv_data.df["address"].unique())
    if rent_data_csv_file is not None:
        all_unique_addresses.update(set(rent_csv_data.df["address"].unique()))
    all_unique_geocoded_addresses = geocoded_addresses.get_all_geocoded_addresses()

    # Update new geocoded addresses.
    missing_addresses = all_unique_addresses.difference(all_unique_geocoded_addresses)
    print("Found {} new addresses to be geocoded in loaded CSV data.".format(len(missing_addresses)))
    if len(missing_addresses) > 0:
        geocoded_addresses.update_geocoded_addresses(missing_addresses, country_codes = ["sg"])
        geocoded_addresses.to_json(processed_data_dir / geocoded_addresses_json_file)
        print("    Updated {} new geocoded addresses.".format(len(missing_addresses)))

    # Check for problematic geocodes.
    problem_addresses = geocoded_addresses.verify_geocoded_latitudes_and_longitudes(country = "SINGAPORE")
    if len(problem_addresses) > 0:
        print("Warning - the following {} addresses do not seem to have been geocoded correctly.".format(
            len(problem_addresses))
        )
        for i, p in enumerate(problem_addresses):
            print("    {:05d}: {}.".format(i, p))

    # Merge geocoded addresses with the resale flat prices CSV data.
    geocode_df = geocoded_addresses.address_dict_to_df()
    csv_df = csv_data.get_df()
    processed_data_df = pd.merge(left=csv_df, right=geocode_df, left_on="address", right_on="address", how="left")

    # Merge geocoded addresses with the rent CSV data.
    rent_csv_df = rent_csv_data.get_df()
    processed_rent_data_df = pd.merge(left=rent_csv_df, right=geocode_df, left_on="address", right_on="address", how="left")
    
    # Output the merged processed resale flat prices data to disk.
    # TODO create an output function.
    if output_csv_file[-3:] == "zip":
        compression = "zip"
    else:
        compression = None
    print("Saving processed resale flat prices data to {}.".format(processed_data_dir / output_csv_file))
    processed_data_df.to_csv(processed_data_dir / output_csv_file, index = False, compression = compression)

    # Optional: output the merged processed rent data to disk:
    if rent_data_csv_file is not None:
        if "rent-prices.csv.zip"[-3:] == "zip":
            compression = "zip"
        else:
            compression = None
        print("Saving processed rent data to {}.".format(processed_data_dir / output_rent_csv_file))
        processed_rent_data_df.to_csv(processed_data_dir / output_rent_csv_file, index = False, compression = compression)
