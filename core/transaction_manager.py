from datetime import datetime
from database.models import Transaction
from utils.crypto import CryptoManager


class TransactionManager:
    @staticmethod
    def add_transaction(amount, category_name, description="", is_income=False, date=None):
        if date is None:
            date = datetime.now()
            
        transaction = Transaction.create(
            amount=CryptoManager.encrypt_number(amount),
            category_name=CryptoManager.encrypt_string(category_name),
            description=CryptoManager.encrypt_string(description) if description else "",
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
    def get_all_categories():
        transactions = Transaction.select()
        categories = set()
        for t in transactions:
            categories.add(CryptoManager.decrypt_string(t.category_name))
        return list(categories)
