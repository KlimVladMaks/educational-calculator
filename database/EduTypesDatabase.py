import json


class EduTypesDatabase:
    """
    База данных для работы с видами обучения.
    """
    def __init__(self, parent_db):
        self.db = parent_db
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
        edu_types = self.data.get("edu_types", [])
        return edu_types

    def delete(self, edu_type_del):
        self.load_data()
        edu_types = self.data.get("edu_types", [])
        for i in range(len(edu_types)):
            if edu_types[i] == edu_type_del:
                edu_types.pop(i)
                break
        self.save_data()
        self.db.groups.delete_by_edu_type(edu_type_del)
    
    def add(self, new_edu_type):
        self.load_data()
        edu_types = self.data.get("edu_types", [])
        edu_types.append(new_edu_type)
        self.save_data()
    
    def update(self, old_edu_type, new_edu_type):
        self.load_data()
        edu_types = self.data.get("edu_types", [])
        for i in range(len(edu_types)):
            if edu_types[i] == old_edu_type:
                edu_types[i] = new_edu_type
                break
        self.save_data()
        self.db.groups.update_edu_type(old_edu_type, new_edu_type)
