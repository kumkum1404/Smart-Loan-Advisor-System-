import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def update_bank_rates():

    banks = [

        {
            "name": "State Bank of India",
            "rate": 8.35,
            "processing_fee": "0.35%",
            "tenure": 30,
            "rating": 4.8
        },

        {
            "name": "HDFC Bank",
            "rate": 8.50,
            "processing_fee": "0.50%",
            "tenure": 30,
            "rating": 4.7
        },

        {
            "name": "ICICI Bank",
            "rate": 8.60,
            "processing_fee": "0.50%",
            "tenure": 25,
            "rating": 4.6
        },

        {
            "name": "Axis Bank",
            "rate": 8.70,
            "processing_fee": "0.45%",
            "tenure": 25,
            "rating": 4.5
        }

    ]

    path = os.path.join(
        BASE_DIR,
        "data",
        "banks.json"
    )

    with open(path, "w") as file:

        json.dump(
            banks,
            file,
            indent=4
        )

    print("✅ Bank data updated successfully.")


if __name__ == "__main__":

    update_bank_rates()