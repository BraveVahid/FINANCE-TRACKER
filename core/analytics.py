from peewee import fn
from datetime import datetime
import pandas as pd
from database.models import Transaction
from utils.crypto import CryptoManager
from dateutil.relativedelta import relativedelta


class FinancialAnalytics:
    @staticmethod
    def get_monthly_balance():
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        income_transactions = (Transaction.select().where(
            (Transaction.is_income == True) &
            (fn.strftime("%m", Transaction.date) == str(current_month).zfill(2)) &
            (fn.strftime("%Y", Transaction.date) == str(current_year))
        ))

        expense_transactions = (Transaction.select().where(
            (Transaction.is_income == False) &
            (fn.strftime("%m", Transaction.date) == str(current_month).zfill(2)) &
            (fn.strftime("%Y", Transaction.date) == str(current_year))
        ))

        income = sum([CryptoManager.decrypt_number(t.amount) for t in income_transactions])
        expenses = sum([CryptoManager.decrypt_number(t.amount) for t in expense_transactions])
        
        return {
            "income": income,
            "expenses": expenses,
            "balance": income - expenses
        }

    @staticmethod
    def get_expense_breakdown():
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        expense_transactions = (Transaction.select().where(
            (Transaction.is_income == False) &
            (fn.strftime("%m", Transaction.date) == str(current_month).zfill(2)) &
            (fn.strftime("%Y", Transaction.date) == str(current_year))
        ))
        
        result = {}
        for transaction in expense_transactions:
            category = CryptoManager.decrypt_string(transaction.category_name)
            amount = CryptoManager.decrypt_number(transaction.amount)
            
            if category in result:
                result[category] += amount
            else:
                result[category] = amount
            
        total_expenses = sum(result.values()) or 1

        for category, amount in result.items():
            result[category] = {
                "amount": amount,
                "percentage": (amount / total_expenses) * 100
            }
        return result

    @staticmethod
    def get_transaction_history(limit=50):
        transactions = Transaction.select().order_by(Transaction.date.desc()).limit(limit)

        data = []
        for t in transactions:
            data.append({
                "id": t.id,
                "date": t.date,
                "category": CryptoManager.decrypt_string(t.category_name),
                "description": CryptoManager.decrypt_string(t.description) if t.description else None,
                "amount": CryptoManager.decrypt_number(t.amount),
                "is_income": t.is_income
            })
        return pd.DataFrame(data)

    @staticmethod
    def get_monthly_trend():
        result = []

        current_date = datetime.now().replace(day=1)

        for i in range(6):
            target_date = current_date - relativedelta(months=i)
            target_year = target_date.year
            target_month = target_date.month

            income_transactions = (Transaction.select().where(
                (Transaction.is_income == True) &
                (fn.strftime("%m", Transaction.date) == str(target_month).zfill(2)) &
                (fn.strftime("%Y", Transaction.date) == str(target_year))
            ))
            expense_transactions = (Transaction.select().where(
                (Transaction.is_income == False) &
                (fn.strftime("%m", Transaction.date) == str(target_month).zfill(2)) &
                (fn.strftime("%Y", Transaction.date) == str(target_year))
            ))

            income = sum([CryptoManager.decrypt_number(t.amount) for t in income_transactions])
            expenses = sum([CryptoManager.decrypt_number(t.amount) for t in expense_transactions])
            month_name = target_date.strftime("%b")

            result.append({
                "month": month_name,
                "income": income,
                "expenses": expenses,
                "balance": income - expenses
            })

        return result[::-1]
