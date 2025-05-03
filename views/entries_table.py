import tkinter as tk
from tkinter import ttk
from typing import Optional
from config import SKIP_COLOR, TABLE_COLUMNS, FONT
from models.weight_entry import WeightEntry

class EntriesTable(ttk.Frame):
    def __init__(self, parent, data_controller, input_panel=None):  # Add input_panel parameter
        super().__init__(parent, padding=10, relief=tk.RIDGE, borderwidth=1)
        self.data_controller = data_controller
        self.input_panel = input_panel 
        self.grid_rowconfigure(0, weight=1)  # Make the frame expandable
        self.grid_columnconfigure(0, weight=1)
        
        # Define minimum widths for each column
        self.MIN_WIDTHS = {
            'Date': 80,
            'Pre-Gym': 80,
            'Post-Gym': 80,
            'Difference': 80,
            'Preworkout': 80,
            'Calories': 80,
            'Note': 80,
            'Meals': 80
        }
        
        # Create custom style for Treeview
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Required for full styling control
        
        # Configure Treeview colors
        self.style.configure("Custom.Treeview",
                           background="#ffffff",         # White background
                           foreground="#333333",         # Dark gray text
                           fieldbackground="#ffffff",    # Background behind items
                           borderwidth=0,
                           font=(FONT, 11))
        
        # Configure Treeview heading colors
        self.style.configure("Custom.Treeview.Heading",
                            background="#3d3d3d",       # Dark gray header
                            foreground="#ffffff",       # White text
                            font=(FONT, 11, "bold"),
                            padding=5,
                            relief="flat")
        
        # Configure selection colors
        self.style.map("Custom.Treeview",
                      background=[('selected', '#4d4d4d')],  # Selection color
                      foreground=[('selected', '#ffffff')])  # White text when selected
        
        self.create_widgets()
        self.update_entries()

    def create_widgets(self):
        # Main container frame for better layout control
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        main_frame.grid_rowconfigure(1, weight=1)  # Make treeview area expandable
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title label
        ttk.Label(
            main_frame, 
            text="Recent Entries", 
            font=(FONT, 14, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Treeview with scrollbars in a separate frame
        tree_container = ttk.Frame(main_frame)
        tree_container.grid(row=1, column=0, sticky="nsew")
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Create treeview with custom style
        self.tree = ttk.Treeview(
            tree_container,
            columns=[col[0] for col in TABLE_COLUMNS],
            show='headings',
            height=8,
            selectmode='browse',
            style="Custom.Treeview"  # Apply our custom style
        )
        
        # Configure columns with minimum widths and stretch for some columns
        for idx, (col_name, width) in enumerate(TABLE_COLUMNS):
            self.tree.heading(col_name, text=col_name)
            stretch = col_name in ['Note', 'Meals']  # Allow these columns to be wider
            
            # Get the minimum width for this column, defaulting to 'width' if not specified
            min_width = self.MIN_WIDTHS.get(col_name, width)
            initial_width = max(width, min_width)
            
            self.tree.column(
                col_name, 
                width=initial_width, 
                anchor='center',
                stretch=stretch,
                minwidth=min_width  # Minimum width the column can be resized to
            )
        
        # Add scrollbars with custom styling
        self.style.configure("Custom.Vertical.TScrollbar",
                           troughcolor="#e0e0e0",
                           background="#a0a0a0",
                           bordercolor="#e0e0e0",
                           arrowcolor="#333333",
                           gripcount=0)
        
        self.style.configure("Custom.Horizontal.TScrollbar",
                           troughcolor="#e0e0e0",
                           background="#a0a0a0",
                           bordercolor="#e0e0e0",
                           arrowcolor="#333333",
                           gripcount=0)
        
        y_scroll = ttk.Scrollbar(
            tree_container, 
            orient='vertical', 
            command=self.tree.yview,
            style="Custom.Vertical.TScrollbar"
        )
        x_scroll = ttk.Scrollbar(
            tree_container, 
            orient='horizontal', 
            command=self.tree.xview,
            style="Custom.Horizontal.TScrollbar"
        )
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Grid layout with sticky attributes
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')
        
        # Configure tags for skipped entries
        self.tree.tag_configure('skipped', 
                               foreground=SKIP_COLOR,
                               background="#ffffff")  # Keep white background
        
        # Edit/Delete buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        self.edit_btn = ttk.Button(
            button_frame, 
            text="Edit Selected", 
            command=self.edit_selected,
            state=tk.DISABLED
        )
        self.edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.delete_btn = ttk.Button(
            button_frame, 
            text="Delete Selected", 
            command=self.delete_selected,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_selection_change)

    def update_entries(self):
        """Force refresh the table from data source"""
        self.tree.delete(*self.tree.get_children())
        
        try:
            entries = self.data_controller.get_recent_entries()
            for entry in entries:
                if entry.skipped:
                    self.tree.insert('', 'end', 
                        values=(
                            entry.date,
                            "Skipped", "", "", "", "", "", ""
                        ),
                        tags=('skipped',)
                    )
                else:
                    # Calculate difference if both weights exist
                    diff = ""
                    if entry.pre_gym and entry.post_gym:
                        try:
                            diff = f"{float(entry.post_gym)-float(entry.pre_gym):.1f}"
                        except ValueError:
                            pass
                    
                    # Format meals more cleanly
                    meals = []
                    if entry.breakfast and entry.breakfast != "None":
                        meals.append(f"B: {entry.breakfast}")
                    if entry.lunch and entry.lunch != "None":
                        meals.append(f"L: {entry.lunch}")
                    if entry.snacks and entry.snacks != "None":
                        meals.append(f"S: {entry.snacks}")
                    if entry.dinner and entry.dinner != "None":
                        meals.append(f"D: {entry.dinner}")
                    meals_str = ", ".join(meals) if meals else ""
                    
                    self.tree.insert('', 'end',
                        values=(
                            entry.date,
                            f"{float(entry.pre_gym):.1f}" if entry.pre_gym else "-",
                            f"{float(entry.post_gym):.1f}" if entry.post_gym else "-",
                            diff,
                            entry.preworkout or "",
                            str(entry.calories_burned) if entry.calories_burned else "",
                            entry.note if entry.note else "",
                            meals_str
                        )
                    )
                    
            # Auto-size the columns to fit content (but respect minimum widths)
            for col in self.tree["columns"]:
                current_minwidth = self.tree.column(col, 'minwidth')
                new_width = tk.font.Font().measure(col.title()) + 20
                self.tree.column(col, width=max(new_width, current_minwidth))
                
        except Exception as e:
            print(f"Error updating entries: {e}")
            tk.messagebox.showerror("Error", f"Failed to load entries: {str(e)}")

    def on_selection_change(self, event):
        selected = self.tree.selection()
        state = tk.NORMAL if selected else tk.DISABLED
        self.edit_btn.config(state=state)
        self.delete_btn.config(state=state)

    def get_selected_date(self) -> Optional[str]:
        selected = self.tree.selection()
        if selected:
            return self.tree.item(selected[0])['values'][0]
        return None

    def edit_selected(self):
        date = self.get_selected_date()
        if date:
            entry = self.data_controller.get_entry_by_date(date)
            if entry and self.input_panel:  # Use the stored reference
                self.input_panel.populate_entry_data(entry)
            else:
                print(f"Debug: {'No entry found' if not entry else 'No input panel reference'}")

    def delete_selected(self):
        date = self.get_selected_date()
        if date and tk.messagebox.askyesno("Confirm", f"Delete entry for {date}?"):
            self.data_controller.delete_entry(date)
            self.update_entries()