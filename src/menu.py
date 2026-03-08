"""
menu.py - Command-line interface and menu system
Personal Finance Manager
"""

from src.expense import Expense, VALID_CATEGORIES
from src.file_manager import (
    load_expenses, save_expenses,
    backup_data, restore_data, list_backups
)
from src.utils import (
    get_valid_amount, get_valid_category, get_valid_date,
    get_valid_description, get_menu_choice, print_header,
    print_divider, pause, confirm, filter_by_keyword, filter_by_category
)
from src.reports import (
    display_all_expenses, display_category_report,
    display_monthly_report, display_annual_summary
)


def clear_screen():
    print("\n" * 2)


def print_main_menu():
    print_header("PERSONAL FINANCE MANAGER")
    print("  MAIN MENU\n")
    print("  1. Add New Expense")
    print("  2. View All Expenses")
    print("  3. Category-wise Summary")
    print("  4. Monthly Report")
    print("  5. Annual Summary")
    print("  6. Search Expenses")
    print("  7. Delete an Expense")
    print("  8. Backup / Restore Data")
    print("  9. Exit")
    print_divider()


def add_expense(expenses):
    print_header("ADD NEW EXPENSE")
    try:
        amount = get_valid_amount("  Enter amount: ₹")
        category = get_valid_category("  Enter category: ")
        date = get_valid_date("  Enter date (YYYY-MM-DD) or Enter for today: ")
        description = get_valid_description("  Enter description: ")

        expense = Expense(amount, category, date, description)
        expenses.append(expense)
        save_expenses(expenses)

        print(f"\n  ✅ Expense added successfully!")
        print(f"     {expense}")
    except KeyboardInterrupt:
        print("\n  ↩️  Add cancelled.")
    except Exception as e:
        print(f"\n  ❌ Error adding expense: {e}")


def view_all_expenses(expenses):
    print_header("VIEW ALL EXPENSES")
    display_all_expenses(expenses)


def category_summary_menu(expenses):
    print_header("CATEGORY-WISE SUMMARY")
    display_category_report(expenses)


def monthly_report_menu(expenses):
    print_header("MONTHLY REPORT")
    display_monthly_report(expenses)


def annual_summary_menu(expenses):
    print_header("ANNUAL SUMMARY")
    display_annual_summary(expenses)


def search_expenses(expenses):
    print_header("SEARCH EXPENSES")
    print("  Search by:")
    print("  1. Keyword in description")
    print("  2. Category")
    print_divider("-", 40)
    choice = get_menu_choice(2, "  Your choice: ")

    if choice == 1:
        keyword = input("  Enter keyword: ").strip()
        results = filter_by_keyword(expenses, keyword)
        print(f"\n  Found {len(results)} result(s) for '{keyword}':")
        display_all_expenses(results)

    elif choice == 2:
        category = get_valid_category("  Enter category to filter: ")
        results = filter_by_category(expenses, category)
        print(f"\n  Expenses in category '{category}':")
        display_all_expenses(results)


def delete_expense(expenses):
    print_header("DELETE AN EXPENSE")
    if not expenses:
        print("  ℹ️  No expenses to delete.")
        return

    display_all_expenses(expenses)
    print()
    raw = input("  Enter expense number to delete (1 = first row, 0 to cancel): ").strip()
    try:
        idx = int(raw)
        if idx == 0:
            return
        if 1 <= idx <= len(expenses):
            target = expenses[idx - 1]
            print(f"\n  Selected: {target}")
            if confirm("  Confirm delete? (y/n): "):
                expenses.pop(idx - 1)
                save_expenses(expenses)
                print("  ✅ Expense deleted.")
            else:
                print("  ↩️  Deletion cancelled.")
        else:
            print("  ⚠️  Invalid number.")
    except ValueError:
        print("  ⚠️  Invalid input.")


def backup_restore_menu(expenses):
    print_header("BACKUP / RESTORE DATA")
    print("  1. Create Backup")
    print("  2. Restore from Backup")
    print("  3. List Backups")
    print("  4. Back to Main Menu")
    print_divider("-", 40)
    choice = get_menu_choice(4, "  Your choice: ")

    if choice == 1:
        path, err = backup_data()
        if err:
            print(f"  ❌ Backup failed: {err}")
        else:
            print(f"  ✅ Backup created: {path}")

    elif choice == 2:
        backups = list_backups()
        if not backups:
            print("  ℹ️  No backups found.")
            return
        print("\n  Available backups:")
        for i, b in enumerate(backups, 1):
            print(f"    {i}. {b}")
        raw = input("\n  Enter backup number to restore (0 to cancel): ").strip()
        try:
            idx = int(raw)
            if idx == 0:
                return
            if 1 <= idx <= len(backups):
                if confirm("  This will overwrite current data. Continue? (y/n): "):
                    ok, err = restore_data(backups[idx - 1])
                    if ok:
                        expenses.clear()
                        expenses.extend(load_expenses())
                        print("  ✅ Data restored successfully.")
                    else:
                        print(f"  ❌ Restore failed: {err}")
            else:
                print("  ⚠️  Invalid number.")
        except ValueError:
            print("  ⚠️  Invalid input.")

    elif choice == 3:
        backups = list_backups()
        if not backups:
            print("  ℹ️  No backups found.")
        else:
            print(f"\n  {len(backups)} backup(s) found:")
            for b in backups:
                print(f"    • {b}")


def run_app():
    """Main application loop."""
    expenses = load_expenses()
    print(f"\n  ✅ Loaded {len(expenses)} expense(s) from file.")

    while True:
        clear_screen()
        print_main_menu()
        choice = get_menu_choice(9, "\n  Enter your choice (1-9): ")

        clear_screen()

        if choice == 1:
            add_expense(expenses)
        elif choice == 2:
            view_all_expenses(expenses)
        elif choice == 3:
            category_summary_menu(expenses)
        elif choice == 4:
            monthly_report_menu(expenses)
        elif choice == 5:
            annual_summary_menu(expenses)
        elif choice == 6:
            search_expenses(expenses)
        elif choice == 7:
            delete_expense(expenses)
        elif choice == 8:
            backup_restore_menu(expenses)
        elif choice == 9:
            print("\n  👋 Thank you for using Personal Finance Manager. Goodbye!\n")
            break

        pause()
