from ui.app import FinanceTrackerApp
from database.db import setup_database

if __name__ == "__main__":
    try:
        setup_database()
        app = FinanceTrackerApp()
        app.run()
    except Exception as e:
        print(f"{e.__class__.__name__} running error")
