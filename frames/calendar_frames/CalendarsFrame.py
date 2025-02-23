import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
from frames.BaseFrame import BaseFrame
from frames.calendar_frames.AddCalendarFrame import AddCalendarFrame
from widgets.Table import Table
from database.Database import Database
from widgets.Calculator import Calculator


class CalendarsFrame(BaseFrame):
    """
    Фрейм для работы с производственными календарями.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = ttk.Button(self.master, text="Назад", command=self.go_back)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)

        ttk.Label(self, text="Производственные календари").pack(pady=10)
        self.create_table()

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(pady=10)
        ttk.Button(self.buttons_frame,
                   text="Добавить календарь",
                   command=self.open_add_calendar).grid(row=0, column=0, padx=10)
        ttk.Button(self.buttons_frame,
                   text="Загрузить календарь",
                   command=self.download_calendar).grid(row=0, column=1, padx=10)
    
    def create_table(self):
        columns = [
            ("Название", 150),
            ("Начало", 100),
            ("Конец", 100),
            ("Рабочие дни", 100),
            ("Выходные дни", 100),
            ("Всего дней", 100),
        ]
        self.table = Table(self, columns)
        self.table_data = self.get_table_data()
        self.table.add_rows(self.table_data)
        self.table.pack()

        self.create_context_menu()
    
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
            item_data = self.table.tree.item(item)
            values = item_data['values']
            self.db.calendars.delete(values[0])
            self.table.tree.delete(item)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def get_table_data(self):
        table_data = []
        calendars_data = self.db.calendars.get_all()
        for data in calendars_data:
            table_data.append(data)
        for data in table_data:
            total_days = Calculator.count_days(data[1], data[2])
            days_off = len(data[3])
            working_days = total_days - days_off
            data.pop()
            data.append(working_days)
            data.append(days_off)
            data.append(total_days)
        return table_data

    def update(self):
        new_table_data = self.get_table_data()
        self.table.update(new_table_data)
    
    def download_calendar(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                new_calendar_data = [data["name"], data["start_date"], data["end_date"], data["days_off_list"]]
                self.db.calendars.add(new_calendar_data)
                self.update_table()
    
    def update_table(self):
        new_table_data = self.get_table_data()
        self.table.update(new_table_data)
    
    def open_add_calendar(self):
        self.add_calendar_frame = AddCalendarFrame(self.master, self)
        self.add_calendar_frame.display_frame()
