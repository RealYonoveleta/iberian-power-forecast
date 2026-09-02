import pandas as pd

raw_hydro_forecast_df = pd.read_parquet("data/raw/hydro_generation_forecast.parquet")
df = raw_hydro_forecast_df.copy()

df.to_parquet("data/features/hydro_generation_forecast_features.parquet")
