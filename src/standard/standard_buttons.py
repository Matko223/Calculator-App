"""
@file standard_buttons.py
@brief This module provides the standard buttons for the calculator application.

@author: Martin Valapka
"""

import sys
import os
from decimal import getcontext, Decimal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QIcon
from PySide6.QtCore import Qt, QSize
from standard import mathlib
from currency.currency_converter import CurrencyConverter
from day.date_calculation import DateCalculation
from help.help_menu import HelpWindow
from sidebar.mode_menu import Sidebar
from bmi.bmi_calculator import BMICalculator
from expression.photomath_mode import PhotomathMode
from settings.settings import Settings
from utils.img_path import resource_path
import ctypes

# Color definitions
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class StandardButtons(QWidget):
    """
    @brief A class that represents the standard buttons for the calculator application.
    """
    def __init__(self, parent=None):
        """
        @brief Initializes the StandardButtons class.
        @param parent: The parent widget.
        """ 
        super().__init__(parent)

        self.parent_app = parent
        
        # Digit button positions
        self.digits = {
            7: (1, 1),
            8: (1, 2),
            9: (1, 3),
            4: (2, 1),
            5: (2, 2),
            6: (2, 3),
            1: (3, 1),
            2: (3, 2),
            3: (3, 3),
            0: (4, 2)
        }

        # Operation button symbols
        self.operations = {
            "/": "\u00F7",
            "*": "\u00D7",
            "-": "-",
            "+": "+"
        }

        # Special operation button positions
        self.special_operations = {
            "x²": (0, 0),
            "C": (0, 1, 1, 2),
            "⌫": (0, 3, 1, 2),
            "√": (1, 0),
            "!": (2, 0),
            "|x|": (3, 0),
            "%": (4, 0),
            ".": (4, 1),
            "=": (4, 3)
        }

        self.buttonFrame = QWidget(self)
        self.buttonFrame.setFixedHeight(280)
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.buttonFrame)
        
        self.buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(3, 3, 3, 3)
        
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonFrameLayout.addLayout(self.buttonLayout)
        
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

    def create_digit_buttons(self):
        """
        @brief Creates and configures buttons for digits 0-9.
        """
        for digit, pos in self.digits.items():
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
            button.setFixedSize(79, 55)
            button.clicked.connect(lambda _, d=digit: self.parent_app.show_numbers(d))
            self.buttonLayout.addWidget(button, pos[0], pos[1])

            shortcut = QShortcut(QKeySequence(str(digit)), self)
            shortcut.activated.connect(lambda d=digit: self.parent_app.show_numbers(d))

    def create_operator_buttons(self):
        """
        @brief Creates and configures buttons for arithmetic operators (+, -, *, /).
        """
        operator_positions = {
            "/": (1, 4),
            "*": (2, 4),
            "-": (3, 4),
            "+": (4, 4),
        }

        for operator, pos in operator_positions.items():
            button = QPushButton(self.operations[operator])
            button.setFont(QFont("Arial", 20))
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ORANGE};
                }}
                QPushButton:hover {{
                    background-color: {HOVER_OPERATOR};
                }}
            """)
            button.setFixedSize(79, 55)
            button.clicked.connect(lambda _, op=operator: self.parent_app.show_operators(op))
            self.buttonLayout.addWidget(button, pos[0], pos[1])

            shortcut = QShortcut(QKeySequence(operator), self)
            shortcut.activated.connect(lambda op=operator: self.parent_app.show_operators(op))

    def create_special_buttons(self):
        """
        @brief Creates and configures buttons for special operations (e.g., x², C, √, !, |x|, %, ., =).
        """
        for operation, pos in self.special_operations.items():
            if operation == "x²":
                self.create_exponentiation_button(pos)
            elif operation == "C":
                self.create_clear_button(pos)
            elif operation == "⌫":
                self.create_delete_button(pos)
            elif operation == "√":
                self.create_square_root_button(pos)
            elif operation == "!":
                self.create_factorial_button(pos)
            elif operation == "|x|":
                self.create_absolute_value_button(pos)
            elif operation == "%":
                self.create_modulo_button(pos)
            elif operation == ".":
                self.create_decimal_button(pos)
            elif operation == "=":
                self.create_equals_button(pos)

    def create_exponentiation_button(self, pos):
        """
        @brief Creates and configures the button for exponentiation (x²).
        @param pos: Position of the button in the grid layout as a tuple (row, column).
        """
        button = QPushButton("x\u207F")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_GRAY};
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """)
        button.setFixedSize(79, 55)
        button.clicked.connect(self.parent_app.handle_exponentiation)
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_clear_button(self, pos):
        """
        @brief Creates and configures the button for clearing the current expression (C).
        @param pos: Position of the button in the grid layout as a tuple (row, column, rowspan, colspan).
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
        button.setFixedSize(79 * 2, 55)
        button.clicked.connect(self.parent_app.handle_clear)
        self.buttonLayout.addWidget(button, pos[0], pos[1], pos[2], pos[3])
        shortcut_clear = QShortcut(QKeySequence("C"), self)
        shortcut_clear.activated.connect(self.parent_app.handle_clear)

    def create_delete_button(self, pos):
        """
        @brief Creates and configures the button for deleting the last character (⌫).
        @param pos: Position of the button in the grid layout as a tuple (row, column, rowspan, colspan).
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
        button.setFixedSize(79 * 2, 55)
        button.clicked.connect(self.parent_app.handle_delete)
        self.buttonLayout.addWidget(button, pos[0], pos[1], pos[2], pos[3])
        shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), self)
        shortcut.activated.connect(self.parent_app.handle_delete)

    def create_square_root_button(self, pos):
        """
        @brief Creates and configures the button for square root operation (ⁿ√x).
        @param pos: Position of the button in the grid layout as a tuple (row, column).
        """
        button = QPushButton("ⁿ√x")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_GRAY};
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """)
        button.setFixedSize(79, 55)
        button.clicked.connect(self.parent_app.handle_root)
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_factorial_button(self, pos):
        """
        @brief Creates and configures the button for factorial operation (x!).
        @param pos: Position of the button in the grid layout as a tuple (row, column).
        """
        button = QPushButton("x!")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_GRAY};
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """)
        button.setFixedSize(79, 55)
        button.clicked.connect(self.parent_app.handle_factorial)
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_absolute_value_button(self, pos):
        """
        @brief Creates and configures the button for absolute value operation (|x|).
        @param pos: Position of the button in the grid layout as a tuple (row, column).
        """
        button = QPushButton("|x|")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_GRAY};
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """)
        button.setFixedSize(79, 55)
        button.clicked.connect(self.parent_app.handle_absolute_value)
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_modulo_button(self, pos):
        """
        @brief Creates and configures the button for modulo operation (mod).
        @param pos: Position of the button in the grid layout as a tuple (row, column).
        """
        button = QPushButton("mod")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_GRAY};
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """)
        button.setFixedSize(79, 55)
        button.clicked.connect(self.parent_app.handle_modulo)
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_decimal_button(self, pos):
        """
        @brief Creates and configures the button for decimal point (.) operation.
        @param pos: Position of the button in the grid layout as a tuple (row, column).
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
        button.setFixedSize(79, 55)
        button.clicked.connect(self.parent_app.handle_decimal_point)
        self.buttonLayout.addWidget(button, pos[0], pos[1])
        shortcut_decimal = QShortcut(QKeySequence(Qt.Key_Period), self)
        shortcut_decimal.activated.connect(self.parent_app.handle_decimal_point)

    def create_equals_button(self, pos):
        """
        @brief Creates and configures the button for equals operation (=).
        @param pos tuple The position of the button in the grid layout as a tuple (row, column).
        """
        button = QPushButton("=")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ORANGE};
            }}
            QPushButton:hover {{
                background-color: {HOVER_OPERATOR};
            }}
        """)
        button.setFixedSize(79, 55)
        button.clicked.connect(lambda: self.parent_app.evaluate(equals_button=True))
        self.buttonLayout.addWidget(button, pos[0], pos[1])

        shortcut_enter = QShortcut(QKeySequence(Qt.Key_Enter), self)
        shortcut_enter.activated.connect(lambda: self.parent_app.evaluate(equals_button=True))
        shortcut_return = QShortcut(QKeySequence(Qt.Key_Return), self)
        shortcut_return.activated.connect(lambda: self.parent_app.evaluate(equals_button=True))
        shortcut_equals = QShortcut(QKeySequence("="), self)
        shortcut_equals.activated.connect(lambda: self.parent_app.evaluate(equals_button=True))
