import sys
sys.dont_write_bytecode = True

import yaml

from pathlib import Path
import pandas as pd
import geopandas

# Local imports.
from resale_flat_prices.csv_data.csv_data import CsvData
from resale_flat_prices.geocode.geocoded_addresses import GeocodedAddresses


if __name__ == "__main__":
    tools_dir = Path(__file__).parent
    main_dir = tools_dir.parent

    with open(tools_dir / "data_pipeline.yml", "r") as f:
        config = yaml.safe_load(f)

    # Data directories.
    csv_data_dir = Path(config.get("csv_data_dir", main_dir / "data/ResaleFlatPrices/"))
    processed_data_dir = Path(config.get("processed_data_dir", main_dir / "data/processed_data/"))
    # H3 cell resolution.
    h3_resolution = config.get("h3_resolution", 9)
    # CRS.
    crs = config.get("crs", "EPSG:4326")

    # Load and process raw CSV files published on https://data.gov.sg/collections/189/view.
    csv_data = CsvData(csv_data_dir, wanted_columns = "default")
    csv_data.load_csv_files()
    csv_data.compile_csv_data()
    csv_data.process_csv_data()
    print("Loaded and compiled CSV data into shape {}.".format(csv_data.df.shape))

    # Load geocoded addresses.
    geocoded_addresses = GeocodedAddresses()
    geocoded_addresses.read_json(processed_data_dir / "geocoded_addresses.json")
    print("Loaded {} existing geocoded addresses.".format(len(geocoded_addresses.address_dict)))

    # Check for new addresses to be geocoded.
    all_unique_addresses = set(csv_data.df["address"].unique())
    all_unique_geocoded_addresses = geocoded_addresses.get_all_geocoded_addresses()

    # Update new geocoded addresses.
    missing_addresses = all_unique_addresses.difference(all_unique_geocoded_addresses)
    print("Found {} new addresses to be geocoded in loaded CSV data.".format(len(missing_addresses)))
    if len(missing_addresses) > 0:
        print("Updating {} new geocoded addresses.".format(len(missing_addresses)))
        geocoded_addresses.update_geocoded_addresses(missing_addresses)
        geocoded_addresses.to_json(processed_data_dir / "geocoded_addresses.json")

    # Check for problematic geocodes.
    problem_addresses = geocoded_addresses.verify_geocoded_latitudes_and_longitudes(country = "SINGAPORE")
    if len(problem_addresses) > 0:
        print("Warning - the following {} addresses do not seem to have been geocoded correctly.".format(
            len(problem_addresses))
        )
        for i, p in enumerate(problem_addresses):
            print("{:05d}: {}.".format(i, p))

    # H3 cell creation from latitudes and longitudes.
    right_df = geocoded_addresses.make_h3_geometries(resolution = h3_resolution, crs = crs)
    left_df = csv_data.get_df()

    df = pd.merge(left = left_df, right = right_df, left_on = "address", right_on = "address", how = "left")
    df = geopandas.GeoDataFrame(df, crs = right_df.crs)
    unique_cells = df[["h3", "geometry"]].drop_duplicates()