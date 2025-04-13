import tkinter as tk
from frames.main_menu_frame import MainMenuFrame


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Образовательный калькулятор")
    root.geometry("700x400")
    root.resizable(False, False)
    main_frame = MainMenuFrame(root)
    main_frame.display_frame()
    root.mainloop()
