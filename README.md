# Student Marks Predictor

A simple machine learning web app. A linear regression model (scikit-learn) predicts a student's final marks from study hours, attendance, previous marks and sleep hours. The UI is built with Flask, HTML, CSS and JavaScript.

The training data is synthetic and for demonstration only. To use real data, edit `make_dataset()` in `train_model.py` to load your own CSV with the same columns.

## Project structure

```
.
├── app.py               # Flask app (UI + /predict API)
├── train_model.py       # Generates data, trains and saves the model
├── templates/index.html
├── static/style.css
├── static/script.js
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── .gitignore
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                    # trains a missing model, then opens http://localhost:5000

# Optional: train or regenerate the model separately
python train_model.py
```

## Run with Docker

```bash
docker build -t marks-predictor .
docker run -p 5000:5000 marks-predictor
```

Then open http://localhost:5000.

## API

`POST /predict` with JSON:

```json
{"study_hours": 6, "attendance": 85, "previous_marks": 70, "sleep_hours": 7}
```

Response:

```json
{"predicted_marks": 77.4, "grade": "B"}
```

`GET /health` returns `{"status": "ok"}`.
