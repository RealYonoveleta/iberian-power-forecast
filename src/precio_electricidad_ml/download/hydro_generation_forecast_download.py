import pandas as pd
from precio_electricidad_ml.download.esios_indicator_download import download_esios_indicator_data

# P48 scheduled hydro generation, split into large hydro (UGH) and small/non-UGH hydro
INDICATORS = [71, 72]

datasets = [
    download_esios_indicator_data(indicator)
    for indicator in INDICATORS
]

df = pd.concat(datasets)
df = df.groupby("datetime", as_index=False)["value"].sum()

df = df.rename(columns={"value": "hydro_generation_forecast"})
df = df.sort_values("datetime")
df.to_parquet("data/raw/hydro_generation_forecast.parquet")
