import os
import datetime

DATE_FORMAT = "%Y-%m-%d"

def validate_date(date_str: str) -> bool:
    """Validates if a string matches YYYY-MM-DD format."""
    try:
        datetime.datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False

def validate_amount(amount_str: str) -> float:
    """Validates and converts a string to a positive float amount."""
    val = float(amount_str)
    if val <= 0:
        raise ValueError("Amount must be greater than 0.")
    return round(val, 2)

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_bar_chart(data: dict, max_width: int = 30) -> str:
    """Generates a text-based horizontal bar chart from a dictionary of category: amount."""
    if not data:
        return "No data to display."
    
    max_val = max(data.values()) if max(data.values()) > 0 else 1
    lines = []
    
    for key, value in data.items():
        bar_length = int((value / max_val) * max_width)
        bar = "█" * bar_length
        lines.append(f"{key:<15} | {bar:<{max_width}}  ₹{value:.2f}")
        
    return "\n".join(lines)
