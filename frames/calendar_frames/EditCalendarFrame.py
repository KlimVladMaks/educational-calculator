import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from database.Database import Database
from widgets.BackButton import BackButton


class EditCalendarFrame(BaseFrame):
    """
    Фрейм для изменения данных производственного календаря.
    """
    def __init__(self, master, parent_frame, old_calendar_name):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.old_calendar_name = old_calendar_name
        self.db = Database()
        self.old_calendar_data = self.db.calendars.get(self.old_calendar_name)
        self.create_frame()
    
    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.pack()

        ttk.Label(self, text="Изменить производственный календарь").pack(pady=10)

        self.name_label = ttk.Label(self, text="Название:")
        self.name_label.pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self, width=50)
        self.name_entry.pack(pady=(0, 10))
        self.name_entry.insert(0, self.old_calendar_data[0])

        self.input_duration_frame = ttk.Frame(self)
        self.input_duration_frame.pack(pady=10)

        self.start_date_label = ttk.Label(self.input_duration_frame, text="Дата начала:")
        self.start_date_label.grid(row=0, column=0, padx=10)
        self.end_date_label = ttk.Label(self.input_duration_frame, text="Дата окончания:")
        self.end_date_label.grid(row=0, column=1, padx=10)

        self.start_date_entry = ttk.Entry(self.input_duration_frame)
        self.start_date_entry.grid(row=1, column=0, padx=10)
        self.start_date_entry.insert(0, self.old_calendar_data[1])
        self.end_date_entry = ttk.Entry(self.input_duration_frame)
        self.end_date_entry.grid(row=1, column=1, padx=10)
        self.end_date_entry.insert(0, self.old_calendar_data[2])

        self.days_off_label = ttk.Label(self, text="Даты нерабочих дней")
        self.days_off_label.pack(pady=(10, 0))
        self.days_off_entry = tk.Text(self, width=50, height=5)
        self.days_off_entry.pack(pady=(0, 10))
        self.days_off_entry.insert("1.0", "\n".join(self.old_calendar_data[3]))

        ttk.Button(self, text="Сохранить изменения", command=self.save_calendar).pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def save_calendar(self):
        name = str(self.name_entry.get())
        start_date = str(self.start_date_entry.get())
        end_date = str(self.end_date_entry.get())
        text = self.days_off_entry.get("1.0", tk.END)
        days_off_list = [line.strip() for line in text.splitlines() if line.strip()]
        new_calendar_data = [name, start_date, end_date, days_off_list]
        self.db.calendars.update(self.old_calendar_name, new_calendar_data)
        self.parent_frame.update()
        self.go_back()
