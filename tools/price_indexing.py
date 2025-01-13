import sys
sys.dont_write_bytecode = True

import yaml

from pathlib import Path
import pandas as pd

from resale_flat_prices.resale_flat_data.resale_flat_data import ResaleFlatData
from resale_flat_prices.resale_flat_data.rent_prices_data import RentPricesData


if __name__ == "__main__":
    tools_dir = Path(__file__).parent
    main_dir = tools_dir.parent

    with open(tools_dir / "price_indexing.yml", "r") as f:
        config = yaml.safe_load(f)

    # Data directories and files.
    processed_data_dir = main_dir / config.get("processed_data_dir", "data/processed_data/")

    resale_data_csv_file = processed_data_dir /  config.get("resale_data_csv_file", "resale-flat-prices.csv.zip")

    rent_data_csv_file = config.get("rent_data_csv_file", None)
    if rent_data_csv_file is not None:
        rent_data_csv_file = processed_data_dir / Path(rent_data_csv_file)

    # Resale flat data.
    resale_flat_data = ResaleFlatData(processed_data_dir / resale_data_csv_file)
    resale_flat_data.read_csv()
    resale_flat_data.df = resale_flat_data.df.sort_values(["year_month", "town"])

    unique_towns = resale_flat_data.df["town"].unique()
    unique_street_names = resale_flat_data.df["street_name_cleaned"].unique()
    resale_flat_data.df["flat_type"] = resale_flat_data.df["flat_type"].apply(lambda x: x.replace("-", " "))
    resale_flat_data.make_point_geometries(crs = "EPSG:4326")

    # Rent price data.
    rent_data = RentPricesData(processed_data_dir / rent_data_csv_file)
    rent_data.read_csv()
    rent_data.df = rent_data.df.sort_values(["year_month", "town"])

    rent_data.df["flat_type"] = rent_data.df["flat_type"].apply(lambda x: x.replace("-", " "))
    rent_data.make_point_geometries(crs = "EPSG:4326")

    min_year = int(max([resale_flat_data.df["year"].min(), rent_data.df["year"].min()]))
    resale_flat_data.df = resale_flat_data.df[resale_flat_data.df["year"] >= min_year]
    rent_data.df = rent_data.df[rent_data.df["year"] >= min_year]

    # Make time series.
    price_column = config.get("price_column", "price_per_sqft")
    rent_column = config.get("rent_column", "monthly_rent")
