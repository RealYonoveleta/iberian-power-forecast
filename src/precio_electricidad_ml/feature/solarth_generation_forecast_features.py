import pandas as pd

raw_solarpv_forecast_df = pd.read_parquet("data/raw/indicator_543.parquet")
df = raw_solarpv_forecast_df.copy()

df.to_parquet("data/features/solarth_generation_forecast_features.parquet")
