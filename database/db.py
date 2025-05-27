from peewee import *

db = SqliteDatabase("finance_tracker.db")

def setup_database():
    from database.models import Transaction, Settings
    db.connect()
    db.create_tables(models=[Transaction, Settings], safe=True)
    
    if Settings.select().count() == 0:
        Settings.create(theme="Light")
