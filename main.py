from ui.app import FinanceTrackerApp
from database.db import setup_database

if __name__ == "__main__":
    setup_database()
    app = FinanceTrackerApp()
    app.run()
