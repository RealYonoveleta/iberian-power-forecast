import pandas as pd

raw_demand_df = pd.read_parquet("data/raw/indicator_544.parquet")
df = raw_demand_df.copy()

# lags (shift >= MAX_HORIZON in build_dataset.py, so always <= prediction_time)
df["demand_lag_24h"] = df["demand_forecast"].shift(24)
df["demand_lag_48h"] = df["demand_forecast"].shift(48)
df["demand_lag_1w"] = df["demand_forecast"].shift(24 * 7)

# windows
rolling_24h = (
    df["demand_forecast"]
    .shift(24)
    .rolling(24)
)

df["demand_rolling_24h_mean"] = rolling_24h.mean()
df["demand_rolling_24h_std"] = rolling_24h.std()
df["demand_rolling_24h_mean_diff"] = df["demand_rolling_24h_mean"].diff()

rolling_1w = (
    df["demand_forecast"]
    .shift(24)
    .rolling(24 * 7)
)

df["demand_rolling_1w_mean"] = rolling_1w.mean()
df["demand_rolling_1w_std"] = rolling_1w.std()
df["demand_rolling_1w_mean_diff"] = df["demand_rolling_1w_mean"].diff()

df = df.dropna()

df.to_parquet("data/features/demand_features.parquet")