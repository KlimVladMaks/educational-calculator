import tkinter as tk
from tkinter import ttk
from frames.BaseFrame import BaseFrame
from database.Database import Database
from widgets.BackButton import BackButton


class EditProgramFrame(BaseFrame):
    """
    Фрейм для изменения данных учебной программы.
    """
    def __init__(self, master, parent_frame, old_program_data):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.old_program_data = old_program_data
        self.db = Database()
        self.create_frame()

    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)

        ttk.Label(self, text="Изменить учебную программу").pack(pady=10)

        ttk.Label(self, text="Название:").pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self, width=50)
        self.name_entry.insert(0, self.old_program_data[0])
        self.name_entry.pack(pady=(0, 10))

        self.input_duration_frame = ttk.Frame(self)
        self.input_duration_frame.pack(pady=10)

        ttk.Label(self.input_duration_frame, text="Теория:").grid(row=0, column=0, padx=5)
        ttk.Label(self.input_duration_frame, text="Практика:").grid(row=0, column=1, padx=5)
        ttk.Label(self.input_duration_frame, text="Экзамены:").grid(row=0, column=2, padx=5)

        self.theory_entry = ttk.Entry(self.input_duration_frame)
        self.theory_entry.insert(0, str(self.old_program_data[1]))
        self.theory_entry.grid(row=1, column=0, padx=5)
        self.practice_entry = ttk.Entry(self.input_duration_frame)
        self.practice_entry.insert(0, str(self.old_program_data[2]))
        self.practice_entry.grid(row=1, column=1, padx=5)
        self.exams_entry = ttk.Entry(self.input_duration_frame)
        self.exams_entry.insert(0, str(self.old_program_data[3]))
        self.exams_entry.grid(row=1, column=2, padx=5)

        self.theory_entry.bind("<KeyRelease>", self.update_total)
        self.practice_entry.bind("<KeyRelease>", self.update_total)
        self.exams_entry.bind("<KeyRelease>", self.update_total)

        self.total_label = ttk.Label(self, text=f"Всего (дней): 0")
        self.total_label.pack(pady=10)
        self.update_total()

        ttk.Button(self, text="Обновить учебную программу", command=self.update_program).pack(pady=10)
    
    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def update_total(self, event=None):
        try:
            theory = int(self.theory_entry.get()) if self.theory_entry.get() else 0
            practice = int(self.practice_entry.get()) if self.practice_entry.get() else 0
            exams = int(self.exams_entry.get()) if self.exams_entry.get() else 0
            total = theory + practice + exams
            self.total_label.config(text=f"Всего (дней): {total}")
        except ValueError:
            self.total_label.config(text="Всего (дней): 0")
    
    def update_program(self):
        updated_program_data = []

        name = str(self.name_entry.get())
        theory = int(self.theory_entry.get())
        practice = int(self.practice_entry.get())
        exams = int(self.exams_entry.get())

        updated_program_data.append(name)
        updated_program_data.append(theory)
        updated_program_data.append(practice)
        updated_program_data.append(exams)

        self.db.programs.update(self.old_program_data[0], updated_program_data)

        self.parent_frame.update()
        self.go_back()
