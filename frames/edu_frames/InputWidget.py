import tkinter as tk
from tkinter import ttk


class InputWidget():
    """
    Виджет для ввода данных.
    """
    def __init__(self, parent_frame, entry_label, do_button_name, do_func, cancel_func, init_entry=""):
        self.frame = ttk.Frame(parent_frame)
        ttk.Label(self.frame, text=entry_label).pack()
        self.entry = ttk.Entry(self.frame, width=40)
        self.entry.pack(pady=(0, 5))
        self.entry.insert(0, init_entry)
        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.pack(pady=(5, 0))
        ttk.Button(self.buttons_frame, text=do_button_name, command=do_func).grid(row=0, column=0, padx=5)
        ttk.Button(self.buttons_frame, text="Отмена", command=cancel_func).grid(row=0, column=1, padx=5)
    
    def pack(self):
        self.frame.pack(pady=5)
    
    def destroy(self):
        self.frame.destroy()
