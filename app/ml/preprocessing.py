from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def get_preprocessor():

    numeric_features = [
        "Age",
        "Dependents",
        "Monthly_Income",
        "Monthly_Expenses",
        "Existing_EMI",
        "Savings",
        "Credit_Score",
        "Credit_History",
        "Loan_Amount",
        "Loan_Tenure"
    ]

    categorical_features = [
        "Gender",
        "Married",
        "Education",
        "Employment_Type",
        "Loan_Type",
        "Property_Area"
    ]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    return preprocessor