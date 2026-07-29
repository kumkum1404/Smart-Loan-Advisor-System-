import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model.pkl"

model = joblib.load(MODEL_PATH)

def predict_loan(data):

    df = pd.DataFrame([data])

    prediction = model.predict(df)[0]

    probabilities = model.predict_proba(df)[0]

    classes = model.classes_

    confidence = round(
        probabilities[list(classes).index(prediction)] * 100,
        2
    )

    return str(prediction), confidence