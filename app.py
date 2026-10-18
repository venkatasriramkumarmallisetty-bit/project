from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "model.pkl"

app = Flask(__name__)

def load_model():
    """Load the model, training it if the generated artifact is absent."""
    if not MODEL_PATH.exists():
        from train_model import main as train
        train()
    artifact = joblib.load(MODEL_PATH)
    return artifact["model"], artifact["features"]


model, FEATURES = load_model()

# Allowed range for each input (min, max)
LIMITS = {
    "study_hours": (0, 16),
    "attendance": (0, 100),
    "previous_marks": (0, 100),
    "sleep_hours": (0, 12),
}

FIELD_SETTINGS = {
    "study_hours": {"step": 0.5, "default": 5},
    "attendance": {"step": 1, "default": 80},
    "previous_marks": {"step": 1, "default": 60},
    "sleep_hours": {"step": 0.5, "default": 7},
}


def grade_for(marks: float) -> str:
    if marks >= 90:
        return "A+"
    if marks >= 80:
        return "A"
    if marks >= 70:
        return "B"
    if marks >= 60:
        return "C"
    if marks >= 40:
        return "D"
    return "F"


@app.route("/")
def index():
    fields = [
        {"name": name, "min": LIMITS[name][0], "max": LIMITS[name][1], **FIELD_SETTINGS[name]}
        for name in FEATURES
    ]
    return render_template("index.html", fields=fields)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    values = {}

    for name in FEATURES:
        try:
            value = float(data[name])
        except (KeyError, TypeError, ValueError):
            return jsonify(error=f"'{name}' is missing or not a number."), 400

        low, high = LIMITS[name]
        if not low <= value <= high:
            return jsonify(error=f"'{name}' must be between {low} and {high}."), 400
        values[name] = value

    frame = pd.DataFrame([values], columns=FEATURES)
    marks = float(model.predict(frame)[0])
    marks = round(min(max(marks, 0), 100), 1)

    return jsonify(predicted_marks=marks, grade=grade_for(marks))


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
