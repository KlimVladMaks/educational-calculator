from tkinter import ttk
from database.database import Database


class StageInput:

    def __init__(self, sc_frame, index, scroll_func, delete_func, move_up_func, move_down_func, update_label_func):
        self.sc_frame = sc_frame
        self.index = index
        self.scroll_func = scroll_func
        self.delete_func = delete_func
        self.move_up_func = move_up_func
        self.move_down_func = move_down_func
        self.update_label_func = update_label_func
        self.db = Database()
        self.frame = ttk.Frame(self.sc_frame)

        self.index_label = ttk.Label(self.frame, text=f"{str(self.index + 1)})")
        self.index_label.grid(row=0, column=0, padx=5)

        self.input_stage_frame = ttk.Frame(self.frame)
        self.input_stage_frame.grid(row=0, column=1, padx=5)
        ttk.Label(self.input_stage_frame, text="Название этапа:").pack()
        self.stages_list = self.db.edu_stages.get_all_stages()
        self.stage_combobox = ttk.Combobox(self.input_stage_frame, values=self.stages_list, state="readonly")
        self.stage_combobox.pack()
        self.stage_combobox.bind("<MouseWheel>", self.scroll_func)

        self.input_days_frame = ttk.Frame(self.frame)
        self.input_days_frame.grid(row=0, column=2, padx=5)
        ttk.Label(self.input_days_frame, text="Число дней:").pack()

        validate_command = sc_frame.register(self.validate_positive_integer)
        self.days_entry = ttk.Entry(self.input_days_frame, validate="key", validatecommand=(validate_command, '%P'))
        
        self.days_entry.pack()

        self.days_entry.bind("<KeyRelease>", lambda event: self.update_label_func())

        ttk.Button(self.frame, text="↑", width=3, command=self.move_up).grid(row=0, column=3, padx=5)
        ttk.Button(self.frame, text="↓", width=3, command=self.move_down).grid(row=0, column=4, padx=5)
        ttk.Button(self.frame, text="-", width=3, command=self.delete).grid(row=0, column=5, padx=5)
    
    def pack(self, pady):
        self.frame.pack(pady=pady)
    
    def delete(self):
        self.delete_func(self.index)
        self.frame.destroy()

    def move_up(self):
        self.move_up_func(self.index)
    
    def move_down(self):
        self.move_down_func(self.index)

    def disable_mouse_wheel_scroll(self, event):
        return "break"

    def update_index(self, new_index: int):
        self.index = new_index
        self.index_label["text"] = f"{str(self.index + 1)})"

    def validate_positive_integer(self, new_value):
        if new_value == "":
            return True
        if new_value.isdigit():
            return True
        return False





