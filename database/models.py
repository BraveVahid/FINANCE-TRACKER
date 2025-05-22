from peewee import *
from datetime import datetime
from database.db import db


class Transaction(Model):
    amount = FloatField() 
    description = CharField(null=True)
    category_name = CharField()
    date = DateField(default=datetime.now().date())
    is_income = BooleanField(default=False)

    class Meta:
        database = db


class Settings(Model):
    theme = CharField(default="Light")

    class Meta:
        database = db
