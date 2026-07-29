import json
import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from preprocessing import get_preprocessor


# -------------------------------
# PATHS
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR.parent.parent / "dataset" / "custom_loan_dataset.csv"

MODEL_PATH = BASE_DIR / "model.pkl"

PREPROCESSOR_PATH = BASE_DIR / "preprocessor.pkl"

METRICS_PATH = BASE_DIR / "metrics.json"


# -------------------------------
# LOAD DATA
# -------------------------------

print("Loading Dataset...")
df = pd.read_csv(DATASET_PATH)
print(df.head())


# -------------------------------
# FEATURES
# -------------------------------

X = df.drop(
    columns=[
        "Loan_Status",
        "Debt_Ratio",
        "Savings_Ratio",
        "Financial_Score"
    ]
)

y = df["Loan_Status"]


# -------------------------------
# TRAIN TEST SPLIT
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)


# -------------------------------
# PREPROCESSOR
# -------------------------------

preprocessor = get_preprocessor()


# -------------------------------
# MODELS
# -------------------------------

models = {

    "Logistic Regression": LogisticRegression(max_iter=1000),

    "Decision Tree": DecisionTreeClassifier(random_state=42),

    "Random Forest": RandomForestClassifier(

        n_estimators=200,

        random_state=42

    ),

    "Gradient Boosting": GradientBoostingClassifier(

        random_state=42

    ),

    "SVM": SVC(

        probability=True,

        random_state=42

    )

}


best_model = None
best_name = None
best_accuracy = 0
best_pipeline = None
metrics = {}
print("\nTraining Started...\n")

for name, model in models.items():
    print(f"Training {name}...")
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)
    prediction = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, prediction)
    precision = precision_score(
        y_test,
        prediction,
        pos_label="Approved"

    )

    recall = recall_score(

        y_test,

        prediction,

        pos_label="Approved"

    )

    f1 = f1_score(

        y_test,

        prediction,

        pos_label="Approved"

    )

    print(f"Accuracy : {accuracy*100:.2f}%")

    print("--------------------------------")

    metrics[name] = {

        "accuracy": round(accuracy * 100, 2),

        "precision": round(precision * 100, 2),

        "recall": round(recall * 100, 2),

        "f1_score": round(f1 * 100, 2)

    }

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model

        best_name = name

        best_pipeline = pipeline


# -------------------------------
# SAVE MODEL
# -------------------------------

joblib.dump(best_pipeline, MODEL_PATH)

joblib.dump(preprocessor, PREPROCESSOR_PATH)


# -------------------------------
# SAVE METRICS
# -------------------------------

final_metrics = {

    "best_model": best_name,

    "accuracy": round(best_accuracy * 100, 2),

    "all_models": metrics

}

with open(METRICS_PATH, "w") as file:

    json.dump(final_metrics, file, indent=4)


# -------------------------------
# RESULT
# -------------------------------

print("\n=================================")

print("Training Completed Successfully")

print(f"Best Model : {best_name}")

print(f"Accuracy : {best_accuracy*100:.2f}%")

print("=================================")

print("\nFiles Saved")

print("✔ model.pkl")

print("✔ preprocessor.pkl")

print("✔ metrics.json")