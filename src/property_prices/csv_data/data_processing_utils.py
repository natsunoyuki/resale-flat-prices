# Clean and perform feature engineering on the loaded resale price DataFrame.

from datetime import datetime
import numpy as np

# Fixed constants.
CURRENT_YEAR = datetime.today().year
  

# Dependent functions for each resale price data feature.
# month
def clean_month(df):
    df["datetime"] = df["month"].apply(
        lambda x: np.datetime64(
            "{}-{:02d}".format(int(x.split("-")[0]), int(x.split("-")[1])), "M",
        ),
    )
    #df["year_month"] = df["month"].copy()
    #df["year"] = df["month"].apply(lambda x: int(x.split("-")[0]))
    #df["month"] = df["month"].apply(lambda x: int(x.split("-")[1]))
    #df["datetime"] = df[["year", "month"]].apply(
    #    lambda DF: np.datetime64("{}-{:02d}".format(DF["year"], DF["month"]), "M"), axis=1
    #)
    return df


# town
def town_cleaner(x):
    if x == "CENTRAL":
        x = "CENTRAL AREA"
    return x

def town_categorizer(x):
    if x == "ANG MO KIO":
        x = 0
    elif x == "BEDOK":
        x = 1
    elif x == "BISHAN":
        x = 2
    elif x == "BUKIT BATOK":
        x = 3
    elif x == "BUKIT MERAH":
        x = 4
    elif x == "BUKIT PANJANG":
        x = 5
    elif x == "BUKIT TIMAH":
        x = 6
    elif x == "CENTRAL AREA":
        x = 7
    elif x == "CHOA CHU KANG":
        x = 8
    elif x == "CLEMENTI":
        x = 9
    elif x == "GEYLANG":
        x = 10
    elif x == "HOUGANG":
        x = 11
    elif x == "JURONG EAST":
        x = 12
    elif x == "JURONG WEST":
        x = 13
    elif x == "KALLANG/WHAMPOA":
        x = 14
    elif x == "LIM CHU KANG":
        x = 15
    elif x == "MARINE PARADE":
        x = 16
    elif x == "PASIR RIS":
        x = 17
    elif x == "PUNGGOL":
        x = 18
    elif x == "QUEENSTOWN":
        x = 19
    elif x == "SEMBAWANG":
        x = 20
    elif x == "SENGKANG":
        x = 21
    elif x == "SERANGOON":
        x = 22
    elif x == "TAMPINES":
        x = 23
    elif x == "TOA PAYOH":
        x = 24
    elif x == "WOODLANDS":
        x = 25
    elif x == "YISHUN":
        x = 26
    else:
        x = -999
    return x


def clean_town(df):
    df["town"] = df["town"].apply(town_cleaner)
    # df["town_cleaned"] = df["town"].apply(town_categorizer)
    return df


# street_name
def street_name_cleaner(x):
    """
    "street_name" is full of abbreviations which sometimes confuse geocoders.
    Replace those abbreviations with their proper forms.
    Inputs
        x: string
    Outputs
        x: string
    """
    if "NTH" in x and "NORTH" not in x:
        x = x.replace("NTH", "NORTH")
    if "STH" in x and "SOUTH" not in x:
        x = x.replace("STH", "SOUTH")
    if " DR" in x and "DRIVE" not in x:
        x = x.replace(" DR", " DRIVE")
    if " RD" in x and "ROAD" not in x:
        x = x.replace(" RD", " ROAD")
    if " ST" in x and "STREET" not in x:
        x = x.replace(" ST", " STREET")
    if " AVE" in x and "AVENUE" not in x:
        x = x.replace(" AVE", " AVENUE")
    if "CTRL" in x and "CENTRAL" not in x:
        x = x.replace("CTRL", "CENTRAL")
    if "CRES" in x and "CRESCENT" not in x:
        x = x.replace("CRES", "CRESCENT")
    if "PL " in x and "PLACE" not in x:
        x = x.replace("PL ", "PLACE ")
    if " PL" in x and "PLAINS" not in x and "PLAZA" not in x:
        x = x.replace(" PL", " PLACE")
    if "BT" in x and "BUKIT" not in x:
        x = x.replace("BT", "BUKIT")
    if "JLN" in x and "JALAN" not in x:
        x = x.replace("JLN", "JALAN")
    if "C'WEALTH" in x and "COMMONWEALTH" not in x:
        x = x.replace("C'WEALTH", "COMMONWEALTH")
    if " CL" in x and "CLOSE" not in x:
        x = x.replace("CL", "CLOSE")
    if "KG" in x and "KAMPONG" not in x:
        x = x.replace("KG", "KAMPONG")
    if "LOR " in x and "LORONG" not in x:
        x = x.replace("LOR ", "LORONG ")
    if "MKT" in x and "MARKET" not in x:
        x = x.replace("MKT", "MARKET")
    if "PK" in x and "PARK" not in x:
        x = x.replace("PK", "PARK")
    if "HTS" in x and "HEIGHTS" not in x:
        x = x.replace("HTS", "HEIGHTS")
    if "UPP " in x and "UPPER" not in x:
        x = x.replace("UPP", "UPPER")
    if "TG" in x and "TANJONG" not in x:
        x = x.replace("TG","TANJONG")
    if " TER" in x and "TERRACE" not in x:
        x = x.replace("TER","TERRACE")
    if "GDNS" in x and "GARDENS" not in x:
        x = x.replace("GDNS","GARDENS")
    if " CTR " in x and "CENTRE" not in x:
        x = x.replace(" CTR ", " CENTRE ")
    return x
    

def clean_street_name(df):
    """
    "street_name" is full of abbreviations which sometimes confuse geocoders.
    Replace those abbreviations with their proper forms.
    Inputs
        df: DataFrame
    Outputs
        df: DataFrame
    """
    df["street_name"] = df["street_name"].apply(street_name_cleaner)
    return df


# address
def make_address(df):
    """
    "address" is formed from "block" and "street_name".
    Inputs
        df: DataFrame
    Outputs
        df: DataFrame
    """
    df["address"] = df["block"] + " " + df["street_name"]
    return df


# flat_type
def flat_type_cleaner(x):
    return x.replace("-", " ")

def flat_type_formatter(x):
    if x == "1 ROOM" or x == "1-ROOM":
        res = 1
    elif x == "2 ROOM" or x == "2-ROOM":
        res = 2
    elif x == "3 ROOM" or x == "3-ROOM":
        res = 3
    elif x == "4 ROOM" or x == "4-ROOM":
        res = 4
    elif x == "5 ROOM" or x == "5-ROOM":
        res = 5
    elif x == "EXECUTIVE" or x == "EXECUTIVE":
        res = 6
    elif x == "MULTI-GENERATION" or x == "MULTI GENERATION":
        res = 7
    else:
        res = -999999 # Error value.
    return res


def clean_flat_type(df):
    """
    Inputs
        df: DataFrame
    Outputs
        df: DataFrame
    """
    df["flat_type"] = df["flat_type"].apply(flat_type_cleaner)
    # df["flat_type_num"] = df["flat_type"].apply(flat_type_formatter)
    return df
    

# storey_range
def storey_range_formatter(x, max_storey = 50):
    lower_storey = int(x[:2])
    upper_storey = int(x[-2:])
    group = (lower_storey + upper_storey) / 2
    return group / max_storey


def clean_storey_range(df):
    df["storey_range_num"] = df["storey_range"].apply(storey_range_formatter)
    return df


# flat_model
def flat_model_formatter(x):
    if x == "TYPE S1":
        pass
    return x


def clean_flat_model(df):
    # Convert everything to upper case for consistency.
    df["flat_model"] = df["flat_model"].apply(lambda x: x.upper())
    return df


# floor_area_sqm
def sqm_to_sqft(x):
    # Convert square metres to square feet.
    return x * 10.7639
    

def sqft_to_sqm(x):
    # Convert square feet to square metres.
    return x / 10.7639


def floor_area_scaler(x, xmin, xmax):
    return (np.log10(x) - np.log10(xmin)) / (np.log10(xmax) - np.log10(xmin))


def clean_floor_area_sqm(df):
    min_floor_area = df["floor_area_sqm"].min()
    max_floor_area = df["floor_area_sqm"].max()
    df["floor_area_norm"] = df["floor_area_sqm"].apply(
        floor_area_scaler, args = (min_floor_area, max_floor_area))
    return df


# resale_price
def get_price_per_sqft(df):
    """
    Calculate the price per square feet for each flat. Feet and inches are superior to SI units.
    """
    df["price_per_sqft"] = df["resale_price"] / df["floor_area_sqm"].apply(sqm_to_sqft)
    df["price_per_sqft"] = df["price_per_sqft"].astype(int)
    return df


def get_price_per_sqm(df):
    """
    Instead of determining the price per flat, it might be a better idea to determine the price
    per square metre.
    """
    df["price_per_sqm"] = df["resale_price"] / df["floor_area_sqm"]
    df["price_per_sqm"] = df["price_per_sqm"].astype(int)
    return df


# lease_commence_date
def age_scaler(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)


def get_age_from_lease_commence_date(df, current_year = CURRENT_YEAR):
    df["age"] = current_year - df["lease_commence_date"]
    return df


def clean_lease_commence_date(df, current_year = CURRENT_YEAR):
    df = get_age_from_lease_commence_date(df, current_year)

    # Scale the age to [0, 1]
    min_age = df["age"].min()
    max_age = df["age"].max()

    df["age"] = df["age"].apply(age_scaler, args = (min_age, max_age))
    return df


# Rent data feature cleaning functions.
def clean_rent_approval_date(df):
    df = df.rename(columns={"rent_approval_date": "month"})
    df["datetime"] = df["month"].apply(
        lambda x: np.datetime64(
            "{}-{:02d}".format(int(x.split("-")[0]), int(x.split("-")[1])), "M",
        ),
    )
    #df["month"] = df["rent_approval_date"].copy()
    #df["year"] = df["month"].apply(lambda x: int(x.split("-")[0]))
    #df["month"] = df["month"].apply(lambda x: int(x.split("-")[1]))
    #df = df.rename(columns = {"rent_approval_date": "year_month"})
    #df["datetime"] = df[["year", "month"]].apply(
    #    lambda DF: np.datetime64("{}-{:02d}".format(DF["year"], DF["month"]), "M"), axis=1
    #)
    return df