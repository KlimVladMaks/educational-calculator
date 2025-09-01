from database.base_database import BaseDatabase


class EduTypesDatabase(BaseDatabase):

    def __init__(self, parent_db):
        super().__init__(parent_db)
    
    def get_all_edu_types(self):
        self.load_data()
        edu_types = self.data.get("edu_types", [])
        return edu_types

    def delete_edu_type(self, edu_type_name):
        self.load_data()
        edu_types = self.data.get("edu_types", [])
        for i, edu_type in enumerate(edu_types):
            if edu_type == edu_type_name:
                del edu_types[i]
                break
        self.save_data()
        self.db.groups.delete_by_edu_type(edu_type_name)

    def add_new_edu_type(self, new_edu_type):
        self.load_data()
        edu_types_list = self.data.get("edu_types", [])
        edu_types_list.append(new_edu_type)
        self.save_data()

    def update_edu_type(self, old_edu_type, new_edu_type):
        self.load_data()
        edu_types_list = self.data.get("edu_types", [])
        for i, edu_type in enumerate(edu_types_list):
            if edu_type == old_edu_type:
                edu_types_list[i] = new_edu_type
                break
        self.save_data()
        self.db.groups.update_edu_type(old_edu_type, new_edu_type)






