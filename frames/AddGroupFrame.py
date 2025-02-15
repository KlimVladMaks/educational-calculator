import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame


# Данные для примера
example_calendars = ["Календарь 1", "Календарь 2", "Календарь 3"]
example_programs = ["Программа 1", "Программа 2", "Программа 3"]


class AddGroupFrame(BaseFrame):
    """
    Фрейм для добавления новой учебной группы.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.create_frame()
    
    def create_frame(self):
        self.back_button = ttk.Button(self.master, text="Назад", command=self.go_back)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)

        ttk.Label(self, text="Добавить учебную группу").pack(pady=10)

        self.input_name_frame = ttk.Frame(self)
        self.input_name_frame.pack(pady=10)

        self.start_date_label = ttk.Label(self.input_name_frame, text="Название:")
        self.start_date_label.grid(row=0, column=0, padx=5)
        self.start_date_entry = ttk.Entry(self.input_name_frame, width=50)
        self.start_date_entry.grid(row=0, column=1, padx=5)

        self.comboboxes_frame = ttk.Frame(self)
        self.comboboxes_frame.pack(pady=10)

        self.calendar_label = ttk.Label(self.comboboxes_frame, text="Выберите календарь:")
        self.calendar_label.grid(row=0, column=0, padx=10, pady=5)
        self.program_label = ttk.Label(self.comboboxes_frame, text="Выберите программу:")
        self.program_label.grid(row=0, column=1, padx=10, pady=5)

        self.calendar_combobox = ttk.Combobox(self.comboboxes_frame, values=example_calendars, state="readonly")
        self.calendar_combobox.grid(row=1, column=0, padx=10)
        self.program_combobox = ttk.Combobox(self.comboboxes_frame, values=example_programs, state="readonly")
        self.program_combobox.grid(row=1, column=1, padx=10)

        self.input_start_date_frame = ttk.Frame(self)
        self.input_start_date_frame.pack(pady=20)

        self.start_date_label = ttk.Label(self.input_start_date_frame, text="Дата начала обучения:")
        self.start_date_label.grid(row=0, column=0, padx=5)
        self.start_date_entry = ttk.Entry(self.input_start_date_frame)
        self.start_date_entry.grid(row=0, column=1, padx=5)

        self.total_days_label = ttk.Label(self, text="Дней обучения: 0")
        self.total_days_label.pack(pady=10)
        self.end_date_label = ttk.Label(self, text="Дата окончания обучения: 2025-01-01")
        self.end_date_label.pack(pady=10)

        ttk.Button(self, text="Добавить учебную группу").pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
