import pytest
from finance_tracker.expense import Expense

def test_expense_creation():
    exp = Expense(amount=150.50, category="Food", description="Dinner", date="2026-03-15")
    assert exp.amount == 150.50
    assert exp.category == "Food"
    assert exp.date == "2026-03-15"

def test_invalid_amount():
    with pytest.raises(ValueError):
        Expense(amount=-20, category="Test", description="Fail")

def test_invalid_date():
    with pytest.raises(ValueError):
        Expense(amount=10, category="Test", description="Fail", date="15-03-2026")
