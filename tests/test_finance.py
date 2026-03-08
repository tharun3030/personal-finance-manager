"""
tests/test_finance.py - Unit tests for Personal Finance Manager
Run with: python -m pytest tests/ -v
   or:    python tests/test_finance.py
"""

import sys
import os
import unittest
import tempfile
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.expense import Expense, VALID_CATEGORIES
from src.file_manager import save_expenses, load_expenses
from src.utils import filter_by_keyword, filter_by_category, filter_by_month
from src.reports import compute_totals, category_summary


class TestExpenseClass(unittest.TestCase):

    def test_valid_creation(self):
        e = Expense(1500, "Food", "2024-03-15", "Groceries")
        self.assertEqual(e.amount, 1500.0)
        self.assertEqual(e.category, "Food")
        self.assertEqual(e.date, "2024-03-15")
        self.assertEqual(e.description, "Groceries")

    def test_amount_is_float(self):
        e = Expense("250.50", "Transport", "2024-01-01", "Bus pass")
        self.assertIsInstance(e.amount, float)

    def test_invalid_date_raises(self):
        with self.assertRaises(ValueError):
            Expense(100, "Food", "15-03-2024", "Bad date")

    def test_invalid_category_defaults_to_other(self):
        e = Expense(100, "Gambling", "2024-01-01", "Casino")
        self.assertEqual(e.category, "Other")

    def test_category_case_insensitive(self):
        e = Expense(100, "food", "2024-01-01", "Lunch")
        self.assertEqual(e.category, "Food")

    def test_str_contains_key_info(self):
        e = Expense(500, "Health", "2024-06-01", "Dentist")
        s = str(e)
        self.assertIn("2024-06-01", s)
        self.assertIn("Health", s)
        self.assertIn("500.00", s)

    def test_to_dict(self):
        e = Expense(300, "Shopping", "2024-02-10", "Books")
        d = e.to_dict()
        self.assertEqual(d["amount"], 300.0)
        self.assertEqual(d["category"], "Shopping")


class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.tmpdir, "test_expenses.csv")
        self.expenses = [
            Expense(1000, "Food", "2024-01-10", "Grocery"),
            Expense(500, "Transport", "2024-01-15", "Bus"),
            Expense(2000, "Shopping", "2024-02-01", "Clothes"),
        ]

    def test_save_and_load_roundtrip(self):
        save_expenses(self.expenses, self.test_file)
        loaded = load_expenses(self.test_file)
        self.assertEqual(len(loaded), 3)
        self.assertEqual(loaded[0].amount, 1000.0)
        self.assertEqual(loaded[1].category, "Transport")
        self.assertEqual(loaded[2].description, "Clothes")

    def test_load_missing_file_returns_empty(self):
        result = load_expenses(os.path.join(self.tmpdir, "nonexistent.csv"))
        self.assertEqual(result, [])

    def test_saved_file_has_header(self):
        save_expenses(self.expenses, self.test_file)
        with open(self.test_file, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
        self.assertEqual(header, ["Date", "Category", "Amount", "Description"])


class TestFilters(unittest.TestCase):

    def setUp(self):
        self.expenses = [
            Expense(500, "Food", "2024-01-10", "Grocery run"),
            Expense(200, "Transport", "2024-01-20", "Bus ticket"),
            Expense(1500, "Food", "2024-02-05", "Restaurant dinner"),
            Expense(800, "Entertainment", "2024-02-15", "Cinema"),
        ]

    def test_filter_by_keyword(self):
        results = filter_by_keyword(self.expenses, "dinner")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].amount, 1500)

    def test_filter_by_keyword_case_insensitive(self):
        results = filter_by_keyword(self.expenses, "GROCERY")
        self.assertEqual(len(results), 1)

    def test_filter_by_category(self):
        results = filter_by_category(self.expenses, "Food")
        self.assertEqual(len(results), 2)

    def test_filter_by_month(self):
        results = filter_by_month(self.expenses, 2024, 2)
        self.assertEqual(len(results), 2)

    def test_filter_no_match(self):
        results = filter_by_keyword(self.expenses, "vacation")
        self.assertEqual(results, [])


class TestReports(unittest.TestCase):

    def setUp(self):
        self.expenses = [
            Expense(1000, "Food", "2024-01-01", "A"),
            Expense(2000, "Transport", "2024-01-02", "B"),
            Expense(3000, "Food", "2024-01-03", "C"),
        ]

    def test_compute_totals(self):
        total, avg, count = compute_totals(self.expenses)
        self.assertEqual(total, 6000.0)
        self.assertAlmostEqual(avg, 2000.0)
        self.assertEqual(count, 3)

    def test_compute_totals_empty(self):
        total, avg, count = compute_totals([])
        self.assertEqual(total, 0.0)
        self.assertEqual(count, 0)

    def test_category_summary(self):
        summary = category_summary(self.expenses)
        self.assertIn("Food", summary)
        self.assertEqual(summary["Food"][0], 4000.0)
        self.assertEqual(summary["Food"][1], 2)
        self.assertEqual(summary["Transport"][0], 2000.0)

    def test_category_summary_sorted_desc(self):
        summary = category_summary(self.expenses)
        totals = [v[0] for v in summary.values()]
        self.assertEqual(totals, sorted(totals, reverse=True))


if __name__ == "__main__":
    print("Running Personal Finance Manager Tests...\n")
    unittest.main(verbosity=2)
