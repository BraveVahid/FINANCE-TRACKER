import csv


def export_transactions(transactions, file_path="transactions"):
    try:
        with open(file_path, "w", newline="") as file:
            if not transactions:
                return False, "No transactions to export"

            fieldnames = transactions[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
            return True, file_path
        
    except FileNotFoundError:
        return False, f"Error: The directory for '{file_path}' does not exist."

    except PermissionError:
        return False, f"Error: Permission denied to write to '{file_path}'."

    except:
        return False
