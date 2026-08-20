import pandas as pd

raw_meteo_df = pd.read_parquet("data/raw/meteo_data.parquet")
df = raw_meteo_df.copy()

df_wide = (
    df.set_index(["datetime", "location"])
    .unstack("location")
)

df_wide.columns = [
    f"{feature}_{location}"
    for feature, location
    in df_wide.columns
]

df_wide = df_wide.reset_index()

df_wide.to_parquet("data/features/meteo_features.parquet")