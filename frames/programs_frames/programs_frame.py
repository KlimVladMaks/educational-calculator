import tkinter as tk
from tkinter import ttk
from frames.base_frame import BaseFrame
from frames.programs_frames.add_program_frame import AddProgramFrame
from frames.programs_frames.edit_program_frame import EditProgramFrame
from database.database import Database
from widgets.back_button import BackButton
from widgets.table import Table


class ProgramsFrame(BaseFrame):
    """
    Фрейм для работы с учебными программами.
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
        ttk.Label(self, text="Учебные программы").pack(pady=10)
        self.create_table()
        self.add_program_button = ttk.Button(self, text="Добавить учебную программу",
                                             command=self.open_add_program_frame)
        self.add_program_button.pack(pady=10)
    
    def create_table(self) -> None:
        """
        Создаёт таблицу с учебными программами.
        """
        table_columns = self.get_table_columns()
        self.table = Table(self, table_columns, height=11)
        table_rows = self.get_table_rows()
        self.table.add_rows(table_rows)
        self.table.add_menu_command(label="Изменить", command=self.open_edit_program_frame)
        self.table.add_menu_command(label="Удалить", command=self.delete_program)
        self.table.pack(pady=10)
    
    def go_back(self) -> None:
        """
        Уничтожает текущий фрейм и открывает предыдущий.
        """
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()

    def get_table_columns(self):
        table_columns = [
            ["Название", 150],
            ["Всего дней", 100]
        ]
        unique_stages_names = self.db.programs.get_unique_stages_names()
        for stage_name in unique_stages_names:
            table_column = []
            table_column.append(stage_name)
            table_column.append(100)
            table_columns.append(table_column)
        return table_columns

    def get_table_rows(self):
        table_rows = []
        unique_stages_names = self.db.programs.get_unique_stages_names()
        programs_names = self.db.programs.get_all_programs_names()
        for program_name in programs_names:
            table_row = []
            table_row.append(program_name)
            program_duration = self.db.programs.get_program_duration(program_name)
            table_row.append(program_duration)
            for stage_name in unique_stages_names:
                stage_duration = self.db.programs.get_program_stage_duration(program_name, stage_name)
                table_row.append(stage_duration)
            table_rows.append(table_row)
        return table_rows

    def open_edit_program_frame(self):
        selected_program_data = self.table.get_selected_row()
        old_program_name = str(selected_program_data[0])
        edit_program_frame = EditProgramFrame(self.master, self, old_program_name)
        edit_program_frame.display_frame()

    def delete_program(self):
        selected_program_data = self.table.get_selected_row()
        self.db.programs.delete_program(str(selected_program_data[0]))
        self.table.delete_selected()

    def open_add_program_frame(self):
        add_program_frame = AddProgramFrame(self.master, self)
        add_program_frame.display_frame()

    def update_table(self):
        self.table.destroy()
        self.add_program_button.destroy()
        self.create_table()
        self.add_program_button = ttk.Button(self, text="Добавить учебную программу",
                                             command=self.open_add_program_frame)
        self.add_program_button.pack(pady=10)




