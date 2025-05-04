from datetime import datetime


class InputValidator:
    @staticmethod
    def validate_amount(amount):
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Amount must be greater than zero"
            return True, amount
        except ValueError:
            return False, "Amount must be a valid number"

    @staticmethod
    def validate_category(category):
        if len(category.strip()) == 0:
            return False, "Category cannot be empty"

        if len(category.strip()) > 15:
            return False, "Category must be 15 characters or less"

        if not all(c.isalnum() or c.isspace() for c in category.strip()):
            return False, "Category must contain only letters, numbers, and spaces"

        return True, category.strip()

    @staticmethod
    def validate_date(date):
        try:
            input_date = datetime.strptime(date, "%Y-%m-%d")
            current_date = datetime.now()

            if input_date.date() > current_date.date():
                return False, "Future dates are not allowed"

            return True, input_date
        except ValueError:
            return False, "Date must be in YYYY-MM-DD format"

    @staticmethod
    def validate_description(description):
        if len(description) > 100:
            return False, "Description must be 100 characters or less"
        return True, description
