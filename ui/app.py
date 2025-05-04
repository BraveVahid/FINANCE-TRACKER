import customtkinter as ctk
from ui.dashboard import DashboardFrame
from ui.transaction_panel import TransactionPanel
from ui.settings_panel import SettingsPanel
from database.models import Settings


class FinanceTrackerApp:
    """
    Main application class that initializes and manages the Finance Tracker application.
    
    This class is responsible for setting up the main UI components, handling tab navigation,
    and managing application-wide settings like theme preferences.
    """
    def __init__(self):
        """
        Initialize the Finance Tracker application with main window settings, theme configuration,
        and UI setup.
        """
        # Create the main application window
        self.main_frame = None
        self.tab_view = None
        self.dashboard = None
        self.transaction_panel = None
        self.settings_panel = None

        self.app = ctk.CTk()
        self.app.title("Finance Assistant")
        self.app.geometry("900x600")
        self.app.minsize(800, 500)
        
        # Load user settings from database
        self.settings = Settings.select().first()
        ctk.set_appearance_mode(self.settings.theme)
        
        # Set up the UI components
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configure the main UI components including the tab view and individual panels.
        Sets up grid layout and initializes the Dashboard, Transaction, and Settings panels.
        """
        # Configure main grid layout
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        
        # Create main frame container
        self.main_frame = ctk.CTkFrame(self.app)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure main frame grid layout
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Create tab view for navigation
        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Add tabs for different sections
        self.tab_view.add("Dashboard")
        self.tab_view.add("Transactions")
        self.tab_view.add("Settings")

        # Configure grid layout for each tab
        for tab_name in ["Dashboard", "Transactions", "Settings"]:
            self.tab_view.tab(tab_name).grid_columnconfigure(0, weight=1)
            self.tab_view.tab(tab_name).grid_rowconfigure(0, weight=1)

        # Initialize dashboard panel
        self.dashboard = DashboardFrame(self.tab_view.tab("Dashboard"))
        self.dashboard.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Initialize transaction panel with callback to refresh dashboard
        self.transaction_panel = TransactionPanel(self.tab_view.tab("Transactions"), refresh_callback=self.refresh_dashboard)
        self.transaction_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Initialize settings panel with callback to refresh all UI components
        self.settings_panel = SettingsPanel(self.tab_view.tab("Settings"), refresh_callback=self.refresh_all)
        self.settings_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def refresh_dashboard(self):
        """
        Refresh the dashboard data.
        Called when transactions are added or deleted to update financial metrics.
        """
        self.dashboard.refresh_data()
    
    def refresh_all(self):
        """
        Refresh all components of the application.
        Called when settings are changed to update theme and data across all panels.
        """
        # Reload settings from database
        self.settings = Settings.select().first()
        ctk.set_appearance_mode(self.settings.theme)
        
        # Refresh all UI components
        self.dashboard.refresh_data()
        self.transaction_panel.refresh_categories()
        self.transaction_panel.refresh_transactions()
    
    def run(self):
        """
        Start the application main loop.
        """
        self.app.mainloop()
