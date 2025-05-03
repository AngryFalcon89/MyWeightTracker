import tkinter as tk
from tkinter import ttk
import os
import sys
from config import BG_COLOR, TEXT_COLOR, CARD_COLOR, ACCENT_COLOR, NOT_ACTIVE_COLOR, FONT
from .input_panel import InputPanel
from .entries_table import EntriesTable
from .stats_panel import StatsPanel

class MainView(tk.Tk):
    def __init__(self, data_controller, stats_controller):
        super().__init__()

        # Get the application's root directory
        if getattr(sys, 'frozen', False):
            # Running in a bundle
            app_dir = os.path.dirname(sys.executable)
            if app_dir.endswith('MacOS'):
                # On macOS, need to go up to the Resources directory
                app_dir = os.path.dirname(os.path.dirname(app_dir))
                app_dir = os.path.join(app_dir, 'Resources')
            self.icon_path = os.path.join(app_dir, 'assets', 'icon.png')
        else:
            # Running in a normal Python environment
            self.icon_path = "assets/icon.png"

        try:
            self.iconphoto(False, tk.PhotoImage(file=self.icon_path))
        except tk.TclError:
            print(f"Warning: Could not load icon from {self.icon_path}")
        
        # Window setup
        self.data_controller = data_controller
        self.stats_controller = stats_controller
        
        self._force_light_appearance()
        self._configure_root_window()
        self._setup_styles()
        self.create_widgets()
    
    def _force_light_appearance(self):
        """Force light mode appearance"""
        try:
            self.tk.call('::tk::unsupported::MacWindowStyle', 'style', self._w, 'light')
        except tk.TclError:
            self.configure(bg=BG_COLOR)
    
    def _configure_root_window(self):
        """Configure window properties"""
        self.title("Weight Tracker")
        self.geometry("1200x800")
        self.minsize(1000, 700)
    
    def _setup_styles(self):
        """Configure widget styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Base styles
        self.style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR, font=(FONT, 12))
        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, padding=5)
        self.style.configure('Title.TLabel', font=(FONT, 24, 'bold'))
        self.style.configure('Card.TFrame', background=CARD_COLOR, borderwidth=0)
        self.style.configure('Accent.TButton', background=ACCENT_COLOR, foreground='white', 
                           font=(FONT, 12, 'bold'), borderwidth=0, padding=10)
        self.style.map('Accent.TButton', background=[('active', ACCENT_COLOR), ('pressed', NOT_ACTIVE_COLOR)])
    
    def create_widgets(self):
        """Create the main layout"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title frame
        title_frame = ttk.Frame(main_frame, style='Card.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            title_frame,
            text="My Weight Tracker",
            style='Title.TLabel'
        ).pack(pady=10)
        
        # Content area - using grid for precise control
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Input (full height)
        self.input_panel = InputPanel(content_frame, self.data_controller,
        refresh_callback=self.refresh_entries)
        self.input_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Right panels container
        right_panel = ttk.Frame(content_frame)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Top right - Entries table
        self.entries_table = EntriesTable(right_panel, self.data_controller,
        input_panel=self.input_panel)
        self.entries_table.pack(fill=tk.BOTH, expand=True)
        
        # Bottom right - Stats panel
        self.stats_panel = StatsPanel(right_panel, self.stats_controller)
        self.stats_panel.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Configure weights
        content_frame.columnconfigure(0, weight=1)  # Input panel
        content_frame.columnconfigure(1, weight=1)  # Right panels
        content_frame.rowconfigure(0, weight=1)
        
        right_panel.rowconfigure(0, weight=1)  # Entries table
        right_panel.rowconfigure(1, weight=1)  # Stats panel
        right_panel.columnconfigure(0, weight=1)

    def refresh_entries(self):
        """Refresh the entries table"""
        self.entries_table.update_entries()