import tkinter as tk
from tkinter import ttk
from database.Database import Database


class StageInput:
    """
    Поле ввода одного этапа учебной программы.
    (Используется в конструкторе этапов учебной программы).
    """
    def __init__(self, sc_frame, index, move_up_func, move_down_func, delete_func):
        self.sc_frame = sc_frame
        self.index = index
        self.move_up_func = move_up_func
        self.move_down_func = move_down_func
        self.delete_func = delete_func
        self.input_frame = ttk.Frame(self.sc_frame)
        self.db = Database()

        self.index_label = ttk.Label(self.input_frame, text=f"{str(self.index + 1)})")
        self.index_label.grid(row=0, column=0, padx=5)

        self.input_name_frame = ttk.Frame(self.input_frame)
        self.input_name_frame.grid(row=0, column=1, padx=5)
        ttk.Label(self.input_name_frame, text="Название этапа:").pack()
        self.names_list = self.db.edu_stages.get_all()
        self.name_combobox = ttk.Combobox(self.input_name_frame, values=self.names_list, state="readonly")
        self.name_combobox.pack()

        self.input_days_frame = ttk.Frame(self.input_frame)
        self.input_days_frame.grid(row=0, column=2, padx=5)
        ttk.Label(self.input_days_frame, text="Число дней:").pack()
        self.days_entry = ttk.Entry(self.input_days_frame)
        self.days_entry.pack()
        
        ttk.Button(self.input_frame, text="↑", width=3, command=self.move_up).grid(row=0, column=3, padx=5)
        ttk.Button(self.input_frame, text="↓", width=3, command=self.move_down).grid(row=0, column=4, padx=5)
        ttk.Button(self.input_frame, text="-", width=3, command=self.delete).grid(row=0, column=5, padx=5)
    
    def pack(self):
        self.input_frame.pack(pady=5)
    
    def delete(self):
        self.delete_func(self.index)
        self.input_frame.destroy()
    
    def update_index(self, new_index):
        self.index = new_index
        self.index_label["text"] = f"{str(self.index + 1)})"
    
    def move_up(self):
        self.move_up_func(self.index)
    
    def move_down(self):
        self.move_down_func(self.index)
