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
        ttk.Label(self, text="Учебные программы").pack(pady=10)
        self.create_table()
        ttk.Button(self, text="Добавить учебную программу", command=self.open_add_program).pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def create_table(self):
        columns = [
            ("Название", 150),
            ("Теория", 100),
            ("Практика", 100),
            ("Экзамены", 100),
            ("Всего", 100)
        ]
        self.table = Table(self, columns)
        self.table_data = self.get_table_data()
        self.table.add_rows(self.table_data)
        self.table.pack()

        self.create_context_menu()
    
    def get_table_data(self):
        table_data = []
        programs_data = self.db.programs.get_all()
        for data in programs_data:
            table_data.append(data)
        for data in table_data:
            total_days = data[1] + data[2] + data[3]
            data.append(total_days)
        return table_data
    
    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Удалить", command=self.delete_selected)
        self.table.tree.bind("<Button-3>", self.show_context_menu)
    
    def delete_selected(self):
        selected_items = self.table.tree.selection()
        for item in selected_items:
            item_data = self.table.tree.item(item)
            values = item_data['values']
            self.db.programs.delete(str(values[0]))
            self.table.tree.delete(item)
    
    def show_context_menu(self, event):
        row_id = self.table.tree.identify_row(event.y)
        if row_id:
            self.table.tree.selection_set(row_id)
            self.menu.post(event.x_root, event.y_root)
    
    def open_add_program(self):
        self.add_program_frame = AddProgramFrame(self.master, self)
        self.add_program_frame.display_frame()
    
    def update(self):
        new_table_data = self.get_table_data()
        self.table.update(new_table_data)
