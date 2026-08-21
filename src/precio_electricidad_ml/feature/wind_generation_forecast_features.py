import pandas as pd

raw_wind_forecast_df = pd.read_parquet("data/raw/indicator_541.parquet")
df = raw_wind_forecast_df.copy()

df.to_parquet("data/features/wind_generation_forecast_features.parquet")
