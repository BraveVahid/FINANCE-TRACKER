from peewee import *
from datetime import datetime
from database.db import db

class BaseModel(Model):
    class Meta:
        database = db


class Transaction(BaseModel):
    amount = FloatField() 
    description = CharField(null=True)
    category_name = CharField()
    date = DateField(default=datetime.now().date())
    is_income = BooleanField(default=False)


class Settings(BaseModel):
    theme = CharField(default="Light")
