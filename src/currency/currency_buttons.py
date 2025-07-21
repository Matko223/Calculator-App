"""
@file: currency_buttons.py
@brief: This module provides buttons for the currency calculator application.

@author: Martin Valapka
"""

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QGridLayout)
from utils.img_path import resource_path

# Color definitions
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class CurrencyButtons(QWidget):
    """
    @brief A class that represents buttons for the currency calculator.
    """
    
    def __init__(self, parent=None):
        """
        @brief Initializes the CurrencyButtons class.
        @param parent: The parent widget (CurrencyConverter).
        """
        super().__init__(parent)
        self.parent = parent
        
        self.buttonFrame = QFrame()
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrame.setFixedHeight(180)

        self.buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(1)
        self.buttonFrameLayout.addLayout(self.buttonLayout)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.buttonFrame)
        
        self.setup_buttons()
    
    def setup_buttons(self):
        """
        @brief Sets up all the buttons for the currency converter
        """
        self.digits = {
            7: (1, 0),
            8: (1, 1),
            9: (1, 2),
            4: (2, 0),
            5: (2, 1),
            6: (2, 2),
            1: (3, 0),
            2: (3, 1),
            3: (3, 2),
            0: (4, 1)
        }

        self.special_operations = {
            "C": (1, 3, 1, 2),
            "⌫": (2, 3, 1, 2),
            "CONVERT": (3, 3, 4, 5),
            ".": (4, 0),
        }
        
        self.create_clear_button()
        self.create_delete_button()

        for digit, (row, col) in self.digits.items():
            self.create_digit_button(digit, row, col)

        self.create_decimal_button()
        self.create_convert_button()
    
    def create_clear_button(self):
        """
        @brief Creates the clear button
        """
        button = QPushButton("C")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_REST};
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """)
        button.setFixedSize(79 * 2, 45)
        button.clicked.connect(self.parent.clear_input if self.parent else lambda: None)
        self.buttonLayout.addWidget(button, *self.special_operations["C"])

    def create_delete_button(self):
        """
        @brief Creates the delete button
        """
        button = QPushButton("⌫")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_REST};
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """)
        button.setFixedSize(79 * 2, 45)
        button.clicked.connect(self.parent.delete_digit if self.parent else lambda: None)
        self.buttonLayout.addWidget(button, *self.special_operations["⌫"])

    def create_digit_button(self, digit, row, col):
        """
        @brief Creates a button for a digit
        @param digit: Current digit
        @param row: Row
        @param col: Column
        """
        button = QPushButton(str(digit))
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_GRAY};
            }}
            QPushButton:hover {{
                background-color: {GRAY};
            }}
        """)

        if digit == 0:
            button.setFixedSize(79 * 2, 45)
        else:
            button.setFixedSize(79, 45)
        button.clicked.connect(lambda _, d=digit: self.parent.append_digit(str(d)) if self.parent else None)
        self.buttonLayout.addWidget(button, row, col)

        if self.parent:
            shortcut = QShortcut(QKeySequence(str(digit)), self.parent)
            shortcut.activated.connect(lambda d=digit: self.parent.append_digit(str(d)))

    def create_decimal_button(self):
        """
        @brief Creates the decimal button
        """
        button = QPushButton(".")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_GRAY};
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """)
        button.setFixedSize(79, 45)
        button.clicked.connect(lambda: self.parent.append_digit(".") if self.parent else None)
        self.buttonLayout.addWidget(button, *self.special_operations["."])

    def create_convert_button(self):
        """
        @brief Creates the convert button
        """
        button = QPushButton("CONVERT")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ORANGE};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {HOVER_OPERATOR};
            }}
        """)
        button.setFixedSize(79 * 2, 45 * 2)
        button.clicked.connect(self.parent.convert_currency if self.parent else lambda: None)
        self.buttonLayout.addWidget(button, *self.special_operations["CONVERT"])
        