from tkinter import ttk
from frames.base_frame import BaseFrame
from database.database import Database
from widgets.back_button import BackButton
from widgets.table import Table
from widgets.input_widget import InputWidget


class StagesFrame(BaseFrame):

    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.place()

        ttk.Label(self, text="Этапы обучения").pack(pady=5)
        self.create_table()

        self.add_button = ttk.Button(self, text="Добавить этап обучения", command=self.open_add_widget)
        self.add_button.pack(pady=5)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()

    def create_table(self):
        columns = [
            ("Этап обучения", 300)
        ]
        self.table = Table(self, columns, 11)
        table_rows = self.get_table_rows()
        self.table.add_rows(table_rows)
        self.table.add_menu_command(label="Изменить", command=self.open_edit_widget)
        self.table.add_menu_command(label="Удалить", command=self.delete_stage)
        self.table.pack(pady=5)
    
    def update_table(self):
        new_table_rows = self.get_table_rows()
        self.table.update_rows(new_table_rows)
    
    def get_table_rows(self):
        table_rows = []
        for stage in self.db.edu_stages.get_all_stages():
            table_rows.append([stage])
        return table_rows
    
    def open_add_widget(self):
        self.add_button.pack_forget()
        self.add_widget = InputWidget(self, label="Добавить этап обучения", do_button_name="Добавить", 
                                      do_func=self.add_stage, cancel_button_name="Отменить",
                                      cancel_func=self.cancel_add)
        self.add_widget.pack(pady=5)
        self.table.lock()
        self.table.remove_selections()
    
    def open_edit_widget(self):
        self.add_button.pack_forget()
        selected_stage_data = self.table.get_selected_row()
        self.editable_stage = selected_stage_data[0]
        self.edit_widget = InputWidget(self, label="Изменить этап обучения", do_button_name="Сохранить", 
                                      do_func=self.edit_stage, cancel_button_name="Отменить",
                                      cancel_func=self.cancel_edit, init_entry_value=self.editable_stage)
        self.edit_widget.pack(pady=5)
        self.table.lock()

    def delete_stage(self):
        selected_stage_data = self.table.get_selected_row()
        self.db.edu_stages.delete_stage(selected_stage_data[0])
        self.table.delete_selected()

    def add_stage(self):
        new_stage = self.add_widget.entry.get()
        self.db.edu_stages.add_new_stage(new_stage)
        self.update_table()
        self.table.unlock()
        self.add_widget.destroy()
        self.add_button.pack(pady=5)
    
    def edit_stage(self):
        updated_stage = self.edit_widget.entry.get()
        if updated_stage != self.editable_stage:
            self.db.edu_stages.update_stage(self.editable_stage, updated_stage)
            self.update_table()
        self.table.unlock()
        self.edit_widget.destroy()
        self.add_button.pack(pady=5)
    
    def cancel_add(self):
        self.add_widget.destroy()
        self.add_button.pack(pady=5)
        self.table.unlock()
    
    def cancel_edit(self):
        self.edit_widget.destroy()
        self.add_button.pack(pady=5)
        self.table.unlock()





