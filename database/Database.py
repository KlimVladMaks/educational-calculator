from database.CalendarsDatabase import CalendarsDatabase
from database.ProgramsDatabase import ProgramsDatabase
from database.GroupsDatabase import GroupsDatabase


class Database:

    def __init__(self):
        self.calendars = CalendarsDatabase()
        self.programs = ProgramsDatabase()
        self.groups = GroupsDatabase()
