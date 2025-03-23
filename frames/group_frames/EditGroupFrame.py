import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from database.Database import Database
from widgets.BackButton import BackButton
from widgets.Calculator import Calculator


class EditGroupFrame(BaseFrame):
    """
    Фрейм для изменения данный учебной группы.
    """
    def __init__(self, master, parent_frame, old_group_name):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.old_group_name = old_group_name
        self.db = Database()
        self.old_group_data = self.db.groups.get_group_data_list(self.old_group_name)
        self.create_frame()
    
    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.pack()

        ttk.Label(self, text="Изменить данные учебной группы").pack(pady=10)

        ttk.Label(self, text="Название:").pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self, width=50)
        self.name_entry.pack(pady=(0, 10))
        self.name_entry.insert(0, self.old_group_data[0])

        self.comboboxes_frame = ttk.Frame(self)
        self.comboboxes_frame.pack(pady=10)

        ttk.Label(self.comboboxes_frame, text="Выберите календарь:").grid(
            row=0, column=0, padx=10, pady=5)
        ttk.Label(self.comboboxes_frame, text="Выберите программу:").grid(
            row=0, column=1, padx=10, pady=5)
        ttk.Label(self.comboboxes_frame, text="Выберите вид обучения:").grid(
            row=0, column=2, padx=10, pady=5)
        
        self.calendars_names = self.db.calendars.get_all_names()
        self.programs_names = self.db.programs.get_all_names()
        self.edu_types = self.db.edu_types.get_all()

        self.calendar_combobox = ttk.Combobox(self.comboboxes_frame,
                                              values=self.calendars_names,
                                              state="readonly")
        self.calendar_combobox.grid(row=1, column=0, padx=10)
        self.calendar_combobox.set(self.old_group_data[1])

        self.program_combobox = ttk.Combobox(self.comboboxes_frame,
                                             values=self.programs_names,
                                             state="readonly")
        self.program_combobox.grid(row=1, column=1, padx=10)
        self.program_combobox.set(self.old_group_data[2])

        self.edu_type_combobox = ttk.Combobox(self.comboboxes_frame,
                                              values=self.edu_types,
                                              state="readonly")
        self.edu_type_combobox.grid(row=1, column=2, padx=10)
        self.edu_type_combobox.set(self.old_group_data[3])

        ttk.Label(self, text="Дата начала обучения:").pack(pady=(10, 0))
        self.start_date_entry = ttk.Entry(self)
        self.start_date_entry.pack(pady=(0, 10))
        self.start_date_entry.insert(0, self.old_group_data[4])

        self.study_days_label = ttk.Label(self, text="Дней обучения: -")
        self.study_days_label.pack(pady=(10, 5))
        self.total_days_label = ttk.Label(self, text="Всего дней: -")
        self.total_days_label.pack(pady=5)
        self.end_date_label = ttk.Label(
            self, text="Дата окончания обучения: -")
        self.end_date_label.pack(pady=(5, 10))

        ttk.Button(self, text="Сохранить изменения",
                   command=self.save_group).pack(pady=10)
        
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def save_group(self):
        new_group_data = []

        name = self.name_entry.get()
        calendar = self.calendar_combobox.get()
        program = self.program_combobox.get()
        edu_type = self.edu_type_combobox.get()
        start_date = self.start_date_entry.get()

        new_group_data.append(name)
        new_group_data.append(calendar)
        new_group_data.append(program)
        new_group_data.append(edu_type)
        new_group_data.append(start_date)

        self.db.groups.update(self.old_group_name, new_group_data)
        self.parent_frame.update_table()
        self.go_back()
