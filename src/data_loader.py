import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
bls_api_key = os.getenv("BLS_API_KEY")


#solano series id with the appropiate type it's measuring
solano_series = {
    "unemployment_rate": "LAUCN060950000000003",
    "unemployment": "LAUCN060950000000004",
    "employment": "LAUCN060950000000005",
    "labor_force": "LAUCN060950000000006"
}

#retrive data from bls api 
def get_solano_data():
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


    headers = {"Content-Type": "application/json"}

    #requesting solano series matching the specific series ID from 2020-2025 with specified api key
    request_data = {
        "seriesid": list(solano_series.values()),
        "startyear": "2020",
        "endyear": "2025",
        "registrationKey": bls_api_key
    }
    
    retrieved = requests.post(url, json=request_data, headers=headers)

    return retrieved.json()


#clean up the json data into a list of tuples
def cleaned_data(data):
    records = []

    #loops through to seperate data points from their series id
    #i.e. launch... gets seperated with it's corresponding data for unemployement(UE) and rate, employment and labor force
    #each data point has a subsequent year, period, periodName, and value
    for item in data['Results']['series']:
        data_points, series_id = item['data'], item['seriesID']

        #inner loop then seperates the data points into individual items
        for point in data_points:
            records.append((series_id, point['year'], point['period'], point['value']))

    return records 


#takes the list of tuples and makes it into a cleaned pandas table
def clean_dataframe(records):
    #seperates series id, year, period, and value into their own columns
    clean_df = pd.DataFrame(records, columns=["series_id", "year", "period", "value"])

    #converts value to a number 
    clean_df["value"] = pd.to_numeric(clean_df["value"], errors="coerce")

    #starts the table at second index since bls data are framed M01...
    clean_df["month"] = clean_df["period"].str[1:]

    #gives proper datetime framing for all dates
    clean_df["date"] = pd.to_datetime(clean_df["year"] + "-" + clean_df["month"])


    clean_df = clean_df[["series_id", "date", "value"]]
    return clean_df



def load_multipliers():
    return pd.read_csv("data/multipliers.csv")

def load_timeline():
    return pd.read_csv("data/growth_timeline.csv")


if __name__ == "__main__":
    data = get_solano_data()
    clean = cleaned_data(data)
    normalized = clean_dataframe(clean)
    print(normalized)


    timeline = load_timeline
    print(timeline)
    multipliers = load_multipliers()
    print(multipliers)
