from datetime import datetime


class InputValidator:
    """
    A class for validating user input in the finance application.
    
    This class provides static methods to validate various types of input
    such as amounts, categories, dates, and descriptions.
    """
    
    @staticmethod
    def validate_amount(amount):
        """
        Validate that an amount is a positive number.
        
        Args:
            amount (str): The amount to validate
            
        Returns:
            tuple: (is_valid, result)
                - is_valid (bool): True if valid, False otherwise
                - result: The converted float value if valid, error message if invalid
        """
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Amount must be greater than zero"
            return True, amount
        except ValueError:
            return False, "Amount must be a valid number"

    @staticmethod
    def validate_category(category):
        """
        Validate that a category name meets requirements.
        
        Requirements:
        - Not empty
        - 15 characters or fewer
        - Contains only alphanumeric characters and spaces
        
        Args:
            category (str): The category name to validate
            
        Returns:
            tuple: (is_valid, result)
                - is_valid (bool): True if valid, False otherwise
                - result: The trimmed category if valid, error message if invalid
        """
        if len(category.strip()) == 0:
            return False, "Category cannot be empty"

        if len(category.strip()) > 15:
            return False, "Category must be 15 characters or less"

        if not all(c.isalnum() or c.isspace() for c in category.strip()):
            return False, "Category must contain only letters, numbers, and spaces"

        return True, category.strip()

    @staticmethod
    def validate_date(date):
        """
        Validate that a date string is in the correct format and not in the future.
        
        Args:
            date (str): Date string in YYYY-MM-DD format
            
        Returns:
            tuple: (is_valid, result)
                - is_valid (bool): True if valid, False otherwise
                - result: The parsed datetime object if valid, error message if invalid
        """
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
        """
        Validate that a description is not too long.
        
        Args:
            description (str): The description to validate
            
        Returns:
            tuple: (is_valid, result)
                - is_valid (bool): True if valid, False otherwise
                - result: The description if valid, error message if invalid
        """
        if len(description) > 100:
            return False, "Description must be 100 characters or less"
        return True, description
