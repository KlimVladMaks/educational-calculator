from tkinter import ttk
from frames.base_frame import BaseFrame
from database.database import Database
from widgets.back_button import BackButton
from widgets.table import Table
from widgets.input_widget import InputWidget


class EduTypesFrame(BaseFrame):

    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.place()

        ttk.Label(self, text="Виды обучения").pack(pady=5)
        self.create_table()

        self.add_button = ttk.Button(self, text="Добавить вид обучения", command=self.open_add_widget)
        self.add_button.pack(pady=5)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def create_table(self):
        columns = [
            ("Вид обучения", 300)
        ]
        self.table = Table(self, columns, 11)
        table_rows = self.get_table_rows()
        self.table.add_rows(table_rows)
        self.table.add_menu_command(label="Изменить", command=self.open_edit_widget)
        self.table.add_menu_command(label="Удалить", command=self.delete_edu_type)
        self.table.pack(pady=5)
    
    def update_table(self):
        new_table_rows = self.get_table_rows()
        self.table.update_rows(new_table_rows)
    
    def get_table_rows(self):
        table_rows = []
        for edu_type in self.db.edu_types.get_all_edu_types():
            table_rows.append([edu_type])
        return table_rows
    
    def open_add_widget(self):
        self.add_button.pack_forget()
        self.add_widget = InputWidget(self, label="Добавить вид обучения", do_button_name="Добавить", 
                                      do_func=self.add_edu_type, cancel_button_name="Отменить",
                                      cancel_func=self.cancel_add)
        self.add_widget.pack(pady=5)
        self.table.lock()
        self.table.remove_selections()
    
    def open_edit_widget(self):
        self.add_button.pack_forget()
        selected_edu_type_data = self.table.get_selected_row()
        self.editable_edu_type = selected_edu_type_data[0]
        self.edit_widget = InputWidget(self, label="Изменить вид обучения", do_button_name="Сохранить", 
                                      do_func=self.edit_edu_type, cancel_button_name="Отменить",
                                      cancel_func=self.cancel_edit, init_entry_value=self.editable_edu_type)
        self.edit_widget.pack(pady=5)
        self.table.lock()
    
    def delete_edu_type(self):
        selected_edu_type_data = self.table.get_selected_row()
        self.db.edu_types.delete_edu_type(selected_edu_type_data[0])
        self.table.delete_selected()
    
    def add_edu_type(self):
        new_edu_type = self.add_widget.entry.get()
        self.db.edu_types.add_new_edu_type(new_edu_type)
        self.update_table()
        self.table.unlock()
        self.add_widget.destroy()
        self.add_button.pack(pady=5)
    
    def edit_edu_type(self):
        updated_edu_type = self.edit_widget.entry.get()
        if updated_edu_type != self.editable_edu_type:
            self.db.edu_types.update_edu_type(self.editable_edu_type, updated_edu_type)
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






