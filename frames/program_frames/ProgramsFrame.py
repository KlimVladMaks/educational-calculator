import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from frames.program_frames.AddProgramFrame import AddProgramFrame
from widgets.Table import Table
from database.Database import Database
from widgets.BackButton import BackButton

class ProgramsFrame(BaseFrame):
    """
    Фрейм для работы с учебными программами.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.pack()
        ttk.Label(self, text="Учебные программы").pack(pady=10)
        self.create_table()
        self.add_program_button = ttk.Button(self, 
                                             text="Добавить учебную программу", 
                                             command=self.open_add_program)
        self.add_program_button.pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def create_table(self):
        table_columns = self.get_table_columns()
        self.table = Table(self, table_columns)
        table_rows = self.get_table_rows()
        self.table.add_rows(table_rows)
        self.table.pack()
        self.create_context_menu()
    
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
            total_days = self.db.programs.get_total_days(program_name)
            table_row.append(total_days)
            for stage_name in unique_stages_names:
                number_of_days = self.db.programs.get_number_of_days_for_stage(program_name, stage_name)
                table_row.append(number_of_days)
            table_rows.append(table_row)
        return table_rows

    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Изменить")
        self.menu.add_command(label="Удалить", command=self.delete_selected)
        self.table.tree.bind("<Button-3>", self.show_context_menu)
    
    def delete_selected(self):
        selected_items = self.table.tree.selection()
        item = selected_items[0]
        item_data = self.table.tree.item(item)
        values = item_data["values"]
        self.db.programs.delete(str(values[0]))
        self.table.tree.delete(item)
        self.update_table()
    
    def show_context_menu(self, event):
        row_id = self.table.tree.identify_row(event.y)
        if row_id:
            self.table.tree.selection_set(row_id)
            self.menu.post(event.x_root, event.y_root)
    
    def open_add_program(self):
        add_program_frame = AddProgramFrame(self.master, self)
        add_program_frame.display_frame()
    
    def update_table(self):
        self.table.destroy()
        self.add_program_button.destroy()
        self.create_table()
        self.add_program_button = ttk.Button(self, 
                                             text="Добавить учебную программу", 
                                             command=self.open_add_program)
        self.add_program_button.pack(pady=10)
