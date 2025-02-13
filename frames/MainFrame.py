import tkinter as tk
from frames.BaseFrame import BaseFrame
from frames.CalendarsFrame import CalendarsFrame
from frames.ProgramsFrame import ProgramsFrame
from frames.GroupsFrame import GroupsFrame
from frames.UploadingFrame import UploadingFrame


class MainFrame(BaseFrame):
    """
    Фрейм с главным меню.
    """
    def __init__(self, master):
        super().__init__(master)
        self.create_frame()
    
    def create_frame(self):
        button_width = 60
        button_height = 2
        padding_between_buttons = 8

        tk.Button(self,
                  text="Производственные календари",
                  command=self.open_calendars,
                  width=button_width,
                  height=button_height).pack(pady=padding_between_buttons)

        tk.Button(self,
                  text="Учебные программы",
                  command=self.open_programs,
                  width=button_width,
                  height=button_height).pack(pady=padding_between_buttons)
        
        tk.Button(self,
                  text="Учебные группы",
                  command=self.open_groups,
                  width=button_width,
                  height=button_height).pack(pady=padding_between_buttons)
        
        tk.Button(self,
                  text="Выгрузить в Word",
                  command=self.open_uploading,
                  width=button_width,
                  height=button_height).pack(pady=padding_between_buttons)
    
    def display_frame(self):
        super().display_frame()
        self.master.minsize(width=700, height=400)

    def open_calendars(self):
        calendars_frame = CalendarsFrame(self.master, self)
        calendars_frame.display_frame()
    
    def open_programs(self):
        programs_frame = ProgramsFrame(self.master, self)
        programs_frame.display_frame()
    
    def open_groups(self):
        groups_frame = GroupsFrame(self.master, self)
        groups_frame.display_frame()
    
    def open_uploading(self):
        uploading_frame = UploadingFrame(self.master, self)
        uploading_frame.display_frame()
