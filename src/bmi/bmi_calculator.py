"""
@file bmi_calculator.py
@brief File containing BMI calculation mode for the calculator application.

@author Martin Valapka (xvalapm00)
@date 10.09. 2024
"""

from PySide6.QtCore import QSize, Qt, QRegularExpression, QEvent
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)
from bmi.bmi_display import BmiDisplay, ACTIVE_STYLE, AMOUNT_STYLE
from bmi.bmi_buttons import BmiButtons
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


class BMICalculator(QWidget):
    """
    @brief A class that represents a Body Mass Index (BMI) calculator.
    """

    def __init__(self):
        """
        @brief Initializes the BMICalculator class.
        """
        super().__init__()
        self.mode_menu_button = None
        self.help_menu_button = None
        self.help_window = None
        
        self.displayFrame = BmiDisplay()
        
        self.height_input = self.displayFrame.height_input
        self.weight_input = self.displayFrame.weight_input
        self.height_feet_input = self.displayFrame.height_feet_input
        self.height_inches_input = self.displayFrame.height_inches_input
        self.result_input = self.displayFrame.result_input
        self.height_unit_combo = self.displayFrame.height_unit_combo
        self.weight_unit_combo = self.displayFrame.weight_unit_combo
        
        self.current_input = self.height_input
        
        self.buttonPanel = BmiButtons(self)
        self.buttonFrame = self.buttonPanel.buttonFrame

        self.init_ui()
        
        for input_field in [
            self.height_input, self.weight_input,
            self.height_feet_input, self.height_inches_input,
            self.result_input
        ]:
            input_field.installEventFilter(self.displayFrame)

    def init_ui(self):
        """
        @brief Initializes the user interface of the calculator.
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        input_layout = QVBoxLayout()
        input_layout.setSpacing(0)
        input_layout.addWidget(self.displayFrame, 1)
        input_layout.addWidget(self.buttonFrame, 1)
        layout.addLayout(input_layout)
        
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)
        
        self.buttonPanel.current_input = self.current_input

    def append_digit(self, digit):
        """
        @brief Appends a digit to the current input field.
        @param digit: The digit to append to the current input field.
        """
        if self.current_input:
            current_text = self.current_input.text()

            # Special handling for feet and inches inputs
            if self.current_input in [self.height_feet_input, self.height_inches_input]:
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

    def clear_input(self):
        """
        @brief Clears all input fields, resets their styles, and sets the focus to the current input field.
        """
        self.height_input.clear()
        self.weight_input.clear()
        self.result_input.clear()
        self.height_feet_input.clear()
        self.height_inches_input.clear()

        if self.height_unit_combo.currentText() == "cm":
            self.current_input = self.height_input
        else:
            self.current_input = self.height_feet_input

        for input_field in [self.height_input, self.height_feet_input,
                            self.height_inches_input, self.weight_input]:
            input_field.setStyleSheet(AMOUNT_STYLE)

        self.current_input.setStyleSheet(ACTIVE_STYLE)
        self.result_input.setStyleSheet(AMOUNT_STYLE)
        self.current_input.setFocus()        
        self.buttonPanel.current_input = self.current_input

    def delete_digit(self):
        """
        @brief Deletes the last digit from the current input field.
        """
        if self.current_input:
            current_text = self.current_input.text()
            self.current_input.setText(current_text[:-1])
            self.current_input.setStyleSheet(ACTIVE_STYLE)

    def switch_input(self):
        """
        @brief Switches input focus with proper styling
        """
        for input_field in [self.height_input, self.height_feet_input,
                            self.height_inches_input, self.weight_input]:
            input_field.setStyleSheet(AMOUNT_STYLE)

        self.result_input.setText("")

        if self.height_unit_combo.currentText() == "ft":
            if self.current_input == self.height_feet_input:
                self.current_input = self.height_inches_input
            elif self.current_input == self.height_inches_input:
                self.current_input = self.weight_input
            else:
                self.current_input = self.height_feet_input
        else:
            if self.current_input == self.height_input:
                self.current_input = self.weight_input
            else:
                self.current_input = self.height_input

        self.current_input.setStyleSheet(ACTIVE_STYLE)
        self.current_input.setFocus(Qt.MouseFocusReason)
        
        self.buttonPanel.current_input = self.current_input

    def switch_input_event(self, event):
        """
        @brief Handles the event of switching input fields.
        @param event: The event that triggers the switch.
        """
        self.switch_input()
        event.accept()

    def update_height_inputs(self):
        """
        @brief Updates the height inputs based on the selected height unit.
        """
        if self.height_unit_combo.currentText() == "ft":
            self.height_input.hide()
            self.height_feet_input.show()
            self.height_inches_input.show()
            self.current_input = self.height_feet_input
            self.height_feet_input.setStyleSheet(ACTIVE_STYLE)
            self.height_inches_input.setStyleSheet(AMOUNT_STYLE)
            self.height_feet_input.setFocus()
        else:
            self.height_input.show()
            self.height_feet_input.hide()
            self.height_inches_input.hide()
            self.current_input = self.height_input
            self.height_input.setStyleSheet(ACTIVE_STYLE)
            self.height_input.setFocus()

        self.weight_input.setStyleSheet(AMOUNT_STYLE)
        self.buttonPanel.current_input = self.current_input

    def calculate_bmi(self):
        """
        @brief Calculates the Body Mass Index (BMI).
        """
        try:
            height_unit = self.height_unit_combo.currentText()
            weight_unit = self.weight_unit_combo.currentText()

            if height_unit == "ft":
                feet = float(self.height_feet_input.text()) if self.height_feet_input.text() else 0
                inches = float(self.height_inches_input.text()) if self.height_inches_input.text() else 0
                height = feet * 0.3048 + inches * 0.0254
            else:
                height = float(self.height_input.text()) / 100

            if weight_unit == "lb":
                weight = float(self.weight_input.text()) * 0.453592
            else:
                weight = float(self.weight_input.text())

            bmi = weight / (height * height)
            self.result_input.setText(f"{bmi:.2f}")
        except ValueError:
            self.result_input.setText("Invalid input")
        except ZeroDivisionError:
            self.result_input.setText("Height cannot be 0")
