import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame


class AddProgramFrame(BaseFrame):
    """
    Фрейм для добавления новой учебной программы.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.create_frame()
    
    def create_frame(self):
        self.back_button = ttk.Button(self.master, text="Назад", command=self.go_back)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)

        ttk.Label(self, text="Добавить учебную программу").pack(pady=10)

        self.input_name_frame = ttk.Frame(self)
        self.input_name_frame.pack(pady=10)

        self.name_label = ttk.Label(self.input_name_frame, text="Название:")
        self.name_label.grid(row=0, column=0, padx=5)
        self.name_entry = ttk.Entry(self.input_name_frame, width=50)
        self.name_entry.grid(row=0, column=1, padx=5)

        self.input_duration_frame = ttk.Frame(self)
        self.input_duration_frame.pack(pady=10)

        self.theory_label = ttk.Label(self.input_duration_frame, text="Теория:")
        self.theory_label.grid(row=0, column=0, padx=5)
        self.practice_label = ttk.Label(self.input_duration_frame, text="Практика:")
        self.practice_label.grid(row=0, column=1, padx=5)
        self.exams_label = ttk.Label(self.input_duration_frame, text="Экзамены:")
        self.exams_label.grid(row=0, column=2, padx=5)

        self.theory_entry = ttk.Entry(self.input_duration_frame)
        self.theory_entry.grid(row=1, column=0, padx=5)
        self.practice_entry = ttk.Entry(self.input_duration_frame)
        self.practice_entry.grid(row=1, column=1, padx=5)
        self.exams_entry = ttk.Entry(self.input_duration_frame)
        self.exams_entry.grid(row=1, column=2, padx=5)

        self.total_label = ttk.Label(self, text="Всего: 0")
        self.total_label.pack(pady=10)

        ttk.Button(self, text="Добавить учебную программу").pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
