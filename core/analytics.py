from peewee import fn
from datetime import datetime
import pandas as pd
from database.models import Transaction, Category


class FinancialAnalytics:
    @staticmethod
    def get_monthly_balance():
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        income_query = (Transaction.select(fn.SUM(Transaction.amount).alias('total')).where(
            (Transaction.is_income == True) &
            (fn.strftime('%m', Transaction.date) == str(current_month).zfill(2)) &
            (fn.strftime('%Y', Transaction.date) == str(current_year))
        ))

        expense_query = (Transaction.select(fn.SUM(Transaction.amount).alias('total')).where(
            (Transaction.is_income == False) &
            (fn.strftime('%m', Transaction.date) == str(current_month).zfill(2)) &
            (fn.strftime('%Y', Transaction.date) == str(current_year))
        ))
        
        income = income_query.scalar() or 0
        expenses = expense_query.scalar() or 0
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses
        }

    @staticmethod
    def get_expense_breakdown():
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        expense_data = (Transaction.select(Category.name, fn.SUM(Transaction.amount).alias('total')).join(Category).where(
            (Transaction.is_income == False) &
            (fn.strftime('%m', Transaction.date) == str(current_month).zfill(2)) &
            (fn.strftime('%Y', Transaction.date) == str(current_year))
        ).group_by(Category.name))
        
        result = {}
        for item in expense_data:
            result[item.category.name] = item.total
            
        total_expenses = sum(result.values()) or 1

        for category, amount in result.items():
            result[category] = {
                'amount': amount,
                'percentage': (amount / total_expenses) * 100
            }
        return result

    @staticmethod
    def get_transaction_history(limit=50):
        query = Transaction.select(Transaction, Category.name).join(Category).order_by(Transaction.date.desc())
        
        if limit is not None:
            query = query.limit(limit)
        
        transactions = query

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
        result = []
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        for i in range(months):
            target_month = ((current_month - i - 1) % 12) + 1
            target_year = current_year if target_month <= current_month else current_year - 1
            
            income_query = (Transaction.select(fn.SUM(Transaction.amount).alias('total')).where(
                (Transaction.is_income == True) &
                (fn.strftime('%m', Transaction.date) == str(target_month).zfill(2)) &
                (fn.strftime('%Y', Transaction.date) == str(target_year))
            ))
                           
            expense_query = (Transaction.select(fn.SUM(Transaction.amount).alias('total')).where(
                (Transaction.is_income == False) &
                (fn.strftime('%m', Transaction.date) == str(target_month).zfill(2)) &
                (fn.strftime('%Y', Transaction.date) == str(target_year))
            ))
            
            income = income_query.scalar() or 0
            expenses = expense_query.scalar() or 0
            
            month_name = datetime(target_year, target_month, 1).strftime('%b')
            
            result.append({
                'month': month_name,
                'income': income,
                'expenses': expenses,
                'balance': income - expenses
            })
            
        return result[::-1]
