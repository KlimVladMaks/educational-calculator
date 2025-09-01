from database.base_database import BaseDatabase


class GroupsDatabase(BaseDatabase):
    """
    База данных для работы с данными учебных групп.
    """

    def __init__(self, parent_db):
        super().__init__(parent_db)

    def delete_by_calendar(self, calendar_name: str) -> None:
        self.load_data()
        for group in self.data.get("groups", []):
            if group["calendar"] == calendar_name:
                self.delete_group(group["name"])

    def delete_by_program(self, program_name):
        self.load_data()
        for group in self.data.get("groups", []):
            if group["program"] == program_name:
                self.delete_group(group["name"])

    def delete_by_edu_type(self, edu_type_name):
        self.load_data()
        for group in self.data.get("groups", []):
            if group["edu_type"] == edu_type_name:
                self.delete_group(group["name"])

    def get_all_groups_names(self):
        self.load_data()
        groups_names = []
        for group in self.data.get("groups", []):
            groups_names.append(group["name"])
        return groups_names

    def get_group_data_dict(self, group_name):
        self.load_data()
        for group in self.data.get("groups", []):
            if group["name"] == group_name:
                return group

    def delete_group(self, group_name):
        self.load_data()
        groups = self.data.get("groups", [])
        for i, group in enumerate(groups):
            if group["name"] == group_name:
                del groups[i]
                break
        self.save_data()

    def update_program(self, old_program_name, new_program_name):
        self.load_data()
        for group in self.data.get("groups", []):
            if group["program"] == old_program_name:
                group["program"] = new_program_name
        self.save_data()

    def update_calendar(self, old_calendar_name, new_calendar_name):
        self.load_data()
        for group in self.data.get("groups", []):
            if group["calendar"] == old_calendar_name:
                group["calendar"] = new_calendar_name
        self.save_data()

    def update_edu_type(self, old_edu_type, new_edu_type):
        self.load_data()
        for group in self.data.get("groups", []):
            if group["edu_type"] == old_edu_type:
                group["edu_type"] = new_edu_type
        self.save_data()

    def add_new_group(self, new_group_data):
        self.load_data()
        name, calendar, program, edu_type, start_date = new_group_data
        new_group = {
            "name": name,
            "calendar": calendar,
            "program": program,
            "edu_type": edu_type,
            "start_date": start_date
        }
        groups = self.data.get("groups", [])
        groups.append(new_group)
        self.save_data()

    def update_group(self, old_group_name, new_group_data):
        self.load_data()
        new_name, new_calendar, new_program, new_edu_type, new_start_date = new_group_data
        for group in self.data.get("groups", []):
            if group["name"] == old_group_name:
                group["name"] = new_name
                group["calendar"] = new_calendar
                group["program"] = new_program
                group["edu_type"] = new_edu_type
                group["start_date"] = new_start_date
                break
        self.save_data()

    def get_all_groups_by_program(self, program_name):
        self.load_data()
        groups = []
        for group in self.data.get("groups", []):
            if group["program"] == program_name:
                groups.append(group["name"])
        return groups
