# 💰 Personal Finance Manager

A comprehensive command-line personal finance tracking system built in Python using object-oriented design, CSV-based data persistence, and modular code architecture.

---

## 📋 Project Overview

The Personal Finance Manager helps you track daily expenses, generate insightful reports, and analyze your spending patterns — all from the terminal. It requires **no external libraries**, using only Python's standard library.

### Key Features
- ✅ Add, view, search, and delete expenses
- ✅ Category-wise spending summary with visual bar charts
- ✅ Monthly and annual reports (exportable to `.txt`)
- ✅ Automatic data backup and restore
- ✅ Full input validation and error handling
- ✅ 19 unit tests covering all core modules

---

## 🗂️ Project Structure

```
finance_manager/
│
├── main.py                   # Entry point — run this to start the app
├── requirements.txt          # No external dependencies needed
│
├── src/                      # Source code modules
│   ├── __init__.py
│   ├── expense.py            # Expense class definition
│   ├── file_manager.py       # CSV read/write, backup/restore
│   ├── menu.py               # CLI menus and user interaction
│   ├── reports.py            # Report generation and analysis
│   └── utils.py              # Validation helpers and formatters
│
├── data/
│   ├── expenses.csv          # Main data file (auto-created)
│   └── backups/              # Timestamped backup files
│
├── reports/                  # Exported report text files
│
├── tests/
│   └── test_finance.py       # 19 unit tests (unittest)
│
└── docs/
    └── user_guide.md         # Detailed user guide
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- No pip installs required

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/personal-finance-manager.git
cd personal-finance-manager

# 2. Verify Python version
python --version   # Should be 3.8+

# 3. Run the application
python main.py
```

---

## 🚀 Usage

```
python main.py
```

You will see the main menu:

```
=================================================================
  PERSONAL FINANCE MANAGER
=================================================================
  MAIN MENU

  1. Add New Expense
  2. View All Expenses
  3. Category-wise Summary
  4. Monthly Report
  5. Annual Summary
  6. Search Expenses
  7. Delete an Expense
  8. Backup / Restore Data
  9. Exit
```

### Adding an Expense
```
ADD NEW EXPENSE
  Enter amount: ₹1500
  Categories: Food, Transport, Entertainment, Shopping, Health, Utilities, Education, Other
  Enter category: Food
  Enter date (YYYY-MM-DD) or Enter for today: 2024-03-15
  Enter description: Grocery shopping

  ✅ Expense added successfully!
     2024-03-15 | Food            |    ₹1500.00 | Grocery shopping
```

### Category Summary Output
```
=======================================================
  CATEGORY-WISE SUMMARY
=======================================================
  Category           Total        Count   % Share
-------------------------------------------------------
  Food             ₹5,200.00         8    42.0%  ████████
  Shopping         ₹4,500.00         2    36.4%  ███████
  Utilities        ₹3,550.00         3    28.7%  █████
  ...
```

---

## 🧪 Running Tests

```bash
python tests/test_finance.py
```

Expected output:
```
Running Personal Finance Manager Tests...

test_amount_is_float ... ok
test_category_case_insensitive ... ok
...

Ran 19 tests in 0.011s
OK
```

---

## 🏗️ Architecture & Design

### Data Flow
```
User Input → Validation (utils.py) → Expense Object (expense.py)
                                             ↓
                                    Save to CSV (file_manager.py)
                                             ↓
                              Load & Analyze (reports.py) → Display
```

### Core Classes & Modules

| Module | Responsibility |
|--------|---------------|
| `expense.py` | `Expense` class with validation, `__str__`, `to_dict` |
| `file_manager.py` | `load_expenses()`, `save_expenses()`, backup/restore |
| `utils.py` | Input validation, filtering, formatting helpers |
| `reports.py` | `compute_totals()`, `category_summary()`, report builders |
| `menu.py` | All CLI menus and the main `run_app()` loop |

### Data Persistence
Expenses are stored as a flat CSV file (`data/expenses.csv`):
```
Date,Category,Amount,Description
2024-01-15,Food,1500.0,Grocery shopping
2024-01-18,Transport,350.0,Monthly bus pass
```

### Expense Categories
`Food`, `Transport`, `Entertainment`, `Shopping`, `Health`, `Utilities`, `Education`, `Other`

---

## 🛡️ Error Handling

- **Invalid amounts**: Re-prompts until a positive number is entered
- **Invalid dates**: Enforces `YYYY-MM-DD` format
- **Invalid categories**: Defaults to `Other` with a warning
- **Missing data file**: Returns empty list (file created on first save)
- **Corrupt CSV rows**: Skipped with a warning, rest of data preserved
- **KeyboardInterrupt**: Caught gracefully at app level

---

## 💡 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run from the project root: `python main.py` |
| Data not saving | Check write permissions on the `data/` directory |
| Date rejected | Use format `YYYY-MM-DD` e.g. `2024-03-15` |
| Category not accepted | Enter exactly as shown (case-insensitive) |

---

## 📦 Dependencies

No external packages. Uses only Python Standard Library:
- `csv` — data persistence
- `os`, `shutil` — file and directory operations  
- `datetime`, `calendar` — date handling
- `collections` — `defaultdict` for aggregation
- `unittest` — test framework

---

## 👤 Author

Built as a Python learning project covering:
- Object-Oriented Programming (classes, methods, encapsulation)
- File I/O with CSV module
- Modular code organization
- Input validation and error handling
- Unit testing with `unittest`
- Command-line interface design

