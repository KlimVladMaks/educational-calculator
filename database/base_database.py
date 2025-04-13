import json


class BaseDatabase:
    """
    Базовая база данных для наследования.
    Предоставляет общий базовый функционал для базы данных.
    """
    def __init__(self, parent_db: 'database.database.Database') -> None:
        """
        Аргументы:
            parent_db: Родительская база данных, которая выступает обёрткой для специализированных баз данных.
        """
        self.db = parent_db
        self.load_data()
    
    def load_data(self) -> None:
        """
        Загружает данные из JSON-файла, чтобы с ними можно было работать.
        Желательно вызывать перед любой работой с данными БД, чтобы всегда работать с актуальными данными.
        """
        with open(self.db.file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
    
    def save_data(self) -> None:
        """
        Сохраняет данные, изменённые базой данных, обратно в JSON-файл.
        """
        with open(self.db.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
