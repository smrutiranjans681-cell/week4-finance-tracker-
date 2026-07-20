from datetime import datetime
from finance_tracker.utils import validate_date, validate_amount, DATE_FORMAT

class Expense:
    def __init__(self, amount: float, category: str, description: str, date: str = None, expense_id: int = None):
        self.expense_id = expense_id
        self.amount = validate_amount(str(amount))
        self.category = category.strip().title()
        self.description = description.strip()
        
        if date:
            if not validate_date(date):
                raise ValueError(f"Invalid date format: {date}. Expected YYYY-MM-DD.")
            self.date = date
        else:
            self.date = datetime.today().strftime(DATE_FORMAT)

    def to_dict(self) -> dict:
        """Converts object to dictionary representation."""
        return {
            "id": self.expense_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an Expense object from a dictionary."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data["date"],
            expense_id=data.get("id")
        )

    def __repr__(self):
        return f"<Expense {self.expense_id}: {self.category} - ₹{self.amount} on {self.date}>"
