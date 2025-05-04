from peewee import *

# Database connection
db = SqliteDatabase("finance_tracker.db")

def ensure_settings():
    """
    Ensure that default settings exist in the database.
    
    This function checks if settings exist and creates default ones if needed.
    """
    from database.models import Settings
    if Settings.select().count() == 0:
        Settings.create(theme="Light")
    else:
         Settings.select().first()

def setup_database():
    """
    Set up the database by creating tables and ensuring default settings.
    
    This function should be called when the application starts.
    """
    from database.models import Transaction, Category, Settings
    db.connect()
    db.create_tables([Transaction, Category, Settings], safe=True)
    ensure_settings()
