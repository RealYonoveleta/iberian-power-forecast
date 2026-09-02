import pandas as pd
from precio_electricidad_ml.download.esios_indicator_download import download_esios_indicator_data

INDICATOR = 10001

# published per-province (33x payload); yearly chunks time out, use monthly + lower concurrency
df = download_esios_indicator_data(INDICATOR, chunk_offset={"months": 1}, max_workers=3)
# sum to a single national hourly figure
df = df.groupby("datetime", as_index=False)["value"].sum()

# recent dates are published at 15-min resolution (Spain's move to quarter-hourly settlement)
df = (
    df.set_index("datetime")
    .resample("1h")
    .mean()
    .reset_index()
)

df = df.rename(columns={"value": "available_generation_capacity"})
df = df.sort_values("datetime")
df.to_parquet("data/raw/available_generation_capacity.parquet")
