"""
reports.py - Report generation and data analysis
Personal Finance Manager
"""

from collections import defaultdict
from src.utils import (
    format_currency, format_table_row, print_header, print_divider,
    filter_by_month, filter_by_category, get_available_months
)
from src.expense import VALID_CATEGORIES
from src.file_manager import export_report


# ─── Summary Calculations ────────────────────────────────────────────────────

def compute_totals(expenses):
    """Return (total, average, count) for a list of expenses."""
    if not expenses:
        return 0.0, 0.0, 0
    total = sum(e.amount for e in expenses)
    avg = total / len(expenses)
    return total, avg, len(expenses)


def category_summary(expenses):
    """Return dict {category: (total, count)} sorted by total descending."""
    data = defaultdict(lambda: [0.0, 0])
    for e in expenses:
        data[e.category][0] += e.amount
        data[e.category][1] += 1
    return dict(sorted(data.items(), key=lambda x: x[1][0], reverse=True))


# ─── Report Builders ─────────────────────────────────────────────────────────

def build_expenses_table(expenses, title="ALL EXPENSES"):
    """Return a formatted string table of expenses."""
    lines = []
    lines.append("=" * 75)
    lines.append(f"  {title}")
    lines.append("=" * 75)
    header = format_table_row("Date", "Category", "Amount", "Description")
    lines.append(header)
    lines.append("-" * 75)
    for e in expenses:
        lines.append(format_table_row(e.date, e.category, e.amount, e.description))
    lines.append("-" * 75)
    total, avg, count = compute_totals(expenses)
    lines.append(f"  Total Expenses: {count}   |   Total: {format_currency(total)}   |   Avg: {format_currency(avg)}")
    lines.append("=" * 75)
    return "\n".join(lines)


def build_category_report(expenses):
    """Return a formatted category-wise summary string."""
    summary = category_summary(expenses)
    total_all, _, _ = compute_totals(expenses)
    lines = []
    lines.append("=" * 55)
    lines.append("  CATEGORY-WISE SUMMARY")
    lines.append("=" * 55)
    lines.append(f"  {'Category':<18} {'Total':>12} {'Count':>7} {'% Share':>9}")
    lines.append("-" * 55)
    for cat, (total, count) in summary.items():
        pct = (total / total_all * 100) if total_all else 0
        bar = "█" * int(pct / 5)
        lines.append(f"  {cat:<18} {format_currency(total):>12} {count:>7}   {pct:>5.1f}%  {bar}")
    lines.append("-" * 55)
    lines.append(f"  {'TOTAL':<18} {format_currency(total_all):>12}")
    lines.append("=" * 55)
    return "\n".join(lines)


def build_monthly_report(expenses, year, month):
    """Return a monthly report string for given year/month."""
    month_expenses = filter_by_month(expenses, year, month)
    month_name = f"{year}-{month:02d}"
    lines = []
    lines.append("=" * 65)
    lines.append(f"  MONTHLY REPORT — {month_name}")
    lines.append("=" * 65)

    if not month_expenses:
        lines.append(f"  No expenses recorded for {month_name}.")
        lines.append("=" * 65)
        return "\n".join(lines)

    # Category breakdown
    summary = category_summary(month_expenses)
    total, avg, count = compute_totals(month_expenses)
    lines.append(f"  {'Category':<18} {'Total':>12} {'Count':>7}")
    lines.append("-" * 45)
    for cat, (t, c) in summary.items():
        lines.append(f"  {cat:<18} {format_currency(t):>12} {c:>7}")
    lines.append("-" * 45)
    lines.append(f"  {'TOTAL':<18} {format_currency(total):>12} {count:>7}")
    lines.append(f"  Average per expense: {format_currency(avg)}")
    lines.append("=" * 65)

    # Individual entries
    lines.append("\n  ITEMIZED EXPENSES:")
    lines.append("-" * 75)
    for e in sorted(month_expenses, key=lambda x: x.date):
        lines.append(f"  {e}")
    lines.append("=" * 75)
    return "\n".join(lines)


def build_annual_summary(expenses, year):
    """Return year-over-year monthly breakdown string."""
    year_expenses = [e for e in expenses if e.date.startswith(str(year))]
    lines = []
    lines.append("=" * 60)
    lines.append(f"  ANNUAL SUMMARY — {year}")
    lines.append("=" * 60)
    if not year_expenses:
        lines.append(f"  No expenses for {year}.")
        lines.append("=" * 60)
        return "\n".join(lines)

    monthly_totals = defaultdict(float)
    for e in year_expenses:
        month = int(e.date.split("-")[1])
        monthly_totals[month] += e.amount

    import calendar
    lines.append(f"  {'Month':<12} {'Total':>14} {'Bar':}")
    lines.append("-" * 60)
    max_total = max(monthly_totals.values()) if monthly_totals else 1
    for m in range(1, 13):
        total = monthly_totals.get(m, 0)
        bar_len = int((total / max_total) * 30) if total else 0
        bar = "█" * bar_len
        lines.append(f"  {calendar.month_name[m]:<12} {format_currency(total):>14}  {bar}")

    grand_total, grand_avg, grand_count = compute_totals(year_expenses)
    lines.append("-" * 60)
    lines.append(f"  Annual Total:   {format_currency(grand_total)}")
    lines.append(f"  Annual Average: {format_currency(grand_avg)} per expense")
    lines.append(f"  Total Records:  {grand_count}")
    lines.append("=" * 60)
    return "\n".join(lines)


# ─── Display Wrappers ─────────────────────────────────────────────────────────

def display_all_expenses(expenses):
    if not expenses:
        print("\n  ℹ️  No expenses found.")
        return
    print("\n" + build_expenses_table(expenses))


def display_category_report(expenses):
    if not expenses:
        print("\n  ℹ️  No expenses to summarize.")
        return
    print("\n" + build_category_report(expenses))


def display_monthly_report(expenses):
    available = get_available_months(expenses)
    if not available:
        print("\n  ℹ️  No expense data available.")
        return

    print("\n  Available months:")
    for i, (y, m) in enumerate(available, 1):
        print(f"    {i}. {y}-{m:02d}")

    while True:
        raw = input("\n  Select month number (or 0 to cancel): ").strip()
        try:
            choice = int(raw)
            if choice == 0:
                return
            if 1 <= choice <= len(available):
                year, month = available[choice - 1]
                report = build_monthly_report(expenses, year, month)
                print("\n" + report)
                if input("\n  Export this report to file? (y/n): ").strip().lower() == "y":
                    path = export_report(report, f"monthly_{year}_{month:02d}")
                    print(f"  ✅ Report saved to: {path}")
                return
            print(f"  ⚠️  Enter a number between 0 and {len(available)}.")
        except ValueError:
            print("  ⚠️  Invalid input.")


def display_annual_summary(expenses):
    years = sorted(set(e.date[:4] for e in expenses), reverse=True)
    if not years:
        print("\n  ℹ️  No expense data available.")
        return

    print("\n  Available years:")
    for i, y in enumerate(years, 1):
        print(f"    {i}. {y}")

    while True:
        raw = input("\n  Select year number (or 0 to cancel): ").strip()
        try:
            choice = int(raw)
            if choice == 0:
                return
            if 1 <= choice <= len(years):
                report = build_annual_summary(expenses, int(years[choice - 1]))
                print("\n" + report)
                return
            print(f"  ⚠️  Enter a number between 0 and {len(years)}.")
        except ValueError:
            print("  ⚠️  Invalid input.")
