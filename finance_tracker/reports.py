from typing import Dict, List
from collections import defaultdict
from finance_tracker.expense import Expense
from finance_tracker.utils import generate_bar_chart

def get_category_breakdown(expenses: List[Expense]) -> Dict[str, float]:
    """Aggregates spending total per category."""
    totals = defaultdict(float)
    for exp in expenses:
        totals[exp.category] += exp.amount
    return dict(totals)

def get_monthly_summary(expenses: List[Expense], year_month: str) -> Dict[str, Any]:
    """
    Computes analytics for a specified month (Format: YYYY-MM).
    """
    filtered = [e for e in expenses if e.date.startswith(year_month)]
    total_spent = sum(e.amount for e in filtered)
    cat_breakdown = get_category_breakdown(filtered)
    
    return {
        "month": year_month,
        "count": len(filtered),
        "total_spent": round(total_spent, 2),
        "category_breakdown": cat_breakdown
    }

def print_text_report(summary: dict, budget: float = 0.0):
    """Prints a styled text summary with a visual bar chart."""
    print("\n" + "=" * 50)
    print(f"       MONTHLY REPORT: {summary['month']}")
    print("=" * 50)
    print(f"Total Transactions : {summary['count']}")
    print(f"Total Spent        : ₹{summary['total_spent']:.2f}")
    
    if budget > 0:
        remaining = budget - summary['total_spent']
        pct_used = (summary['total_spent'] / budget) * 100
        print(f"Monthly Budget     : ₹{budget:.2f}")
        print(f"Remaining Budget   : ₹{remaining:.2f} ({pct_used:.1f}% used)")
        if remaining < 0:
            print("⚠️ ALERT: You have exceeded your monthly budget!")
            
    print("-" * 50)
    print("      CATEGORY BREAKDOWN (VISUAL CHART)")
    print("-" * 50)
    print(generate_bar_chart(summary['category_breakdown']))
    print("=" * 50)
