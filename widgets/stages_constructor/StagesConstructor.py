import tkinter as tk
from tkinter import ttk
from widgets.stages_constructor.StageInput import StageInput
from database.Database import Database


class StagesConstructor:
    """
    Конструктор этапов учебной программы.
    """
    def __init__(self, main_frame, canvas, init_program_name=None):
        self.main_frame = main_frame
        self.canvas = canvas
        self.db = Database()
        self.sc_frame = ttk.Frame(main_frame)
        self.stages_list = []
        self.add_stage_button = ttk.Button()
        self.add_new_stage()

        if init_program_name is not None:
            self.set_init_values(init_program_name)
    
    def pack(self):
        self.sc_frame.pack(pady=10)
    
    def add_new_stage(self):
        self.add_stage_button.destroy()

        index = len(self.stages_list)
        new_stage = StageInput(self.sc_frame,
                               index, self.move_stage_up,
                               self.move_stage_down,
                               self.delete_stage,
                               self.on_mouse_wheel)
        new_stage.pack()
        self.stages_list.append(new_stage)

        self.add_stage_button = ttk.Button(self.sc_frame,
                                           text="+ Добавить этап",
                                           command=self.add_new_stage)
        self.add_stage_button.pack(pady=(10, 0))

        self.sc_frame.update_idletasks()
        self.canvas.yview_moveto(1)
    
    def delete_stage(self, index):
        self.stages_list.pop(index)
        new_index = 0
        for stage in self.stages_list:
            stage.update_index(new_index)
            new_index += 1
        if len(self.stages_list) == 0:
            self.add_new_stage()
    
    def move_stage_up(self, index):
        if index == 0:
            return
        
        stage = self.stages_list[index]
        name = str(stage.name_combobox.get())
        days = str(stage.days_entry.get())

        upper_stage = self.stages_list[index - 1]
        u_name = str(upper_stage.name_combobox.get())
        u_days = str(upper_stage.days_entry.get())

        upper_stage.name_combobox.set(name)
        upper_stage.days_entry.delete(0, tk.END)
        upper_stage.days_entry.insert(0, days)

        stage.name_combobox.set(u_name)
        stage.days_entry.delete(0, tk.END)
        stage.days_entry.insert(0, u_days)
    
    def move_stage_down(self, index):
        if index == (len(self.stages_list) - 1):
            return

        stage = self.stages_list[index]
        name = str(stage.name_combobox.get())
        days = str(stage.days_entry.get())

        lower_stage = self.stages_list[index + 1]
        l_name = str(lower_stage.name_combobox.get())
        l_days = str(lower_stage.days_entry.get())

        lower_stage.name_combobox.set(name)
        lower_stage.days_entry.delete(0, tk.END)
        lower_stage.days_entry.insert(0, days)

        stage.name_combobox.set(l_name)
        stage.days_entry.delete(0, tk.END)
        stage.days_entry.insert(0, l_days)
    
    def get_stages(self):
        stages_data = []
        for stage in self.stages_list:
            stage_data = []
            stage_data.append(stage.name_combobox.get())
            stage_data.append(int(stage.days_entry.get()))
            stages_data.append(stage_data)
        return stages_data

    def set_init_values(self, init_program_name):
        self.stages_list[0].input_frame.destroy()
        self.stages_list.pop()
        stages = self.db.programs.get_stages_list(init_program_name)
        for stage in stages:
            self.add_new_stage()
            self.stages_list[-1].name_combobox.set(stage[0])
            self.stages_list[-1].days_entry.insert(0, str(stage[1]))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"


