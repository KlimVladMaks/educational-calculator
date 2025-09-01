import tkinter as tk
from tkinter import ttk
import typing as tp


class BackButton:
    """
    Кнопка "Назад". При нажатии возвращает на предыдущий фрейм.
    Имеет абсолютное позиционирование.
    """
    def __init__(self, master: tk.Tk, command: tp.Callable):
        """
        Аргументы:
            master: Окно приложения.
            command: Функция фрейма, закрывающая текущий фрейм и открывающая предыдущий.
        """
        self.master = master
        self.back_button = ttk.Button(self.master, text="Назад", command=command)
    
    def destroy(self):
        """
        Уничтожает кнопку.
        """
        self.back_button.destroy()
    
    def place(self):
        """
        Располагает кнопку на окне приложения
        (используется абсолютное позиционирование).
        """
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)