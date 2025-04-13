from tkinter import ttk


class InputWidget:
    
    def __init__(self, main_frame, label, do_button_name, do_func, 
                 cancel_button_name, cancel_func, init_entry_value=""):
        self.frame = ttk.Frame(main_frame)
        ttk.Label(self.frame, text=label).pack()
        self.entry = ttk.Entry(self.frame, width=40)
        self.entry.insert(0, init_entry_value)
        self.entry.pack(pady=(0, 5))
        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.pack(pady=(5, 0))
        ttk.Button(self.buttons_frame, text=do_button_name, command=do_func).grid(row=0, column=0, padx=5)
        ttk.Button(self.buttons_frame, text=cancel_button_name, command=cancel_func).grid(row=0, column=1, padx=5)
    
    def pack(self, pady):
        self.frame.pack(pady=pady)
    
    def destroy(self):
        self.frame.destroy()





