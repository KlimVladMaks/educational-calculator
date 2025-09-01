from datetime import datetime, timedelta
from database.database import Database


class Calculator:
    """
    Калькулятор для расчётов, требующихся при работе программы.
    """

    def count_days_between_dates(start_date: str, end_date: str) -> int:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        delta = (end - start).days + 1
        return delta

    def calculate_end_date(calendar_name, program_name, start_date_str):
        db = Database()
        days_off_list = db.calendars.get_days_off_list(calendar_name)
        study_days = db.programs.get_total_days(program_name)
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        days_off_dates = {datetime.strptime(date, "%Y-%m-%d") for date in days_off_list}
        current_date = start_date
        days_counter = 0
        while days_counter < study_days:
            if current_date not in days_off_dates:
                days_counter += 1
            current_date += timedelta(days=1)
        current_date -= timedelta(days=1)
        return current_date.strftime("%Y-%m-%d")

    def calculate_stages_intervals(calendar_name, program_name, start_date):
        db = Database()
        stages = db.programs.get_program_stages_list(program_name)
        days_off_list = db.calendars.get_days_off_list(calendar_name)

        current_date = datetime.strptime(start_date, "%Y-%m-%d")

        result = []

        for stage in stages:
            stage_name, duration = stage
            stage_start_date = current_date

            working_days_count = 0
            while working_days_count < duration:
                if current_date.strftime("%Y-%m-%d") not in days_off_list:
                    working_days_count += 1
                current_date += timedelta(days=1)
            
            stage_end_date = current_date - timedelta(days=1)

            result.append([
                stage_name,
                stage_start_date.strftime("%Y-%m-%d"),
                stage_end_date.strftime("%Y-%m-%d")
            ])

            while current_date.strftime("%Y-%m-%d") in days_off_list:
                current_date += timedelta(days=1)
        
        return result

    def convert_date_to_dd_mm_yyyy(date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")






