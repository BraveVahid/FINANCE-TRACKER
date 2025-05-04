from peewee import fn
from datetime import datetime
import pandas as pd
from database.models import Transaction, Category


class FinancialAnalytics:
    """
    A class for performing financial analytics on transaction data.
    
    This class provides methods to analyze financial data stored in the database,
    including monthly balance calculations, expense breakdown, transaction history,
    and monthly trend analysis.
    """

    @staticmethod
    def get_monthly_balance():
        """
        Calculate the income, expenses, and balance for the current month.
        
        Returns:
            dict: A dictionary containing the following keys:
                - income (float): Total income for the current month.
                - expenses (float): Total expenses for the current month.
                - balance (float): Net balance (income - expenses) for the current month.
        """
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Query to get total income for current month
        income_query = (Transaction.select(fn.SUM(Transaction.amount).alias('total')).where(
            (Transaction.is_income == True) &
            (fn.strftime('%m', Transaction.date) == str(current_month).zfill(2)) &
            (fn.strftime('%Y', Transaction.date) == str(current_year))
        ))

        # Query to get total expenses for current month
        expense_query = (Transaction.select(fn.SUM(Transaction.amount).alias('total')).where(
            (Transaction.is_income == False) &
            (fn.strftime('%m', Transaction.date) == str(current_month).zfill(2)) &
            (fn.strftime('%Y', Transaction.date) == str(current_year))
        ))
        
        # Use 0 as default if no transactions exist
        income = income_query.scalar() or 0
        expenses = expense_query.scalar() or 0
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses
        }

    @staticmethod
    def get_expense_breakdown():
        """
        Get a breakdown of expenses by category for the current month.
        
        Returns:
            dict: A dictionary where keys are category names and values are dictionaries with:
                - amount (float): Total amount spent in that category
                - percentage (float): Percentage of total expenses this category represents
        """
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Get expenses grouped by category
        expense_data = (Transaction.select(Category.name, fn.SUM(Transaction.amount).alias('total')).join(Category).where(
            (Transaction.is_income == False) &
            (fn.strftime('%m', Transaction.date) == str(current_month).zfill(2)) &
            (fn.strftime('%Y', Transaction.date) == str(current_year))
        ).group_by(Category.name))
        
        result = {}
        for item in expense_data:
            result[item.category.name] = item.total
            
        # Calculate percentage of total for each category (avoid division by zero)
        total_expenses = sum(result.values()) or 1

        for category, amount in result.items():
            result[category] = {
                'amount': amount,
                'percentage': (amount / total_expenses) * 100
            }
        return result

    @staticmethod
    def get_transaction_history(limit=50):
        """
        Retrieve transaction history sorted by date (most recent first).
        
        Args:
            limit (int, optional): Maximum number of transactions to return. Defaults to 50.
            
        Returns:
            pandas.DataFrame: DataFrame containing transaction records with the following columns:
                - id: Transaction ID
                - date: Transaction date
                - category: Category name
                - description: Transaction description
                - amount: Transaction amount
                - is_income: Boolean indicating if transaction is income
        """
        query = Transaction.select(Transaction, Category.name).join(Category).order_by(Transaction.date.desc())
        
        if limit is not None:
            query = query.limit(limit)
        
        transactions = query

        # Convert query results to list of dictionaries
        data = []
        for t in transactions:
            data.append({
                'id': t.id,
                'date': t.date,
                'category': t.category.name,
                'description': t.description,
                'amount': t.amount,
                'is_income': t.is_income
            })
            
        return pd.DataFrame(data)

    @staticmethod
    def get_monthly_trend(months=6):
        """
        Get monthly income, expenses, and balance trends for the past specified months.
        
        Args:
            months (int, optional): Number of previous months to include. Defaults to 6.
            
        Returns:
            list: List of dictionaries, each containing:
                - month (str): Month abbreviation (e.g., 'Jan')
                - income (float): Total income for that month
                - expenses (float): Total expenses for that month
                - balance (float): Net balance for that month
                
        Note:
            Results are returned in chronological order (oldest first).
        """
        result = []
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Calculate data for each month in the specified range
        for i in range(months):
            target_month = ((current_month - i - 1) % 12) + 1
            target_year = current_year if target_month <= current_month else current_year - 1
            
            # Query for monthly income
            income_query = (Transaction.select(fn.SUM(Transaction.amount).alias('total')).where(
                (Transaction.is_income == True) &
                (fn.strftime('%m', Transaction.date) == str(target_month).zfill(2)) &
                (fn.strftime('%Y', Transaction.date) == str(target_year))
            ))
                           
            # Query for monthly expenses
            expense_query = (Transaction.select(fn.SUM(Transaction.amount).alias('total')).where(
                (Transaction.is_income == False) &
                (fn.strftime('%m', Transaction.date) == str(target_month).zfill(2)) &
                (fn.strftime('%Y', Transaction.date) == str(target_year))
            ))
            
            # Use 0 as default if no transactions exist
            income = income_query.scalar() or 0
            expenses = expense_query.scalar() or 0
            
            month_name = datetime(target_year, target_month, 1).strftime('%b')
            
            result.append({
                'month': month_name,
                'income': income,
                'expenses': expenses,
                'balance': income - expenses
            })
            
        # Return results in chronological order
        return result[::-1]
