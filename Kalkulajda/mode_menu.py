from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QFrame, \
    QPushButton
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize

LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
LARGE = "Arial 25 bold"
SMALL = "Arial 15"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation = None
        self.is_visible = False
        self.setFixedWidth(0)
        self.setMaximumWidth(200)
        self.setStyleSheet(f"""
            background-color: {DARK_GRAY};
        """)

        self.content_widget = QWidget()

        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title = QLabel("Calculator Modes")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        modes = ["Standard", "Photomath mode", "Graphing", "Programmer", "Date Calculation", "BMI", "Currency"]
        for mode in modes:
            button = QPushButton(mode)

            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {GRAY};
                    color: white;
                    border: none;
                    padding: 10px;
                    font-weight: bold;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: {LIGHT_GRAY};
                }}
            """)
            layout.addWidget(button)

        layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.content_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {DARK_GRAY};
                border-right: 52px solid {LIGHT_GRAY};
            }}
            QScrollBar {{
                background-color: {DARK_GRAY};
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)

    def toggle(self):
        target_width = 200 if not self.is_visible else 0
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()
        self.is_visible = not self.is_visible

    def sizeHint(self):
        return QSize(200, super().sizeHint().height())