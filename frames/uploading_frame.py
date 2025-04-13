from tkinter import ttk
from tkinter import filedialog
from frames.base_frame import BaseFrame
from importer.Importer import Importer
from widgets.back_button import BackButton


class UploadingFrame(BaseFrame):

    def __init__(self, master, parent_frame):
        super().__init__(master)
        self.parent_frame = parent_frame
        self.importer = Importer("./database.json")
        self.create_frame()

    def create_frame(self):
        self.back_button = BackButton(self.master, command=self.go_back)
        self.back_button.place()

        ttk.Label(self, text="Выгрузить данные").pack(pady=10)

        ttk.Button(self, text="Выгрузить в DOCX", command=self.upload_to_docx).pack(pady=10)
        ttk.Button(self, text="Выгрузить в XLSX", command=self.upload_to_xlsx).pack(pady=10)
    
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







