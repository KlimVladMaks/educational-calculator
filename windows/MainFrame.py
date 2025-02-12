import tkinter as tk
from windows.BaseFrame import BaseFrame
from windows.CalendarsFrame import CalendarsFrame
from windows.ProgramsFrame import ProgramsFrame
from windows.GroupsFrame import GroupsFrame
from windows.UploadingFrame import UploadingFrame


class MainFrame(BaseFrame):
    """
    Фрейм с главным меню.
    """
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Образовательный калькулятор")
        self.create_frame()

    def create_frame(self):
        self.pack(expand=True)
        button_width = 60
        button_height = 2
        padding_y = 5
        self.master.minsize(width=600, height=400)

        tk.Button(self,
                text="Производственные календари",
                command=self.open_calendars,
                width=button_width,
                height=button_height).pack(pady=padding_y)

        tk.Button(self,
                text="Учебные программы",
                command=self.open_programs,
                width=button_width,
                height=button_height).pack(pady=padding_y)

        tk.Button(self,
                text="Учебные группы",
                command=self.open_groups,
                width=button_width,
                height=button_height).pack(pady=padding_y)

        tk.Button(self,
                text="Выгрузить в Word",
                command=self.open_uploading,
                width=button_width,
                height=button_height).pack(pady=padding_y)

    def display_frame(self):
        self.pack(expand=True)

    def open_calendars(self):
        self.pack_forget()
        CalendarsFrame(self.master, self).pack()
    
    def open_programs(self):
        self.pack_forget()
        ProgramsFrame(self.master, self).pack()
    
    def open_groups(self):
        self.pack_forget()
        GroupsFrame(self.master, self).pack()
    
    def open_uploading(self):
        self.pack_forget()
        UploadingFrame(self.master, self).pack()
