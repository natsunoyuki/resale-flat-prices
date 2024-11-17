# h3-py: Uber's H3 Hexagonal Hierarchical Geospatial Indexing System in Python
# https://uber.github.io/h3-py/intro.html
import h3
import pandas as pd


def cell_grid_ring_monthly_median_price(
    df, 
    h3_index, 
    date_column = "year_month", 
    price_column = "price_per_sqm",
    grid_ring_distance = 1, 
    h3_column_name = "h3",
):
    """
    Certain cells have very few (~2) rows of data. Instead of calculating 
    the median for a single cell, calculate the median for a grid-ring of 7 cells instead!
    Inputs
        df: DataFrame
        h3_index: string
        date_column: string (optional)
        price_column: string (optional)
        grid_ring_distance: int (optional)
        h3_column_name: string (optional)
    Outputs
        median_price: DataFrame
    """
    # 1. Get the grid-ring of cells within grid_ring_distance around the cell of interest.
    k_ring_indices = sorted(list(h3.grid_ring(h3_index, k = grid_ring_distance)))
    
    # 2. Get all rows of data with H3 index in the list of k_ring cells obtained above.
    df = df[df[h3_column_name].isin(k_ring_indices)][[date_column, price_column]]
    
    # 3. Obtain the median price of all those rows of data.
    median_price = df.groupby([date_column]).median().reset_index()
    median_price = median_price.sort_values(date_column)
    # median_price["N"] = len(df)
    return median_price


def grid_ring_monthly_median_price(
    df, 
    date_column = "year_month", 
    price_column = "price_per_sqm",
    grid_ring_distance = 1, 
    h3_column_name = "h3",
):
    """
    Gets the grid-ring median price for all unique H3 indices in the DataFrame.
    Inputs
        df: DataFrame
        date_column: string (optional)
        price_column: string (optional)
        grid_ring_distance: int (optional)
        h3_column_name: string (optional)
    Outputs
        median_price: DataFrame
    """
    h3_indices = df[h3_column_name].unique()
    h3_median_prices = []
    
    for i in range(len(h3_indices)):
        # For each unique h3 index in the data, calculate the median price.
        h3_median_price = cell_grid_ring_monthly_median_price(
            df, 
            h3_indices[i], 
            date_column, 
            price_column,
            grid_ring_distance, 
            h3_column_name,
        )
        h3_median_price[h3_column_name] = h3_indices[i]
        h3_median_prices.append(h3_median_price)
        
    median_prices_df = pd.concat(h3_median_prices, ignore_index = True) 
    return median_prices_df