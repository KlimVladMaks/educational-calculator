import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from database.Database import Database
from widgets.Calculator import Calculator
from widgets.BackButton import BackButton


class AddGroupFrame(BaseFrame):
    """
    Фрейм для добавления новой учебной группы.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)

        ttk.Label(self, text="Добавить учебную группу").pack(pady=10)

        ttk.Label(self, text="Название:").pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self, width=50)
        self.name_entry.pack(pady=(0, 10))

        self.comboboxes_frame = ttk.Frame(self)
        self.comboboxes_frame.pack(pady=10)

        ttk.Label(self.comboboxes_frame, text="Выберите календарь:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(self.comboboxes_frame, text="Выберите программу:").grid(row=0, column=1, padx=10, pady=5)

        self.calendars_names = self.get_calendars_names()
        self.programs_names = self.get_programs_names()

        self.calendar_combobox = ttk.Combobox(self.comboboxes_frame,
                                              values=self.calendars_names,
                                              state="readonly")
        self.calendar_combobox.grid(row=1, column=0, padx=10)
        self.calendar_combobox.bind("<<ComboboxSelected>>", self.update_labels)
        self.program_combobox = ttk.Combobox(self.comboboxes_frame,
                                             values=self.programs_names,
                                             state="readonly")
        self.program_combobox.grid(row=1, column=1, padx=10)
        self.program_combobox.bind("<<ComboboxSelected>>", self.update_labels)

        ttk.Label(self, text="Дата начала обучения:").pack(pady=(10, 0))
        self.start_date_entry = ttk.Entry(self)
        self.start_date_entry.pack(pady=(0, 10))
        self.start_date_entry.bind("<KeyRelease>", self.update_labels)

        self.total_days_label = ttk.Label(self, text="Обучение займёт (дней): -")
        self.total_days_label.pack(pady=10)
        self.end_date_label = ttk.Label(self, text="Дата окончания обучения: -")
        self.end_date_label.pack(pady=10)

        ttk.Button(self, text="Добавить учебную группу", command=self.add_group).pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def get_calendars_names(self):
        calendars_names = []
        calendars_data = self.db.calendars.get_all()
        for data in calendars_data:
            calendars_names.append(data[0])
        return calendars_names

    def get_programs_names(self):
        programs_names = []
        programs_data = self.db.programs.get_all()
        for data in programs_data:
            programs_names.append(data[0])
        return programs_names
    
    def update_labels(self, event=None):
        try:
            calendar_name = self.calendar_combobox.get()
            program_name = self.program_combobox.get()
            start_date = str(self.start_date_entry.get())
            if (calendar_name == "") or (program_name == ""):
                return
            end_date = Calculator.calculate_end_date(calendar_name, program_name, start_date)
            total_days = Calculator.count_days_between_dates(start_date, end_date)
            self.total_days_label.config(text=f"Обучение займёт (дней): {total_days}")
            self.end_date_label.config(text=f"Дата окончания обучения: {end_date}")
        except:
            self.total_days_label.config(text="Обучение займёт (дней): -")
            self.end_date_label.config(text="Дата окончания обучения: -")
    
    def add_group(self):
        self.new_group_data = []

        self.name = str(self.name_entry.get())
        self.calendar = str(self.calendar_combobox.get())
        self.program = str(self.program_combobox.get())
        self.start_date = str(self.start_date_entry.get())

        self.new_group_data.append(self.name)
        self.new_group_data.append(self.calendar)
        self.new_group_data.append(self.program)
        self.new_group_data.append(self.start_date)

        self.db.groups.add(self.new_group_data)

        self.parent_frame.update()
        self.go_back()
