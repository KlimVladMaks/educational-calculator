from tkinter import ttk
from datetime import datetime


class DateEntry:

    def __init__(self, frame):
        self.frame = frame
        self.entry = ttk.Entry(self.frame)
    
    def grid(self, row, column, padx):
        self.entry.grid(row=row, column=column, padx=padx)
    
    def pack(self, pady):
        self.entry.pack(pady=pady)
    
    def get(self):
        date_str = self.entry.get()
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        return date_obj.strftime("%Y-%m-%d")

    def insert(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        self.entry.insert(0, date_obj.strftime("%d.%m.%Y"))
    
    def bind(self, sequence, func) -> str:
        self.entry.bind(sequence, func)



