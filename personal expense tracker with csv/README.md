# Personal Expense Tracker with CSV

A simple command-line personal expense tracker that stores data in CSV format. Built with Python, no external dependencies required.

## Features

- **Add expenses** with amount, category, description, and date
- **View expenses** - all, by category, or by date range
- **Category summary** - see spending breakdown by category
- **Monthly summary** - track spending over time
- **CSV storage** - data persists in a simple CSV file
- **Export/Import** - backup and restore your data
- **Interactive menu** - easy to use interface
- **Command-line interface** - scriptable for automation

## Quick Start

```bash
# Run interactive mode
python expense_tracker.py

# Or run with commands
python expense_tracker.py add 25.50 "Food & Dining" "Lunch with friends"
python expense_tracker.py list
python expense_tracker.py summary
```

## Installation

No installation needed! Just ensure you have Python 3.6+ installed:

```bash
python --version
# Python 3.6.0 or higher
```

## Usage

### Interactive Mode (Recommended)

```bash
python expense_tracker.py
```

This launches a menu-driven interface:
```
==================================================
      PERSONAL EXPENSE TRACKER
==================================================
1. Add Expense
2. View All Expenses
3. View Expenses by Category
4. View Expenses by Date Range
5. Category Summary
6. Monthly Summary
7. Delete Expense
8. Export to CSV
9. Import from CSV
10. Show Total Expenses
0. Exit
```

### Command Line Interface

```bash
# Add an expense
python expense_tracker.py add <amount> <category> <description> [date]
python expense_tracker.py add 15.75 "Transportation" "Bus fare" 2024-01-15

# List all expenses
python expense_tracker.py list

# List expenses by category
python expense_tracker.py list "Food & Dining"

# List expenses by date range
python expense_tracker.py list "" 2024-01-01 2024-01-31

# Show category summary
python expense_tracker.py summary

# Show monthly summary
python expense_tracker.py monthly

# Show total expenses
python expense_tracker.py total

# Delete an expense
python expense_tracker.py delete 5

# Export to CSV
python expense_tracker.py export backup.csv

# Import from CSV
python expense_tracker.py import backup.csv

# List categories
python expense_tracker.py categories
```

### Custom CSV File

```bash
# Use a different CSV file
python expense_tracker.py my_expenses.csv

# Or set environment variable
export EXPENSE_TRACKER_CSV=my_expenses.csv
python expense_tracker.py
```

## CSV Format

The tracker uses a simple CSV format:

```csv
id,date,category,amount,description
1,2024-01-15,Food & Dining,25.50,Lunch with friends
2,2024-01-16,Transportation,15.75,Bus fare
```

You can open this file in Excel, Google Sheets, or any spreadsheet application.

## Default Categories

- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Education
- Travel
- Other

You can also create custom categories.

## Example Session

```bash
$ python expense_tracker.py

==================================================
      PERSONAL EXPENSE TRACKER
==================================================
1. Add Expense
2. View All Expenses
3. View Expenses by Category
4. View Expenses by Date Range
5. Category Summary
6. Monthly Summary
7. Delete Expense
8. Export to CSV
9. Import from CSV
10. Show Total Expenses
0. Exit
--------------------------------------------------
Enter choice: 1
Enter amount: $45.00
Choose category (number or name): 1
Enter description: Groceries
Enter date (YYYY-MM-DD) [today]: 

Added expense: #1 - Food & Dining - $45.00

Enter choice: 1
Enter amount: $25.50
Choose category (number or name): Transportation
Enter description: Uber to airport
Enter date (YYYY-MM-DD) [today]: 2024-01-10

Added expense: #2 - Transportation - $25.50

Enter choice: 5

Category                  Count      Total
--------------------------------------------------
Food & Dining                 1     $45.00
Transportation                1     $25.50
--------------------------------------------------
TOTAL                                    $70.50

Enter choice: 0
Goodbye!
```

## Data Location

By default, expenses are stored in `expenses.csv` in the same directory as the script. You can change this by:

1. Passing a filename as the first argument
2. Setting the `EXPENSE_TRACKER_CSV` environment variable

## Tips

- **Backup regularly**: Use `export` to create backups
- **Import from spreadsheets**: Save as CSV and import
- **Date format**: Always use YYYY-MM-DD (e.g., 2024-01-15)
- **Categories**: Type the name or number from the list

## Requirements

- Python 3.6+

No external packages required - uses only standard library modules:
- `csv` for file I/O
- `datetime` for date handling
- `dataclasses` for data structures
- `typing` for type hints

## License

MIT License - Feel free to use and modify!