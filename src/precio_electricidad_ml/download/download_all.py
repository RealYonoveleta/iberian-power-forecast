import runpy

# meteo_data_download is excluded: unused pending a leak-safe rewrite, see repo notes
MODULES = [
    "precio_electricidad_ml.download.elec_data_download",
    "precio_electricidad_ml.download.demand_data_download",
    "precio_electricidad_ml.download.wind_generation_forecast_download",
    "precio_electricidad_ml.download.solar_generation_forecast_download",
    "precio_electricidad_ml.download.solarth_generation_forecast_download",
    "precio_electricidad_ml.download.interconnection_balance_download",
    "precio_electricidad_ml.download.mechanism_adjustment_download",
    "precio_electricidad_ml.download.nuclear_generation_forecast_download",
    "precio_electricidad_ml.download.hydro_generation_forecast_download",
    "precio_electricidad_ml.download.available_generation_capacity_download",
]

for module in MODULES:
    print(f"Downloading {module}")
    runpy.run_module(module, run_name="__main__")
