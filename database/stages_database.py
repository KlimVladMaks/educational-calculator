from database.base_database import BaseDatabase


class StagesDatabase(BaseDatabase):

    def __init__(self, parent_db):
        super().__init__(parent_db)
    
    def get_all_stages(self):
        self.load_data()
        stages = self.data.get("edu_stages", [])
        return stages
    
    def add_new_stage(self, new_stage):
        self.load_data()
        stages_list = self.data.get("edu_stages", [])
        stages_list.append(new_stage)
        self.save_data()

    def delete_stage(self, stage_name):
        self.load_data()
        stages = self.data.get("edu_stages", [])
        for i, stage in enumerate(stages):
            if stage == stage_name:
                del stages[i]
                break
        self.save_data()
        self.db.programs.delete_by_stage(stage_name)

    def update_stage(self, old_stage, new_stage):
        self.load_data()
        stages_list = self.data.get("edu_stages", [])
        for i, stage in enumerate(stages_list):
            if stage == old_stage:
                stages_list[i] = new_stage
                break
        self.save_data()
        self.db.programs.update_stage(old_stage, new_stage)






