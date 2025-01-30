<div align = "center"><img src = "assets/resale-flat-prices.jpg" width = "640"></div>

# Singapore Property Resale and Rent Prices
Analysis and predictive modelling for Singapore property resale prices and rents.

Main data sources for resale prices and rents:
1. Resale flat prices: https://data.gov.sg/collections/189/view.
2. Flat rent prices: https://data.gov.sg/datasets/d_c9f57187485a850908655db0e8cfe651/view

Additional data sources for handling geocoded addresses:
3. HDB existing building information: https://data.gov.sg/collections/2033/view
4. LTA road name road code information: https://www.lta.gov.sg/content/dam/ltagov/industry_innovations/industry_matters/development_construction_resources/Street_Work_Proposals/Standards_and_Specifications/GIS_Data_Hub/road_name_road_code_jan2024.xlsx

This repository is currently a work in progress.

# Installation
Clone this repository, and install locally with a virtual environment.
```bash
git clone https://github.com/natsunoyuki/sg-property-prices
cd sg-property-prices

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools
pip install -e .
```

# Usage

## HDB Building Information Preparation
The raw resale and rent data only provides location information in the form of street addresses. In-depth analysis usually requires more precise representations of addresses, such as the geospatial coordinates. While it is possible to use geocoders such as <a href = "https://nominatim.org">Nominatim</a> to perform geocoding of street addresses, we can also make full use of published HDB existing building and LTA road name information to obtain the same information. 

The script `tools/hdb_building_info.py` prepares HDB building information and LTA road name information for geocoding street addresses in the resale and rent data processing pipeline. Place the downloaded HDB existing building information GeoJSON file under `data/HDBExistingBuilding/`, and the downloaded LTA road name road code information Excel file under `data/RoadNameRoadCode/`. 

Then, specify the pipeline configuration in `tools/hdb_building_info.yml` and run the script:
```bash
python3 tools/hdb_building_info.py
```
This script loads the GeoJSON and Excel files, processes their contents, and saves them to the GeoJSON file `data/processed_data/hdb_addresses.json`. This GeoJSON file will be used in the resale and rent data processing pipelie for geocoding HDB street coordinates.

## Raw Resale and Rent Data Processing Pipeline
Before any form of analysis or visualization can be performed, the raw resale and rent prices data must be cleaned and combined with other useful data, such as the HDB building information (geocoded address information). The script `tools/raw_data_pipeline.py` performs this function.

Place the downloaded raw CSV files under `data/ResaleFlatPrices`. Additionally, if pre-existing geocoded addresses already exist, they should be placed in the GeoJSON file `data/processed_data/hdb_addresses.json`.

Then, specify the pipeline configuration in `tools/hdb_data_pipeline.yml`, and run the script:
```bash
python3 tools/hdb_data_pipeline.py
```
This script loads the raw CSV files and processes their contents, as well as any pre-existing geocoded addresses. New addresses are geocoded using the Nominatim geocoder, and added to `hdb_addresses.json`. The processed CSV contents are then merged with the geocoded addresses, and the processed resale prices and rent data are saved to `data/processed_data/resale-flat-prices.parquet` and `data/processed_data/rent-prices.parquet` respectively. These files can be used for further resale and rent price analyses.
