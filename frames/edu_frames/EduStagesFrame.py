import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from frames.edu_frames.InputWidget import InputWidget
from database.Database import Database
from widgets.BackButton import BackButton
from widgets.Table import Table


class EduStagesFrame(BaseFrame):
    """
    Фрейм для работы с этапами обучения.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.pack()
    
        ttk.Label(self, text="Этапы обучения").pack(pady=5)
        self.create_table()

        self.add_button = ttk.Button(self, text="Добавить этап обучения", command=self.open_add_widget)
        self.add_button.pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def create_table(self):
        columns = [
            ("Этап обучения", 300)
        ]
        self.table = Table(self, columns)
        table_rows = self.get_table_rows()
        self.table.add_rows(table_rows)
        self.table.pack()
        self.create_context_menu()
    
    def get_table_rows(self):
        table_rows = []
        for edu_stage in self.db.edu_stages.get_all():
            table_rows.append([edu_stage])
        return table_rows
    
    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Изменить", command=self.open_edit_widget)
        self.menu.add_command(label="Удалить", command=self.delete_selected)
        self.table.tree.bind("<Button-3>", self.show_context_menu)
    
    def delete_selected(self):
        selected_items = self.table.tree.selection()
        item = selected_items[0]
        item_data = self.table.tree.item(item)
        values = item_data['values']
        self.db.edu_stages.delete(str(values[0]))
        self.table.tree.delete(item)
    
    def open_edit_widget(self):
        selected_items = self.table.tree.selection()
        item = selected_items[0]
        item_data = self.table.tree.item(item)
        values = item_data['values']
        edu_stage_name = str(values[0])
        self.editable_stage = edu_stage_name
        self.edit_widget = InputWidget(self, "Название", "Сохранить", 
                                       self.edit_edu_stage, self.cancel_edit, edu_stage_name)
        self.add_button.pack_forget()
        self.edit_widget.pack()
        self.lock_table()
    
    def show_context_menu(self, event):
        row_id = self.table.tree.identify_row(event.y)
        if row_id:
            self.table.tree.selection_set(row_id)
            self.menu.post(event.x_root, event.y_root)
    
    def open_add_widget(self):
        self.add_button.pack_forget()
        self.add_widget = InputWidget(self, "Название:", "Добавить", self.add_edu_stage, self.cancel_add)
        self.add_widget.pack()
        self.lock_table()
        selected_items = self.table.tree.selection()
        for item in selected_items:
            self.table.tree.selection_remove(item)

    def add_edu_stage(self):
        new_edu_stage = self.add_widget.entry.get()
        self.db.edu_stages.add(new_edu_stage)
        self.update_table()
        self.add_widget.destroy()
        self.add_button.pack(pady=5)
    
    def update_table(self):
        new_table_rows = self.get_table_rows()
        self.table.update(new_table_rows)
        self.unlock_table()
    
    def cancel_add(self):
        self.add_widget.destroy()
        self.add_button.pack(pady=5)
        self.unlock_table()
    
    def edit_edu_stage(self):
        edited_stage = self.edit_widget.entry.get()
        self.db.edu_stages.update(self.editable_stage, edited_stage)
        self.update_table()
        self.edit_widget.destroy()
        self.add_button.pack(pady=5)
        self.unlock_table()
    
    def cancel_edit(self):
        self.edit_widget.destroy()
        self.add_button.pack(pady=5)
        self.unlock_table()
    
    def lock_table(self):
        self.table.tree.bind("<Button-1>", lambda e: "break")
        self.table.tree.bind("<Button-3>", lambda e: "break")
        self.table.tree.bind("<Double-1>", lambda e: "break")
    
    def unlock_table(self):
        self.table.tree.unbind("<Button-1>")
        self.table.tree.bind("<Button-3>", self.show_context_menu)
        self.table.tree.unbind("<Double-1>")
