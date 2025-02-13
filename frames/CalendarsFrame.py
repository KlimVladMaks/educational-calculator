import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame


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
        tk.Label(self, text="Производственные календари").pack(pady=10)
        tk.Button(self, text="Назад", command=self.go_back).pack(pady=10)
        self.create_table()
        self.create_context_menu()
        tk.Button(self, text="Добавить производственный календарь").pack(pady=10)
    
    def create_table(self):
        self.sort_order = True
        self.current_sort_column = None

        columns = ("name", "start_date", "end_date", "total_days", "working_days", "days_off")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(pady=10)

        self.tree.heading("name", text="Название", command=lambda: self.sort_column("name"))
        self.tree.heading("start_date", text="Начало", command=lambda: self.sort_column("start_date"))
        self.tree.heading("end_date", text="Конец", command=lambda: self.sort_column("end_date"))
        self.tree.heading("total_days", text="Всего дней", command=lambda: self.sort_column("total_days"))
        self.tree.heading("working_days", text="Рабочие дни", command=lambda: self.sort_column("working_days"))
        self.tree.heading("days_off", text="Выходные дни", command=lambda: self.sort_column("days_off"))

        self.tree.column("name", width=150)
        self.tree.column("start_date", width=100)
        self.tree.column("end_date", width=100)
        self.tree.column("total_days", width=100)
        self.tree.column("working_days", width=100)
        self.tree.column("days_off", width=100)

        # Используем данные для примера
        for calendar in example_calendars:
            self.tree.insert("", tk.END, values=calendar)

    def sort_column(self, col):
        if self.current_sort_column == col:
            self.sort_order = not self.sort_order
        else:
            self.sort_order = True
            self.current_sort_column = col
        
        data = [(self.tree.item(item)["values"], item) for item in self.tree.get_children()]
        data.sort(key=lambda x: x[0][self.tree["columns"].index(col)], reverse=not self.sort_order)

        self.tree.delete(*self.tree.get_children())
        for values, item in data:
            self.tree.insert("", tk.END, iid=item, values=values)
        
        self.update_sorting_arrows()
    
    def update_sorting_arrows(self):
        for col in self.tree["columns"]:
            current_title = self.tree.heading(col)["text"].rstrip(" ↑↓")
            if col == self.current_sort_column:
                arrow = " ↑" if self.sort_order else " ↓"
                self.tree.heading(col, text=current_title + arrow)
            else:
                self.tree.heading(col, text=current_title)

    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Удалить", command=self.delete_selected)
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            self.menu.post(event.x_root, event.y_root)

    def delete_selected(self):
        selected_item = self.tree.selection()
        for item in selected_item:
            self.tree.delete(item)

    def display_frame(self):
        super().display_frame()
        self.master.minsize(width=700, height=400)

    def go_back(self):
        self.destroy()
        self.parent_frame.display_frame()
