import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from database.Database import Database
from widgets.Calculator import Calculator


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
        self.back_button = ttk.Button(self.master, text="Назад", command=self.go_back)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)
    
        ttk.Label(self, text="Добавить учебную группу").pack(pady=10)

        self.input_name_frame = ttk.Frame(self)
        self.input_name_frame.pack(pady=10)

        self.name_label = ttk.Label(self.input_name_frame, text="Название:")
        self.name_label.grid(row=0, column=0, padx=5)
        self.name_entry = ttk.Entry(self.input_name_frame, width=50)
        self.name_entry.grid(row=0, column=1, padx=5)

        self.comboboxes_frame = ttk.Frame(self)
        self.comboboxes_frame.pack(pady=10)

        self.calendar_label = ttk.Label(self.comboboxes_frame, text="Выберите календарь:")
        self.calendar_label.grid(row=0, column=0, padx=10, pady=5)
        self.program_label = ttk.Label(self.comboboxes_frame, text="Выберите программу:")
        self.program_label.grid(row=0, column=1, padx=10, pady=5)

        self.calendars_names = []
        self.calendars_data = self.db.calendars.get_all()
        for data in self.calendars_data:
            self.calendars_names.append(data[0])
        self.programs_names = []
        self.programs_data = self.db.programs.get_all()
        for data in self.programs_data:
            self.programs_names.append(data[0])

        self.calendar_combobox = ttk.Combobox(self.comboboxes_frame, values=self.calendars_names, state="readonly")
        self.calendar_combobox.grid(row=1, column=0, padx=10)
        self.calendar_combobox.bind("<<ComboboxSelected>>", self.update_labels)
        self.program_combobox = ttk.Combobox(self.comboboxes_frame, values=self.programs_names, state="readonly")
        self.program_combobox.grid(row=1, column=1, padx=10)
        self.program_combobox.bind("<<ComboboxSelected>>", self.update_labels)

        self.input_start_date_frame = ttk.Frame(self)
        self.input_start_date_frame.pack(pady=20)

        self.name_label = ttk.Label(self.input_start_date_frame, text="Дата начала обучения:")
        self.name_label.grid(row=0, column=0, padx=5)
        self.start_date_entry = ttk.Entry(self.input_start_date_frame)
        self.start_date_entry.grid(row=0, column=1, padx=5)
        self.start_date_entry.bind("<KeyRelease>", self.update_labels)

        # Добавить функции для расчёта
        self.total_days_label = ttk.Label(self, text="Обучение займёт (дней): -")
        self.total_days_label.pack(pady=10)
        self.end_date_label = ttk.Label(self, text="Дата окончания обучения: -")
        self.end_date_label.pack(pady=10)

        ttk.Button(self, text="Добавить учебную группу", command=self.add_group).pack(pady=10)

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
    
    def update_labels(self, event=None):
        try:
            calendar_name = self.calendar_combobox.get()
            program_name = self.program_combobox.get()
            start_date = str(self.start_date_entry.get())
            if (calendar_name == "") or (program_name == ""):
                return
            end_date = Calculator.calculate_end_date(calendar_name, program_name, start_date)
            total_days = Calculator.count_days(start_date, end_date)
            self.total_days_label.config(text=f"Обучение займёт (дней): {total_days}")
            self.end_date_label.config(text=f"Дата окончания обучения: {end_date}")
        except:
            self.total_days_label.config(text="Обучение займёт (дней): -")
            self.end_date_label.config(text="Дата окончания обучения: -")


    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
