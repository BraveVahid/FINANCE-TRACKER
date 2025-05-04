from peewee import *

db = SqliteDatabase('finance_assistant.db')

def ensure_settings():
    from database.models import Settings
    if Settings.select().count() == 0:
        Settings.create(theme="Light")
    else:
         Settings.select().first()

def setup_database():
    from database.models import Transaction, Category, Settings
    db.connect()
    db.create_tables([Transaction, Category, Settings], safe=True)
    ensure_settings()
