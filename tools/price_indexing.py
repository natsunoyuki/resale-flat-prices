import sys
sys.dont_write_bytecode = True

import yaml

from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor

from resale_flat_prices.resale_flat_data.resale_flat_data import ResaleFlatData
from resale_flat_prices.resale_flat_data.rent_prices_data import RentPricesData


if __name__ == "__main__":
    tools_dir = Path(__file__).parent
    main_dir = tools_dir.parent

    with open(tools_dir / "price_indexing.yml", "r") as f:
        config = yaml.safe_load(f)

    # Data directories and files.
    processed_data_dir = main_dir / config.get("processed_data_dir", "data/processed_data/")

    resale_data_csv_file = config.get("resale_data_csv_file", "resale-flat-prices.csv.zip")

    output_resale_data_csv_file = config.get("output_resale_data_csv_file", "resale-flat-prices-indexed.csv.zip")

    rent_data_csv_file = config.get("rent_data_csv_file", None)
    if rent_data_csv_file is not None:
        rent_data_csv_file = Path(rent_data_csv_file)
        output_rent_data_csv_file = config.get("output_rent_data_csv_file", "rent-prices.csv-indexed.zip")

    price_column = config.get("price_column", "price_per_sqft")
    rent_column = config.get("rent_column", "monthly_rent")


    # Resale flat data.
    resale_flat_data = ResaleFlatData(processed_data_dir / resale_data_csv_file)
    resale_flat_data.read_csv()
    resale_flat_data.df["datetime"] = resale_flat_data.df["datetime"].apply(lambda x: np.datetime64(x))
    resale_flat_data.df = resale_flat_data.df.sort_values(["datetime", "town"])

    unique_towns = resale_flat_data.df["town"].unique()
    unique_street_names = resale_flat_data.df["street_name_cleaned"].unique()
    resale_flat_data.df["flat_type"] = resale_flat_data.df["flat_type"].apply(lambda x: x.replace("-", " "))
    resale_flat_data.make_point_geometries(crs = "EPSG:4326")

    min_year = int(resale_flat_data.df["year"].min())
    min_datetime = resale_flat_data.df["datetime"].min()
    max_datetime = resale_flat_data.df["datetime"].max()


    # Rent price data.
    if rent_data_csv_file is not None:
        rent_data = RentPricesData(processed_data_dir / rent_data_csv_file)
        rent_data.read_csv()
        rent_data.df["datetime"] = rent_data.df["datetime"].apply(lambda x: np.datetime64(x))
        rent_data.df = rent_data.df.sort_values(["datetime", "town"])

        rent_data.df["flat_type"] = rent_data.df["flat_type"].apply(lambda x: x.replace("-", " "))
        rent_data.make_point_geometries(crs = "EPSG:4326")

        min_year = int(max([resale_flat_data.df["year"].min(), rent_data.df["year"].min()]))
        min_datetime = max(min_datetime, rent_data.df["datetime"].min())
        max_datetime = max(max_datetime, rent_data.df["datetime"].max())

        rent_data.df = rent_data.df[rent_data.df["year"] >= min_year]
    else:
        rent_data = None

    resale_flat_data.df = resale_flat_data.df[resale_flat_data.df["year"] >= min_year]

    print("    Loaded resale_flat_data.df.shape: {}.".format(resale_flat_data.df.shape))
    if rent_data is not None:
        print("    Loaded rent_data.df.shape: {}.".format(rent_data.df.shape))


    # Make time series.
    datetime_df = pd.DataFrame(
        {
            "datetime": np.arange(
                min_datetime, max_datetime + np.timedelta64(31, "D"), dtype = 'datetime64[M]'
            )
        }
    )
    datetime_df["X"] = np.arange(1, len(datetime_df) + 1, 1) / len(datetime_df)

    dfs = {}
    dfs_rent = {}
    for s in unique_street_names:
        if np.sum(resale_flat_data.df["street_name_cleaned"] == s) > 0:
            dfs[s] = resale_flat_data.df[resale_flat_data.df["street_name_cleaned"] == s]
            dfs[s] = dfs[s][["datetime", price_column]].groupby(["datetime"]).median().reset_index()
            dfs[s] = pd.merge(
                datetime_df, dfs[s], left_on = ["datetime"], right_on = ["datetime"], how = "left"
            )
            dfs[s] = dfs[s].dropna()
    
        if rent_data is not None:
            if np.sum(rent_data.df["street_name_cleaned"] == s) > 0:
                dfs_rent[s] = rent_data.df[rent_data.df["street_name_cleaned"] == s]
                dfs_rent[s] = dfs_rent[s][["datetime", rent_column]].groupby(["datetime"]).median().reset_index()
                dfs_rent[s] = pd.merge(
                    datetime_df, dfs_rent[s], left_on = ["datetime"], right_on = ["datetime"], how = "left"
                )
                dfs_rent[s] = dfs_rent[s].dropna()

    print("    {} unique resale street names.".format(len(dfs.keys())))
    if rent_data is not None:
        print("    {} unique rent street names.".format(len(dfs_rent.keys())))

    X_pred_months = datetime_df["datetime"].values.astype("datetime64[M]")
    X_pred = datetime_df["X"].values
    X_pred = X_pred.reshape(-1, 1)

    future_months = config.get("future_months", 1)
    for i in range(future_months):
        X_pred_months = np.hstack([X_pred_months, X_pred_months[-1] + 1])
        X_pred = np.vstack([X_pred, X_pred[-1] + (X_pred[-1] - X_pred[-2])])

    
    # Resale price indexing model training.
    n_estimators = config.get("n_estimators", 10)
    max_depth = config.get("max_depth", 2)
    max_depth_low_data = config.get("max_depth_low_data", 1)
    low_data_threshold = config.get("low_data_threshold", 10)
    criterion = config.get("criterion", "absolute_error")

    models = {}
    y_preds = {}
    scores = {}
    for k in dfs.keys():
        y = dfs[k]["price_per_sqft"].values
        X = dfs[k]["X"].values.reshape(-1, 1)
        if len(y) >= low_data_threshold:
            models[k] = RandomForestRegressor(
                n_estimators=n_estimators, max_depth=max_depth, criterion=criterion
            )
        else:
            models[k] = RandomForestRegressor(
                n_estimators=n_estimators, max_depth=max_depth_low_data, criterion=criterion
            )
            
        models[k].fit(X, y)
        y_pred = models[k].predict(X)
        dfs[k]["prediction"] = y_pred
        y_pred = y_pred / y_pred[-1]
        dfs[k]["price_index"] = y_pred
        y_preds[k] = models[k].predict(X_pred)
        scores[k] = r2_score(y, models[k].predict(X))


    # Rent indexing model training.
    if rent_data is not None:
        models_rent = {}
        y_preds_rent = {}
        scores_rent = {}
        for k in dfs_rent.keys():
            y = dfs_rent[k][rent_column].values
            X = dfs_rent[k]["X"].values.reshape(-1, 1)
            if len(y) >= low_data_threshold:
                models_rent[k] = RandomForestRegressor(
                    n_estimators=n_estimators, max_depth=max_depth, criterion=criterion
                )
            else:
                models_rent[k] = RandomForestRegressor(
                    n_estimators=n_estimators, max_depth=max_depth_low_data, criterion=criterion
                )
            models_rent[k].fit(X, y)
            y_pred = models_rent[k].predict(X)
            dfs_rent[k]["prediction"] = y_pred
            y_pred = y_pred / y_pred[-1]
            dfs_rent[k]["rent_index"] = y_pred
            y_preds_rent[k] = models_rent[k].predict(X_pred)
            scores_rent[k] = r2_score(y, models_rent[k].predict(X))


    # Update price DataFrames with price indexes.
    price_index_df = pd.DataFrame()
    for k in dfs.keys():
        _df = dfs[k][["datetime", "price_index"]].copy()
        _df["street_name_cleaned"] = k
        price_index_df = pd.concat([price_index_df, _df])

    if rent_data is not None:
        rent_index_df = pd.DataFrame()
        for k in dfs_rent.keys():
            _df = dfs_rent[k][["datetime", "rent_index"]].copy()
            _df["street_name_cleaned"] = k
            rent_index_df = pd.concat([rent_index_df, _df])

    resale_flat_data_indexed_df = resale_flat_data.df.merge(
        price_index_df, 
        how = "left", 
        left_on=["datetime", "street_name_cleaned"],
        right_on=["datetime", "street_name_cleaned"],
    )
    assert len(resale_flat_data.df) == len(resale_flat_data_indexed_df)

    if rent_data is not None:
        rent_data_indexed_df = rent_data.df.merge(
            rent_index_df,
            how = "left",
            left_on=["datetime", "street_name_cleaned"],
            right_on=["datetime", "street_name_cleaned"],
        )
        assert len(rent_data.df) == len(rent_data_indexed_df)


    # Output indexed prices to disk.
    if output_resale_data_csv_file[-3:] == "zip":
        compression = "zip"
    else:
        compression = None
    print("    Saving indexed resale flat prices data to {}.".format(processed_data_dir / output_resale_data_csv_file))
    resale_flat_data_indexed_df.to_csv(
        processed_data_dir / output_resale_data_csv_file, index = False, compression = compression
    )

    if rent_data is not None:
        if output_rent_data_csv_file[-3:] == "zip":
            compression = "zip"
        else:
            compression = None
        print("    Saving indexed rent prices data to {}.".format(processed_data_dir / output_rent_data_csv_file))
        rent_data_indexed_df.to_csv(
            processed_data_dir / output_rent_data_csv_file, index = False, compression = compression
        )
