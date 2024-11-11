import h3


# Constants involving H3 cell resolution.
# A resolution of 8 results in a hexagonal cell of roughly 1 km2 area and 0.5 km edge length.
def latlon_to_h3(df, resolution = 8):
    """
    Converts latitude and longitude to a specified H3 resolution.
    Inputs
        df: DataFrame
    Outputs
        df: DataFrame
    """
    df["h3"] = df.apply(
        lambda DF: h3.latlng_to_cell(DF["latitude"], DF["longitude"], resolution), 
        axis = 1
    )
    return df