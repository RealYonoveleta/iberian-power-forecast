from precio_electricidad_ml.esios import request_esios_indicator
from datetime import datetime
import pandas as pd
from precio_electricidad_ml.download.utils import generate_chunks, download_chunks

TOKEN = "1b6edff118e8b67af659702f3f89aef846b9e3452ef795f3008885c5780c4a46"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-api-key": TOKEN
}

INDICATOR = 600
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 1, 1)
SPAIN_GEO_ID = 3

chunks = generate_chunks(START_DATE, END_DATE)

print(chunks)

def process_cunk(start, end):
    params = {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "geo_ids[]": [SPAIN_GEO_ID],
    }

    data = request_esios_indicator(INDICATOR, params=params)

    spain = [row for row in data["indicator"]["values"]]

    return spain

data = download_chunks(chunks, process_cunk)

df = pd.DataFrame(data)

df = df[["datetime", "value"]]
df = df.rename(columns={"value": "price"})
df["datetime"] = pd.to_datetime(
    df["datetime"],
    utc=True
)

spot_price = df.sort_values("datetime")

spot_price.to_parquet("data/raw/indicator_600.parquet")