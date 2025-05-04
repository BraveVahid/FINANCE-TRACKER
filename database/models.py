from peewee import *
from datetime import datetime
from database.db import db

class BaseModel(Model):
    class Meta:
        database = db

class Category(BaseModel):
    name = CharField(unique=True)

class Transaction(BaseModel):
    amount = FloatField()
    description = CharField(null=True)
    category = ForeignKeyField(Category, backref='transactions')
    date = DateTimeField(default=datetime.now)
    is_income = BooleanField(default=False)

class Settings(BaseModel):
    theme = CharField(default="Light")
