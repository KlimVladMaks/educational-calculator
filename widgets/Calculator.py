from database.Database import Database
from datetime import datetime, timedelta


class Calculator:
    
    def calculate_end_date(calendar_name, program_name, start_date_str):
        db = Database()
        days_off_list = db.calendars.get(str(calendar_name))[3]
        study_days = db.programs.get_total_days(str(program_name))
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        day_off_dates = {datetime.strptime(date, "%Y-%m-%d") for date in days_off_list}
        current_date = start_date
        days_counted = 0
        while days_counted < study_days:
            if current_date not in day_off_dates:
                days_counted += 1
            current_date += timedelta(days=1)
        current_date -= timedelta(days=1)
        return current_date.strftime("%Y-%m-%d")
    
    def count_days_between_dates(start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        delta = (end - start).days + 1
        return delta

    def calculate_stages_intervals(calendar_name: str, program_name: str, start_date: str) -> list[list[str]]:
        """
        Рассчитать временные интервалы для учебных этапов.
        Возвращает список в следующем формате:
        [["Название_этапа_1", "Дата_начала_этапа_1", "Дата_окончания_этапа_1"], [...], ...]
        """
        db = Database()
        stages: list[list[str]] = db.programs.get_stages_list(program_name)
        days_off_list: list[str] = db.calendars.get_days_off_list(calendar_name)

        # Преобразуем start_date в объект datetime
        current_date = datetime.strptime(start_date, "%Y-%m-%d")

        result = []

        for stage in stages:
            stage_name, duration = stage
            stage_start_date = current_date

            # Считаем рабочие дни для этапа
            working_days_count = 0
            while working_days_count < duration:
                # Проверяем, является ли текущий день выходным
                if current_date.strftime("%Y-%m-%d") not in days_off_list:
                    working_days_count += 1
                # Переходим к следующему дню
                current_date += timedelta(days=1)

            # Дата окончания этапа — это предыдущий день (так как current_date был увеличен на 1 после последнего рабочего дня)
            stage_end_date = current_date - timedelta(days=1)

            # Добавляем этап в результат
            result.append([
                stage_name,
                stage_start_date.strftime("%Y-%m-%d"),
                stage_end_date.strftime("%Y-%m-%d")
            ])

            # Начинаем следующий этап с рабочего дня
            while current_date.strftime("%Y-%m-%d") in days_off_list:
                current_date += timedelta(days=1)

        return result






