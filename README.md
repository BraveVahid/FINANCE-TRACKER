# Personal Finance Tracker

A Python desktop application with CustomTkinter GUI for tracking income/expenses, featuring financial analytics, interactive charts, data encryption, and CSV export capabilities.

## Features

- **Transaction Management**: Add, edit, and delete income/expense transactions
- **Financial Analytics**: Monthly balance tracking and expense categorization
- **Interactive Charts**: Pie charts, line graphs, and bar charts for data visualization
- **Data Security**: Built-in encryption for sensitive financial data
- **Theme Support**: Light and dark mode themes
- **Data Export**: Export transaction history to CSV format
- **Search & Filter**: Search through transaction history

### Dashboard
- Monthly summary with income, expenses, and balance
- Expense breakdown pie chart
- Balance trend line chart
- Income vs. expenses comparison

### Transaction Management
- Easy-to-use form for adding transactions
- Transaction history with search functionality

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup
1. Clone the repository:
```bash
git clone https://github.com/BraveVahid/FINANCE-TRACKER
cd FINANCE-TRACKER
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Dependencies

- `customtkinter` - Modern GUI framework
- `pandas` - Data manipulation and analysis
- `peewee` - Lightweight ORM for database operations
- `matplotlib` - Chart generation and data visualization
- `numpy` - Numerical computing support

## Usage

### Adding Transactions
1. Navigate to the "Transactions" tab
2. Fill in the transaction details:
   - Amount (required)
   - Category (required, max 15 characters)
   - Description (optional, max 100 characters)
   - Type (Income or Expense)
   - Date (YYYY-MM-DD format)
3. Click "Add Transaction"

### Viewing Analytics
1. Go to the "Dashboard" tab to view:
   - Current month's financial summary
   - Expense breakdown by category
   - 6-month balance trend
   - Income vs expenses comparison

### Exporting Data
1. Navigate to the "Settings" tab
2. Click "Export Transactions"
3. Choose your save location
4. Data will be exported in CSV format

### Changing Theme
1. Go to the "Settings" tab
2. Click "Toggle Theme" to switch between Light and Dark modes

## Database

The application uses SQLite database (`finance_tracker.db`) to store:
- Transaction records (encrypted)
- Application settings
- User preferences

## Security Features

- **Data Encryption**: All sensitive data (amounts, categories, descriptions) are encrypted before database storage
- **Input Validation**: Comprehensive validation prevents invalid data entry
- **Local Storage**: All data is stored locally on your machine

## Screenshots
![Dark Mode](Screenshot1.png)
![Light Mode](Screenshot2.png)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

### Common Issues

**Application won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.7+ required)

**Charts not displaying:**
- Verify matplotlib installation
- Try switching themes in Settings

**Database errors:**
- Delete `finance_tracker.db` to reset the database
- Restart the application

**Export not working:**
- Ensure you have write permissions to the selected directory
- Check that the file path is valid

## Support

For issues, questions, or contributions, please create an issue in the repository's issue tracker.
