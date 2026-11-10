#!/usr/bin/env python3
"""
Personal Expense Tracker with CSV Storage

A simple command-line expense tracker that stores data in CSV format.
Features:
- Add expenses with amount, category, description, and date
- View all expenses
- View summary by category
- View monthly summary
- Export/Import CSV
- Basic data validation
"""

import csv
import os
import sys
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Expense:
    """Represents a single expense entry."""
    id: int
    date: str
    category: str
    amount: float
    description: str

    def to_row(self) -> List[str]:
        """Convert expense to CSV row."""
        return [str(self.id), self.date, self.category, f"{self.amount:.2f}", self.description]

    @classmethod
    def from_row(cls, row: List[str]) -> 'Expense':
        """Create expense from CSV row."""
        return cls(
            id=int(row[0]),
            date=row[1],
            category=row[2],
            amount=float(row[3]),
            description=row[4]
        )


class ExpenseTracker:
    """Main expense tracker class handling CSV storage and operations."""

    DEFAULT_CATEGORIES = [
        "Food & Dining",
        "Transportation",
        "Shopping",
        "Entertainment",
        "Bills & Utilities",
        "Healthcare",
        "Education",
        "Travel",
        "Other"
    ]

    def __init__(self, csv_file: str = "expenses.csv"):
        self.csv_file = csv_file
        self.expenses: List[Expense] = []
        self.next_id = 1
        self.load_expenses()

    def load_expenses(self) -> None:
        """Load expenses from CSV file."""
        if not os.path.exists(self.csv_file):
            self.expenses = []
            self.next_id = 1
            return

        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header != ['id', 'date', 'category', 'amount', 'description']:
                    print(f"Warning: CSV header mismatch. Expected standard format.")
                    return

                self.expenses = []
                max_id = 0
                for row in reader:
                    if len(row) == 5:
                        try:
                            expense = Expense.from_row(row)
                            self.expenses.append(expense)
                            max_id = max(max_id, expense.id)
                        except (ValueError, IndexError) as e:
                            print(f"Warning: Skipping invalid row: {row} - {e}")

                self.next_id = max_id + 1
            print(f"Loaded {len(self.expenses)} expenses from {self.csv_file}")
        except Exception as e:
            print(f"Error loading expenses: {e}")
            self.expenses = []
            self.next_id = 1

    def save_expenses(self) -> None:
        """Save expenses to CSV file."""
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'date', 'category', 'amount', 'description'])
                for expense in self.expenses:
                    writer.writerow(expense.to_row())
            print(f"Saved {len(self.expenses)} expenses to {self.csv_file}")
        except Exception as e:
            print(f"Error saving expenses: {e}")

    def add_expense(self, amount: float, category: str, description: str, date: Optional[str] = None) -> Expense:
        """Add a new expense."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            # Validate date format
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        if not category.strip():
            raise ValueError("Category cannot be empty")

        expense = Expense(
            id=self.next_id,
            date=date,
            category=category.strip(),
            amount=round(amount, 2),
            description=description.strip()
        )

        self.expenses.append(expense)
        self.next_id += 1
        self.save_expenses()
        return expense

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense by ID."""
        for i, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                del self.expenses[i]
                self.save_expenses()
                return True
        return False

    def get_expenses(self, category: Optional[str] = None, start_date: Optional[str] = None,
                     end_date: Optional[str] = None) -> List[Expense]:
        """Get filtered expenses."""
        filtered = self.expenses

        if category:
            filtered = [e for e in filtered if e.category.lower() == category.lower()]

        if start_date:
            filtered = [e for e in filtered if e.date >= start_date]

        if end_date:
            filtered = [e for e in filtered if e.date <= end_date]

        return sorted(filtered, key=lambda e: e.date, reverse=True)

    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        categories = set(e.category for e in self.expenses)
        return sorted(categories)

    def get_category_summary(self) -> dict:
        """Get summary of expenses by category."""
        summary = {}
        for expense in self.expenses:
            if expense.category not in summary:
                summary[expense.category] = {"total": 0.0, "count": 0}
            summary[expense.category]["total"] += expense.amount
            summary[expense.category]["count"] += 1
        return summary

    def get_monthly_summary(self) -> dict:
        """Get summary of expenses by month."""
        summary = {}
        for expense in self.expenses:
            month = expense.date[:7]  # YYYY-MM
            if month not in summary:
                summary[month] = {"total": 0.0, "count": 0}
            summary[month]["total"] += expense.amount
            summary[month]["count"] += 1
        return dict(sorted(summary.items(), reverse=True))

    def get_total_expenses(self) -> float:
        """Get total of all expenses."""
        return sum(e.amount for e in self.expenses)

    def export_csv(self, output_file: str) -> None:
        """Export expenses to a different CSV file."""
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'date', 'category', 'amount', 'description'])
                for expense in self.expenses:
                    writer.writerow(expense.to_row())
            print(f"Exported {len(self.expenses)} expenses to {output_file}")
        except Exception as e:
            print(f"Error exporting: {e}")

    def import_csv(self, input_file: str, merge: bool = True) -> int:
        """Import expenses from a CSV file."""
        if not os.path.exists(input_file):
            print(f"File not found: {input_file}")
            return 0

        imported = 0
        try:
            with open(input_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header != ['id', 'date', 'category', 'amount', 'description']:
                    print("Invalid CSV format. Expected headers: id,date,category,amount,description")
                    return 0

                new_expenses = []
                for row in reader:
                    if len(row) == 5:
                        try:
                            expense = Expense.from_row(row)
                            new_expenses.append(expense)
                            imported += 1
                        except (ValueError, IndexError) as e:
                            print(f"Skipping invalid row: {row} - {e}")

            if imported > 0:
                if merge:
                    # Check for duplicate IDs and reassign if needed
                    existing_ids = {e.id for e in self.expenses}
                    for expense in new_expenses:
                        if expense.id in existing_ids:
                            expense.id = self.next_id
                            self.next_id += 1
                        existing_ids.add(expense.id)
                    self.expenses.extend(new_expenses)
                else:
                    # Replace all expenses with imported ones
                    self.expenses = new_expenses
                    # Update next_id to avoid conflicts
                    max_id = max((e.id for e in self.expenses), default=0)
                    self.next_id = max_id + 1

                self.save_expenses()
            print(f"Imported {imported} expenses from {input_file}")
            return imported
        except Exception as e:
            print(f"Error importing: {e}")
            return 0


def print_expenses(expenses: List[Expense]) -> None:
    """Pretty print a list of expenses."""
    if not expenses:
        print("No expenses found.")
        return

    print(f"\n{'ID':>4}  {'Date':<12}  {'Category':<20}  {'Amount':>10}  {'Description'}")
    print("-" * 80)
    for exp in expenses:
        print(f"{exp.id:>4}  {exp.date:<12}  {exp.category:<20}  ${exp.amount:>9.2f}  {exp.description}")


def print_category_summary(summary: dict) -> None:
    """Print category summary."""
    if not summary:
        print("No expenses to summarize.")
        return

    print(f"\n{'Category':<25}  {'Count':>6}  {'Total':>12}")
    print("-" * 50)
    total = 0
    for cat, data in sorted(summary.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"{cat:<25}  {data['count']:>6}  ${data['total']:>11.2f}")
        total += data['total']
    print("-" * 50)
    print(f"{'TOTAL':<25}  {'':>6}  ${total:>11.2f}")


def print_monthly_summary(summary: dict) -> None:
    """Print monthly summary."""
    if not summary:
        print("No expenses to summarize.")
        return

    print(f"\n{'Month':<10}  {'Count':>6}  {'Total':>12}")
    print("-" * 35)
    total = 0
    for month, data in summary.items():
        print(f"{month:<10}  {data['count']:>6}  ${data['total']:>11.2f}")
        total += data['total']
    print("-" * 35)
    print(f"{'TOTAL':<10}  {'':>6}  ${total:>11.2f}")


def get_valid_amount(prompt: str) -> float:
    """Get a valid amount from user."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value <= 0:
                print("Amount must be positive.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_valid_date(prompt: str, allow_empty: bool = True) -> Optional[str]:
    """Get a valid date from user."""
    while True:
        value = input(prompt).strip()
        if allow_empty and not value:
            return None
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")


def get_valid_category(tracker: ExpenseTracker, prompt: str) -> str:
    """Get a valid category from user."""
    categories = tracker.get_categories()
    all_categories = list(set(categories + tracker.DEFAULT_CATEGORIES))

    print("\nAvailable categories:")
    for i, cat in enumerate(all_categories, 1):
        print(f"  {i}. {cat}")
    print(f"  {len(all_categories) + 1}. Custom category")

    while True:
        choice = input(prompt).strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(all_categories):
                return all_categories[idx]
            elif idx == len(all_categories):
                custom = input("Enter custom category: ").strip()
                if custom:
                    return custom
                print("Category cannot be empty.")
            else:
                print("Invalid choice.")
        elif choice:
            return choice
        else:
            print("Please enter a category.")


def main_menu() -> None:
    """Display main menu."""
    print("\n" + "=" * 50)
    print("      PERSONAL EXPENSE TRACKER")
    print("=" * 50)
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Expenses by Category")
    print("4. View Expenses by Date Range")
    print("5. Category Summary")
    print("6. Monthly Summary")
    print("7. Delete Expense")
    print("8. Export to CSV")
    print("9. Import from CSV")
    print("10. Show Total Expenses")
    print("0. Exit")
    print("-" * 50)


def run_interactive(tracker: ExpenseTracker) -> None:
    """Run the interactive menu loop."""
    while True:
        main_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            # Add expense
            try:
                amount = get_valid_amount("Enter amount: $")
                category = get_valid_category(tracker, "Choose category (number or name): ")
                description = input("Enter description: ").strip()
                if not description:
                    description = "No description"
                date = get_valid_date("Enter date (YYYY-MM-DD) [today]: ", allow_empty=True)
                expense = tracker.add_expense(amount, category, description, date)
                print(f"\nAdded expense: #{expense.id} - {expense.category} - ${expense.amount:.2f}")
            except ValueError as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nCancelled.")

        elif choice == "2":
            # View all expenses
            expenses = tracker.get_expenses()
            print_expenses(expenses)

        elif choice == "3":
            # View by category
            categories = tracker.get_categories()
            if not categories:
                print("No categories found.")
                continue
            print("\nCategories:")
            for i, cat in enumerate(categories, 1):
                print(f"  {i}. {cat}")
            try:
                idx = int(input("Choose category number: ")) - 1
                if 0 <= idx < len(categories):
                    expenses = tracker.get_expenses(category=categories[idx])
                    print_expenses(expenses)
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            # View by date range
            start = get_valid_date("Start date (YYYY-MM-DD) [all]: ", allow_empty=True)
            end = get_valid_date("End date (YYYY-MM-DD) [all]: ", allow_empty=True)
            expenses = tracker.get_expenses(start_date=start, end_date=end)
            print_expenses(expenses)

        elif choice == "5":
            # Category summary
            summary = tracker.get_category_summary()
            print_category_summary(summary)

        elif choice == "6":
            # Monthly summary
            summary = tracker.get_monthly_summary()
            print_monthly_summary(summary)

        elif choice == "7":
            # Delete expense
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                if tracker.delete_expense(expense_id):
                    print(f"Deleted expense #{expense_id}")
                else:
                    print(f"Expense #{expense_id} not found.")
            except ValueError:
                print("Invalid ID.")

        elif choice == "8":
            # Export CSV
            filename = input("Export filename [expenses_export.csv]: ").strip()
            if not filename:
                filename = "expenses_export.csv"
            tracker.export_csv(filename)

        elif choice == "9":
            # Import CSV
            filename = input("Import filename: ").strip()
            if filename:
                merge = input("Merge with existing (keep IDs)? [Y/n]: ").strip().lower() != 'n'
                tracker.import_csv(filename, merge=merge)

        elif choice == "10":
            # Show total
            total = tracker.get_total_expenses()
            print(f"\nTotal Expenses: ${total:.2f}")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


def run_cli(tracker: ExpenseTracker, args: List[str]) -> None:
    """Run command-line interface."""
    if not args:
        run_interactive(tracker)
        return

    cmd = args[0]

    if cmd == "add":
        if len(args) < 4:
            print("Usage: python expense_tracker.py add <amount> <category> <description> [date]")
            return
        try:
            amount = float(args[1])
            category = args[2]
            description = args[3]
            date = args[4] if len(args) > 4 else None
            expense = tracker.add_expense(amount, category, description, date)
            print(f"Added: #{expense.id} {expense.date} {expense.category} ${expense.amount:.2f} {expense.description}")
        except ValueError as e:
            print(f"Error: {e}")

    elif cmd == "list":
        category = args[1] if len(args) > 1 else None
        start = args[2] if len(args) > 2 else None
        end = args[3] if len(args) > 3 else None
        expenses = tracker.get_expenses(category=category, start_date=start, end_date=end)
        print_expenses(expenses)

    elif cmd == "summary":
        summary = tracker.get_category_summary()
        print_category_summary(summary)

    elif cmd == "monthly":
        summary = tracker.get_monthly_summary()
        print_monthly_summary(summary)

    elif cmd == "total":
        total = tracker.get_total_expenses()
        print(f"Total: ${total:.2f}")

    elif cmd == "delete":
        if len(args) < 2:
            print("Usage: python expense_tracker.py delete <id>")
            return
        try:
            expense_id = int(args[1])
            if tracker.delete_expense(expense_id):
                print(f"Deleted expense #{expense_id}")
            else:
                print(f"Expense #{expense_id} not found.")
        except ValueError:
            print("Invalid ID.")

    elif cmd == "export":
        filename = args[1] if len(args) > 1 else "expenses_export.csv"
        tracker.export_csv(filename)

    elif cmd == "import":
        if len(args) < 2:
            print("Usage: python expense_tracker.py import <filename> [merge]")
            return
        filename = args[1]
        merge = args[2].lower() != 'false' if len(args) > 2 else True
        tracker.import_csv(filename, merge=merge)

    elif cmd == "categories":
        cats = tracker.get_categories()
        for cat in cats:
            print(cat)

    else:
        print(f"Unknown command: {cmd}")
        print("Available commands: add, list, summary, monthly, total, delete, export, import, categories")


if __name__ == "__main__":
    # Allow custom CSV file via environment variable or first argument
    csv_file = os.environ.get("EXPENSE_TRACKER_CSV", "expenses.csv")

    # Check if first arg is a CSV file (not a command)
    if len(sys.argv) > 1 and sys.argv[1].endswith('.csv') and sys.argv[1] not in ['add', 'list', 'summary', 'monthly', 'total', 'delete', 'export', 'import', 'categories']:
        csv_file = sys.argv[1]
        sys.argv.pop(1)

    tracker = ExpenseTracker(csv_file)

    if len(sys.argv) > 1:
        run_cli(tracker, sys.argv[1:])
    else:
        run_interactive(tracker)