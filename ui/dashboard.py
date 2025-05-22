import customtkinter as ctk
from core.analytics import FinancialAnalytics
from utils.charts import ChartGenerator
from database.models import Settings


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.analytics = FinancialAnalytics()
        self.settings = Settings.select().first()

        self.pie_chart = None
        self.line_chart = None
        self.bar_chart = None

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.setup_summary_frame()
        self.setup_chart_frames()

        self.refresh_data()

    def setup_summary_frame(self):
        self.summary_frame = ctk.CTkFrame(self)
        self.summary_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.title_label = ctk.CTkLabel(self.summary_frame, text="MONTHLY SUMMARY", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(pady=(10, 15))

        summary_container = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        summary_container.pack(fill="x", padx=20, pady=5)

        summary_container.grid_columnconfigure(0, weight=1)
        summary_container.grid_columnconfigure(1, weight=1)
        summary_container.grid_columnconfigure(2, weight=1)

        income_frame = ctk.CTkFrame(summary_container)
        income_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        income_label = ctk.CTkLabel(income_frame, text="INCOME", font=ctk.CTkFont(weight="bold"))
        income_label.pack(pady=(5, 0))

        self.income_value = ctk.CTkLabel(income_frame, text="$0.00", font=ctk.CTkFont(size=24), text_color="#4CAF50")
        self.income_value.pack(pady=(0, 5))

        expenses_frame = ctk.CTkFrame(summary_container)
        expenses_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        expenses_label = ctk.CTkLabel(expenses_frame, text="EXPENSE", font=ctk.CTkFont(weight="bold"))
        expenses_label.pack(pady=(5, 0))

        self.expenses_value = ctk.CTkLabel(expenses_frame, text="$0.00", font=ctk.CTkFont(size=24), text_color="#F44336")
        self.expenses_value.pack(pady=(0, 5))

        balance_frame = ctk.CTkFrame(summary_container)
        balance_frame.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

        balance_label = ctk.CTkLabel(balance_frame, text="BALANCE", font=ctk.CTkFont(weight="bold"))
        balance_label.pack(pady=(5, 0))

        self.balance_value = ctk.CTkLabel(balance_frame, text="$0.00", font=ctk.CTkFont(size=24), text_color="#2196F3")
        self.balance_value.pack(pady=(0, 5))

    def setup_chart_frames(self):
        self.pie_frame = ctk.CTkFrame(self)
        self.pie_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        pie_title = ctk.CTkLabel(self.pie_frame, text="EXPENSE BREAKDOWN", font=ctk.CTkFont(size=16, weight="bold"))
        pie_title.pack(pady=10)

        self.pie_chart_frame = ctk.CTkFrame(self.pie_frame, fg_color="transparent")
        self.pie_chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.line_frame = ctk.CTkFrame(self)
        self.line_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        line_title = ctk.CTkLabel(self.line_frame, text="BALANCE TREND", font=ctk.CTkFont(size=16, weight="bold"))
        line_title.pack(pady=10)

        self.line_chart_frame = ctk.CTkFrame(self.line_frame, fg_color="transparent")
        self.line_chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.bar_frame = ctk.CTkFrame(self)
        self.bar_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        bar_title = ctk.CTkLabel(self.bar_frame, text="INCOME VS. EXPENSE", font=ctk.CTkFont(size=16, weight="bold"))
        bar_title.pack(pady=10)

        self.bar_chart_frame = ctk.CTkFrame(self.bar_frame, fg_color="transparent")
        self.bar_chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_data(self):
        try:
            self.settings = Settings.select().first()
            
            balance_data = self.analytics.get_monthly_balance()

            self.income_value.configure(text=f"${balance_data['income']:.2f}")
            self.expenses_value.configure(text=f"${balance_data['expenses']:.2f}")

            balance_amount = balance_data['balance']
            if balance_amount >= 0:
                balance_color = "#4CAF50"
            else:
                balance_color = "#F44336" 
                
            self.balance_value.configure(text=f"${balance_amount:.2f}", text_color=balance_color)

            expense_data = self.analytics.get_expense_breakdown()
            trend_data = self.analytics.get_monthly_trend()

            self.update_charts(expense_data, trend_data)
            
        except Exception as e:
            print(f"Error refreshing data: {e.__class__.__name__}")

    def update_charts(self, expense_data, trend_data):
        try:
            for widget in self.pie_chart_frame.winfo_children():
                widget.destroy()

            for widget in self.line_chart_frame.winfo_children():
                widget.destroy()

            for widget in self.bar_chart_frame.winfo_children():
                widget.destroy()

            chart_generator = ChartGenerator()
            
            current_theme = self.settings.theme
            
            self.pie_chart = chart_generator.create_pie_chart(expense_data, self.pie_chart_frame, theme=current_theme)
            if self.pie_chart:
                self.pie_chart.get_tk_widget().pack(fill="both", expand=True)

            self.line_chart = chart_generator.create_line_chart(trend_data, self.line_chart_frame, theme=current_theme)
            if self.line_chart:
                self.line_chart.get_tk_widget().pack(fill="both", expand=True)

            self.bar_chart = chart_generator.create_bar_chart(trend_data, self.bar_chart_frame, theme=current_theme)
            if self.bar_chart:
                self.bar_chart.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error updating charts: {e.__class__.__name__}")
