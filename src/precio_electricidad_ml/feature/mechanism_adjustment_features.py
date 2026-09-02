import pandas as pd

raw_mechanism_adjustment_df = pd.read_parquet("data/raw/indicator_10403.parquet")
df = raw_mechanism_adjustment_df.copy()

df.to_parquet("data/features/mechanism_adjustment_features.parquet")
