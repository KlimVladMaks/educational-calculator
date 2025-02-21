import json


class CalendarsDatabase:
    """
    База данных для работы с производственными календарями.
    Коды (индексы) для данных:
    0 - Название производственного календаря (первичный ключ).
    1 - Начальная дата производственного календаря.
    2 - Конечная дата производственного календаря.
    3 - Список с датами выходных дней
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
        calendars = self.data.get('calendars', [])
        result = []
        for calendar in calendars:
            result.append([
                calendar['name'],
                calendar['start_date'],
                calendar['end_date'],
                calendar['days_off_list']
            ])
        return result

    def get(self, name):
        self.load_data()
        calendars = self.data.get('calendars', [])
        for calendar in calendars:
            if calendar['name'] == name:
                return [
                    calendar['name'],
                    calendar['start_date'],
                    calendar['end_date'],
                    calendar['days_off_list']
                ]
    
    def delete(self, name):
        self.load_data()
        calendars = self.data.get('calendars', [])
        for i, calendar in enumerate(calendars):
            if calendar['name'] == name:
                del calendars[i]
                self.save_data()
                return True
        return False
