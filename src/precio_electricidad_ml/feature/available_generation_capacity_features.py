import pandas as pd

raw_available_capacity_df = pd.read_parquet("data/raw/available_generation_capacity.parquet")
df = raw_available_capacity_df.copy()

df.to_parquet("data/features/available_generation_capacity_features.parquet")
