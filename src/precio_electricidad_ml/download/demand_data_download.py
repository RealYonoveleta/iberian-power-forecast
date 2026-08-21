import pandas as pd
from datetime import datetime
from precio_electricidad_ml.esios import request_esios_indicator
from precio_electricidad_ml.download.utils import generate_chunks, download_chunks

INDICATOR = 544
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 1, 1)

chunks = generate_chunks(START_DATE, END_DATE)

def process_chunk(start_date, end_date):

    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "time_trunc": "hour",
        "time_agg": "average"
    }

    data = request_esios_indicator(INDICATOR, params=params)

    return [row for row in data["indicator"]["values"]]

data = download_chunks(chunks, process_chunk)

df = pd.DataFrame(data)

df["datetime"] = pd.to_datetime(
    df["datetime"],
    utc=True
)

df = df[["datetime", "value"]]

df = df.rename(columns={"value": "demand"})

df = df.sort_values("datetime")

df.to_parquet("data/raw/indicator_544.parquet")