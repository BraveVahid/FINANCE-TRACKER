from datetime import datetime
from database.models import Transaction, Category


class TransactionManager:
    """
    Manager class for handling transaction-related operations.
    
    This class provides methods to create, retrieve, update, and delete
    financial transactions in the database.
    """

    @staticmethod
    def add_transaction(amount, category_name, description="", is_income=False, date=None):
        """
        Add a new transaction to the database.
        
        Args:
            amount (float): Transaction amount
            category_name (str): Name of the transaction category
            description (str, optional): Transaction description. Defaults to empty string.
            is_income (bool, optional): Whether the transaction is income. Defaults to False.
            date (datetime, optional): Transaction date. Defaults to current date/time.
            
        Returns:
            Transaction: The newly created Transaction instance
        """
        # Get or create category
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
        """
        Delete a transaction from the database.
        
        Args:
            transaction_id (int): ID of the transaction to delete
            
        Returns:
            bool: True if transaction was deleted, False if not found
        """
        transaction = Transaction.get_or_none(Transaction.id == transaction_id)
        if transaction:
            transaction.delete_instance()
            return True
        return False

    @staticmethod
    def get_transaction(transaction_id):
        """
        Retrieve a transaction by its ID.
        
        Args:
            transaction_id (int): ID of the transaction to retrieve
            
        Returns:
            Transaction or None: The transaction if found, None otherwise
        """
        return Transaction.get_or_none(Transaction.id == transaction_id)

    @staticmethod
    def get_all_categories():
        """
        Get a list of all category names in the database.
        
        Returns:
            list: List of category names as strings
        """
        return [category.name for category in Category.select()]
