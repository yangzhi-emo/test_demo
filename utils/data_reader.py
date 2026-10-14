
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "test_data.json"

def get_login_cases():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["login_cases"]