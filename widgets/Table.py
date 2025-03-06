import tkinter as tk
from tkinter import ttk


class Table:
    """
    Таблица.
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
            self.column_widths.append(column[1])
        
        self.table_frame = ttk.Frame(self.frame)
        self.table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.table_frame, columns=self.column_names, show="headings")

        for name in self.column_names:
            self.tree.heading(name, text=name, command=lambda name=name: self.sort_column(name))
        for column in self.columns:
            self.tree.column(column[0], width=column[1], stretch=False)
        
        self.scroll_x = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scroll_x.set)

        self.scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll_y.set)

        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<Button-1>", self.on_treeview_click)

    def add_rows(self, rows):
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def pack(self):
        self.tree.pack(pady=10)

    def update(self, new_rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.add_rows(new_rows)

    def sort_column(self, col):
        if self.current_sort_column == col:
            self.sort_order = not self.sort_order
        else:
            self.sort_order = True
            self.current_sort_column = col

        data = [(self.tree.item(item)["values"], item)
                for item in self.tree.get_children()]

        is_numeric = all(
            isinstance(x[0][self.tree["columns"].index(col)], (int, float))
            for x in data if x[0][self.tree["columns"].index(col)] != ''
        )

        if is_numeric:
            data.sort(key=lambda x: float(
                x[0][self.tree["columns"].index(col)]), reverse=not self.sort_order)
        else:
            data.sort(key=lambda x: str(
                x[0][self.tree["columns"].index(col)]), reverse=not self.sort_order)

        self.tree.delete(*self.tree.get_children())
        for values, item in data:
            self.tree.insert("", tk.END, iid=item, values=values)

        self.update_sorting_arrows()

    def update_sorting_arrows(self):
        for col in self.tree["columns"]:
            current_title = self.tree.heading(col)["text"].strip("↑↓ ")
            if col == self.current_sort_column:
                arrow = "↑ " if self.sort_order else "↓ "
                self.tree.heading(col, text=arrow + current_title)
            else:
                self.tree.heading(col, text=current_title)

    def on_treeview_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "nothing":
            self.tree.selection_remove(self.tree.selection())

    def destroy(self):
        self.table_frame.destroy()
