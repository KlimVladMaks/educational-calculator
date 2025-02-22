import tkinter as tk
from tkinter import ttk
import json
from frames.BaseFrame import BaseFrame
from frames.AddGroupFrame import AddGroupFrame
from widgets.Table import Table
from database.Database import Database
from widgets.Calculator import Calculator
from calendar_app.calendar_project import CalendarApp


class GroupsFrame(BaseFrame):
    """
    Фрейм для работы с учебными группами.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = ttk.Button(self.master, text="Назад", command=self.go_back)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)

        ttk.Label(self, text="Учебные группы").pack(pady=10)
        self.create_table()
        ttk.Button(self, text="Добавить учебную группу", command=self.open_add_groups).pack(pady=10)
    
    def create_table(self):
        self.create_comboboxes()

        columns = [
            ("Название", 150),
            ("Календарь", 100),
            ("Программа", 100),
            ("Дата начала", 100),
            ("Дата окончания", 100),
            ("Дней обучения", 100)
        ]
        self.table = Table(self, columns)
        self.table_data = self.get_table_data()
        self.table.add_rows(self.table_data)
        self.table.pack()

        self.create_context_menu()
    
    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Календарь", command=self.open_calendar_app)
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
            self.db.groups.delete(str(values[0]), str(values[1]), str(values[2]))
            self.table.tree.delete(item)
    
    def get_table_data(self):
        table_data = []
        groups_data = self.db.groups.get_all()
        for data in groups_data:
            table_data.append(data)
        for data in table_data:
            end_date = Calculator.calculate_end_date(data[1], data[2], data[3])
            data.append(end_date)
            number_of_days = Calculator.count_days(data[3], data[4])
            data.append(number_of_days)
        return table_data

    def create_comboboxes(self):
        self.comboboxes_frame = ttk.Frame(self)
        self.comboboxes_frame.pack(pady=10)

        calendars_names = self.get_calendars_names()
        programs_names = self.get_programs_names()
        calendars_names.insert(0, "Все календари")
        programs_names.insert(0, "Все программы")

        self.calendar_combobox = ttk.Combobox(self.comboboxes_frame, values=calendars_names, state="readonly")
        self.calendar_combobox.grid(row=0, column=0, padx=10)
        self.calendar_combobox.set(calendars_names[0])
        self.calendar_combobox.bind("<<ComboboxSelected>>", self.filter_table)

        self.program_combobox = ttk.Combobox(self.comboboxes_frame, values=programs_names, state="readonly")
        self.program_combobox.grid(row=0, column=1, padx=10)
        self.program_combobox.set(programs_names[0])
        self.program_combobox.bind("<<ComboboxSelected>>", self.filter_table)
    
    def get_calendars_names(self, program_name=None):
        calendars_names = []
        groups_data = self.db.groups.get_all()
        for data in groups_data:
            if ((program_name is None) or \
                (program_name == "Все программы") or \
                (program_name == data[2])) and (data[1] not in calendars_names):
                calendars_names.append(data[1])
        return calendars_names

    def get_programs_names(self, calendar_name=None):
        programs_names = []
        groups_data = self.db.groups.get_all()
        for data in groups_data:
            if ((calendar_name is None) or \
                (calendar_name == "Все календари") or \
                (calendar_name == data[1])) and (data[2] not in programs_names):
                programs_names.append(data[2])
        return programs_names

    def filter_table(self, event=None):
        selected_calendar = self.calendar_combobox.get()
        selected_program = self.program_combobox.get()
        table_data = []
        all_table_data = self.get_table_data()
        for data in all_table_data:
            if ((selected_calendar == "Все календари") or (data[1] == selected_calendar)) and \
               ((selected_program == "Все программы") or (data[2] == selected_program)):
                table_data.append(data)
        self.table.update(table_data)
        self.update_comboboxes()
    
    def update_comboboxes(self):
        selected_calendar = self.calendar_combobox.get()
        selected_program = self.program_combobox.get()

        calendars_names = self.get_calendars_names(selected_program)
        programs_names = self.get_programs_names(selected_calendar)

        calendars_names.insert(0, "Все календари")
        programs_names.insert(0, "Все программы")

        self.calendar_combobox["values"] = calendars_names
        self.program_combobox["values"] = programs_names

        self.calendar_combobox.set(selected_calendar)
        self.program_combobox.set(selected_program)
    
    def go_back(self):
        self.back_button.destroy()
        self.pack_forget()
        self.parent_frame.display_frame()
    
    def update(self):
        new_table_data = self.get_table_data()
        self.table.update(new_table_data)
        self.calendar_combobox.set("Все календари")
        self.program_combobox.set("Все программы")
        self.update_comboboxes()
    
    def open_add_groups(self):
        self.add_group_frame = AddGroupFrame(self.master, self)
        self.add_group_frame.display_frame()
    
    def open_calendar_app(self):
        selected_items = self.table.tree.selection()
        item = selected_items[0]
        item_data = self.table.tree.item(item)
        group_data = item_data['values']
        self.prepare_files_for_calendar_app(group_data)
        new_window = tk.Toplevel(self.master)
        new_window.grab_set()
        CalendarApp(new_window)
    
    def prepare_files_for_calendar_app(self, group_data):
        days_off = []
        filename = "database.json"
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            calendars = data.get('calendars', [])
            for calendar in calendars:
                if calendar["name"] == group_data[1]:
                    days_off = calendar["days_off_list"]
                    break
        filename = ".\calendar_app\days_off.json"
        with open(filename, 'w+', encoding='utf-8') as file:
            data = {
                "Праздник": [],
                "Выходной": days_off
            }
            json.dump(data, file, ensure_ascii=False, indent=4)
        end_date = Calculator.calculate_end_date(group_data[1], group_data[2], group_data[3])
        filename = ".\calendar_app\study_periods.json"
        with open(filename, 'w+', encoding='utf-8') as file:
            data = [
                {"start_date": group_data[3],
                 "end_date": end_date,
                 "type": "theory"}
            ]
            json.dump(data, file, ensure_ascii=False, indent=4)
