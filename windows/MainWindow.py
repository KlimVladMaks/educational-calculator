from windows.CalendarsWindow import CalendarsWindow
from windows.ProgramsWindow import ProgramsWindow
from windows.GroupsWindow import GroupsWindow
from windows.UploadingWindow import UploadingWindow
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)


class MainWindow(QMainWindow):
    """
    Окно с главным меню.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Образовательный калькулятор")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        calendars_button = QPushButton("Производственные календари")
        programs_button = QPushButton("Учебные программы")
        groups_button = QPushButton("Учебные группы")
        uploading_button = QPushButton("Выгрузить в Word")

        calendars_button.clicked.connect(self.open_calendars_window)
        programs_button.clicked.connect(self.open_programs_window)
        groups_button.clicked.connect(self.open_groups_window)
        uploading_button.clicked.connect(self.open_uploading_window)

        layout.addWidget(calendars_button)
        layout.addWidget(programs_button)
        layout.addWidget(groups_button)
        layout.addWidget(uploading_button)

        central_widget.setLayout(layout)
    
    def open_calendars_window(self):
        self.calendars_window = CalendarsWindow(self)
        self.calendars_window.show()
        self.close()
    
    def open_programs_window(self):
        self.program_windows = ProgramsWindow(self)
        self.program_windows.show()
        self.close()
    
    def open_groups_window(self):
        self.groups_windows = GroupsWindow(self)
        self.groups_windows.show()
        self.close()
    
    def open_uploading_window(self):
        self.uploading_windows = UploadingWindow(self)
        self.uploading_windows.show()
        self.close()
