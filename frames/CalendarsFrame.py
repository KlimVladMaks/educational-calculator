import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from widgets.Table import Table


# Данные для примера
example_calendars = [
    ("Календарь 1", "2025-01-01", "2026-01-01", "100", "90", "10"),
    ("Календарь 2", "2026-01-01", "2027-01-01", "100", "80", "20"),
    ("Календарь 3", "2027-01-01", "2028-01-01", "100", "70", "30"),
    ("Календарь 4", "2028-01-01", "2029-01-01", "100", "60", "40"),
    ("Календарь 5", "2029-01-01", "2030-01-01", "100", "50", "50")
]


class CalendarsFrame(BaseFrame):
    """
    Фрейм для работы с производственными календарями.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.create_frame()

    def create_frame(self):
        self.back_button = ttk.Button(self.master, text="Назад", command=self.go_back)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)

        ttk.Label(self, text="Производственные календари").pack(pady=10)
        self.create_table()
        self.create_context_menu()
        ttk.Button(self, text="Добавить производственный календарь").pack(pady=10)
    
    def create_table(self):
        columns = [
            ("Название", 150),
            ("Начало", 100),
            ("Конец", 100),
            ("Всего дней", 100),
            ("Рабочие дни", 100),
            ("Выходные дни", 100),
        ]
        self.table = Table(self, columns)
        self.table.add_rows(example_calendars)
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
