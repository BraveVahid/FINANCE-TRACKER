from ui.app import FinanceTrackerApp
from database.db import setup_database


if __name__ == "__main__":
    """
    Main entry point for the Finance Tracker application.
    
    Sets up the database and launches the application.
    """
    try:
        setup_database()
        app = FinanceTrackerApp()
        app.run()
    except Exception as e:
        print(f"{e.__class__.__name__} running error")
