"""
@file: expression_buttons.py
@brief: This module provides buttons for the calculator application.

@author: Martin Valapka
"""

import re
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, \
    QLineEdit, QStackedLayout, QLineEdit
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QIcon, QRegularExpressionValidator
from PySide6.QtCore import Qt, QSize, QRegularExpression
import math

# Color definitions
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class ExpressionButtons(QWidget):
    """
    @brief A class that represents buttons for mathematical expressions.
    """
    def __init__(self, parent=None):
        """
        @brief Initializes the ExpressionButtons widget.
        @param parent: The parent widget.
        """
        super().__init__(parent)
        self.parent_widget = parent

        # Initialize dictionaries for digits, operations, special operations, and brackets
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

        self.operations = {
            "/": "\u00F7",
            "*": "\u00D7",
            "-": "-",
            "+": "+"
        }

        self.special_operations = {
            "x²": (0, 0),
            "C": (0, 3),
            "⌫": (0, 4),
            "√": (1, 0),
            "!": (2, 0),
            "|x|": (3, 0),
            "π": (4, 0),
            ".": (4, 1),
            "=": (4, 3)
        }

        self.brackets = {
            "(": (0, 1),
            ")": (0, 2)
        }
        
        buttonFrame = QWidget(self)
        buttonFrame.setFixedHeight(280)
        buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrameLayout = QVBoxLayout(buttonFrame)
        self.buttonFrameLayout.setContentsMargins(3, 3, 3, 3)

        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonFrameLayout.addLayout(self.buttonLayout)
        buttonFrame.setLayout(self.buttonFrameLayout)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_bracket_buttons()

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
            button.clicked.connect(lambda _, d=digit: self.parent_widget.show_numbers(d))
            self.buttonLayout.addWidget(button, pos[0], pos[1])

            shortcut = QShortcut(QKeySequence(str(digit)), self)
            shortcut.activated.connect(lambda d=digit: self.parent_widget.show_numbers(d))

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
            button.clicked.connect(lambda _, op=operator: self.parent_widget.show_operators(op))
            self.buttonLayout.addWidget(button, pos[0], pos[1])

            shortcut = QShortcut(QKeySequence(operator), self)
            shortcut.activated.connect(lambda op=operator: self.parent_widget.show_operators(op))

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
            elif operation == "π":
                self.create_pi_button(pos)
            elif operation == ".":
                self.create_decimal_button(pos)
            elif operation == "=":
                self.create_equals_button(pos)

    def create_bracket_buttons(self):
        """
        @brief Creates and configures buttons for brackets
        """
        for bracket, pos in self.brackets.items():
            button = QPushButton(bracket)
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
            button.clicked.connect(lambda _, b=bracket: self.parent_widget.show_brackets(b))
            self.buttonLayout.addWidget(button, pos[0], pos[1])

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
        button.clicked.connect(self.parent_widget.handle_exponentiation)
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
        button.setFixedSize(79, 55)
        button.clicked.connect(self.parent_widget.handle_clear)
        self.buttonLayout.addWidget(button, pos[0], pos[1])
        shortcut_clear = QShortcut(QKeySequence("C"), self)
        shortcut_clear.activated.connect(self.parent_widget.handle_clear)

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
        button.setFixedSize(79, 55)
        button.clicked.connect(self.parent_widget.handle_delete)
        self.buttonLayout.addWidget(button, pos[0], pos[1])
        shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), self)
        shortcut.activated.connect(self.parent_widget.handle_delete)

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
        button.clicked.connect(self.parent_widget.handle_root)
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
        button.clicked.connect(self.parent_widget.handle_factorial)
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
        button.clicked.connect(self.parent_widget.handle_absolute_value)
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_pi_button(self, pos):
        """
        @brief Creates and configures the button for pi operation (π).
        @param pos: Position of the button in the grid layout as a tuple (row, column).
        """
        button = QPushButton("π")
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
        button.clicked.connect(self.parent_widget.handle_pi)
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
        button.clicked.connect(self.parent_widget.handle_decimal_point)
        self.buttonLayout.addWidget(button, pos[0], pos[1])
        shortcut_decimal = QShortcut(QKeySequence(Qt.Key_Period), self)
        shortcut_decimal.activated.connect(self.parent_widget.handle_decimal_point)

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
        button.clicked.connect(self.parent_widget.calculate)
        self.buttonLayout.addWidget(button, pos[0], pos[1])
