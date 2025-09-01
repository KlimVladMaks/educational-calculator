import os
import json
from database.calendars_database import CalendarsDatabase
from database.programs_database import ProgramsDatabase
from database.groups_database import GroupsDatabase
from database.stages_database import StagesDatabase
from database.edu_types_database import EduTypesDatabase

class Database:
    """
    Общая база данных приложения.
    Служит обёрткой для специализированных баз данных.
    """
    def __init__(self) -> None:
        self.file_path = "database.json"
        self.check_and_create_database_file()

        self.calendars = CalendarsDatabase(self)
        self.programs = ProgramsDatabase(self)
        self.groups = GroupsDatabase(self)
        self.edu_stages = StagesDatabase(self)
        self.edu_types = EduTypesDatabase(self)
    
    def check_and_create_database_file(self) -> None:
        """
        Проверяет наличие и при отсутствии создаёт JSON-файл для базы данных.
        """
        if not os.path.exists(self.file_path):
            initial_data = {
                "calendars": [],
                "programs": [],
                "groups": [],
                "edu_stages": [],
                "edu_types": []
            }
            with open(self.file_path, 'w') as json_file:
                json.dump(initial_data, json_file, indent=4)
