import os
from finance_tracker import file_handler
from finance_tracker.expense import Expense

def test_save_and_load(tmp_path):
    # Setup temporary file path override
    file_handler.JSON_PATH = os.path.join(tmp_path, "test_expenses.json")
    file_handler.DATA_DIR = str(tmp_path)
    
    test_data = {
        "budget": 5000.0,
        "expenses": [{"id": 1, "amount": 100.0, "category": "Food", "description": "Lunch", "date": "2026-03-10"}]
    }
    
    assert file_handler.save_data(test_data) is True
    loaded = file_handler.load_data()
    assert loaded["budget"] == 5000.0
    assert len(loaded["expenses"]) == 1
