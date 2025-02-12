import tkinter as tk
from windows.MainFrame import MainFrame


if __name__ == "__main__":
    root = tk.Tk()
    MainFrame(root).pack()
    root.mainloop()
