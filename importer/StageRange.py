class StageRange:
    """
    Вспомогательный класс для хранения одного этапа обучения:
      - название этапа (например, 'Теория')
      - дата начала (date)
      - дата окончания (date)
    """
    def __init__(self, stage_name, start_date, end_date):
        self.stage_name = stage_name
        self.start_date = start_date
        self.end_date = end_date

    def is_single_day(self):
        return self.start_date == self.end_date

    def __str__(self):
        # Например: "Теория 24.02.2025 – 14.04.2025" или если один день, то "Теория 24.02.2025"
        start_str = self.start_date.strftime("%d.%m.%Y")
        end_str = self.end_date.strftime("%d.%m.%Y")
        if self.is_single_day():
            return f"{self.stage_name} {start_str}"
        else:
            return f"{self.stage_name} {start_str} – {end_str}"
