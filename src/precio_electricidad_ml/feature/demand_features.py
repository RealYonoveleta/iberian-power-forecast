import pandas as pd

raw_demand_df = pd.read_parquet("data/raw/indicator_544.parquet")
df = raw_demand_df.copy()

df.to_parquet("data/features/demand_features.parquet")