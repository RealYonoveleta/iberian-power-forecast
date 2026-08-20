import pandas as pd

df = pd.read_parquet("data/raw/indicator_600.parquet")

# calendar
df["month"] = df["datetime"].dt.month
df["weekday"] = df["datetime"].dt.weekday
df["hour"] = df["datetime"].dt.hour

# lags
df["lag_24h"] = df["price"].shift(24)
df["lag_48h"] = df["price"].shift(48)
df["lag_1w"] = df["price"].shift(24 * 7)

# windows
rolling_24h = (
    df["price"]
    .shift(24)
    .rolling(24)
)

df["rolling_24h_mean"] = rolling_24h.mean()
df["rolling_24h_std"] = rolling_24h.std()
df["rolling_24h_mean_diff"] = df["rolling_24h_mean"].diff()

rolling_1w = (
    df["price"]
    .shift(24)
    .rolling(24 * 7)
)

df["rolling_1w_mean"] = rolling_1w.mean()
df["rolling_1w_std"] = rolling_1w.std()
df["rolling_1w_mean_diff"] = df["rolling_1w_mean"].diff()

df = df.dropna()

df.to_parquet("data/features/spot_price_features.parquet")