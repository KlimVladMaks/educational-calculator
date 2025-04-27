import tkinter as tk
from datetime import datetime


class DatesText:
    
    def __init__(self, frame, width, height):
        self.frame = frame
        self.text = tk.Text(self.frame, width=width, height=height)
    
    def pack(self, pady):
        self.text.pack(pady=pady)
    
    def get_dates_list(self):
        dates_text = self.text.get("1.0", tk.END)
        dates_list_dd_mm_yyyy = [line.strip() for line in dates_text.splitlines() if line.strip()]
        dates_list_yyyy_mm_dd = []
        for date in dates_list_dd_mm_yyyy:
            date_obj = datetime.strptime(date, "%d.%m.%Y")
            dates_list_yyyy_mm_dd.append(date_obj.strftime("%Y-%m-%d"))
        return dates_list_yyyy_mm_dd

    def insert(self, dates_list_yyyy_mm_dd):
        dates_list_dd_mm_yyyy = []
        for date in dates_list_yyyy_mm_dd:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            dates_list_dd_mm_yyyy.append(date_obj.strftime("%d.%m.%Y"))
        self.text.insert("1.0", "\n".join(dates_list_dd_mm_yyyy))
    
    def delete(self):
        self.text.delete("1.0", tk.END)




