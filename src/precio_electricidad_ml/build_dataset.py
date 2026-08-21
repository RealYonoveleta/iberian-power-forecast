import pandas as pd

spot_price_features = pd.read_parquet("data/features/spot_price_features.parquet")
meteo_features = pd.read_parquet("data/features/meteo_features.parquet")
demand_features = pd.read_parquet("data/features/demand_features.parquet")

df = spot_price_features.copy()

MAX_HORIZON = 24

datasets = []

for h in range(1, MAX_HORIZON + 1):
    tmp = df.copy()

    tmp["hours_ahead"] = h
    tmp["target"] = tmp["price"].shift(-h)

    future_time = tmp["datetime"] + pd.to_timedelta(h, unit="h")

    tmp["target_time"] = future_time
    tmp["target_hour"] = future_time.dt.hour
    tmp["target_weekday"] = future_time.dt.weekday

    datasets.append(tmp)

df = (
    pd.concat(datasets)
    .dropna()
    .sort_index()
    .rename(columns={"datetime": "prediction_time"})
)

df = (
    df
    .merge(
        meteo_features,
        left_on="target_time",
        right_on="datetime",
        how="inner"
    )
    .drop(columns=["datetime"])
    .merge(
        demand_features,
        left_on="target_time",
        right_on="datetime",
        how="inner"
    )
    .drop(columns=["datetime"])
)

df.to_parquet("data/datasets/training_dataset.parquet")