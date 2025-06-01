from peewee import *
from datetime import datetime
from database.db import db


class BaseModel(Model):
    class Meta:
        database = db


class Transaction(BaseModel):
    id = AutoField()
    amount = FloatField() 
    description = CharField(null=True)
    category_name = CharField()
    date = DateField(default=datetime.now().date())
    is_income = BooleanField(default=False)


class Settings(BaseModel):
    id = AutoField()
    theme = CharField(default="Light")
