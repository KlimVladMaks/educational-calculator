import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from frames.AddGroupFrame import AddGroupFrame
from widgets.Table import Table


# Данные для примера
example_calendars = ["Все календари", "Календарь 1", "Календарь 2", "Календарь 3"]
example_programs = ["Все программы", "Программа 1", "Программа 2", "Программа 3"]
example_groups = [
    ("Группа 1", "Календарь 1", "Программа 1", "2025-01-01", "2026-01-01", "500"),
    ("Группа 2", "Календарь 2", "Программа 10", "2026-01-01", "2027-01-01", "300"),
    ("Группа 3", "Календарь 1", "Программа 15", "2027-01-01", "2028-01-01", "400"),
    ("Группа 4", "Календарь 2", "Программа 5", "2028-01-01", "2029-01-01", "200"),
    ("Группа 5", "Календарь 1", "Программа 25", "2029-01-01", "2030-01-01", "100"),
]


class GroupsFrame(BaseFrame):
    """
    Фрейм для работы с учебными группами.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.create_frame()
    
    def create_frame(self):
        self.back_button = ttk.Button(self.master, text="Назад", command=self.go_back)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)

        ttk.Label(self, text="Учебные группы").pack(pady=10)

        self.comboboxes_frame = ttk.Frame(self)
        self.comboboxes_frame.pack(pady=10)

        self.calendar_combobox = ttk.Combobox(self.comboboxes_frame, values=example_calendars, state="readonly")
        self.calendar_combobox.grid(row=0, column=0, padx=10)
        self.calendar_combobox.set(example_calendars[0])

        self.program_combobox = ttk.Combobox(self.comboboxes_frame, values=example_programs, state="readonly")
        self.program_combobox.grid(row=0, column=1, padx=10)
        self.program_combobox.set(example_programs[0])

        self.create_table()
        self.create_context_menu()

        ttk.Button(self, text="Добавить учебную группу", command=self.open_add_groups).pack(pady=10)

    def create_table(self):
        columns = [
            ("Название", 150),
            ("Календарь", 100),
            ("Программа", 100),
            ("Дата начала", 100),
            ("Дата окончания", 100),
            ("Дней обучения", 100)
        ]
        self.table = Table(self, columns)
        self.table.add_rows(example_groups)
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
        self.pack_forget()
        self.parent_frame.display_frame()
    
    def open_add_groups(self):
        self.add_group_frame = AddGroupFrame(self.master, self)
        self.add_group_frame.display_frame()
