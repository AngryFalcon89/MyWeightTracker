import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import BG_COLOR, CARD_COLOR, FONT, TEXT_COLOR
from utils.graph_utils import create_weight_graph

class StatsPanel(ttk.Frame):
    def __init__(self, parent, stats_controller):
        super().__init__(parent, padding=10)
        self.stats_controller = stats_controller
        self.configure(style='Card.TFrame')  # Use the same card style as other components
        
        # Create layout
        self.create_widgets()
        self.update_stats()

    def create_widgets(self):
        # Title
        ttk.Label(
            self,
            text="Weekly Statistics",
            font=(FONT, 12, "bold"),
            style='TLabel'  # Use consistent label style
        ).pack(anchor="w", pady=(0, 10))
        
        # Stats display area
        self.stats_container = ttk.Frame(self)
        self.stats_container.pack(fill=tk.BOTH, expand=True)
        
        # Graph button with consistent styling
        ttk.Button(
            self,
            text="Show Graph",
            command=self.show_graph,
            style='Accent.TButton'  # Use the same button style as elsewhere
        ).pack(pady=(10, 0))

    def update_stats(self):
        # Clear previous stats
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        
        stats = self.stats_controller.calculate_stats()
        
        if stats["status"] == "insufficient_data":
            ttk.Label(
                self.stats_container,
                text="Not enough data for statistics",
                font=(FONT, 11),
                style='TLabel'
            ).pack(pady=10)
            return
        
        # Create stats grid with consistent styling
        grid = ttk.Frame(self.stats_container)
        grid.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid columns
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        
        # Add stats rows
        self.add_stat_row(grid, 0, "Time Period:", f"{stats['first_date']} to {stats['last_date']}")
        self.add_stat_row(grid, 1, "Total Change:", f"{stats['total_loss']:.2f} kg")
        self.add_stat_row(grid, 2, "Weekly Average:", f"{stats['weekly_loss']:.2f} kg/week")
        self.add_stat_row(grid, 3, "Avg Calories:", f"{stats['avg_calories']:.0f} kcal")
        
        if stats['projection']:
            self.add_stat_row(grid, 4, "Projected Goal:", stats['projection'])

    def add_stat_row(self, parent, row, label, value):
        """Helper to create consistent stat rows"""
        ttk.Label(
            parent,
            text=label,
            font=(FONT, 11, "bold"),
            style='TLabel'
        ).grid(row=row, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Label(
            parent,
            text=value,
            font=(FONT, 11),
            style='TLabel'
        ).grid(row=row, column=1, sticky="w", padx=5, pady=2)

    def show_graph(self):
        dates, pre_weights, post_weights, skipped_dates = self.stats_controller.prepare_graph_data()
        fig = create_weight_graph(dates, pre_weights, post_weights, skipped_dates)
        
        # Create graph window with consistent styling
        graph_window = tk.Toplevel(self)
        graph_window.title("Weight Progress Graph")
        graph_window.geometry("800x600")
        
        # Make the graph background match the app
        fig.patch.set_facecolor(BG_COLOR)
        
        # Embed graph
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Close button with consistent styling
        btn_frame = ttk.Frame(graph_window)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="Close",
            command=graph_window.destroy,
            style='Accent.TButton'
        ).pack()