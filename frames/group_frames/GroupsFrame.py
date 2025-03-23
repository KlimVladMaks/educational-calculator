import os
import tkinter as tk
from tkinter import ttk
import json
from frames.BaseFrame import BaseFrame
from frames.group_frames.AddGroupFrame import AddGroupFrame
from frames.group_frames.EditGroupFrame import EditGroupFrame
from widgets.Table import Table
from database.Database import Database
from widgets.Calculator import Calculator
from calendar_app.CalendarApp import CalendarApp
from widgets.BackButton import BackButton


class GroupsFrame(BaseFrame):
    """
    Фрейм для работы с учебными группами.
    """

    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()

    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.pack()

        ttk.Label(self, text="Учебные группы").pack(pady=10)
        self.create_table()
        ttk.Button(self, text="Добавить учебную группу",
                   command=self.open_add_groups).pack(pady=10)

    def create_table(self):
        self.create_comboboxes()
        columns = [
            ("Название", 150),
            ("Календарь", 100),
            ("Программа", 100),
            ("Вид обучения", 100),
            ("Дата начала", 100),
            ("Дата окончания", 100),
            ("Дней обучения", 100),
            ("Всего дней", 100)
        ]
        self.table = Table(self, columns)
        self.table_data = self.get_table_rows()
        self.table.add_rows(self.table_data)
        self.table.pack()

        self.create_context_menu()

    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()

    def create_comboboxes(self):
        self.comboboxes_frame = ttk.Frame(self)
        self.comboboxes_frame.pack(pady=10)

        calendars_names = self.get_calendars_names()
        programs_names = self.get_programs_names()
        calendars_names.insert(0, "Все календари")
        programs_names.insert(0, "Все программы")

        self.calendar_combobox = ttk.Combobox(
            self.comboboxes_frame, values=calendars_names, state="readonly")
        self.calendar_combobox.grid(row=0, column=0, padx=10)
        self.calendar_combobox.set(calendars_names[0])
        self.calendar_combobox.bind("<<ComboboxSelected>>", self.filter_table)

        self.program_combobox = ttk.Combobox(
            self.comboboxes_frame, values=programs_names, state="readonly")
        self.program_combobox.grid(row=0, column=1, padx=10)
        self.program_combobox.set(programs_names[0])
        self.program_combobox.bind("<<ComboboxSelected>>", self.filter_table)

    def get_calendars_names(self, program_name=None):
        calendars_names = []
        groups_data = self.db.groups.get_all()
        for data in groups_data:
            if ((program_name is None) or
                (program_name == "Все программы") or
                    (program_name == data[2])) and (data[1] not in calendars_names):
                calendars_names.append(data[1])
        return calendars_names

    def get_programs_names(self, calendar_name=None):
        programs_names = []
        groups_data = self.db.groups.get_all()
        for data in groups_data:
            if ((calendar_name is None) or
                (calendar_name == "Все календари") or
                    (calendar_name == data[1])) and (data[2] not in programs_names):
                programs_names.append(data[2])
        return programs_names

    def filter_table(self, event=None):
        selected_calendar = self.calendar_combobox.get()
        selected_program = self.program_combobox.get()
        filtered_table_data = []
        all_table_data = self.get_table_rows()
        for data in all_table_data:
            if ((selected_calendar == "Все календари") or (data[1] == selected_calendar)) and \
               ((selected_program == "Все программы") or (data[2] == selected_program)):
                filtered_table_data.append(data)
        self.table.update(filtered_table_data)
        self.update_comboboxes()

    def get_table_rows(self):
        table_data = []
        groups_data = self.db.groups.get_all()
        for data in groups_data:
            table_data.append(data)
        for data in table_data:
            end_date = Calculator.calculate_end_date(data[1], data[2], data[4])
            data.append(end_date)
            total_study_days = self.db.programs.get_total_days(data[2])
            data.append(total_study_days)
            total_days = Calculator.count_days_between_dates(data[4], data[5])
            data.append(total_days)
        return table_data

    def update_comboboxes(self):
        selected_calendar = self.calendar_combobox.get()
        selected_program = self.program_combobox.get()

        calendars_names = self.get_calendars_names(selected_program)
        programs_names = self.get_programs_names(selected_calendar)

        calendars_names.insert(0, "Все календари")
        programs_names.insert(0, "Все программы")

        self.calendar_combobox["values"] = calendars_names
        self.program_combobox["values"] = programs_names

        self.calendar_combobox.set(selected_calendar)
        self.program_combobox.set(selected_program)

    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(
            label="Календарь", command=self.open_calendar_app)
        self.menu.add_command(label="Изменить", command=self.open_edit_group)
        self.menu.add_command(label="Удалить", command=self.delete_selected)
        self.table.tree.bind("<Button-3>", self.show_context_menu)

    def open_edit_group(self):
        selected_items = self.table.tree.selection()
        item = selected_items[0]
        item_data = self.table.tree.item(item)
        values = item_data["values"]
        group_name = values[0]
        edit_group_frame = EditGroupFrame(self.master, self, group_name)
        edit_group_frame.display_frame()

    def open_calendar_app(self):
        selected_items = self.table.tree.selection()
        item = selected_items[0]
        item_data = self.table.tree.item(item)
        group_data = item_data['values']
        self.prepare_files_for_calendar_app(group_data[0])
        new_window = tk.Toplevel(self.master)
        new_window.grab_set()
        CalendarApp(new_window)

    def prepare_files_for_calendar_app(self, group_name: str) -> None:
        directory = "./calendar_app"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Получаем список данных группы в формате:
        # ["0: name", "1: calendar", "2: program", "3: edu_type", "4: start_date"]
        group_data: list[str] = self.db.groups.get_group_data_list(group_name)

        days_off_list: list[str] = self.db.calendars.get_days_off_list(group_data[1])
        filename = ".\calendar_app\days_off.json"
        with open(filename, 'w+', encoding='utf-8') as file:
            data = {
                "Праздник": [],
                "Выходной": days_off_list
            }
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        # Получаем список временных интервалов для этапов в формате:
        # [["Название_этапа_1", "Дата_начала_этапа_1", "Дата_окончания_этапа_1"], [...], ...]
        stages_intervals: list[list[str]] = Calculator.calculate_stages_intervals(group_data[1], 
                                                                                  group_data[2], group_data[4])
        
        study_periods: list[dict[str, str]] = []
        type: str = ""
        for stage_interval in stages_intervals:
            match stage_interval[0]:
                case "Теория":
                    type = "theory"
                case "Практика":
                    type = "practice"
                case "Консультация":
                    type = "consultation"
                case "Экзамен":
                    type = "exam"
                case "Пробная поездка":
                    type = "trial_ride"
                case _:
                    type = stage_interval[0]
            study_period = {
                "start_date": stage_interval[1],
                "end_date": stage_interval[2],
                "type": type
            }
            study_periods.append(study_period)
        
        filename = ".\calendar_app\study_periods.json"
        with open(filename, 'w+', encoding='utf-8') as file:
            json.dump(study_periods, file, ensure_ascii=False, indent=4)

    def delete_selected(self):
        selected_items = self.table.tree.selection()
        for item in selected_items:
            item_data = self.table.tree.item(item)
            values = item_data['values']
            self.db.groups.delete(str(values[0]))
            self.table.tree.delete(item)

    def show_context_menu(self, event):
        row_id = self.table.tree.identify_row(event.y)
        if row_id:
            self.table.tree.selection_set(row_id)
            self.menu.post(event.x_root, event.y_root)

    def open_add_groups(self):
        self.add_group_frame = AddGroupFrame(self.master, self)
        self.add_group_frame.display_frame()

    def update_table(self):
        new_table_data = self.get_table_rows()
        self.table.update(new_table_data)
        self.calendar_combobox.set("Все календари")
        self.program_combobox.set("Все программы")
        self.update_comboboxes()
