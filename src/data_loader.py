import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
bls_api_key = os.getenv("BLS_API_KEY")


solano_series = {
    "unemployment_rate": "LAUCN060950000000003",
    "unemployment": "LAUCN060950000000004",
    "employment": "LAUCN060950000000005",
    "labor_force": "LAUCN060950000000006"
}

def get_solano_data():
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    headers = {"Content-Type": "application/json"}

    payload = {
        "seriesid": list(solano_series.values()),
        "startyear": "2020",
        "endyear": "2025",
        "registrationKey": bls_api_key
    }
    
    response = requests.post(url, json=payload, headers=headers)

    return response.json()


def cleaned_data(data):
    records = []

    for item in data['Results']['series']:
        data_points, series_id = item['data'], item['seriesID']

        for point in data_points:
            records.append((series_id, point['year'], point['period'], point['value']))

    return records 

def clean_dataframe(records):
    clean_df = pd.DataFrame(records, columns=["series_id", "year", "period", "value"])
    clean_df["value"] = pd.to_numeric(clean_df["value"], errors="coerce")
    clean_df["month"] = clean_df["period"].str[1:]
    clean_df["date"] = pd.to_datetime(clean_df["year"] + "-" + clean_df["month"])

    clean_df = clean_df[["series_id", "date", "value"]]
    return clean_df
    
def load_multipliers():
    return pd.read_csv("data/multipliers.csv")


if __name__ == "__main__":
    data = get_solano_data()
    clean = cleaned_data(data)
    normalized = clean_dataframe(clean)
    print(normalized)

    
    multipliers = load_multipliers()
    print(multipliers)
