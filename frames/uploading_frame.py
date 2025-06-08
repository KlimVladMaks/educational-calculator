import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from frames.base_frame import BaseFrame
from importer.Importer import Importer
from widgets.back_button import BackButton
from database.database import Database


class UploadingFrame(BaseFrame):

    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.db = Database()
        self.importer = Importer("./database.json")
        self.create_frame()

    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.place()

        ttk.Label(self, text="Выгрузить данные").pack(pady=10)

        self.selection_frame = ttk.Frame(self)
        self.selection_frame.pack()

        self.all_programs_var = tk.BooleanVar()
        self.all_programs_checkbutton = ttk.Checkbutton(
            self.selection_frame,
            text="Выбрать все программы",
            variable=self.all_programs_var,
            command=self.toggle_all_programs
        )
        self.all_programs_checkbutton.grid(row=0, column=0, padx=20, pady=5)

        self.all_groups_var = tk.BooleanVar()
        self.all_groups_checkbutton = ttk.Checkbutton(
            self.selection_frame,
            text="Выбрать все группы",
            variable=self.all_groups_var,
            command=self.toggle_all_groups
        )
        self.all_groups_checkbutton.grid(row=0, column=1, padx=20, pady=5)

        self.all_programs_names = self.db.programs.get_all_programs_names()
        self.all_groups_names = self.db.groups.get_all_groups_names()

        self.programs_listbox = tk.Listbox(
            self.selection_frame,
            listvariable=tk.StringVar(value=self.all_programs_names),
            selectmode=tk.MULTIPLE,
            exportselection=False
        )
        self.programs_listbox.grid(row=1, column=0, padx=10)
        self.programs_listbox.bind('<<ListboxSelect>>', self.update_programs_checkbox)

        self.groups_listbox = tk.Listbox(
            self.selection_frame,
            listvariable=tk.StringVar(value=self.all_groups_names),
            selectmode=tk.MULTIPLE,
            exportselection=False
        )
        self.groups_listbox.grid(row=1, column=1, padx=10)
        self.groups_listbox.bind('<<ListboxSelect>>', self.update_groups_checkbox)

        ttk.Button(self, text="Выгрузить в DOCX", command=self.upload_to_docx).pack(pady=10)
        ttk.Button(self, text="Выгрузить в XLSX", command=self.upload_to_xlsx).pack(pady=10)

    def toggle_all_programs(self):
        if self.all_programs_var.get():
            self.programs_listbox.selection_set(0, tk.END)
        else:
            self.programs_listbox.selection_clear(0, tk.END)

    def toggle_all_groups(self):
        if self.all_groups_var.get():
            self.groups_listbox.selection_set(0, tk.END)
        else:
            self.groups_listbox.selection_clear(0, tk.END)

    def update_programs_checkbox(self, event):
        selected_count = len(self.programs_listbox.curselection())
        total_count = len(self.all_programs_names)
        
        if selected_count == total_count:
            self.all_programs_var.set(True)
        else:
            self.all_programs_var.set(False)

    def update_groups_checkbox(self, event):
        selected_count = len(self.groups_listbox.curselection())
        total_count = len(self.all_groups_names)
        
        if selected_count == total_count:
            self.all_groups_var.set(True)
        else:
            self.all_groups_var.set(False)

    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def upload_to_docx(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                 filetypes=[("Word documents", "*.docx"),
                                                            ("All files", "*.*")])
        if file_path:
            self.importer.export_docx(file_path)
    
    def upload_to_xlsx(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"),
                                                            ("All files", "*.*")])
        if file_path:
            self.importer.export_excel(file_path)
