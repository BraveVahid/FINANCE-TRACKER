from datetime import datetime
from database.models import Transaction, Category


class TransactionManager:
    @staticmethod
    def add_transaction(amount, category_name, description="", is_income=False, date=None):
        category, _ = Category.get_or_create(name=category_name)
        
        if date is None:
            date = datetime.now()
            
        transaction = Transaction.create(
            amount=amount,
            category=category,
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
    
    def update_transaction(self, transaction_id, **kwargs):
        transaction = self.get_transaction(transaction_id)
        if not transaction:
            return False
            
        if 'category_name' in kwargs:
            category, _ = Category.get_or_create(name=kwargs.pop('category_name'))
            kwargs['category'] = category
            
        for key, value in kwargs.items():
            setattr(transaction, key, value)
            
        transaction.save()
        return transaction

    @staticmethod
    def get_all_categories():
        return [category.name for category in Category.select()]
