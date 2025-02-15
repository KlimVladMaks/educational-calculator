import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from frames.AddProgramFrame import AddProgramFrame
from widgets.Table import Table


# Данные для примера
example_programs = [
    ("Программа 1", "10", "20", "5", "100"),
    ("Программа 2", "20", "40", "10", "200"),
    ("Программа 3", "30", "60", "15", "300"),
    ("Программа 4", "40", "80", "20", "400"),
    ("Программа 5", "50", "100", "25", "500")
]


class ProgramsFrame(BaseFrame):
    """
    Фрейм для работы с учебными программами.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.create_frame()

    def create_frame(self):
        self.back_button = ttk.Button(self.master, text="Назад", command=self.go_back)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)
        
        ttk.Label(self, text="Учебные программы").pack(pady=10)
        self.create_table()
        self.create_context_menu()
        ttk.Button(self, text="Добавить учебную программу", command=self.open_add_program).pack(pady=10)
    
    def create_table(self):
        columns = [
            ("Название", 150),
            ("Теория", 100),
            ("Практика", 100),
            ("Экзамен", 100),
            ("Всего", 100)
        ]
        self.table = Table(self, columns)
        self.table.add_rows(example_programs)
        self.table.pack()

    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Удалить", command=self.delete_selected)
        self.table.tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        row_id = self.table.tree.identify_row(event.y)
        if row_id:
            self.table.tree.selection_set(row_id)
            self.menu.post(event.x_root, event.y_root)
    
    def delete_selected(self):
        selected_items = self.table.tree.selection()
        for item in selected_items:
            self.table.tree.delete(item)

    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()

    def open_add_program(self):
        self.add_program_frame = AddProgramFrame(self.master, self)
        self.add_program_frame.display_frame()
