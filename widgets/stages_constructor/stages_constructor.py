import tkinter as tk
from tkinter import ttk
from database.database import Database
from widgets.stages_constructor.stage_input import StageInput


class StagesConstructor:
    
    def __init__(self, main_frame, scroll_func, update_label_func, init_program_name=None):
        self.main_frame = main_frame
        self.scroll_func = scroll_func
        self.update_label_func = update_label_func
        self.frame = ttk.Frame(main_frame)
        self.db = Database()
        self.stages_list: list[StageInput] = []
        self.add_stage_button = ttk.Button()
        if init_program_name is None:
            self.add_new_stage(is_init=True)
        else:
            self.set_init_values(init_program_name)

    def pack(self, pady):
        self.frame.pack(pady=pady)
    
    def add_new_stage(self, is_init=False):
        self.add_stage_button.destroy()

        index = len(self.stages_list)
        new_stage = StageInput(self.frame, index,
                               self.scroll_func, self.delete_stage,
                               self.move_stage_up, self.move_stage_down,
                               self.update_label_func)
        new_stage.pack(pady=5)
        self.stages_list.append(new_stage)

        self.add_stage_button = ttk.Button(self.frame, text="+ Добавить этап", command=self.add_new_stage)
        self.add_stage_button.pack(pady=(10, 0))

        self.main_frame.update_idletasks()
        self.main_frame.master.yview_moveto(1)

        if not is_init:
            self.update_label_func()

    def delete_stage(self, index: int):
        self.stages_list.pop(index)
        new_index = 0
        for stage in self.stages_list:
            stage.update_index(new_index)
            new_index += 1
        if len(self.stages_list) == 0:
            self.add_new_stage()
        self.update_label_func()
    
    def move_stage_up(self, index: int):
        if index == 0:
            return
        else:
            self.swap_two_stages(index, index - 1)
    
    def move_stage_down(self, index: int):
        if index == (len(self.stages_list) - 1):
            return
        else:
            self.swap_two_stages(index, index + 1)

    def swap_two_stages(self, index_1: int, index_2: int):
        stage_1 = self.stages_list[index_1]
        stage_2 = self.stages_list[index_2]
        data_1 = [stage_1.stage_combobox.get(), stage_1.days_entry.get()]
        data_2 = [stage_2.stage_combobox.get(), stage_2.days_entry.get()]

        stage_1.stage_combobox.set(data_2[0])
        stage_1.days_entry.delete(0, tk.END)
        stage_1.days_entry.insert(0, data_2[1])

        stage_2.stage_combobox.set(data_1[0])
        stage_2.days_entry.delete(0, tk.END)
        stage_2.days_entry.insert(0, data_1[1])
        
    def get_stages(self):
        stages_data = []
        for stage in self.stages_list:
            stage_data = [stage.stage_combobox.get(), int(stage.days_entry.get())]
            stages_data.append(stage_data)
        return stages_data

    def set_init_values(self, init_program_name):
        stages_data = self.db.programs.get_program_stages_list(init_program_name)
        for stage_data in stages_data:
            self.add_new_stage(is_init=True)
            self.stages_list[-1].stage_combobox.set(stage_data[0])
            self.stages_list[-1].days_entry.insert(0, str(stage_data[1]))





