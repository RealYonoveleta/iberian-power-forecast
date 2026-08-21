import requests
import pandas as pd
from datetime import datetime
from precio_electricidad_ml.download.utils import generate_chunks, download_chunks

capitals = {
    "City_Sevilla": {"lat": 37.3891, "lon": -5.9845},
    "City_Zaragoza": {"lat": 41.6488, "lon": -0.8891},
    "City_Oviedo": {"lat": 43.3614, "lon": -5.8494},
    "City_Palma": {"lat": 39.5696, "lon": 2.6502},
    "City_Santa Cruz de Tenerife": {"lat": 28.4636, "lon": -16.2518},
    "City_Santander": {"lat": 43.4623, "lon": -3.8099},
    "City_Toledo": {"lat": 39.8628, "lon": -4.0273},
    "City_Valladolid": {"lat": 41.6523, "lon": -4.7245},
    "City_Barcelona": {"lat": 41.3874, "lon": 2.1686},
    "City_Merida": {"lat": 38.9170, "lon": -6.3444},
    "City_Santiago de Compostela": {"lat": 42.8782, "lon": -8.5448},
    "City_Logrono": {"lat": 42.4627, "lon": -2.4449},
    "City_Madrid": {"lat": 40.4168, "lon": -3.7038},
    "City_Murcia": {"lat": 37.9922, "lon": -1.1307},
    "City_Pamplona": {"lat": 42.8125, "lon": -1.6458},
    "City_Vitoria-Gasteiz": {"lat": 42.8467, "lon": -2.6726},
    "City_Valencia": {"lat": 39.4699, "lon": -0.3763},
}

wind_locations = {
    "Galicia_Wind": {"lat": 42.88, "lon": -8.54},        # Original hub representing coastal and western Galician wind farms
    "Navarra_Wind": {"lat": 42.81, "lon": -1.64},        # Pre-Pyrenees wind corridor with historical high capacity
    "Zaragoza_Wind": {"lat": 41.65, "lon": -0.89},       # Ebro Valley corridor, one of the most consistent wind zones
    "Burgos_Wind": {"lat": 42.34, "lon": -3.70},         # High-altitude plateau wind generation in northern Castile
    "Tarifa_Wind": {"lat": 36.01, "lon": -5.61},         # Strait of Gibraltar, famous for ultra-high wind speeds
    "Albacete_Wind": {"lat": 38.99, "lon": -1.85},       # Core wind generation hub for the southern plains of Castile-La Mancha
    "Lugo_Wind": {"lat": 43.01, "lon": -7.55},           # High-density wind farm cluster in northern Galicia
    "Soria_Wind": {"lat": 41.76, "lon": -2.46},          # High capacity-to-population ratio area in the northern plateau
    "Teruel_Wind": {"lat": 40.34, "lon": -1.10},         # Massive ongoing wind deployment zone in the Maestrazgo region
    "Cadiz_Wind_Interior": {"lat": 36.53, "lon": -6.19}  # Inflow plains behind Tarifa, hosting vast utility-scale wind farms
}


solar_locations = {
    "Caceres_Solar": {"lat": 39.47, "lon": -6.37},       # High irradiance area in northern Extremadura
    "Badajoz_Solar": {"lat": 38.88, "lon": -6.97},       # Major hub featuring some of Europe's largest photovoltaic plants
    "Puertollano_Solar": {"lat": 38.69, "lon": -4.11},    # Industrial solar hub with long-standing PV infrastructure
    "Sevilla_Solar": {"lat": 37.39, "lon": -5.99},       # High solar radiation and massive deployment in the Guadalquivir valley
    "Murcia_Solar": {"lat": 37.99, "lon": -1.13},        # Excellent irradiance within the southeastern Mediterranean basin
    "Ciudad_Real_Solar": {"lat": 38.98, "lon": -3.92},   # Leading province in total installed utility-scale solar capacity
    "Toledo_Solar": {"lat": 39.86, "lon": -4.02},        # Strategic solar generation hub directly feeding the central grid grid
    "Almeria_Solar": {"lat": 36.83, "lon": -2.46},       # Highest number of effective peak sun hours in continental Europe
    "Teruel_Solar": {"lat": 41.11, "lon": -0.42},        # Mega PV projects replacing old coal infrastructure in Andorra-Teruel
    "Alicante_Solar": {"lat": 38.34, "lon": -0.49}       # High solar exposure hub driving eastern Mediterranean generation
}


locations = (
    capitals
    | wind_locations
    | solar_locations
)

url = "https://historical-forecast-api.open-meteo.com/v1/forecast"

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 1, 1)

chunks = generate_chunks(START_DATE, END_DATE)

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

        print(f"Downloading {location}")

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