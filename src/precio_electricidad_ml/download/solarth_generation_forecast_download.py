from precio_electricidad_ml.download.esios_indicator_download import download_esios_indicator_data

INDICATOR = 543

df = download_esios_indicator_data(INDICATOR)

df = df.rename(columns={"value": "solarth_generation_forecast"})
df = df.sort_values("datetime")
df.to_parquet(f"data/raw/indicator_{INDICATOR}.parquet")