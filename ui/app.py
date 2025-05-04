import customtkinter as ctk
from ui.dashboard import DashboardFrame
from ui.transaction_panel import TransactionPanel
from ui.settings_panel import SettingsPanel
from database.models import Settings


class FinanceTrackerApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Finance Assistant")
        self.app.geometry("900x600")
        self.app.minsize(800, 500)
        
        self.settings = Settings.select().first()
        ctk.set_appearance_mode(self.settings.theme)
        
        self.setup_ui()
    
    def setup_ui(self):
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        
        self.main_frame = ctk.CTkFrame(self.app)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.tab_view.add("Dashboard")
        self.tab_view.add("Transactions")
        self.tab_view.add("Settings")

        for tab_name in ["Dashboard", "Transactions", "Settings"]:
            self.tab_view.tab(tab_name).grid_columnconfigure(0, weight=1)
            self.tab_view.tab(tab_name).grid_rowconfigure(0, weight=1)

        self.dashboard = DashboardFrame(self.tab_view.tab("Dashboard"))
        self.dashboard.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.transaction_panel = TransactionPanel(self.tab_view.tab("Transactions"), refresh_callback=self.refresh_dashboard)
        self.transaction_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.settings_panel = SettingsPanel(self.tab_view.tab("Settings"), refresh_callback=self.refresh_all)
        self.settings_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def refresh_dashboard(self):
        self.dashboard.refresh_data()
    
    def refresh_all(self):
        self.settings = Settings.select().first()
        ctk.set_appearance_mode(self.settings.theme)
        
        self.dashboard.refresh_data()
        self.transaction_panel.refresh_categories()
        self.transaction_panel.refresh_transactions()
    
    def run(self):
        self.app.mainloop()
