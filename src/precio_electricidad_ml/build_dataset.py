import pandas as pd

spot_price_features = pd.read_parquet("data/features/spot_price_features.parquet")
meteo_features = pd.read_parquet("data/features/meteo_features.parquet")
demand_features = pd.read_parquet("data/features/demand_features.parquet")
wind_generation_forecast_features = pd.read_parquet("data/features/wind_generation_forecast_features.parquet")
solarpv_generation_forecast_features = pd.read_parquet("data/features/solarpv_generation_forecast_features.parquet")
solarth_generation_forecast_features = pd.read_parquet("data/features/solarth_generation_forecast_features.parquet")

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
        demand_features,
        left_on="target_time",
        right_on="datetime",
        how="inner"
    )
    .drop(columns=["datetime"])
    .merge(
        wind_generation_forecast_features,
        left_on="target_time",
        right_on="datetime",
        how="inner"
    )
    .drop(columns=["datetime"])
    .merge(
        solarpv_generation_forecast_features,
        left_on="target_time",
        right_on="datetime",
        how="inner"
    )
    .drop(columns=["datetime"])
    .merge(
        solarth_generation_forecast_features,
        left_on="target_time",
        right_on="datetime",
        how="inner"
    )
    .drop(columns=["datetime"])
)

df["renewable_generation_forecast"] = (
    df["wind_generation_forecast"]
    + df["solarpv_generation_forecast"]
    + df["solarth_generation_forecast"]
)

df["net_demand"] = df["demand_forecast"] - df["renewable_generation_forecast"]

df["renewable_ratio"] = df["renewable_generation_forecast"] / df["demand_forecast"]

df.to_parquet("data/datasets/training_dataset.parquet")