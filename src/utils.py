"""
utils.py - Utility functions, validation, and formatting helpers
Personal Finance Manager
"""

from datetime import datetime
from src.expense import VALID_CATEGORIES


def get_valid_amount(prompt="Enter amount: "):
    """Prompt user for a valid positive number."""
    while True:
        raw = input(prompt).strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("  ⚠️  Amount must be greater than zero.")
            else:
                return amount
        except ValueError:
            print("  ⚠️  Invalid amount. Enter a numeric value (e.g., 150 or 99.50).")


def get_valid_category(prompt="Enter category: "):
    """Prompt user for a valid expense category."""
    print(f"  Categories: {', '.join(VALID_CATEGORIES)}")
    while True:
        raw = input(prompt).strip()
        for cat in VALID_CATEGORIES:
            if raw.lower() == cat.lower():
                return cat
        print(f"  ⚠️  Invalid category. Choose from: {', '.join(VALID_CATEGORIES)}")


def get_valid_date(prompt="Enter date (YYYY-MM-DD) or press Enter for today: "):
    """Prompt user for a valid date string."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("  ⚠️  Invalid date format. Use YYYY-MM-DD (e.g., 2024-03-15).")


def get_valid_description(prompt="Enter description: "):
    """Prompt user for a non-empty description."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("  ⚠️  Description cannot be empty.")


def get_menu_choice(max_choice, prompt="Enter your choice: "):
    """Get a valid integer menu choice from the user."""
    while True:
        raw = input(prompt).strip()
        try:
            choice = int(raw)
            if 1 <= choice <= max_choice:
                return choice
            print(f"  ⚠️  Please enter a number between 1 and {max_choice}.")
        except ValueError:
            print("  ⚠️  Invalid input. Enter a number.")


def format_currency(amount):
    """Format a number as Indian Rupees."""
    return f"₹{amount:,.2f}"


def format_table_row(date, category, amount, description, widths=(12, 15, 12, 30)):
    """Format a single expense as a table row. Handles both header strings and numeric amounts."""
    desc = description[:widths[3] - 1] if len(str(description)) > widths[3] else description
    try:
        amt_str = f"₹{float(amount):>{widths[2]-1}.2f}"
    except (ValueError, TypeError):
        amt_str = f"{str(amount):>{widths[2]}}"
    return (
        f"{str(date):<{widths[0]}} | "
        f"{str(category):<{widths[1]}} | "
        f"{amt_str} | "
        f"{desc}"
    )


def print_divider(char="=", length=65):
    print(char * length)


def print_header(title):
    print_divider()
    print(f"  {title}")
    print_divider()


def pause():
    input("\nPress Enter to continue...")


def confirm(prompt="Are you sure? (y/n): "):
    """Return True if user confirms."""
    return input(prompt).strip().lower() == "y"


def filter_by_month(expenses, year, month):
    """Filter expenses by year and month (integers)."""
    return [
        e for e in expenses
        if e.date.startswith(f"{year:04d}-{month:02d}")
    ]


def filter_by_category(expenses, category):
    """Filter expenses by category (case-insensitive)."""
    return [e for e in expenses if e.category.lower() == category.lower()]


def filter_by_keyword(expenses, keyword):
    """Filter expenses where description contains keyword."""
    kw = keyword.lower()
    return [e for e in expenses if kw in e.description.lower()]


def get_available_months(expenses):
    """Return sorted list of (year, month) tuples present in expenses."""
    months = set()
    for e in expenses:
        try:
            parts = e.date.split("-")
            months.add((int(parts[0]), int(parts[1])))
        except Exception:
            pass
    return sorted(months)
