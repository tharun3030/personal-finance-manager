"""
expense.py - Expense class definition
Personal Finance Manager
"""

from datetime import datetime


VALID_CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Health", "Utilities", "Education", "Other"]


class Expense:
    """Represents a single financial expense."""

    def __init__(self, amount, category, date, description):
        self.amount = float(amount)
        self.category = self._validate_category(category)
        self.date = self._validate_date(date)
        self.description = str(description).strip()

    def _validate_category(self, category):
        """Validate and normalize category."""
        for valid in VALID_CATEGORIES:
            if category.strip().lower() == valid.lower():
                return valid
        return "Other"

    def _validate_date(self, date):
        """Validate date format."""
        if isinstance(date, datetime):
            return date.strftime("%Y-%m-%d")
        try:
            datetime.strptime(str(date), "%Y-%m-%d")
            return str(date)
        except ValueError:
            raise ValueError(f"Invalid date format: '{date}'. Use YYYY-MM-DD.")

    def to_dict(self):
        """Convert expense to dictionary."""
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description,
        }

    def __str__(self):
        return f"{self.date} | {self.category:<15} | ₹{self.amount:>10.2f} | {self.description}"

    def __repr__(self):
        return f"Expense(amount={self.amount}, category='{self.category}', date='{self.date}')"
