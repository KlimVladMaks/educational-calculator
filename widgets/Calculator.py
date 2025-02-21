from database.Database import Database
from datetime import datetime, timedelta


class Calculator:
    
    def calculate_end_date(calendar_name, program_name, start_date_str):
        db = Database()
        days_off_list = db.calendars.get(calendar_name)[3]
        study_days = db.programs.get_total_days(program_name)
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        day_off_dates = {datetime.strptime(date, "%Y-%m-%d") for date in days_off_list}
        current_date = start_date
        days_counted = 0
        while days_counted < study_days:
            if current_date not in day_off_dates:
                days_counted += 1
            current_date += timedelta(days=1)
        return current_date.strftime("%Y-%m-%d")
    
    def count_days(start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        delta = (end - start).days + 1
        return delta
