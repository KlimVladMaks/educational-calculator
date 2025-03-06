import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from database.Database import Database
from widgets.BackButton import BackButton
from widgets.stages_constructor.StagesConstructor import StagesConstructor


class AddProgramFrame(BaseFrame):
    """
    Фрейм для добавления новой учебной программы.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.create_frame()
    
    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.pack()

        self.create_canvas()

        ttk.Label(self.scrollable_frame, text="Добавить учебную программу").pack(pady=10)

        ttk.Label(self.scrollable_frame, text="Название программы:").pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self.scrollable_frame, width=50)
        self.name_entry.pack(pady=(0, 10))

        self.stages_constructor = StagesConstructor(self.scrollable_frame, self.canvas)
        self.stages_constructor.pack()

        ttk.Label(self.scrollable_frame, text="Всего учебных дней: 0").pack(pady=10)

        ttk.Button(self.scrollable_frame,
                   text="Сохранить учебную программу",
                   command=self.save_program).pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def save_program(self):
        program_name = self.name_entry.get()
        stages = self.stages_constructor.get_stages()
        self.db.programs.add([program_name, stages])
        self.parent_frame.update_table()
        self.go_back()

    def create_canvas(self):
        self.window_width = self.master.winfo_width()
        self.window_height = self.master.winfo_height()
        self.canvas = tk.Canvas(self,
                                borderwidth=0,
                                width=self.window_width - 25,
                                height=self.window_height,
                                highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, width=300)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((150, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
