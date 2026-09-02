import runpy

# meteo_features is excluded: unused pending a leak-safe rewrite, see repo notes
MODULES = [
    "precio_electricidad_ml.feature.spot_price_features",
    "precio_electricidad_ml.feature.demand_features",
    "precio_electricidad_ml.feature.wind_generation_forecast_features",
    "precio_electricidad_ml.feature.solar_generation_forecast_features",
    "precio_electricidad_ml.feature.solarth_generation_forecast_features",
    "precio_electricidad_ml.feature.interconnection_balance_features",
    "precio_electricidad_ml.feature.mechanism_adjustment_features",
    "precio_electricidad_ml.feature.nuclear_generation_forecast_features",
    "precio_electricidad_ml.feature.hydro_generation_forecast_features",
    "precio_electricidad_ml.feature.available_generation_capacity_features",
]

for module in MODULES:
    print(f"Generating {module}")
    runpy.run_module(module, run_name="__main__")
