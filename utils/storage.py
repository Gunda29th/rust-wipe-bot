import json
from pathlib import Path

DATA_FILE = Path("data/schedules.json")


def ensure_data_file():
    """Create schedules.json if it doesn't exist."""
    DATA_FILE.parent.mkdir(exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text("{}", encoding="utf-8")


def load_schedules():
    """Load all saved schedules."""
    ensure_data_file()

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_schedules(data):
    """Save all schedules."""
    ensure_data_file()

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)