from typing import List, Optional
from finance_tracker.expense import Expense
from finance_tracker import file_handler

class ExpenseManager:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.budget: float = 0.0
        self._next_id: int = 1
        self.load_from_storage()

    def load_from_storage(self):
        """Loads records from persistent storage into memory."""
        data = file_handler.load_data()
        self.budget = data.get("budget", 0.0)
        raw_expenses = data.get("expenses", [])
        
        self.expenses = []
        max_id = 0
        for item in raw_expenses:
            exp = Expense.from_dict(item)
            self.expenses.append(exp)
            if exp.expense_id and exp.expense_id > max_id:
                max_id = exp.expense_id
        self._next_id = max_id + 1

    def save_to_storage(self) -> bool:
        """Persists current in-memory data to storage."""
        data = {
            "budget": self.budget,
            "expenses": [exp.to_dict() for exp in self.expenses]
        }
        return file_handler.save_data(data)

    def add_expense(self, amount: float, category: str, description: str, date: str = None) -> Expense:
        """Instantiates and registers a new expense record."""
        exp = Expense(amount, category, description, date, expense_id=self._next_id)
        self._next_id += 1
        self.expenses.append(exp)
        self.save_to_storage()
        return exp

    def delete_expense(self, expense_id: int) -> bool:
        """Removes an expense entry by ID."""
        initial_count = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.expense_id != expense_id]
        if len(self.expenses) < initial_count:
            self.save_to_storage()
            return True
        return False

    def search_expenses(self, keyword: Optional[str] = None, category: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Expense]:
        """Filters expenses matching criteria."""
        results = self.expenses
        
        if keyword:
            kw = keyword.lower()
            results = [e for e in results if kw in e.description.lower() or kw in e.category.lower()]
            
        if category:
            cat = category.lower()
            results = [e for e in results if e.category.lower() == cat]
            
        if start_date:
            results = [e for e in results if e.date >= start_date]
            
        if end_date:
            results = [e for e in results if e.date <= end_date]
            
        return sorted(results, key=lambda x: x.date, reverse=True)

    def set_budget(self, new_budget: float):
        """Updates monthly budget limit."""
        self.budget = new_budget
        self.save_to_storage()

    def get_total_spent(() -> float:
        """Calculates total spend across all recorded expenses."""
        return sum(e.amount for e in self.expenses)
