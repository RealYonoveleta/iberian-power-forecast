from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
import joblib
from pathlib import Path

raw_dataset = pd.read_parquet("data/datasets/training_dataset.parquet")
df = raw_dataset.copy()

VERSION = "xgboost_v1"

unique_dates = (
    df["prediction_time"]
    .sort_values()
    .unique()
)

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

y_train = train["target"]

X_test = test.drop(
    columns=[
        "prediction_time",
        "target_time",
        "target",
    ]
)

y_test = test["target"]

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)

baseline_preds = X_test["lag_24h"]

baseline_mae = mean_absolute_error(
    y_test,
    baseline_preds
)

print(f"MAE: {mae:.2f}")
print(f"Baseline MAE: {baseline_mae:.2f}")

Path(f"models/info/{VERSION}").mkdir(
    parents=True,
    exist_ok=True
)

feature_importance = pd.Series(
    model.feature_importances_,
    index=X_train.columns
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

def mae_by(period):
    return (
        results
        .groupby(period)["abs_error"]
        .mean()
        .sort_index()
    )


mae_by_horizon = mae_by("hours_ahead")
mae_by_month = mae_by("month")

mae_by_horizon.to_csv(
    f"models/info/{VERSION}/{VERSION}_mae_by_horizon.csv"
)

mae_by_month.to_csv(
    f"models/info/{VERSION}/{VERSION}_mae_by_month.csv"
)