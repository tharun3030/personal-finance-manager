"""
file_manager.py - CSV read/write operations and data persistence
Personal Finance Manager
"""

import csv
import os
import shutil
from datetime import datetime
from src.expense import Expense


DATA_DIR = "data"
BACKUP_DIR = "data/backups"
EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.csv")
CSV_HEADERS = ["Date", "Category", "Amount", "Description"]


def ensure_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs("reports", exist_ok=True)


def load_expenses(filename=EXPENSES_FILE):
    """Load expenses from CSV file. Returns list of Expense objects."""
    ensure_directories()
    expenses = []

    if not os.path.exists(filename):
        return expenses

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, start=2):
                try:
                    expense = Expense(
                        amount=row["Amount"],
                        category=row["Category"],
                        date=row["Date"],
                        description=row["Description"],
                    )
                    expenses.append(expense)
                except (KeyError, ValueError) as e:
                    print(f"  ⚠️  Skipping row {row_num}: {e}")
    except Exception as e:
        print(f"  ❌ Error loading expenses: {e}")

    return expenses


def save_expenses(expenses, filename=EXPENSES_FILE):
    """Save list of Expense objects to CSV file."""
    ensure_directories()
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)
            for expense in expenses:
                writer.writerow([
                    expense.date,
                    expense.category,
                    expense.amount,
                    expense.description,
                ])
        return True
    except Exception as e:
        print(f"  ❌ Error saving expenses: {e}")
        return False


def backup_data(filename=EXPENSES_FILE):
    """Create a timestamped backup of the expenses file."""
    ensure_directories()
    if not os.path.exists(filename):
        return None, "No data file found to back up."

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = os.path.join(BACKUP_DIR, f"expenses_backup_{timestamp}.csv")

    try:
        shutil.copy2(filename, backup_filename)
        return backup_filename, None
    except Exception as e:
        return None, str(e)


def restore_data(backup_filename, target=EXPENSES_FILE):
    """Restore expenses from a backup file."""
    if not os.path.exists(backup_filename):
        return False, "Backup file not found."
    try:
        shutil.copy2(backup_filename, target)
        return True, None
    except Exception as e:
        return False, str(e)


def list_backups():
    """Return list of available backup files."""
    ensure_directories()
    backups = []
    if os.path.exists(BACKUP_DIR):
        for f in sorted(os.listdir(BACKUP_DIR), reverse=True):
            if f.startswith("expenses_backup_") and f.endswith(".csv"):
                backups.append(os.path.join(BACKUP_DIR, f))
    return backups


def export_report(content, report_name):
    """Save a text report to the reports directory."""
    ensure_directories()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("reports", f"{report_name}_{timestamp}.txt")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return filename
    except Exception as e:
        return None
