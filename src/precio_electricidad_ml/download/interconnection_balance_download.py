import pandas as pd
from precio_electricidad_ml.download.esios_indicator_download import download_esios_indicator_data

# P48 scheduled interconnection balance indicators, one per border
BORDERS = {
    10014: "portugal",
    10015: "francia",
    10016: "marruecos",
    10017: "andorra",
}

datasets = []

for indicator, border in BORDERS.items():
    df = download_esios_indicator_data(indicator)
    df["border"] = border
    datasets.append(df)

df = pd.concat(datasets)

df = df.rename(columns={"value": "balance"})
df = df.sort_values("datetime")

df.to_parquet("data/raw/interconnection_balance.parquet")