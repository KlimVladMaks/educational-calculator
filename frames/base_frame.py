import tkinter as tk


class BaseFrame(tk.Frame):
    """
    Базовый фрейм для наследования.
    Предоставляет базовый функционал фрейма.
    Все остальные фреймы должны наследоваться от него.
    """
    def __init__(self, master: tk.Tk) -> None:
        """
        Аргументы:
            master: Окно приложения.
        """
        super().__init__(master)
        self.master = master
    
    def display_frame(self) -> None:
        """
        Отображает фрейм в окне приложения
        (при этом все остальные фреймы автоматически скрываются).
        """
        for widget in self.master.winfo_children():
            widget.pack_forget()
        self.pack(fill="both", expand=True)
