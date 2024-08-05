"""
@file mode_menu.py
@brief File containing sidebar of calculator app.
@author Martin Valapka (xvalapm00)
@date 27.07. 2024
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, Signal

LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"


class Sidebar(QWidget):
    """
    @brief Sidebar widget for calculator modes and settings.
    """
    mode_selected = Signal(str)

    def __init__(self, parent=None):
        """
        @brief Constructor for Sidebar.
        @param parent: Parent widget.
        """
        super().__init__(parent)
        self.buttons = {}
        self.animation = None
        self.is_visible = False
        self.setFixedWidth(0)
        self.setMaximumWidth(200)
        self.setStyleSheet(f"background-color: {DARK_GRAY};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(10)

        self.create_title()
        self.create_mode_buttons()
        self.content_layout.addStretch()

        main_layout.addWidget(content_widget)
        self.select_mode("Standard")

    def create_title(self):
        """
        @brief Creates and adds the title label to the content layout.
        """
        title = QLabel("Calculator Modes")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: white; margin-bottom: 5px;")
        self.content_layout.addWidget(title)

    def create_mode_buttons(self):
        """
        @brief Creates and adds the mode buttons to the content layout.
        """
        modes = ["Standard", "Photomath mode", "Graphing", "Programmer", "Date Calculation", "BMI", "Currency",
                 "Settings"]
        for mode in modes:
            button = QPushButton(mode)
            button.setStyleSheet(self.get_button_style())
            button.clicked.connect(lambda checked, m=mode: self.select_mode(m))

            if mode == "Settings":
                icon = QIcon(
                    r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\settings_icon.png')
                button.setIcon(icon)
                button.setIconSize(QSize(25, 25))

            self.buttons[mode] = button
            self.content_layout.addWidget(button)

    def get_button_style(self):
        """
        @brief Returns the stylesheet for the buttons.
        @return Stylesheet string.
        """
        return f"""
            QPushButton {{
                background-color: {GRAY};
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {LIGHT_GRAY};
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
                        background-color: {ORANGE};
                        color: white;
                        border: none;
                        padding: 10px;
                        font-weight: bold;
                        border-radius: 5px;
                        text-align: center;
                    }}
                """)
            else:
                button.setStyleSheet(self.get_button_style())

    def toggle(self):
        """
        @brief Toggles the visibility of the sidebar with an animation.
        """
        target_width = 200 if not self.is_visible else 0
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()
        self.is_visible = not self.is_visible

    def sizeHint(self):
        """
        @brief Provides a size hint for the sidebar.
        @return QSize object with the recommended size.
        """
        return QSize(200, super().sizeHint().height())