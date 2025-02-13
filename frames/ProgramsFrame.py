import tkinter as tk
from frames.BaseFrame import BaseFrame


class ProgramsFrame(BaseFrame):
    """
    Фрейм для работы с учебными программами.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Учебные программы", font=("Arial", 24)).pack(expand=True)
        tk.Button(self, text="Назад", command=self.go_back).pack(pady=10)

    def go_back(self):
        self.pack_forget()
        self.parent_frame.display_frame()
