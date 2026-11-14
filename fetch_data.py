from pathlib import Path
import pandas as pd
import requests

# SETTINGS:

URL = "https://disease.sh/v3/covid-19/countries"
PARAMS = {}

RENAME = {
    "casesPerOneMillion" : "cases/million",
    "deathsPerOneMillion" : "deaths/million",
    "testsPerOneMillion" : "tests/million",
} # Simplifies the names of the columns from the data obtained
KEEP = ["country", "continent", "flag" , "population", "tests", "cases", "deaths", "recovered", "active", "cases/million", "deaths/million", "tests/million"] # columns to be kept
MUST_HAVE = ["country"] # values in this column must be assigned
RECORDS_KEY = []
RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"

# FUNCTIONS:

def get_data(url, Params):
    """This module takes data from a url and returns it in JSON format"""
    try:
        response = requests.get(url, params = Params, timeout = 15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("Could not retrieve data: ", error)
        return None

def make_table(data, RecordsKey):
    """This module makes a dataframe out of the data acquired"""
    records = data[RecordsKey] if RecordsKey else data
    return pd.json_normalize(records, sep = "_" ) # reformats the JSON response with _ as a seperator of each different values

def tidy_data(df):
    """This module renames and keeps required data in the dataframe"""
    df = df.rename(columns=RENAME)
    df["flag"] = data[2]["countryInfo"]["flag"] # assigns "flag" values from the object "countryInfo" to the "flag" column in the dataframe
    df = df[KEEP] # reassigns the dataframe with only the required columns and values
    df = df.dropna(subset=MUST_HAVE) # removes the rows of data which have null values in required fields
    return df # returns the cleaned dataframe

def save_data(df, path):
    """This module saves the table as a CSV file"""
    path.parent.mkdir(exist_ok=True)
    df.to_csv(path, index=False) # saves the dataframe to a csv files withought the indexed positions
    print(f"Saved {len(df)} rows to {path}")

if __name__ == "__main__":
    data = get_data(URL, PARAMS)
    if data is not None:
        # calls the above functions if data has successfully been retrieved
        table = make_table(data, RECORDS_KEY)
        table = tidy_data(table)
        print(table.head())
        save_data(table, RAW_FILE)