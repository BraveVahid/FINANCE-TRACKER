from datetime import datetime
from database.models import Transaction
from peewee import fn


class TransactionManager:

    @staticmethod
    def add_transaction(amount, category_name, description="", is_income=False, date=None):
        if date is None:
            date = datetime.now()
            
        transaction = Transaction.create(
            amount=amount,
            category_name=category_name,
            description=description,
            is_income=is_income,
            date=date
        )
        return transaction

    @staticmethod
    def delete_transaction(transaction_id):
        transaction = Transaction.get_or_none(Transaction.id == transaction_id)
        if transaction:
            transaction.delete_instance()
            return True
        return False

    @staticmethod
    def get_transaction(transaction_id):
        return Transaction.get_or_none(Transaction.id == transaction_id)

    @staticmethod
    def get_all_categories():
        return [t.category_name for t in Transaction.select(fn.DISTINCT(Transaction.category_name))]
