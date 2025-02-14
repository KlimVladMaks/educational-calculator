import tkinter as tk
from tkinter import ttk


class Table:
    """
    Класс для создания таблицы.
    """
    def __init__(self, frame, columns):
        self.frame = frame
        self.columns = columns

        self.sort_order = True
        self.current_sort_column = None

        self.column_names = []
        for column in self.columns:
            self.column_names.append(column[0])
        
        self.column_widths = []
        for column in self.columns:
            self.column_widths.append(columns[1])
        
        self.tree = ttk.Treeview(frame, columns=self.column_names, show="headings")

        for name in self.column_names:
            self.tree.heading(name, text=name, command=lambda name=name: self.sort_column(name))
        for column in self.columns:
            self.tree.column(column[0], width=column[1])

    def add_rows(self, rows):
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def pack(self):
        self.tree.pack(pady=10)

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
