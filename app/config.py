import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "loan_prediction_secret_key"
    )

    DB_PATH = os.path.join(
        BASE_DIR,
        "instance",
        "loan_prediction.db"
    )

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# class Config:

#     SECRET_KEY = os.getenv(
#         "SECRET_KEY",
#         "loan_prediction_secret_key"
#     )

#     SQLALCHEMY_DATABASE_URI = (
#         "sqlite:///" +
#         os.path.join(BASE_DIR, "..", "instance", "loan_prediction.db")
#     )

#     SQLALCHEMY_TRACK_MODIFICATIONS = False