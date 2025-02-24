import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from frames.BaseFrame import BaseFrame
from widgets.BackButton import BackButton
from importer.Importer import Importer


class UploadingFrame(BaseFrame):
    """
    Фрейм для выгрузки данных в Word.
    """
    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.importer = Importer("./database.json")
        self.create_widgets()

    def create_widgets(self):
        self.back_button = BackButton(self.master, command=self.go_back)

        ttk.Label(self, text="Выгрузить данные").pack(pady=10)

        ttk.Button(self, text="Выгрузить в DOCX", command=self.upload_to_docx).pack(pady=10)
        ttk.Button(self, text="Выгрузить в XLSX", command=self.upload_to_xlsx).pack(pady=10)

    def go_back(self):
        self.pack_forget()
        self.parent_frame.display_frame()
    
    def upload_to_docx(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                 filetypes=[("Word documents", "*.docx"),
                                                            ("All files", "*.*")])
        if file_path:
            self.importer.import_to_word(file_path)
    
    def upload_to_xlsx(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"),
                                                            ("All files", "*.*")])
        if file_path:
            self.importer.import_to_excel(file_path)
