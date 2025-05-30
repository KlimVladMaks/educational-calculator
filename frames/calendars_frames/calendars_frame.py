import tkinter as tk
from tkinter import ttk
from frames.base_frame import BaseFrame
from frames.calendars_frames.add_calendar_frame import AddCalendarFrame
from frames.calendars_frames.edit_calendar_frame import EditCalendarFrame
from database.database import Database
from widgets.back_button import BackButton
from widgets.table import Table
from widgets.calculator import Calculator


class CalendarsFrame(BaseFrame):
    """
    Фрейм для работы с производственными календарями.
    """
    def __init__(self, master: tk.Tk, parent_frame: BaseFrame) -> None:
        """
        Аргументы:
        - master: Окно приложения.
        - parent_frame: Родительский фрейм.
        """
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self) -> None:
        """
        Создаёт фрейм (добавляет и настраивает все необходимые компоненты).
        """
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.place()
        ttk.Label(self, text="Производственные календаря").pack(pady=10)
        self.create_table()
        ttk.Button(self, text="Добавить производственный календарь", 
                   command=self.open_add_calendar_frame).pack(pady=5)
    
    def go_back(self) -> None:
        """
        Уничтожает текущий фрейм и открывает предыдущий.
        """
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def create_table(self) -> None:
        """
        Создаёт таблицу с учебными программами.
        """
        columns = [
            ("Название", 150),
            ("Начало", 100),
            ("Конец", 100),
            ("Рабочие дни", 100),
            ("Выходные дни", 100),
            ("Всего дней", 100),
        ]
        self.table = Table(self, columns, height=11)
        table_rows = self.get_table_rows()
        self.table.add_rows(table_rows)
        self.table.pack(pady=10)

        self.table.add_menu_command(label="Изменить", command=self.open_edit_calendar_frame)
        self.table.add_menu_command(label="Удалить", command=self.delete_calendar)
    
    def get_table_rows(self) -> list[list]:
        """
        Выдаёт список со значениями строк таблицы в формате:
        [[<1-е значение 1-й строки>, <2-е значение 1-й строки>, ...], [<1-е значение 2-й строки>, ...], ...].
        """
        table_rows: list[list[str]] = []
        calendars_names = self.db.calendars.get_all_calendars_names()
        for calendar_name in calendars_names:
            table_row: list[str] = [calendar_name]
            calendar_dict = self.db.calendars.get_calendar_data_dict(calendar_name)
            total_days = Calculator.count_days_between_dates(calendar_dict["start_date"], calendar_dict["end_date"])
            days_off = len(calendar_dict["days_off_list"])
            working_days = total_days - days_off
            table_row.append(Calculator.convert_date_to_dd_mm_yyyy(calendar_dict["start_date"]))
            table_row.append(Calculator.convert_date_to_dd_mm_yyyy(calendar_dict["end_date"]))
            table_row.append(working_days)
            table_row.append(days_off)
            table_row.append(total_days)
            table_rows.append(table_row)
        return table_rows
            
    def open_edit_calendar_frame(self):
        selected_calendar_data = self.table.get_selected_row()
        calendar_name = str(selected_calendar_data[0])
        edit_calendar_frame = EditCalendarFrame(self.master, self, calendar_name)
        edit_calendar_frame.display_frame()

    def delete_calendar(self):
        selected_calendar_data = self.table.get_selected_row()
        self.db.calendars.delete_calendar(str(selected_calendar_data[0]))
        self.table.delete_selected()

    def open_add_calendar_frame(self):
        add_calendar_frame = AddCalendarFrame(self.master, self)
        add_calendar_frame.display_frame()

    def update_table(self):
        new_table_rows = self.get_table_rows()
        self.table.update_rows(new_table_rows)




