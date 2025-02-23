import tkinter as tk
from tkinter import ttk


class BackButton():
    """
    Кнопка "Назад" для возвращения к предыдущему фрейму.
    Размещается на главном окне (master) и требует отдельного удаления даже при закрытии фрейма.
    """
    def __init__(self, master, command):
        self.master = master
        self.back_button = ttk.Button(self.master, text="Назад", command=command)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)
    
    def destroy(self):
        self.back_button.destroy()
