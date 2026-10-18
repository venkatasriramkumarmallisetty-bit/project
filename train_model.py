"""Train a simple linear regression model that predicts a student's final marks.

Because no real dataset is supplied, this script generates a synthetic one.
To use real data, replace `make_dataset()` with `pd.read_csv("your_file.csv")`
and keep the same column names.
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "students.csv"
MODEL_PATH = BASE_DIR / "model" / "model.pkl"

FEATURES = ["study_hours", "attendance", "previous_marks", "sleep_hours"]
TARGET = "final_marks"


def make_dataset(n: int = 600, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "study_hours": rng.uniform(0, 10, n).round(1),
            "attendance": rng.uniform(40, 100, n).round(1),
            "previous_marks": rng.uniform(30, 100, n).round(1),
            "sleep_hours": rng.uniform(4, 9, n).round(1),
        }
    )
    noise = rng.normal(0, 4, n)
    df[TARGET] = (
        0.45 * df["previous_marks"]
        + 3.0 * df["study_hours"]
        + 0.18 * df["attendance"]
        + 0.8 * df["sleep_hours"]
        + noise
    ).clip(0, 100).round(1)
    return df


def main() -> None:
    DATA_PATH.parent.mkdir(exist_ok=True)
    MODEL_PATH.parent.mkdir(exist_ok=True)

    df = make_dataset()
    df.to_csv(DATA_PATH, index=False)

    X_train, X_test, y_train, y_test = train_test_split(
        df[FEATURES], df[TARGET], test_size=0.2, random_state=42
    )

    model = LinearRegression().fit(X_train, y_train)
    preds = model.predict(X_test)

    print(f"R2 score : {r2_score(y_test, preds):.3f}")
    print(f"MAE      : {mean_absolute_error(y_test, preds):.2f} marks")

    joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
