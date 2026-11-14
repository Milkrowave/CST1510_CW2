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
}
KEEP = ["country", "continent", "flag" , "population", "tests", "cases", "deaths", "recovered", "active", "cases/million", "deaths/million", "tests/million"]
MUST_HAVE = ["country"]
RECORDS_KEY = []
RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"

# FUNCTIONS:

def get_data(url, Params):
    """This module takes data from a url"""
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
    return pd.json_normalize(records, sep = "_" )

def tidy_data(df):
    """This module renames and keeps required data in the dataframe"""
    df = df.rename(columns=RENAME)
    df["flag"] = data[2]["countryInfo"]["flag"]
    df = df[KEEP]
    df = df.dropna(subset=MUST_HAVE)
    return df

def save_data(df, path):
    """This module saves the table as a CSV file"""
    path.parent.mkdir(exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")

if __name__ == "__main__":
    data = get_data(URL, PARAMS)
    if data is not None:
        table = make_table(data, RECORDS_KEY)
        table = tidy_data(table)
        print(table.head())
        save_data(table, RAW_FILE)