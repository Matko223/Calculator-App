"""
@file: bmi_buttons.py
@brief: This module contains the BMI buttons for the BMI calculator application.

@author: Martin Valapka
"""

from PySide6.QtCore import QSize, Qt, QRegularExpression, QEvent
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)
from bmi.bmi_display import ACTIVE_STYLE, AMOUNT_STYLE
import os

# Color definitions
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class BmiButtons(QWidget):
    """
    @brief A class that represents the BMI buttons widget.
    """
    def __init__(self, calculator, parent=None):
        """
        @brief Initializes the BMI buttons widget.
        @param calculator: The BMI calculator instance that this button widget is connected to.
        @param parent: The parent widget.
        """
        super().__init__(parent)

        self.calculator = calculator
        self.current_input = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.buttonFrame = QFrame()
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(1)
        self.buttonFrameLayout.addLayout(self.buttonLayout)
        
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
            "⌫": (1, 3, 1, 2),
            "C": (2, 3, 1, 2),
            "SWITCH": (3, 3, 1, 2),
            ".": (4, 0),
            "CAL": (4, 3, 2, 2)
        }

        self.create_clear_button()
        self.create_delete_button()

        for digit, (row, col) in self.digits.items():
            self.create_digit_button(digit, row, col)

        self.create_decimal_button()
        self.create_switch_button()
        self.create_calculate_button()

    def set_current_input(self, input_field):
        """
        @brief Sets the current input field that buttons will affect
        @param input_field: The input field to set as current
        """
        self.current_input = input_field

    def create_digit_button(self, digit, row, col):
        """
        @brief Creates a button for a digit.
        @param digit: The digit for the button.
        @param row: The row in the layout to place the button.
        @param col: The column in the layout to place the button.
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
            button.setFixedSize(79 * 2, 55)
        else:
            button.setFixedSize(79, 55)
        button.clicked.connect(lambda _, d=digit: self.append_digit(str(d)))
        self.buttonLayout.addWidget(button, row, col)

        shortcut = QShortcut(QKeySequence(str(digit)), self)
        shortcut.activated.connect(lambda d=digit: self.append_digit(str(d)))

    def create_decimal_button(self):
        """
        @brief Creates a button for the decimal point.
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
        button.clicked.connect(lambda: self.append_digit("."))
        self.buttonLayout.addWidget(button, *self.special_operations["."])

    def create_clear_button(self):
        """
        @brief Creates a button to clear all input fields.
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
        button.clicked.connect(self.clear_input)
        self.buttonLayout.addWidget(button, *self.special_operations["C"])

    def create_switch_button(self):
        """
        @brief Creates a button to switch the current input field.
        """
        button = QPushButton("Switch")
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
        button.clicked.connect(self.switch_input)
        self.buttonLayout.addWidget(button, *self.special_operations["SWITCH"])

    def create_delete_button(self):
        """
        @brief Creates a delete button that removes the last digit from the current input field.
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
        button.clicked.connect(self.delete_digit)
        self.buttonLayout.addWidget(button, *self.special_operations["⌫"])

    def create_calculate_button(self):
        """
        @brief Creates a button for calculating the Body Mass Index (BMI).
        """
        button = QPushButton("CAL")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ORANGE};
            }}
            QPushButton:hover {{
                background-color: {HOVER_OPERATOR};
            }}
        """)
        button.setFixedSize(79 * 2, 55)
        button.clicked.connect(self.calculate_bmi)
        self.buttonLayout.addWidget(button, *self.special_operations["CAL"])

    def append_digit(self, digit):
        """
        @brief Appends a digit to the current input field.
        @param digit: The digit to append to the current input field.
        """
        if not self.current_input:
            self.current_input = self.calculator.current_input
            
        if self.current_input:
            current_text = self.current_input.text()

            if self.current_input in [self.calculator.height_feet_input, self.calculator.height_inches_input]:
                max_length = 1
                if len(current_text) < max_length:
                    if current_text == "" and digit == "0":
                        return
                    if digit == ".":
                        return
                    self.current_input.setText(current_text + digit)
            else:
                if len(current_text) < 5:
                    if current_text == "" and digit == "0":
                        return
                    if digit == ".":
                        if "." in current_text:
                            return
                        if current_text == "":
                            self.current_input.setText("0.")
                            return
                    self.current_input.setText(current_text + digit)

            self.current_input.setFocus()
    
    # Delegations
    def clear_input(self):
        """
        @brief Clears all input fields, resets their styles, and sets the focus to the current input field.
        """
        self.calculator.clear_input()
        
    def delete_digit(self):
        """
        @brief Deletes the last digit from the current input field.
        """
        if not self.current_input:
            self.current_input = self.calculator.current_input
            
        if self.current_input:
            current_text = self.current_input.text()
            self.current_input.setText(current_text[:-1])
            self.current_input.setStyleSheet(ACTIVE_STYLE)
            
    def switch_input(self):
        """
        @brief Switches input focus with proper styling
        """
        self.calculator.switch_input()
        self.current_input = self.calculator.current_input
        
    def calculate_bmi(self):
        """
        @brief Calculates the Body Mass Index (BMI).
        """
        self.calculator.calculate_bmi()
