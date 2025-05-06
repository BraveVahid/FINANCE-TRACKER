# Finance Tracker

A personal finance management application built with Python, CustomTkinter, and SQLite.

## Features

- **Dashboard**: Visual overview of your financial status
  - Monthly summary (income, expenses, balance)
  - Expense breakdown by category (pie chart)
  - Monthly balance trend (line chart)
  - Income vs. expenses comparison (bar chart)

- **Transaction Management**
  - Add new income/expense transactions
  - View, search, and filter transaction history
  - Delete transactions
  - Automatic category management

- **Data Export**
  - Export all transactions to CSV

- **Settings**
  - Light/Dark theme toggle
  - Application preferences

## Installation

### Prerequisites
- Python 3.8+
- pip

### Steps
1. Clone the repository:
```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```


2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Dependencies

- `customtkinter` - Modern UI framework
- `peewee` - ORM for SQLite database
- `matplotlib` - Data visualization
- `pandas` - Data manipulation

## Database Structure

The application uses SQLite with the following tables:

 **Transaction**:
- amount (Float)
- description (String)
- category (ForeignKey to Category)
- date (DateTime)
- is_income (Boolean)

 **Category**:
- name (String, unique)

 **Settings**:
- theme (String)

## Usage

1. **Adding Transactions**:
- Navigate to the Transactions tab
- Fill in the transaction details (amount, category, etc.)
- Click "Add Transaction"

2. **Viewing Reports**:
- The Dashboard tab automatically shows your financial overview
- Charts update in real-time when new transactions are added

3. **Changing Theme**:
- Go to Settings tab
- Click "Toggle Theme" to switch between light and dark modes

4. **Exporting Data**:
- In Settings tab, click "Export Transactions"
- Choose a location to save the CSV file
