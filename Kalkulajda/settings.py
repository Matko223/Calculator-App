"""
@file settings.py
@brief File containing all settings for the calculator application.

@author Martin Valapka (xvalapm00)
@date 18.12. 2024
"""

from PySide6.QtCore import QSize, Qt, QRegularExpression
from PySide6.QtGui import QFont, QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy, QScrollArea)

LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(400, 405)
        self.setStyleSheet(f"background-color: {DARK_GRAY};")

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        title_label = QLabel("Settings")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet(f"""
            color: "white";
            padding: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"background-color: {DARK_GRAY};")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)