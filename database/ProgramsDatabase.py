import json


class ProgramsDatabase:
    """
    База данных для работы с учебными программами.
    Коды (индексы) для данных:
    0 - Название учебной программы (первичный ключ).
    1 - Число дней теории.
    2 - Число дней практики.
    3 - Число дней экзаменов.
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
        programs = self.data.get('programs', [])
        result = []
        for program in programs:
            result.append([
                program['name'],
                program['theory'],
                program['practice'],
                program['exams']
            ])
        return result

    def get(self, name):
        self.load_data()
        programs = self.data.get('programs', [])
        for program in programs:
            if program['name'] == name:
                return [
                    program['name'],
                    program['theory'],
                    program['practice'],
                    program['exams'],
                ]
    
    def get_total_days(self, name):
        self.load_data()
        program_data = self.get(name)
        total_days = program_data[1] + program_data[2] + program_data[3]
        return total_days

    def delete(self, name):
        self.load_data()
        programs = self.data.get('programs', [])
        for i, program in enumerate(programs):
            if program['name'] == name:
                del programs[i]
                self.save_data()
                return True
        return False

    def add(self, program_data):
        name, theory, practice, exams = program_data
        programs = self.data.get('programs', [])
        for program in programs:
            if program['name'] == name:
                return False
        new_program = {
            'name': name,
            'theory': theory,
            'practice': practice,
            'exams': exams
        }
        programs.append(new_program)
        self.save_data()
        return True
