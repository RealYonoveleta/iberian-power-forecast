import pandas as pd

spot_price_features = pd.read_parquet("data/features/spot_price_features.parquet")

FEATURE_FILES = [
    "demand_features",
    "wind_generation_forecast_features",
    "solarpv_generation_forecast_features",
    "solarth_generation_forecast_features",
    "interconnection_balance_features",
    "mechanism_adjustment_features",
    "nuclear_generation_forecast_features",
    "hydro_generation_forecast_features",
    "available_generation_capacity_features",
]

feature_tables = [
    pd.read_parquet(f"data/features/{name}.parquet")
    for name in FEATURE_FILES
]

def merge_feature_tables(df, feature_tables):
    for table in feature_tables:
        df = df.merge(table, left_on="target_time", right_on="datetime", how="inner")
        df = df.drop(columns=["datetime"])
    return df

df = spot_price_features.copy()

MAX_HORIZON = 24

# fixed-date Spain national holidays; regional holidays are out of scope
HOLIDAYS = {
    pd.Timestamp(f"{year}-{month:02d}-{day:02d}").date()
    for year in range(2023, 2027)
    for month, day in [
        (1, 1), (1, 6), (5, 1), (8, 15),
        (10, 12), (11, 1), (12, 6), (12, 8), (12, 25),
    ]
}

datasets = []

for h in range(1, MAX_HORIZON + 1):
    tmp = df.copy()

    tmp["hours_ahead"] = h
    tmp["target"] = tmp["price"].shift(-h)

    future_time = tmp["datetime"] + pd.to_timedelta(h, unit="h")

    tmp["target_time"] = future_time
    tmp["target_hour"] = future_time.dt.hour
    tmp["target_weekday"] = future_time.dt.weekday
    tmp["target_is_holiday"] = future_time.dt.date.isin(HOLIDAYS)

    datasets.append(tmp)

df = (
    pd.concat(datasets)
    .dropna()
    .sort_index()
    .rename(columns={"datetime": "prediction_time"})
)

df = merge_feature_tables(df, feature_tables)

df["renewable_generation_forecast"] = (
    df["wind_generation_forecast"]
    + df["solarpv_generation_forecast"]
    + df["solarth_generation_forecast"]
)

df["net_demand"] = df["demand_forecast"] - df["renewable_generation_forecast"]

# demand not covered by renewables minus scheduled net imports = load domestic dispatchable plants must cover
df["residual_domestic_load"] = df["net_demand"] - df["net_interconnection_balance"]

df["renewable_ratio"] = df["renewable_generation_forecast"] / df["demand_forecast"]

df.to_parquet("data/datasets/training_dataset.parquet")