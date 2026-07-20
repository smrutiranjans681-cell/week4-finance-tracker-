from finance_tracker.expense import Expense
from finance_tracker import reports

def test_get_monthly_summary():
    expenses = [
        Expense(amount=100.0, category="Food", description="Meal 1", date="2026-03-01"),
        Expense(amount=200.0, category="Travel", description="Cab", date="2026-03-05"),
        Expense(amount=50.0, category="Food", description="Meal 2", date="2026-02-15")
    ]
    
    summary = reports.get_monthly_summary(expenses, "2026-03")
    assert summary["count"] == 2
    assert summary["total_spent"] == 300.0
    assert summary["category_breakdown"]["Food"] == 100.0
