import pandas as pd

raw_nuclear_forecast_df = pd.read_parquet("data/raw/indicator_74.parquet")
df = raw_nuclear_forecast_df.copy()

df.to_parquet("data/features/nuclear_generation_forecast_features.parquet")
