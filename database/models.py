from peewee import *
from datetime import datetime
from database.db import db


class BaseModel(Model):
    """
    Base model class for all database models.
    
    This class defines the database connection for all models.
    """
    class Meta:
        database = db


class Category(BaseModel):
    """
    Model representing a transaction category.
    
    Attributes:
        name (CharField): The name of the category (unique)
    """
    name = CharField(unique=True)


class Transaction(BaseModel):
    """
    Model representing a financial transaction.
    
    Attributes:
        amount (FloatField): The transaction amount
        description (CharField): Optional description of the transaction
        category (ForeignKeyField): Reference to the transaction category
        date (DateTimeField): Date and time of the transaction
        is_income (BooleanField): Whether the transaction is income (True) or expense (False)
    """
    amount = FloatField()
    description = CharField(null=True)
    category = ForeignKeyField(Category, backref='transactions')
    date = DateTimeField(default=datetime.now)
    is_income = BooleanField(default=False)


class Settings(BaseModel):
    """
    Model representing application settings.
    
    Attributes:
        theme (CharField): The UI theme (default is "Light")
    """
    theme = CharField(default="Light")
