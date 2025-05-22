import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime
from core.transaction_manager import TransactionManager
from core.analytics import FinancialAnalytics
from utils.validators import InputValidator


class TransactionPanel(ctk.CTkFrame):
    def __init__(self, parent, refresh_callback=None):
        super().__init__(parent)

        self.transaction_manager = TransactionManager()
        self.analytics = FinancialAnalytics()
        self.refresh_callback = refresh_callback
        self.categories = self.transaction_manager.get_all_categories()

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.setup_input_form()
        self.setup_transaction_list()

        self.refresh_transactions()

    def setup_input_form(self):
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        title_label = ctk.CTkLabel(self.input_frame, text="ADD TRANSACTION", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(15, 20))

        amount_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        amount_frame.pack(fill="x", pady=5, padx=20)

        amount_label = ctk.CTkLabel(amount_frame, text="AMOUNT:")
        amount_label.pack(anchor="w")

        self.amount_entry = ctk.CTkEntry(amount_frame, placeholder_text="Enter amount")
        self.amount_entry.pack(fill="x", pady=(0, 5))

        category_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        category_frame.pack(fill="x", pady=5, padx=20)

        category_label = ctk.CTkLabel(category_frame, text="CATEGORY:")
        category_label.pack(anchor="w")

        self.category_entry = ctk.CTkEntry(category_frame, placeholder_text="Enter category (max 15 characters)")
        self.category_entry.pack(fill="x", pady=(0, 5))

        description_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        description_frame.pack(fill="x", pady=5, padx=20)

        description_label = ctk.CTkLabel(description_frame, text="DESCRIPTION:")
        description_label.pack(anchor="w")

        self.description_entry = ctk.CTkEntry(description_frame, placeholder_text="Enter description (optional)")
        self.description_entry.pack(fill="x", pady=(0, 5))

        type_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        type_frame.pack(fill="x", pady=5, padx=20)

        self.transaction_type = ctk.StringVar(value="expense")

        expense_radio = ctk.CTkRadioButton(type_frame, text="Expense", variable=self.transaction_type, value="expense")
        expense_radio.pack(side="left", padx=(0, 10))

        income_radio = ctk.CTkRadioButton(type_frame, text="Income", variable=self.transaction_type, value="income")
        income_radio.pack(side="left")

        date_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=5, padx=20)

        date_label = ctk.CTkLabel(date_frame, text="DATE:")
        date_label.pack(anchor="w")

        current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_entry = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD")
        self.date_entry.insert(0, current_date)
        self.date_entry.pack(fill="x", pady=(0, 5))

        # Form buttons
        button_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=15, padx=20)

        self.add_button = ctk.CTkButton(button_frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.pack(fill="x")

        self.clear_button = ctk.CTkButton(button_frame, text="Clear Form", command=self.clear_form, fg_color="#607D8B")
        self.clear_button.pack(fill="x", pady=(10, 0))

    def setup_transaction_list(self):
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        title_label = ctk.CTkLabel(self.list_frame, text="Transaction History", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(15, 20))

        search_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search transactions...")
        self.search_entry.pack(side="left", fill="x", expand=True)

        self.search_button = ctk.CTkButton(search_frame, text="Search", width=80, command=self.search_transactions)
        self.search_button.pack(side="right", padx=(10, 0))

        tree_frame = ctk.CTkFrame(self.list_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ('date', 'category', 'description', 'amount', 'type')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        self.tree.heading('date', text='Date')
        self.tree.heading('category', text='Category')
        self.tree.heading('description', text='Description')
        self.tree.heading('amount', text='Amount')
        self.tree.heading('type', text='Type')

        self.tree.column('date', width=100)
        self.tree.column('category', width=120)
        self.tree.column('description', width=200)
        self.tree.column('amount', width=100)
        self.tree.column('type', width=70)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<Button-3>", self.show_context_menu)

        button_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)

        self.refresh_button = ctk.CTkButton(button_frame, text="Refresh", command=self.refresh_transactions, fg_color="#607D8B")
        self.refresh_button.pack(side="left")

        self.delete_button = ctk.CTkButton(button_frame, text="Delete Selected", command=self.delete_selected, fg_color="#F44336")
        self.delete_button.pack(side="right")

    def add_transaction(self):
        amount_str = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()
        is_income = self.transaction_type.get() == "income"
        date_str = self.date_entry.get()

        valid_amount, amount_result = InputValidator.validate_amount(amount_str)
        if not valid_amount:
            messagebox.showerror("Invalid Amount", amount_result)
            return

        valid_category, category_result = InputValidator.validate_category(category)
        if not valid_category:
            messagebox.showerror("Invalid Category", category_result)
            return

        valid_description, description_result = InputValidator.validate_description(description)
        if not valid_description:
            messagebox.showerror("Invalid Description", description_result)
            return

        valid_date, date_result = InputValidator.validate_date(date_str)
        if not valid_date:
            messagebox.showerror("Invalid Date", date_result)
            return

        if not is_income:
            balance_data = self.analytics.get_monthly_balance()
            current_balance = balance_data['income'] - balance_data['expenses']

            if amount_result > current_balance:
                messagebox.showerror("Insufficient Funds", f"This expense of ${amount_result:.2f} would result in a negative balance. Current balance: ${current_balance:.2f}")
                return

        transaction = self.transaction_manager.add_transaction(
            amount=amount_result,
            category_name=category_result,
            description=description,
            is_income=is_income,
            date=date_result
        )

        if transaction:
            messagebox.showinfo("Success", "Transaction added successfully")
            self.clear_form()
            self.refresh_transactions()

            if self.refresh_callback:
                self.refresh_callback()
        else:
            messagebox.showerror("Error", "Failed to add transaction")

    def clear_form(self):
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.transaction_type.set("expense")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def refresh_categories(self):
        self.categories = self.transaction_manager.get_all_categories()

    def refresh_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        df = self.analytics.get_transaction_history()

        for _, row in df.iterrows():
            date = row['date'].strftime("%Y-%m-%d")
            amount = f"${row['amount']:.2f}"
            type_str = "Income" if row['is_income'] else "Expense"

            self.tree.insert('', tk.END, iid=row['id'], values=(
                date,
                row['category'],
                row['description'] or "",
                amount,
                type_str
            ))

    def search_transactions(self):
        search_term = self.search_entry.get().lower()

        if not search_term:
            self.refresh_transactions()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        df = self.analytics.get_transaction_history()

        df_filtered = df[
            df['description'].str.lower().str.contains(search_term, na=False) |
            df['category'].str.lower().str.contains(search_term, na=False)
            ]

        for _, row in df_filtered.iterrows():
            date = row['date'].strftime("%Y-%m-%d")
            amount = f"${row['amount']:.2f}"
            type_str = "Income" if row['is_income'] else "Expense"

            self.tree.insert('', tk.END, iid=row['id'], values=(
                date,
                row['category'],
                row['description'] or "",
                amount,
                type_str
            ))

    def delete_selected(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a transaction to delete")
            return

        if messagebox.askyesno("Delete Transaction", "Are you sure you want to delete this transaction?"):
            for item_id in selected_item:
                success = self.transaction_manager.delete_transaction(int(item_id))

                if not success:
                    messagebox.showerror("Error", f"Failed to delete transaction {item_id}")

            self.refresh_transactions()

            if self.refresh_callback:
                self.refresh_callback()

    def show_context_menu(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            return

        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Delete", command=self.delete_selected)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
