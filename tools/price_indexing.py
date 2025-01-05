import sys
sys.dont_write_bytecode = True

import yaml

from pathlib import Path
import pandas as pd


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

    