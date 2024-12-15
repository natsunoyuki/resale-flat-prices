<div align = "center"><img src = "assets/resale-flat-prices.jpg" width = "640"></div>

# Resale Flat Prices
Analysis and predictive modelling using resale flat prices.

1. Resale flat prices: https://data.gov.sg/collections/189/view.
2. Flat rent prices: https://data.gov.sg/datasets/d_c9f57187485a850908655db0e8cfe651/view

This repository is currently a work in progress.

# Installation
Clone this repository, and install locally with a virtual environment.
```bash
git clone https://github.com/natsunoyuki/resale-flat-prices
cd resale-flat-prices

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools
pip install -e .
```

# Usage

## Raw Data Processing Pipeline
Before any form of analysis or visualization can be performed, raw data must be cleaned and processed, and combined with other useful data. The script `tools/data_pipeline.py` performs this important function.

Place the downloaded raw CSV files in the directory `data/ResaleFlatPrices`. Additionally, if pre-existing geocoded addresses already exist, they should be placed in the JSON file `data/processed_data/geocoded_addresses.json`.

Then, specify the pipeline configurations in `tools/data_pipeline.yml`, and run the script:
```bash
python3 tools/data_pipeline.py
```

This script loads the raw CSV files and processes their contents, as well as any pre-existing geocoded addresses. New addresses are geocoded using the `Nominatim` geocoder, and added to `geocoded_addresses.json`. The processed CSV contents are then merged with the geocoded addresses, and the processed data is saved to `data/processed_data/resale-flat-prices.csv.zip`. This data can be used for downstream analysis or visualization tasks.
