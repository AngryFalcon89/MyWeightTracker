import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from config import BG_COLOR, CARD_COLOR, ACCENT_COLOR, TEXT_COLOR, PREWORKOUT_OPTIONS, NOT_ACTIVE_COLOR, FONT, WHITE
from models.weight_entry import WeightEntry
from datetime import datetime

class InputPanel(ttk.Frame):
    def __init__(self, parent, data_controller, refresh_callback=None):
        super().__init__(parent, padding=20, relief=tk.RIDGE, borderwidth=1)
        self.data_controller = data_controller
        self.refresh_callback = refresh_callback
        self.configure(style='Card.TFrame')
        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        style = ttk.Style()
        style.configure("Custom.TEntry", foreground="black", fieldbackground="white")

    def create_widgets(self):
        # Configure grid columns to align all inputs
        self.columnconfigure(1, weight=1)  # Make input column expandable
        self.columnconfigure(2, minsize=40)  # Fixed width for calendar button
        
        # Date input row
        ttk.Label(self, text="Date:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.date_entry = ttk.Entry(self, style="Custom.TEntry")
        self.date_entry.grid(row=0, column=1, sticky="ew", pady=(0, 5))
        self.date_entry.insert(0, self.get_current_date())
        self.date_entry.configure(state='readonly')

        # Calendar button - aligned with input fields
        ttk.Button(
            self, 
            text="📅", 
            width=3,  # Fixed width for better alignment
            command=self.show_calendar
        ).grid(row=0, column=2, sticky="w", padx=(5, 0), pady=(0, 5))
        
        # Weight inputs (aligned with date row)
        ttk.Label(self, text="Pre-gym Weight (kg):").grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.pre_gym_entry = ttk.Entry(self, style="Custom.TEntry")
        self.pre_gym_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=(0, 5))
        self.pre_gym_entry.configure(validate="key")
        self.pre_gym_entry.configure(validatecommand=(
            self.register(self.validate_numeric_input),
            '%P'  # passes the new value after edit
        ))

        ttk.Label(self, text="Post-gym Weight (kg):").grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.post_gym_entry = ttk.Entry(self, style="Custom.TEntry")
        self.post_gym_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=(0, 5))
        self.post_gym_entry.configure(validate="key")
        self.post_gym_entry.configure(validatecommand=(
            self.register(self.validate_numeric_input),
            '%P'  # passes the new value after edit
        ))

        # Pre-workout condition (aligned)
        ttk.Label(self, text="Pre-workout Condition:").grid(row=3, column=0, sticky="w", pady=(0, 5))
        self.preworkout_var = tk.StringVar(value="Normal")
        self.preworkout_dropdown = ttk.Combobox(
            self,
            textvariable=self.preworkout_var,
            values=PREWORKOUT_OPTIONS,
            state="readonly"
        )
        self.preworkout_dropdown.grid(row=3, column=1, columnspan=2, sticky="ew", pady=(0, 5))
        
        # Calories burned (aligned)
        ttk.Label(self, text="Calories Burned:").grid(row=4, column=0, sticky="w", pady=(0, 5))
        self.calories_entry = ttk.Entry(self, style="Custom.TEntry")
        self.calories_entry.grid(row=4, column=1, columnspan=2, sticky="ew", pady=(0, 5))
        self.calories_entry.configure(validate="key")
        self.calories_entry.configure(validatecommand=(
            self.register(self.validate_numeric_input),
            '%P'  # passes the new value after edit
        ))
        
        # Note field (aligned)
        ttk.Label(self, text="Notes:").grid(row=5, column=0, sticky="nw", pady=(0, 5))
        self.note_entry = tk.Text(self, height=4, width=30,wrap="word", bg="white", fg="black", bd=1, highlightthickness=0, insertbackground="black", font=(FONT, 13))
        self.note_entry.grid(row=5, column=1, columnspan=2, sticky="ew", pady=(0, 5))
        
        # Meals frame (full width)
        meals_frame = ttk.LabelFrame(self, text="Daily Meals", padding=10)
        meals_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        meals_frame.columnconfigure(1, weight=1)  # Make meal entry fields expandable
        
        # Meal entries (aligned)
        ttk.Label(meals_frame, text="Breakfast:").grid(row=0, column=0, sticky="w")
        self.breakfast_entry = ttk.Entry(meals_frame, style="Custom.TEntry")
        self.breakfast_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=(0, 5))
        
        ttk.Label(meals_frame, text="Lunch:").grid(row=1, column=0, sticky="w")
        self.lunch_entry = ttk.Entry(meals_frame, style="Custom.TEntry")
        self.lunch_entry.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=(0, 5))
        
        ttk.Label(meals_frame, text="Snacks:").grid(row=2, column=0, sticky="w")
        self.snacks_entry = ttk.Entry(meals_frame, style="Custom.TEntry")
        self.snacks_entry.grid(row=2, column=1, sticky="ew", padx=(5, 0), pady=(0, 5))
        
        ttk.Label(meals_frame, text="Dinner:").grid(row=3, column=0, sticky="w")
        self.dinner_entry = ttk.Entry(meals_frame, style="Custom.TEntry")
        self.dinner_entry.grid(row=3, column=1, sticky="ew", padx=(5, 0), pady=(0, 5))

        # Skipped gym checkbox (full width)
        self.skipped_var = tk.BooleanVar()
        ttk.Checkbutton(
            self,
            text="Skipped Gym Today",
            variable=self.skipped_var,
            command=self.toggle_skipped
        ).grid(row=7, column=0, columnspan=3, pady=(10, 5), sticky="w")

        # Buttons (full width)
        button_frame = ttk.Frame(self)
        button_frame.grid(row=8, column=0, columnspan=3, pady=(10, 0), sticky="ew")
        
        ttk.Button(
            button_frame, 
            text="Save Entry", 
            command=self.save_entry,
            style='Accent.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="Clear Fields", 
            command=self.clear_fields
        ).pack(side=tk.LEFT)

    def get_current_date(self):
        return datetime.now().strftime("%d-%m-%Y")

    def show_calendar(self):
        top = tk.Toplevel(self)
        top.configure(bg=WHITE) 
        cal = Calendar(
            top,
            selectmode='day',
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            date_pattern='dd-mm-y',
            bordercolor=BG_COLOR,
            headersbackground=BG_COLOR,
            background=ACCENT_COLOR

        )
        cal.pack(pady=20, padx=20)

        def set_date():
            # Temporarily make entry writable to change the date
            self.date_entry.configure(state='normal')
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, cal.get_date())
            self.date_entry.configure(state='readonly')  # Set back to readonly
            top.destroy()
        ttk.Button(top,style='Accent.TButton', text="Select Date", command=set_date).pack(pady=10)

    def toggle_skipped(self):
        state = tk.DISABLED if self.skipped_var.get() else tk.NORMAL
        self.pre_gym_entry.config(state=state)
        self.post_gym_entry.config(state=state)
        self.calories_entry.config(state=state)
        self.preworkout_dropdown.config(state=state)

    def save_entry(self):
        date = self.date_entry.get()
        skipped = self.skipped_var.get()
        
        entry = WeightEntry(
            date=date,
            skipped=skipped,
            note=self.note_entry.get("1.0", tk.END).strip(),
            breakfast=self.breakfast_entry.get(),
            lunch=self.lunch_entry.get(),
            snacks=self.snacks_entry.get(),
            dinner=self.dinner_entry.get()
        )
        
        if not skipped:
            try:
                entry.pre_gym = float(self.pre_gym_entry.get())
                if self.post_gym_entry.get():
                    entry.post_gym = float(self.post_gym_entry.get())
                if self.calories_entry.get():
                    entry.calories_burned = int(self.calories_entry.get())
                entry.preworkout = self.preworkout_var.get()
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid numeric input")
                return
        
        self.data_controller.add_entry(entry)
        if self.refresh_callback:
            self.refresh_callback()  # Use the callback
        else:
            print("Warning: No refresh callback provided")
        self.clear_fields()
        tk.messagebox.showinfo("Success", "Entry saved successfully!")

    def clear_fields(self):
        self.date_entry.configure(state='normal')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, self.get_current_date())
        self.date_entry.configure(state='readonly')
        self.pre_gym_entry.delete(0, tk.END)
        self.post_gym_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.note_entry.delete("1.0", tk.END)
        self.breakfast_entry.delete(0, tk.END)
        self.lunch_entry.delete(0, tk.END)
        self.snacks_entry.delete(0, tk.END)
        self.dinner_entry.delete(0, tk.END)
        self.skipped_var.set(False)
        self.preworkout_var.set("Normal")
        self.toggle_skipped()

    def validate_numeric_input(self, new_value):
        """Validate that the input is a positive decimal number"""
        if new_value == "":
            return True  # Allow empty field
        try:
            # Try converting to float
            float(new_value)
            # Check if positive number
            return float(new_value) >= 0
        except ValueError:
            return False
    
    # In InputPanel class
    def populate_entry_data(self, entry):
        """Populate the input fields with data from the selected entry"""
        # Clear all fields first
        self.clear_fields()

        # Set the date (temporarily make writable)
        self.date_entry.configure(state='normal')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, entry.date)
        self.date_entry.configure(state='readonly')

        # Set skipped state
        self.skipped_var.set(entry.skipped)
        self.toggle_skipped()

        if not entry.skipped:
            # Set weight fields
            if entry.pre_gym:
                self.pre_gym_entry.insert(0, str(entry.pre_gym))
            if entry.post_gym:
                self.post_gym_entry.insert(0, str(entry.post_gym))

            # Set preworkout condition
            if entry.preworkout:
                self.preworkout_var.set(entry.preworkout)

            # Set calories burned
            if entry.calories_burned:
                self.calories_entry.insert(0, str(entry.calories_burned))

        # Set note
        if entry.note:
            self.note_entry.insert("1.0", entry.note)

        # Set meals
        if entry.breakfast and entry.breakfast != "None":
            self.breakfast_entry.insert(0, entry.breakfast)
        if entry.lunch and entry.lunch != "None":
            self.lunch_entry.insert(0, entry.lunch)
        if entry.snacks and entry.snacks != "None":
            self.snacks_entry.insert(0, entry.snacks)
        if entry.dinner and entry.dinner != "None":
            self.dinner_entry.insert(0, entry.dinner)