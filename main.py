import os
import json
import sys
import tkinter as tk
from frames.main_menu_frame import MainMenuFrame


def get_actual_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def check_and_create_calendar_app_files():
    current_dir = get_actual_path()
    calendar_app_dir = os.path.join(current_dir, "calendar_app")
    
    if not os.path.exists(calendar_app_dir):
        os.makedirs(calendar_app_dir)
        print(f"Создана папка: {calendar_app_dir}")
    
    required_files = {
        "days_off.json": {},
        "study_periods.json": {}
    }
    
    for filename, default_content in required_files.items():
        file_path = os.path.join(calendar_app_dir, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_content, f, ensure_ascii=False, indent=4)
            print(f"Создан файл: {file_path}")


# Запуск приложения
if __name__ == "__main__":
    check_and_create_calendar_app_files()
    root = tk.Tk()
    root.title("Образовательный калькулятор")
    root.geometry("700x400")
    root.resizable(False, False)
    main_frame = MainMenuFrame(root)
    main_frame.display_frame()
    root.mainloop()
