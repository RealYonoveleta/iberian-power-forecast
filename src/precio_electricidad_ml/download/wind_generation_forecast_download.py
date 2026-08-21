import pandas as pd
from precio_electricidad_ml.download.esios_indicator_download import download_esios_indicator_data

INDICATOR = 541

df = download_esios_indicator_data(INDICATOR)

df = df.rename(columns={"value": "wind_generation_forecast"})
df = df.sort_values("datetime")
df.to_parquet("data/raw/indicator_541.parquet")