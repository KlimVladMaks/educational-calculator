import json


class ProgramsDatabase:
    """
    База данных для работы с учебными программами.
    """
    def __init__(self, parent_db):
        self.parent_db = parent_db
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
        return programs

    def get(self, program_name):
        self.load_data()
        for program in self.data.get('programs', []):
            if program["name"] == program_name:
                return program

    def get_unique_stages_names(self):
        self.load_data()
        unique_stages_names = []
        for program in self.data.get('programs', []):
            for stage in program.get("stages", []):
                stage_name = stage[0]
                if stage_name not in unique_stages_names:
                    unique_stages_names.append(stage_name)
        return sorted(unique_stages_names)
    
    def get_all_programs_names(self):
        self.load_data()
        programs_names = []
        for program in self.data.get("programs", []):
            programs_names.append(program["name"])
        return programs_names

    def get_total_days(self, program_name):
        self.load_data()
        program = self.get(program_name)
        total_days = sum(stage[1] for stage in program["stages"])
        return total_days
    
    def get_number_of_days_for_stage(self, program_name, stage_name):
        self.load_data()
        program = self.get(program_name)
        number_of_days = 0
        for stage in program["stages"]:
            if stage[0] == stage_name:
                number_of_days += stage[1]
        return number_of_days
        
    def delete(self, program_name):
        self.load_data()
        programs = self.data.get('programs', [])
        for i, program in enumerate(programs):
            if program['name'] == program_name:
                del programs[i]
                break
        self.save_data()
        self.parent_db.groups.delete_by_program(program_name)

    def add(self, program_data):
        name, stages = program_data
        programs = self.data.get('programs', [])
        for program in programs:
            if program['name'] == name:
                return False
        new_program = {
            'name': name,
            'stages': stages
        }
        programs.append(new_program)
        self.save_data()
        return True

    def update(self, program_name, updated_program_data):
        self.load_data()
        upd_name, upd_theory, upd_practice, upd_exams = updated_program_data
        programs = self.data.get('programs', [])
        for program in programs:
            if program["name"] == program_name:
                program["name"] = upd_name
                program["theory"] = upd_theory
                program["practice"] = upd_practice
                program["exams"] = upd_exams
                break
        self.save_data()
        self.parent_db.groups.update_program(program_name, upd_name)
    
    def get_all_names(self):
        names = []
        for calendar in self.data.get('programs', []):
            names.append(calendar["name"])
        return names

    def update_edu_stage(self, old_edu_stage, new_edu_stage):
        self.load_data()
        for program in self.data.get("programs", []):
            program_stages = program["stages"]
            for stage in program_stages:
                if stage[0] == old_edu_stage:
                    stage[0] = new_edu_stage
        self.save_data()
    
    def delete_by_edu_stage(self, edu_stage):
        self.load_data()
        programs = self.data.get("programs", [])
        for i, program in enumerate(programs):
            for stage in program["stages"]:
                if stage[0] == edu_stage:
                    del programs[i]
                    break
        self.save_data()
