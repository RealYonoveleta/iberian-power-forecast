import requests
import pandas as pd
from precio_electricidad_ml.download.utils import generate_chunks, download_chunks

locations = {
    "Sevilla": {"lat": 37.3891, "lon": -5.9845},
    "Zaragoza": {"lat": 41.6488, "lon": -0.8891},
    "Oviedo": {"lat": 43.3614, "lon": -5.8494},
    "Palma": {"lat": 39.5696, "lon": 2.6502},
    "Santa Cruz de Tenerife": {"lat": 28.4636, "lon": -16.2518},
    "Santander": {"lat": 43.4623, "lon": -3.8099},
    "Toledo": {"lat": 39.8628, "lon": -4.0273},
    "Valladolid": {"lat": 41.6523, "lon": -4.7245},
    "Barcelona": {"lat": 41.3874, "lon": 2.1686},
    "Merida": {"lat": 38.9170, "lon": -6.3444},
    "Santiago de Compostela": {"lat": 42.8782, "lon": -8.5448},
    "Logrono": {"lat": 42.4627, "lon": -2.4449},
    "Madrid": {"lat": 40.4168, "lon": -3.7038},
    "Murcia": {"lat": 37.9922, "lon": -1.1307},
    "Pamplona": {"lat": 42.8125, "lon": -1.6458},
    "Vitoria-Gasteiz": {"lat": 42.8467, "lon": -2.6726},
    "Valencia": {"lat": 39.4699, "lon": -0.3763},
}

url = "https://historical-forecast-api.open-meteo.com/v1/forecast"

chunks = generate_chunks(
    "2023-01-01",
    "2026-01-01"
)

def process_chunk(start_date, end_date):
    datasets = []

    for location, coords in locations.items():
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "hourly": ["temperature_2m", "wind_speed_100m", "cloud_cover"],
        }   

        response = requests.get(
            url,
            params=params,
        )

        data = response.json()

        tmp = pd.DataFrame(data["hourly"])
        tmp["location"] = location

        datasets.extend(
            tmp.to_dict("records")
        )

    return datasets

data = download_chunks(chunks, process_chunk)

df = pd.DataFrame(data)

df["datetime"] = pd.to_datetime(
    df["time"],
    utc=True
)

df = df.drop(
    columns=["time"]
)

df["location"] = df["location"].astype("category")

df.to_parquet("data/raw/meteo_data.parquet")