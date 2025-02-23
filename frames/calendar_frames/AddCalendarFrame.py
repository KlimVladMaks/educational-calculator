import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from database.Database import Database


class AddCalendarFrame(BaseFrame):
    """
    Фрейм для добавления нового производственного календаря.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = ttk.Button(self.master, text="Назад", command=self.go_back)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)

        ttk.Label(self, text="Добавить производственный календарь").pack(pady=10)

        self.input_name_frame = ttk.Frame(self)
        self.input_name_frame.pack(pady=10)

        self.name_label = ttk.Label(self.input_name_frame, text="Название:")
        self.name_label.grid(row=0, column=0, padx=5)
        self.name_entry = ttk.Entry(self.input_name_frame, width=50)
        self.name_entry.grid(row=1, column=0, padx=5)

        self.input_duration_frame = ttk.Frame(self)
        self.input_duration_frame.pack(pady=10)

        self.start_date_label = ttk.Label(self.input_duration_frame, text="Дата начала:")
        self.start_date_label.grid(row=0, column=0, padx=10)
        self.end_date_label = ttk.Label(self.input_duration_frame, text="Дата окончания:")
        self.end_date_label.grid(row=0, column=1, padx=10)

        self.start_date_entry = ttk.Entry(self.input_duration_frame)
        self.start_date_entry.grid(row=1, column=0, padx=10)
        self.end_date_entry = ttk.Entry(self.input_duration_frame)
        self.end_date_entry.grid(row=1, column=1, padx=10)

        self.days_off_label = ttk.Label(self, text="Даты нерабочих дней")
        self.days_off_label.pack(pady=(10, 0))
        self.days_off_entry = tk.Text(self, width=50, height=5)
        self.days_off_entry.pack(pady=(0, 10))

        ttk.Button(self, text="Добавить производственный календарь", command=self.add_calendar).pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def add_calendar(self):
        name = str(self.name_entry.get())
        start_date = str(self.start_date_entry.get())
        end_date = str(self.end_date_entry.get())
        text = self.days_off_entry.get("1.0", tk.END)
        days_off_list = [date.strip() for date in text.split(',') if date.strip()]
        new_calendar_data = [name, start_date, end_date, days_off_list]
        self.db.calendars.add(new_calendar_data)
        self.parent_frame.update()
        self.go_back()
