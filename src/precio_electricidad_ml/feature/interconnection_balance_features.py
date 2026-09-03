import pandas as pd

raw_interconnection_df = pd.read_parquet("data/raw/interconnection_balance.parquet")
df = raw_interconnection_df.copy()

# chunked downloads can overlap at year boundaries, producing a second, slightly revised value
df = df.drop_duplicates(subset=["datetime", "border"], keep="last")

df_wide = (
    df.set_index(["datetime", "border"])
    .unstack("border")
)

df_wide.columns = [
    f"interconnection_balance_{border}"
    for _, border
    in df_wide.columns
]

df_wide = df_wide.reset_index()

df_wide = df_wide.drop(
    columns=["interconnection_balance_marruecos", "interconnection_balance_andorra"]
)

balance_columns = [
    c for c in df_wide.columns
    if c.startswith("interconnection_balance_")
]

df_wide["net_interconnection_balance"] = df_wide[balance_columns].sum(axis=1)

# lag/rolling on the net balance only; per-border history is noisier and has bigger data gaps
df_wide["net_interconnection_balance_lag_24h"] = df_wide["net_interconnection_balance"].shift(24)

rolling_24h = (
    df_wide["net_interconnection_balance"]
    .shift(24)
    .rolling(24)
)

df_wide["net_interconnection_balance_rolling_24h_mean"] = rolling_24h.mean()
df_wide["net_interconnection_balance_rolling_24h_std"] = rolling_24h.std()
df_wide["net_interconnection_balance_rolling_24h_mean_diff"] = df_wide["net_interconnection_balance_rolling_24h_mean"].diff()

df_wide = df_wide.dropna()

df_wide.to_parquet("data/features/interconnection_balance_features.parquet")
