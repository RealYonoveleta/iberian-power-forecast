from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
import joblib
from pathlib import Path

raw_dataset = pd.read_parquet("data/datasets/training_dataset.parquet")
df = raw_dataset.copy()

VERSION = "xgboost_v1"

split_date = pd.Timestamp(
    "2025-01-01",
    tz="UTC"
)

train = df[
    df["prediction_time"] < split_date
]

test = df[
    df["prediction_time"] >= split_date
]

X_train = train.drop(
    columns=[
        "prediction_time",
        "target_time",
        "target",
    ]
)

y_train = train["target"] - train["price"]

X_test = test.drop(
    columns=[
        "prediction_time",
        "target_time",
        "target",
    ]
)

y_test = test["target"] - test["price"]

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    random_state=42
)

selected_features = [
    "price", 
    "hours_ahead",
    "price_diff_1h",
    "target_hour", 
    "target_weekday", 
    "target_is_holiday"
]

model.fit(X_train[selected_features], y_train)

delta_preds = model.predict(X_test[selected_features])

preds = X_test["price"] + delta_preds

mae = mean_absolute_error(test["target"], preds)

baseline_mae = y_test.abs().mean()

print(f"MAE: {mae:.2f}")
print(f"Baseline MAE: {baseline_mae:.2f}")

Path(f"models/info/{VERSION}").mkdir(
    parents=True,
    exist_ok=True
)

feature_importance = pd.Series(
    model.feature_importances_,
    index=selected_features
).sort_values(ascending=False)

joblib.dump(
    model,
    f"models/{VERSION}.pkl"
)

feature_importance.rename("importance").to_csv(
    f"models/info/{VERSION}/{VERSION}_features.csv",
    index_label="feature"
)

results = test.copy()

results["prediction"] = preds

results["abs_error"] = (
    results["target"]
    - results["prediction"]
).abs()

results["baseline_abs_error"] = (
    results["target"]
    - results["price"]
).abs()

def mae_by(period, column="abs_error"):
    mae_by_period = (
        results
        .groupby(period)[column]
        .mean()
        .sort_index()
    )

    mae_by_period.to_csv(
        f"models/info/{VERSION}/{VERSION}_{column}_by_{period}.csv"
    )

    return mae_by_period


mae_by_horizon = mae_by("hours_ahead")
mae_by_month = mae_by("month")

baseline_mae_by_horizon = mae_by("hours_ahead", column="baseline_abs_error")