import json


class EduStagesDatabase:
    """
    База данных для работы с этапами обучения.
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
        edu_types = self.data.get("edu_stages", [])
        return edu_types

    def delete(self, edu_stage_del):
        self.load_data()
        edu_stages = self.data.get("edu_stages", [])
        for i in range(len(edu_stages)):
            if edu_stages[i] == edu_stage_del:
                edu_stages.pop(i)
                break
        self.save_data()
        self.db.programs.delete_by_edu_stage(edu_stage_del)
    
    def add(self, new_edu_stage):
        self.load_data()
        edu_stages = self.data.get("edu_stages", [])
        edu_stages.append(new_edu_stage)
        self.save_data()
    
    def update(self, old_edu_stage, new_edu_stage):
        self.load_data()
        edu_stages = self.data.get("edu_stages", [])
        for i in range(len(edu_stages)):
            if edu_stages[i] == old_edu_stage:
                edu_stages[i] = new_edu_stage
                break
        self.save_data()
        self.db.programs.update_edu_stage(old_edu_stage, new_edu_stage)
