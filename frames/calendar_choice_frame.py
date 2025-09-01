import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
import json
import datetime

class CalendarApp:
    def __init__(self, master):
        '''
        Инициализация календаря. Привязка к клику по календарю выбора даты. Создание словаря с соотвествием периодов на английском и русском.
        '''
        self.master = master
        self.master.title('Календарь')

        self.calendar = Calendar(master, selectmode='day', year=datetime.datetime.now().year, 
                                 month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.calendar.pack(pady=20)

        self.date_type_var = tk.StringVar(value="Выходной")
        self.date_type_label = tk.Label(master, text="Выберите тип даты:")
        self.date_type_label.pack(pady=5)

        self.radio_weekend = tk.Radiobutton(master, text="Выходной", variable=self.date_type_var, value="Выходной")
        self.radio_weekend.pack(anchor=tk.W)

        self.radio_study_period = tk.Radiobutton(master, text="Учебный период", variable=self.date_type_var, value="Учебный период")
        self.radio_study_period.pack(anchor=tk.W)

        self.selected_dates = set()
        self.study_periods = []

        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

        self.btn_save = tk.Button(master, text='Сохранить', command=self.save_dates)
        self.btn_save.pack(pady=10)

        # Соответствие типов учебных периодов
        self.period_type_mapping = {
            'теория': 'theory',
            'практика': 'practice',
            'консультация': 'consultation',
            'экзамен': 'exam',
            'пробная поездка': 'trial_ride'
        }

    def on_date_selected(self, event):
        '''
        Работа виджета. Выходной добавляется одним кликом. Учебный период требует введения вида и конечной даты в указанном формате. Для сохранения обязательно нажать кнопку "Сохранить".
        '''
        selected_date_str = self.calendar.get_date()
        selected_date = datetime.datetime.strptime(selected_date_str, '%m/%d/%y').date()
        if self.date_type_var.get() == "Выходной":
            weekend_date = selected_date.strftime('%Y-%m-%d')
            self.selected_dates.add(weekend_date)
            messagebox.showinfo("Выбор даты", f"Вы выбрали выходной: {selected_date}")
        elif self.date_type_var.get() == "Учебный период":
            period_type = simpledialog.askstring("Тип учебного периода", "Введите тип (теория, практика, консультация, экзамен, пробная поездка):")
            if period_type in self.period_type_mapping:
                start_date = selected_date
                end_date_str = simpledialog.askstring("Конечная дата", "Введите конечную дату (дд.мм.гггг):")
                if end_date_str:
                    try:
                        end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').date()
                        if end_date >= start_date:
                            self.study_periods.append({
                                'start_date': start_date.strftime('%Y-%m-%d'),  # Преобразуем в строку формата YYYY-MM-DD
                                'end_date': end_date.strftime('%Y-%m-%d'),      # Преобразуем в строку формата YYYY-MM-DD
                                'type': self.period_type_mapping[period_type]    # Переводим на английский
                            })
                            messagebox.showinfo("Выбор периода", f"Вы добавили учебный период: {start_date} - {end_date} ({period_type})")
                        else:
                            messagebox.showerror("Ошибка", "Конечная дата должна быть позже начальной.")
                    except ValueError:
                        messagebox.showerror("Ошибка", "Неверный формат даты. Используйте дд.мм.гггг.")

    def save_dates(self):
        '''
        Сохранение в файлы JSON введенных мероприятий.
        '''
        days_off = {"Выходной": list(self.selected_dates)}
        with open('./calendar_app/days_off.json', 'w', encoding='utf-8') as file:
            json.dump(days_off, file, ensure_ascii=False, indent=4)

        with open('./calendar_app/study_periods.json', 'w', encoding='utf-8') as file:
            json.dump(self.study_periods, file, ensure_ascii=False, indent=4)

        messagebox.showinfo("Сохранение", "Даты успешно сохранены в файлы.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()