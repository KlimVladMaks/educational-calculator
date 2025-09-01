from tkinter import ttk
from datetime import datetime
from frames.base_frame import BaseFrame
from database.database import Database
from widgets.back_button import BackButton
from widgets.date_entry import DateEntry
from widgets.calculator import Calculator


class EditGroupFrame(BaseFrame):

    def __init__(self, master, parent_frame, old_group_name):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.old_group_name = old_group_name
        self.db = Database()
        self.create_frame()

    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.place()

        old_group_data = self.db.groups.get_group_data_dict(self.old_group_name)

        ttk.Label(self, text="Изменить учебную группу").pack(pady=10)

        ttk.Label(self, text="Название:").pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self, width=50)
        self.name_entry.insert(0, old_group_data["name"])
        self.name_entry.pack(pady=(0, 10))

        self.comboboxes_frame = ttk.Frame(self)
        self.comboboxes_frame.pack(pady=10)

        ttk.Label(self.comboboxes_frame, text="Выберите календарь:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(self.comboboxes_frame, text="Выберите программу:").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self.comboboxes_frame, text="Выберите вид обучения:").grid(row=0, column=2, padx=10, pady=5)

        self.calendars_names = self.db.calendars.get_all_calendars_names()
        self.programs_names = self.db.programs.get_all_programs_names()
        self.edu_types = self.db.edu_types.get_all_edu_types()

        self.calendar_combobox = ttk.Combobox(self.comboboxes_frame,
                                              values=self.calendars_names,
                                              state="readonly")
        self.calendar_combobox.set(old_group_data["calendar"])
        self.calendar_combobox.grid(row=1, column=0, padx=10)
        self.calendar_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_preview_labels())

        self.program_combobox = ttk.Combobox(self.comboboxes_frame,
                                             values=self.programs_names,
                                             state="readonly")
        self.program_combobox.set(old_group_data["program"])
        self.program_combobox.grid(row=1, column=1, padx=10)
        self.program_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_preview_labels())

        self.edu_type_combobox = ttk.Combobox(self.comboboxes_frame,
                                              values=self.edu_types,
                                              state="readonly")
        self.edu_type_combobox.set(old_group_data["edu_type"])
        self.edu_type_combobox.grid(row=1, column=2, padx=10)

        ttk.Label(self, text="Дата начала обучения:").pack(pady=(10, 0))
        self.start_date_entry = DateEntry(self)
        self.start_date_entry.insert(old_group_data["start_date"])
        self.start_date_entry.pack(pady=(0, 10))
        self.start_date_entry.bind("<KeyRelease>", lambda event: self.update_preview_labels())

        self.study_days_label = ttk.Label(self, text="Дней обучения: -")
        self.study_days_label.pack(pady=(10, 3))
        self.days_off_label = ttk.Label(self, text="Выходных дней: -")
        self.days_off_label.pack(pady=3)
        self.total_days_label = ttk.Label(self, text="Всего дней: -")
        self.total_days_label.pack(pady=3)
        self.end_date_label = ttk.Label(self, text="Дата окончания обучения: -")
        self.end_date_label.pack(pady=(3, 10))

        self.update_preview_labels()

        ttk.Button(self, text="Сохранить учебную группу", command=self.save_group).pack(pady=10)
    
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

        self.db.groups.update_group(self.old_group_name, new_group_data)
        self.parent_frame.update_table()
        self.go_back()
    
    def update_preview_labels(self):
        try:
            calendar = self.calendar_combobox.get()
            program = self.program_combobox.get()
            start_date = self.start_date_entry.get()

            end_date = Calculator.calculate_end_date(calendar, program, start_date)
            total_days = Calculator.count_days_between_dates(start_date, end_date)
            study_days = self.db.programs.get_total_days(program)
            days_off = total_days - study_days

            date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            end_date = date_obj.strftime("%d.%m.%Y")

            self.study_days_label.config(text=f"Дней обучения: {study_days}")
            self.days_off_label.config(text=f"Выходных дней: {days_off}")
            self.total_days_label.config(text=f"Всего дней: {total_days}")
            self.end_date_label.config(text=f"Дата окончания обучения: {end_date}")

        except:
            self.study_days_label.config(text=f"Дней обучения: -")
            self.days_off_label.config(text=f"Выходных дней: -")
            self.total_days_label.config(text=f"Всего дней: -")
            self.end_date_label.config(text=f"Дата окончания обучения: -")




