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

        self.programs_frame = ttk.Frame(self.selection_frame)
        self.programs_frame.grid(row=1, column=0, padx=10, sticky="nsew")
        
        self.programs_scrollbar = ttk.Scrollbar(self.programs_frame, orient=tk.VERTICAL)
        self.programs_listbox = tk.Listbox(
            self.programs_frame,
            listvariable=tk.StringVar(value=self.all_programs_names),
            selectmode=tk.MULTIPLE,
            exportselection=False,
            yscrollcommand=self.programs_scrollbar.set,
            width=30,
            height=12
        )
        self.programs_scrollbar.config(command=self.programs_listbox.yview)
        
        self.programs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.programs_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.programs_listbox.bind('<<ListboxSelect>>', self.on_programs_selection_change)

        self.groups_frame = ttk.Frame(self.selection_frame)
        self.groups_frame.grid(row=1, column=1, padx=10, sticky="nsew")
        
        self.groups_scrollbar = ttk.Scrollbar(self.groups_frame, orient=tk.VERTICAL)
        self.groups_listbox = tk.Listbox(
            self.groups_frame,
            selectmode=tk.MULTIPLE,
            exportselection=False,
            yscrollcommand=self.groups_scrollbar.set,
            width=30,
            height=12
        )
        self.groups_scrollbar.config(command=self.groups_listbox.yview)
        
        self.groups_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.groups_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.groups_listbox.bind('<<ListboxSelect>>', self.update_groups_checkbox)

        ttk.Button(self, text="Выгрузить в XLSX", command=self.upload_to_xlsx).pack(pady=(15, 5))
        ttk.Button(self, text="Выгрузить в DOCX (таблица)", command=self.upload_to_docx_table).pack(pady=5)
        ttk.Button(self, text="Выгрузить в DOCX (список)", command=self.upload_to_docx_list).pack(pady=5)

    def toggle_all_programs(self):
        if self.all_programs_var.get():
            self.programs_listbox.selection_set(0, tk.END)
        else:
            self.programs_listbox.selection_clear(0, tk.END)
        self.on_programs_selection_change(None)

    def toggle_all_groups(self):
        if self.all_groups_var.get():
            self.groups_listbox.selection_set(0, tk.END)
        else:
            self.groups_listbox.selection_clear(0, tk.END)

    def on_programs_selection_change(self, event):
        self.update_programs_checkbox(event)
        
        selected_program_indices = self.programs_listbox.curselection()
        selected_programs = [self.programs_listbox.get(i) for i in selected_program_indices]
        
        filtered_groups = []
        for program in selected_programs:
            filtered_groups.extend(self.db.groups.get_all_groups_by_program(program))
        
        filtered_groups = list(set(filtered_groups))
        
        self.groups_listbox.delete(0, tk.END)
        for group in sorted(filtered_groups):
            self.groups_listbox.insert(tk.END, group)
        
        self.groups_listbox.selection_clear(0, tk.END)
        self.all_groups_var.set(False)

    def update_programs_checkbox(self, event):
        selected_count = len(self.programs_listbox.curselection())
        total_count = len(self.all_programs_names)
        
        if selected_count == total_count:
            self.all_programs_var.set(True)
        else:
            self.all_programs_var.set(False)

    def update_groups_checkbox(self, event):
        selected_count = len(self.groups_listbox.curselection())
        total_count = self.groups_listbox.size()
        
        if selected_count == total_count and total_count > 0:
            self.all_groups_var.set(True)
        else:
            self.all_groups_var.set(False)

    def go_back(self):
        self.back_button.destroy()
        self.destroy()
        self.parent_frame.display_frame()
    
    def upload_to_docx_table(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                 filetypes=[("Word documents", "*.docx"),
                                                            ("All files", "*.*")])
        if file_path:
            selected_groups_indices = self.groups_listbox.curselection()
            groups = [self.groups_listbox.get(i) for i in selected_groups_indices]
            self.importer.export_docx(file_path, groups)
    
    def upload_to_docx_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                 filetypes=[("Word documents", "*.docx"),
                                                            ("All files", "*.*")])
        if file_path:
            selected_groups_indices = self.groups_listbox.curselection()
            groups = [self.groups_listbox.get(i) for i in selected_groups_indices]
            self.importer.export_group_details_docx(file_path, groups)
    
    def upload_to_xlsx(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"),
                                                            ("All files", "*.*")])
        if file_path:
            selected_groups_indices = self.groups_listbox.curselection()
            groups = [self.groups_listbox.get(i) for i in selected_groups_indices]
            self.importer.export_excel(file_path, groups)
