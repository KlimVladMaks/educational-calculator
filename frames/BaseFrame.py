import tkinter as tk


class BaseFrame(tk.Frame):
    """
    Базовый фрейм для наследования.
    При отображении скрывает все остальные фреймы.
    """
    def __init__(self, master):
        super().__init__(master)
        self.master = master
    
    def display_frame(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        self.pack()
