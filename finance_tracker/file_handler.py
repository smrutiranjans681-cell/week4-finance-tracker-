import os
import json
import csv
import shutil
from datetime import datetime
from typing import List, Dict, Any
from finance_tracker.expense import Expense

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
JSON_PATH = os.path.join(DATA_DIR, "expenses.json")
BACKUP_DIR = os.path.join(DATA_DIR, "backup")
EXPORT_DIR = os.path.join(DATA_DIR, "exports")

def ensure_directories():
    """Ensures necessary data and backup folders exist."""
    for path in [DATA_DIR, BACKUP_DIR, EXPORT_DIR]:
        os.makedirs(path, exist_ok=True)

def load_data() -> Dict[str, Any]:
    """Loads JSON database safely using context manager."""
    ensure_directories()
    if not os.path.exists(JSON_PATH):
        return {"budget": 0.0, "expenses": []}

    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"\n[Warning] Failed to read {JSON_PATH}: {e}. Returning empty state.")
        return {"budget": 0.0, "expenses": []}

def save_data(data: Dict[str, Any]) -> bool:
    """Saves state to JSON atomically using context manager."""
    ensure_directories()
    try:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except IOError as e:
        print(f"\n[Error] Failed to write data to file: {e}")
        return False

def create_backup() -> str:
    """Creates a timestamped backup copy of the JSON data file."""
    ensure_directories()
    if not os.path.exists(JSON_PATH):
        raise FileNotFoundError("Cannot create backup: Data file does not exist.")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"expenses_backup_{timestamp}.json"
    backup_filepath = os.path.join(BACKUP_DIR, backup_filename)
    
    shutil.copy2(JSON_PATH, backup_filepath)
    return backup_filepath

def restore_backup(backup_filename: str) -> bool:
    """Restores database state from a backup file."""
    backup_filepath = os.path.join(BACKUP_DIR, backup_filename)
    if not os.path.exists(backup_filepath):
        raise FileNotFoundError(f"Backup file '{backup_filename}' not found.")
    
    shutil.copy2(backup_filepath, JSON_PATH)
    return True

def export_to_csv(expenses: List[Expense], filename: str = "expenses_export.csv") -> str:
    """Exports list of expenses into CSV format using csv.DictWriter."""
    ensure_directories()
    filepath = os.path.join(EXPORT_DIR, filename)
    fieldnames = ["id", "date", "category", "amount", "description"]
    
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for exp in expenses:
                writer.writerow(exp.to_dict())
        return filepath
    except IOError as e:
        raise IOError(f"Failed to export CSV: {e}")
