from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout
)
from PyQt6.QtCore import Qt


class CalendarsWindow(QMainWindow):
    """
    Окно с производственными календарями.
    """
    def __init__(self, parent_window):
        super().__init__()

        self.parent_window = parent_window

        self.setWindowTitle("Производственные календари")
        self.setGeometry(150, 150, 300, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        label = QLabel("Производственные календари")
        h_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(h_layout)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        central_widget.setLayout(layout)
    
    def go_back(self):
        self.parent_window.show()
        self.close()
