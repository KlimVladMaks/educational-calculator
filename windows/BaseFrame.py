import tkinter as tk


class BaseFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
