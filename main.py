import tkinter as tk
from frames.MainFrame import MainFrame

if __name__ == "__main__":
    root = tk.Tk()
    main_frame = MainFrame(root)
    main_frame.master.title("Образовательный калькулятор")
    main_frame.display_frame()
    root.mainloop()
