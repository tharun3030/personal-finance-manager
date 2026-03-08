# 📖 User Guide — Personal Finance Manager

## Getting Started

Start the application:
```bash
python main.py
```

On first run, a `data/expenses.csv` file is automatically created.  
Sample data is pre-loaded so you can explore all features immediately.

---

## Menu Reference

### 1. Add New Expense
Prompts you for:
- **Amount** — positive number (e.g. `1500` or `99.50`)
- **Category** — one of: `Food`, `Transport`, `Entertainment`, `Shopping`, `Health`, `Utilities`, `Education`, `Other`
- **Date** — format `YYYY-MM-DD`, press Enter to use today's date
- **Description** — free text (required)

The expense is saved to CSV immediately.

---

### 2. View All Expenses
Displays all recorded expenses in a table:
```
Date         | Category        |     Amount | Description
------------------------------------------------------------------------
2024-01-05   | Food            |   ₹1200.00 | Grocery shopping at BigMart
2024-01-08   | Transport       |    ₹350.00 | Monthly bus pass
...
------------------------------------------------------------------------
Total Expenses: 25   |   Total: ₹32,450.00   |   Avg: ₹1,298.00
```

---

### 3. Category-wise Summary
Shows spending broken down by category with percentage share and a visual bar:
```
Category           Total        Count   % Share
-------------------------------------------------------
Food             ₹5,200.00         8    42.0%  ████████
Shopping         ₹4,500.00         2    36.4%  ███████
```

---

### 4. Monthly Report
1. Lists all months with recorded data
2. You select a month by number
3. Shows category breakdown + itemized list for that month
4. Option to export the report to a `.txt` file in `reports/`

---

### 5. Annual Summary
Select a year to see month-by-month totals with a horizontal bar chart:
```
Month            Total           Bar
------------------------------------------------------------
January        ₹7,100.00  ██████████████████████████████
February       ₹5,880.00  ████████████████████████
March          ₹5,600.00  ███████████████████████
```

---

### 6. Search Expenses
**By keyword**: searches description text (case-insensitive)  
**By category**: filters all expenses in a chosen category

---

### 7. Delete an Expense
1. Displays all expenses with row numbers
2. Enter the row number to delete
3. Confirms before deletion
4. Data is saved immediately after deletion

---

### 8. Backup / Restore Data
- **Create Backup**: copies `data/expenses.csv` to `data/backups/expenses_backup_YYYYMMDD_HHMMSS.csv`
- **Restore from Backup**: lists available backups, restores selected file
- **List Backups**: shows all available backup files

---

## Tips
- Back up your data regularly before making bulk changes
- Use monthly reports at the end of each month to review spending
- The category "Other" is a catch-all — try to be specific when adding expenses
- Exported reports are plain text and can be opened in any text editor
