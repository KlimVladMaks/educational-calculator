from tkinter import ttk
from frames.base_frame import BaseFrame
from database.database import Database
from widgets.back_button import BackButton


class AddGroupFrame(BaseFrame):

    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.place()

        ttk.Label(self, text="Добавить учебную группу").pack(pady=10)

        ttk.Label(self, text="Название:").pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self, width=50)
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
        self.calendar_combobox.grid(row=1, column=0, padx=10)

        self.program_combobox = ttk.Combobox(self.comboboxes_frame,
                                             values=self.programs_names,
                                             state="readonly")
        self.program_combobox.grid(row=1, column=1, padx=10)

        self.edu_type_combobox = ttk.Combobox(self.comboboxes_frame,
                                              values=self.edu_types,
                                              state="readonly")
        self.edu_type_combobox.grid(row=1, column=2, padx=10)

        ttk.Label(self, text="Дата начала обучения:").pack(pady=(10, 0))
        self.start_date_entry = ttk.Entry(self)
        self.start_date_entry.pack(pady=(0, 10))

        self.study_days_label = ttk.Label(self, text="Дней обучения: -")
        self.study_days_label.pack(pady=(10, 3))
        self.days_off_label = ttk.Label(self, text="Выходных дней: -")
        self.days_off_label.pack(pady=3)
        self.total_days_label = ttk.Label(self, text="Всего дней: -")
        self.total_days_label.pack(pady=3)
        self.end_date_label = ttk.Label(self, text="Дата окончания обучения: -")
        self.end_date_label.pack(pady=(3, 10))

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

        self.db.groups.add_new_group(new_group_data)
        self.parent_frame.update_table()
        self.go_back()








