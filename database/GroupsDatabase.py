import json


class GroupsDatabase:
    """
    База данных для работы с учебными группами.
    Коды столбцов:
    0 - Название учебной группы (составной первичный ключ 1/3).
    1 - Производственный календарь учебной группы (составной первичный ключ 2/3).
    2 - Учебная программа учебной группы (составной первичный ключ 3/3).
    3 - Дата начала обучения учебной группы.
    """
    def __init__(self):
        self.filename = 'database.json'
        self.load_data()
    
    def load_data(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
    
    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
    
    def get_all(self):
        self.load_data()
        groups = self.data.get('groups', [])
        result = []
        for group in groups:
            result.append([
                group['name'],
                group['calendar'],
                group['program'],
                group['start_date']
            ])
        return result
    
    def delete(self, name, calendar, program):
        self.load_data()
        groups = self.data.get('groups', [])
        for i, group in enumerate(groups):
            if (group['name'] == name) and \
               (group['calendar'] == calendar) and \
               (group['program'] == program):
                del groups[i]
                self.save_data()
                return True
        return False
    
    def add(self, group_data):
        name, calendar, program, start_date = group_data
        groups = self.data.get('groups', [])
        for group in groups:
            if (group['name'] == name) and \
               (group['calendar'] == calendar) and \
               (group['program'] == program):
                return False
        new_group = {
            'name': name,
            'calendar': calendar,
            'program': program,
            'start_date': start_date
        }
        groups.append(new_group)
        self.save_data()
        return True
    
    def delete_by_calendar(self, calendar_name):
        self.load_data()
        groups = self.data.get('groups', [])
        for i, group in enumerate(groups):
            if group["calendar"] == calendar_name:
                del groups[i]
        self.save_data()

    def delete_by_program(self, program_name):
        self.load_data()
        groups = self.data.get('groups', [])
        for i, group in enumerate(groups):
            if group["program"] == program_name:
                del groups[i]
        self.save_data()
    
    def update_program(self, old_program_name, new_program_name):
        self.load_data()
        groups = self.data.get('groups', [])
        for group in groups:
            if group["program"] == old_program_name:
                group["program"] = new_program_name
        self.save_data()
