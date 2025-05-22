import customtkinter as ctk
from tkinter import messagebox, filedialog
from database.models import Settings
from core.analytics import FinancialAnalytics
from utils.export_data import export_transactions


class SettingsPanel(ctk.CTkFrame):
    def __init__(self, parent, refresh_callback=None):
        super().__init__(parent)

        self.settings = Settings.select().first()
        self.refresh_callback = refresh_callback
        self.analytics = FinancialAnalytics()

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_settings_panel()

    def setup_settings_panel(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        title_label = ctk.CTkLabel(main_frame, text="Application Settings", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 30))

        theme_frame = ctk.CTkFrame(main_frame)
        theme_frame.pack(fill="x", pady=10)

        theme_label = ctk.CTkLabel(theme_frame, text="Application Theme", font=ctk.CTkFont(size=16, weight="bold"))
        theme_label.pack(anchor="w", padx=15, pady=(10, 5))

        theme_hint = ctk.CTkLabel(theme_frame, text="Toggle between Light and Dark theme", text_color="#9E9E9E")
        theme_hint.pack(anchor="w", padx=15, pady=(0, 10))

        self.current_theme_label = ctk.CTkLabel(theme_frame, text=f"Current Theme: {self.settings.theme}")
        self.current_theme_label.pack(anchor="w", padx=15, pady=(0, 10))

        self.theme_var = ctk.StringVar(value=self.settings.theme)

        theme_button = ctk.CTkButton(theme_frame, text="Toggle Theme", command=self.toggle_theme)
        theme_button.pack(fill="x", padx=15, pady=(0, 15))

        export_frame = ctk.CTkFrame(main_frame)
        export_frame.pack(fill="x", pady=10)

        export_label = ctk.CTkLabel(export_frame, text="Data Export", font=ctk.CTkFont(size=16, weight="bold"))
        export_label.pack(anchor="w", padx=15, pady=(10, 5))

        export_hint = ctk.CTkLabel(export_frame, text="Export all transactions to a CSV file", text_color="#9E9E9E")
        export_hint.pack(anchor="w", padx=15, pady=(0, 10))

        export_button = ctk.CTkButton(export_frame, text="Export Transactions", command=self.export_transactions, fg_color="#4CAF50")
        export_button.pack(fill="x", padx=15, pady=(0, 15))

    def toggle_theme(self):
        new_theme = "Dark" if self.theme_var.get() == "Light" else "Light"
        self.theme_var.set(new_theme)
        ctk.set_appearance_mode(new_theme)

        self.settings.theme = new_theme
        self.settings.save()

        self.current_theme_label.configure(text=f"Current Theme: {new_theme}")

        if self.refresh_callback:
            self.refresh_callback()

        messagebox.showinfo("Success", f"Theme changed to {new_theme}")

    def export_transactions(self):
        df = self.analytics.get_transaction_history(limit=None) 

        if df.empty:
            messagebox.showinfo("Export Transactions", "No transactions to export")
            return

        transactions = []
        for _, row in df.iterrows():
            date_str = row['date'].strftime("%Y-%m-%d")

            transaction = {
                'Date': date_str,
                'Category': row['category'],
                'Description': row['description'] or "",
                'Amount': f"{row['amount']:.2f}",
                'Type': "Income" if row['is_income'] else "Expense"
            }
            transactions.append(transaction)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Transactions"
        )

        if not file_path:  
            return

        success, result = export_transactions(transactions, file_path)

        if success:
            messagebox.showinfo("Export Successful", f"Transactions exported to:\n{result}")
        else:
            messagebox.showerror("Export Failed", result)
