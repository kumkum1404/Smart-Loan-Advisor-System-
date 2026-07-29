import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BANK_FILE = os.path.join(BASE_DIR, "data", "banks.json")


def get_all_banks():

    with open(BANK_FILE, "r") as f:
        return json.load(f)


def get_best_bank():

    banks = get_all_banks()

    return min(
        banks,
        key=lambda x: x["rate"]
    )