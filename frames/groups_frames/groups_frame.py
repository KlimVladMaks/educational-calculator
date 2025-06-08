import os
import json
import tkinter as tk
from tkinter import ttk
from frames.base_frame import BaseFrame
from frames.groups_frames.add_group_frame import AddGroupFrame
from frames.groups_frames.edit_group_frame import EditGroupFrame
from database.database import Database
from widgets.back_button import BackButton
from widgets.table import Table
from widgets.calculator import Calculator
from calendar_app.CalendarApp import CalendarApp


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
        self.back_button.place()
        ttk.Label(self, text="Учебные группы").pack(pady=10)
        self.create_table()
        ttk.Button(self, text="Добавить учебную группу",
                   command=self.open_add_group_frame).pack(pady=10)

    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()

    def create_table(self):
        columns = [
            ("Название", 150),
            ("Календарь", 100),
            ("Программа", 100),
            ("Вид обучения", 100),
            ("Дата начала", 100),
            ("Дата окончания", 100),
            ("Дней обучения", 100),
            ("Выходных дней", 100),
            ("Всего дней", 100)
        ]
        self.table = Table(self, columns, height=11)
        table_rows = self.get_table_rows()
        self.table.add_rows(table_rows)
        self.table.pack(pady=10)

        self.table.add_menu_command(
            label="Календарь", command=self.open_calendar_app)
        self.table.add_menu_command(
            label="Изменить", command=self.open_edit_group_frame)
        self.table.add_menu_command(label="Удалить", command=self.delete_group)

    def get_table_rows(self):
        table_rows = []
        groups_names = self.db.groups.get_all_groups_names()
        for group_name in groups_names:
            table_row = [group_name]
            group_data_dict = self.db.groups.get_group_data_dict(group_name)
            calendar = group_data_dict["calendar"]
            program = group_data_dict["program"]
            edu_type = group_data_dict["edu_type"]
            start_date = group_data_dict["start_date"]
            end_date = Calculator.calculate_end_date(
                calendar, program, start_date)
            total_days = Calculator.count_days_between_dates(
                start_date, end_date)
            study_days = self.db.programs.get_total_days(program)
            days_off = total_days - study_days
            table_row.append(calendar)
            table_row.append(program)
            table_row.append(edu_type)
            table_row.append(Calculator.convert_date_to_dd_mm_yyyy(start_date))
            table_row.append(Calculator.convert_date_to_dd_mm_yyyy(end_date))
            table_row.append(study_days)
            table_row.append(days_off)
            table_row.append(total_days)
            table_rows.append(table_row)
        return table_rows

    def open_edit_group_frame(self):
        selected_group_data = self.table.get_selected_row()
        old_group_name = str(selected_group_data[0])
        self.edit_group_frame = EditGroupFrame(
            self.master, self, old_group_name)
        self.edit_group_frame.display_frame()

    def delete_group(self):
        selected_group_data = self.table.get_selected_row()
        self.db.groups.delete_group(str(selected_group_data[0]))
        self.table.delete_selected()

    def open_calendar_app(self):
        selected_group_data = self.table.get_selected_row()
        group_name = str(selected_group_data[0])
        self.prepare_files_for_calendar_app(group_name)
        new_window = tk.Toplevel(self.master)
        new_window.grab_set()
        CalendarApp(new_window)

    def prepare_files_for_calendar_app(self, group_name):
        directory = "./calendar_app"
        if not os.path.exists(directory):
            os.makedirs(directory)

        group_data_dict = self.db.groups.get_group_data_dict(group_name)
        group_days_off_list = self.db.calendars.get_days_off_list(
            group_data_dict["calendar"])

        filename = ".\calendar_app\days_off.json"
        with open(filename, 'w+', encoding='utf-8') as file:
            data = {
                "Праздник": [],
                "Выходной": group_days_off_list
            }
            json.dump(data, file, ensure_ascii=False, indent=4)

        stages_intervals = Calculator.calculate_stages_intervals(group_data_dict["calendar"],
                                                                 group_data_dict["program"],
                                                                 group_data_dict["start_date"])
        study_periods = []
        stage_type = ""
        for stage_interval in stages_intervals:
            match stage_interval[0]:
                case "Теория":
                    stage_type = "theory"
                case "Практика":
                    stage_type = "practice"
                case "Консультация":
                    stage_type = "consultation"
                case "Экзамен":
                    stage_type = "exam"
                case "Пробная поездка":
                    stage_type = "trial_ride"
                case _:
                    stage_type = stage_interval[0]
            study_period = {
                "start_date": stage_interval[1],
                "end_date": stage_interval[2],
                "type": stage_type
            }
            study_periods.append(study_period)

        filename = ".\calendar_app\study_periods.json"
        with open(filename, 'w+', encoding='utf-8') as file:
            json.dump(study_periods, file, ensure_ascii=False, indent=4)

    def update_table(self):
        new_table_rows = self.get_table_rows()
        self.table.update_rows(new_table_rows)

    def open_add_group_frame(self):
        add_group_frame = AddGroupFrame(self.master, self)
        add_group_frame.display_frame()
