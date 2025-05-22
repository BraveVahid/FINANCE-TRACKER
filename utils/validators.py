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
        category = category.strip()
        if len(category) == 0:
            return False, "This field cannot be left empty please provide a category."

        if len(category) > 15:
            return False, "The category most not exceed 15 characters."

        if not category.isalpha():
            return False, "the category must contain only letters, numbers, and spaces"

        return True, category

    @staticmethod
    def validate_date(date):
        try:
            input_date = datetime.strptime(date, "%Y-%m-%d")
            current_date = datetime.now()

            if input_date.date() > current_date.date():
                return False, "Future-dated entries are not allowed."

            return True, input_date
        except ValueError:
            return False, "The date must be entered in the format YYYY-MM-DD"

    @staticmethod
    def validate_description(description):
        if len(description) > 100:
            return False, "The description must not be more than 100 characters."
        return True, description
