import os
from finance_tracker.expense_manager import ExpenseManager
from finance_tracker import file_handler, reports
from finance_tracker.utils import validate_date, validate_amount

class FinanceTrackerApp:
    def __init__(self):
        self.manager = ExpenseManager()

    def run(self):
        while True:
            print("\n" + "=" * 50)
            print("          PERSONAL FINANCE TRACKER")
            print("=" * 50)
            print("1. Add New Expense")
            print("2. View All Expenses")
            print("3. Search & Filter Expenses")
            print("4. Generate Monthly Report")
            print("5. View Category Breakdown")
            print("6. Set/Update Monthly Budget")
            print("7. Export Data to CSV")
            print("8. Delete Expense")
            print("9. Backup & Restore Operations")
            print("0. Exit")
            print("=" * 50)
            
            choice = input("\nEnter choice (0-9): ").strip()
            
            try:
                if choice == '1':
                    self.add_expense_ui()
                elif choice == '2':
                    self.view_expenses_ui()
                elif choice == '3':
                    self.search_expenses_ui()
                elif choice == '4':
                    self.monthly_report_ui()
                elif choice == '5':
                    self.category_breakdown_ui()
                elif choice == '6':
                    self.set_budget_ui()
                elif choice == '7':
                    self.export_csv_ui()
                elif choice == '8':
                    self.delete_expense_ui()
                elif choice == '9':
                    self.backup_restore_ui()
                elif choice == '0':
                    print("\nThank you for using Personal Finance Tracker. Goodbye!")
                    break
                else:
                    print("\n[!] Invalid input. Please enter a number between 0 and 9.")
            except Exception as e:
                print(f"\n[!] Unexpected error: {e}")

    def add_expense_ui(self):
        print("\n--- ADD NEW EXPENSE ---")
        try:
            amount = validate_amount(input("Enter Amount (₹): "))
            category = input("Enter Category (e.g., Food, Rent, Travel): ").strip()
            if not category:
                print("Category cannot be empty.")
                return
            description = input("Enter Description: ").strip()
            date_in = input("Enter Date (YYYY-MM-DD) or press Enter for Today: ").strip()
            
            date = date_in if date_in else None
            exp = self.manager.add_expense(amount, category, description, date)
            print(f"\n✓ Expense registered successfully! [ID: {exp.expense_id}]")
        except ValueError as ve:
            print(f"\n[!] Validation Error: {ve}")

    def view_expenses_ui(self):
        print("\n--- ALL EXPENSES ---")
        if not self.manager.expenses:
            print("No expense records found.")
            return

        print(f"{'ID':<5} | {'Date':<12} | {'Category':<15} | {'Amount (₹)':<10} | {'Description'}")
        print("-" * 65)
        for e in sorted(self.manager.expenses, key=lambda x: x.date, reverse=True):
            print(f"{e.expense_id:<5} | {e.date:<12} | {e.category:<15} | {e.amount:<10.2f} | {e.description}")

    def search_expenses_ui(self):
        print("\n--- SEARCH & FILTER EXPENSES ---")
        kw = input("Enter keyword (or press Enter to skip): ").strip()
        cat = input("Enter category (or press Enter to skip): ").strip()
        
        results = self.manager.search_expenses(
            keyword=kw if kw else None,
            category=cat if cat else None
        )
        
        print(f"\nFound {len(results)} matching entry/entries:")
        for e in results:
            print(f"[{e.date}] #{e.expense_id} - {e.category}: ₹{e.amount} ({e.description})")

    def monthly_report_ui(self):
        ym = input("Enter Year-Month to generate report (YYYY-MM): ").strip()
        if len(ym) != 7 or ym[4] != '-':
            print("Invalid format! Use YYYY-MM.")
            return
            
        summary = reports.get_monthly_summary(self.manager.expenses, ym)
        reports.print_text_report(summary, self.manager.budget)

    def category_breakdown_ui(self):
        print("\n--- CATEGORY BREAKDOWN ---")
        breakdown = reports.get_category_breakdown(self.manager.expenses)
        print(reports.generate_bar_chart(breakdown))

    def set_budget_ui(self):
        try:
            amt = validate_amount(input("Enter target monthly budget (₹): "))
            self.manager.set_budget(amt)
            print(f"✓ Monthly budget updated to ₹{amt:.2f}")
        except ValueError as ve:
            print(f"[!] Error: {ve}")

    def export_csv_ui(self):
        try:
            path = file_handler.export_to_csv(self.manager.expenses)
            print(f"✓ Data successfully exported to CSV at: {path}")
        except IOError as e:
            print(f"[!] Export Error: {e}")

    def delete_expense_ui(self):
        try:
            eid = int(input("Enter Expense ID to delete: "))
            if self.manager.delete_expense(eid):
                print(f"✓ Expense #{eid} deleted.")
            else:
                print(f"[!] Expense ID #{eid} not found.")
        except ValueError:
            print("[!] Please enter a valid numerical ID.")

    def backup_restore_ui(self):
        print("\n1. Create Backup")
        print("2. Restore Backup")
        opt = input("Select option (1-2): ").strip()
        
        if opt == '1':
            try:
                path = file_handler.create_backup()
                print(f"✓ Backup created successfully at: {path}")
            except Exception as e:
                print(f"[!] Backup failed: {e}")
        elif opt == '2':
            files = os.listdir(file_handler.BACKUP_DIR) if os.path.exists(file_handler.BACKUP_DIR) else []
            if not files:
                print("No backups available.")
                return
            print("\nAvailable Backups:")
            for idx, f in enumerate(files, 1):
                print(f"{idx}. {f}")
            choice = input("Select backup number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(files):
                selected_file = files[int(choice)-1]
                file_handler.restore_backup(selected_file)
                self.manager.load_from_storage()
                print("✓ Database restored successfully!")
            else:
                print("[!] Invalid choice.")

def main():
    app = FinanceTrackerApp()
    app.run()

if __name__ == "__main__":
    main()
