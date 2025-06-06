from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QSize, Signal
import os
import sys

BACKGROUND_COLOR = "#2C2C2C"
DARK_GRAY = "#3D3D3D"
LIGHT_GRAY = "#A9A9A9"
ORANGE = "#FFA500"
HOVER_COLOR = "#696969"
BUTTON_SELECTED_COLOR = "#FFA500"
BUTTON_TEXT_COLOR = "#FFFFFF"

def resource_path(relative_path):
    """
    @brief Get the absolute path to the resource, works for both development and PyInstaller.
    @param relative_path: The relative path to the resource.
    @return: The absolute path to the resource.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
    

class Sidebar(QWidget):
    """
    @brief Sidebar widget for calculator modes and settings.
    """
    mode_selected = Signal(str)
    visibility_changed = Signal(bool)

    def __init__(self, parent=None):
        """
        @brief Constructor for Sidebar.
        @param parent: Parent widget.
        """
        super().__init__(parent)
        self.buttons = {}
        self.setFixedWidth(240)
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(7)

        self.create_title()
        self.create_mode_buttons()
        self.content_layout.addStretch()

        main_layout.addWidget(content_widget)
        self.select_mode("Standard")

    def create_title(self):
        """
        @brief Creates and adds the title label to the content layout.
        """
        title = QLabel("Modes")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet(f"color: white;")
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)

    def create_mode_buttons(self):
        """
        @brief Creates and adds the mode buttons to the content layout.
        """
        modes = {
            "Standard": resource_path(os.path.join('Pictures', 'calculator_img.png')),
            "Expression": resource_path(os.path.join('Pictures', 'expression.png')),
            "Graphing": resource_path(os.path.join('Pictures', 'function.png')),
            "Programmer": resource_path(os.path.join('Pictures', 'programmer.png')),
            "Date Calculation": resource_path(os.path.join('Pictures', 'calendar.png')),
            "BMI": resource_path(os.path.join('Pictures', 'weights.png')),
            "Currency": resource_path(os.path.join('Pictures', 'currency.png')),
            "Settings": resource_path(os.path.join('Pictures', 'settings.png'))
        }

        for mode, icon_path in modes.items():
            button = QPushButton()
            button.setFont(QFont("Arial", 14))

            button_layout = QHBoxLayout(button)
            button_layout.setContentsMargins(10, 8, 10, 8)
            button_layout.setSpacing(10)

            icon_label = QLabel()
            icon = QIcon(icon_path)
            pixmap = icon.pixmap(QSize(24, 24))
            icon_label.setPixmap(pixmap)
            icon_label.setStyleSheet("background-color: transparent;")
            button_layout.addWidget(icon_label)

            # Add vertical line
            line = QWidget()
            line.setFixedWidth(2)
            line.setStyleSheet("background-color: white;")
            button_layout.addWidget(line)

            text_label = QLabel(mode)
            text_label.setFont(QFont("Arial", 14))
            text_label.setStyleSheet("color: white; background-color: transparent; font-weight: bold;")
            button_layout.addWidget(text_label)

            button_layout.setAlignment(Qt.AlignLeft)

            button.setStyleSheet(self.get_button_style())
            button.clicked.connect(lambda checked, m=mode: self.select_mode(m))
            self.buttons[mode] = button
            self.content_layout.addWidget(button)

    def get_button_style(self):
        """
        @brief Returns the stylesheet for the buttons.
        @return Stylesheet string.
        """
        return f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 8px 10px;
                font-weight: bold;
                border-radius: 10px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """

    def select_mode(self, mode):
        """
        @brief Selects a mode and updates button styles.
        @param mode: The mode to be selected.
        """
        self.mode_selected.emit(mode)
        self.update_button_styles(mode)

    def update_button_styles(self, selected_mode):
        """
        @brief Updates the button styles based on the selected mode.
        """
        for mode, button in self.buttons.items():
            if mode == selected_mode:
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {BUTTON_SELECTED_COLOR};
                        color: {BUTTON_TEXT_COLOR};
                        border: none;
                        padding: 8px 10px;
                        font-weight: bold;
                        border-radius: 10px;
                        text-align: left;
                    }}
                """)
            else:
                button.setStyleSheet(self.get_button_style())

    def toggle_visibility(self):
        """
        @brief Toggles the visibility of the sidebar.
        """
        self.visibility_changed.emit(not self.isVisible())
        self.setVisible(not self.isVisible())