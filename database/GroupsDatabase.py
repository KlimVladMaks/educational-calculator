import json


class GroupsDatabase:
    """
    База данных для работы с учебными группами.
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
                group['edu_type'],
                group['start_date']
            ])
        return result
    
    def get(self, group_id):
        self.load_data()
        groups = self.data.get('groups', [])
        for group in groups:
            if (group["name"] == group_id[0]) and \
               (group["calendar"] == group_id[1]) and \
               (group["program"] == group_id[2]):
                return [
                    group["name"],
                    group["calendar"],
                    group["program"],
                    group["start_date"]
                ]
    
    def delete(self, name):
        self.load_data()
        groups = self.data.get('groups', [])
        for i, group in enumerate(groups):
            if (group['name'] == name):
                del groups[i]
                self.save_data()
                return True
        return False
    
    def add(self, group_data):
        name, calendar, program, edu_type, start_date = group_data
        groups = self.data.get('groups', [])
        new_group = {
            'name': name,
            'calendar': calendar,
            'program': program,
            'edu_type': edu_type,
            'start_date': start_date
        }
        groups.append(new_group)
        self.save_data()
    
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

    def update(self, group_id, updated_group_data):
        self.load_data()
        upd_name, upd_calendar, upd_program, upd_start_date = updated_group_data
        groups = self.data.get('groups', [])
        for group in groups:
            if (group["name"] == group_id[0]) and \
               (group["calendar"] == group_id[1]) and \
               (group["program"] == group_id[2]):
                group["name"] = upd_name
                group["calendar"] = upd_calendar
                group["program"] = upd_program
                group["start_date"] = upd_start_date
                break
        self.save_data()
    
    def delete_by_edu_type(self, edu_type):
        self.load_data()
        groups = self.data.get("groups", [])
        for i, group in enumerate(groups):
            if group["edu_type"] == edu_type:
                del groups[i]
        self.save_data()
    
    def update_edu_type(self, old_edu_type, new_edu_type):
        self.load_data()
        for group in self.data.get("groups", []):
            if group["edu_type"] == old_edu_type:
                group["edu_type"] = new_edu_type
        self.save_data()
