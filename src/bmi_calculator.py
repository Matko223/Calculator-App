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
from img_path import resource_path
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
        self.result_input = None
        self.displayFrame = None
        self.buttonLayout = None
        self.buttonFrame = None
        self.buttonFrameLayout = None

        self.weight_input = QLineEdit()
        self.weight_input.setReadOnly(True)

        self.height_input = QLineEdit()
        self.height_input.setReadOnly(True)

        self.height_feet_input = QLineEdit()
        self.height_feet_input.setReadOnly(True)

        self.height_inches_input = QLineEdit()
        self.height_inches_input.setReadOnly(True)

        self.height_unit_combo = QComboBox()
        self.weight_unit_combo = QComboBox()
        self.current_input = None

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
        self.init_ui()

    def init_ui(self):
        """
        @brief Initializes the user interface of the calculator.
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(0)
        input_layout.addWidget(self.display_frame())
        input_layout.addWidget(self.button_frame())
        layout.addLayout(input_layout)

        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        arrow_icon_path = resource_path(os.path.join('Pictures', '60995.png'))
        arrow_icon_path = arrow_icon_path.replace('\\', '/')

        combobox_style = """
        QComboBox {
            color: white;
            background-color: #4F4F4F;
            font-size: 16px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            font-weight: bold;
            padding: 5px;
        }
        QComboBox:on {
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
        }
        QComboBox::drop-down {
            width: 20px;
            border-left-width: 0px;
            border-top-right-radius: 10px;
        }
        QComboBox::down-arrow {
            image: url(""" + arrow_icon_path + """);
            width: 12px;
            height: 12px;
        }
        QComboBox QAbstractItemView {
            color: white;
            background-color: #4F4F4F;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            outline: none;
        }
        QComboBox QAbstractItemView::item {
            padding: 3px;
            background-color: transparent;
            border-left: 2px solid transparent;
        }
        QComboBox QAbstractItemView::item:hover {
            background-color: transparent;
            border-left: 2px solid #FFA500;
        }
        """

        self.height_unit_combo.setStyleSheet(combobox_style)
        self.height_unit_combo.setFixedSize(70, 30)

        self.weight_unit_combo.setStyleSheet(combobox_style)
        self.weight_unit_combo.setFixedSize(70, 30)

        self.setup_input_validation(self.height_input)
        self.setup_input_validation(self.weight_input)
        self.setup_input_validation(self.height_feet_input)
        self.setup_input_validation(self.height_inches_input)

        for input_field in [self.height_input, self.weight_input,
                            self.height_feet_input, self.height_inches_input,
                            self.result_input]:
            input_field.installEventFilter(self)

    def eventFilter(self, obj, event):
        """
        @brief Only block direct mouse interaction with text fields
        """
        if obj in [self.height_input, self.weight_input,
                   self.height_feet_input, self.height_inches_input,
                   self.result_input]:
            if event.type() in [QEvent.MouseButtonPress,
                                QEvent.MouseButtonDblClick]:
                if self.current_input:
                    self.current_input.setFocus()
                return True
        return super().eventFilter(obj, event)

    def display_frame(self):
        """
        @brief Creates the display frame for the calculator.
        """
        self.displayFrame = QFrame(self)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")

        # Use QGridLayout for the main layout
        layout = QGridLayout(self.displayFrame)
        layout.setContentsMargins(20, 10, 10, 10)
        layout.setHorizontalSpacing(5)
        layout.setVerticalSpacing(8)

        # Add spacer item to push widgets to the right
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer, 0, 0)

        amount_style = """
        QLineEdit {
            color: white;
            background-color: #4F4F4F;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
            padding: 5px;
        }
        """

        # Height input
        height_label = QLabel("Height:")
        height_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(height_label, 0, 1, Qt.AlignRight | Qt.AlignVCenter)

        height_layout = QHBoxLayout()
        height_layout.setSpacing(5)

        self.height_input = QLineEdit()
        self.height_input.setFixedWidth(200)
        self.height_input.setFixedHeight(30)

        self.height_feet_input = QLineEdit()
        self.height_feet_input.setFixedWidth(97)
        self.height_feet_input.setFixedHeight(30)
        self.height_feet_input.setPlaceholderText("Feet")

        self.height_inches_input = QLineEdit()
        self.height_inches_input.setFixedWidth(97)
        self.height_inches_input.setFixedHeight(30)
        self.height_inches_input.setPlaceholderText("Inches")

        self.height_unit_combo = QComboBox()
        self.height_unit_combo.addItems(["cm", "ft"])
        self.height_unit_combo.setFixedWidth(50)
        self.height_unit_combo.currentIndexChanged.connect(self.update_height_inputs)

        height_layout.addWidget(self.height_input)
        height_layout.addWidget(self.height_feet_input)
        height_layout.addWidget(self.height_inches_input)
        height_layout.addWidget(self.height_unit_combo)

        layout.addLayout(height_layout, 0, 2, Qt.AlignLeft | Qt.AlignVCenter)

        # Weight input
        weight_label = QLabel("Weight:")
        weight_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(weight_label, 1, 1, Qt.AlignRight | Qt.AlignVCenter)

        weight_layout = QHBoxLayout()
        weight_layout.setSpacing(5)

        self.weight_input = QLineEdit()
        self.weight_input.setFixedWidth(200)
        self.weight_input.setFixedHeight(30)

        self.weight_unit_combo = QComboBox()
        self.weight_unit_combo.addItems(["kg", "lb"])
        self.weight_unit_combo.setFixedWidth(50)

        weight_layout.addWidget(self.weight_input)
        weight_layout.addWidget(self.weight_unit_combo)

        layout.addLayout(weight_layout, 1, 2, Qt.AlignLeft | Qt.AlignVCenter)

        # Result input
        result_label = QLabel("BMI:")
        result_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(result_label, 2, 1, Qt.AlignRight | Qt.AlignVCenter)

        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)
        self.result_input.setStyleSheet(amount_style)
        self.result_input.setFixedWidth(200)
        self.result_input.setFixedHeight(30)

        layout.addWidget(self.result_input, 2, 2, Qt.AlignLeft | Qt.AlignVCenter)

        self.update_height_inputs()

        if self.height_unit_combo.currentText() == "cm":
            self.current_input = self.height_input
        else:
            self.current_input = self.height_feet_input

        return self.displayFrame

    def button_frame(self):
        """
        @brief Creates the frame for the buttons of the calculator.
        """
        self.buttonFrame = QFrame()
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(1)
        self.buttonFrameLayout.addLayout(self.buttonLayout)

        self.create_clear_button()
        self.create_delete_button()

        for digit, (row, col) in self.digits.items():
            self.create_digit_button(digit, row, col)

        self.create_decimal_button()
        self.create_switch_button()
        self.create_calculate_button()

        return self.buttonFrame

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
        shortcut.activated.connect(lambda d=digit: self.append_digit(d))

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

    def setup_input_validation(self, input_widget):
        """
        @brief Sets up input validation for the given QLineEdit widget.
        @param input_widget: The QLineEdit widget to set up validation for.
        """
        regex = QRegularExpression(r'^(?=.{0,5}$)\d*(\.?\d*)?$')
        validator = QRegularExpressionValidator(regex)
        input_widget.setValidator(validator)

    def clear_input(self):
        """
        @brief Clears all input fields, resets their styles, and sets the focus to the current input field.
        """
        amount_style = """
        QLineEdit {
            color: white;
            background-color: #4F4F4F;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
            padding: 5px;
        }
        """

        active_style = """
        QLineEdit {
            color: white;
            background-color: #4F4F4F;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
            padding: 5px;
            border: 2px solid orange;
        }
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
            input_field.setStyleSheet(amount_style)

        self.current_input.setStyleSheet(active_style)
        self.current_input.setFocus()

    def delete_digit(self):
        """
        @brief Deletes the last digit from the current input field.
        """
        if self.current_input:
            current_text = self.current_input.text()
            self.current_input.setText(current_text[:-1])

    def switch_input(self):
        """
        @brief Switches input focus with proper styling
        """
        amount_style = """
        QLineEdit {
            color: white;
            background-color: #4F4F4F;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
            padding: 5px;
        }
        """

        active_style = """
        QLineEdit {
            color: white;
            background-color: #4F4F4F;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
            padding: 5px;
            border: 2px solid orange;
        }
        """

        # Reset all input field styles
        for input_field in [self.height_input, self.height_feet_input,
                            self.height_inches_input, self.weight_input]:
            input_field.setStyleSheet(amount_style)

        # Clear result
        self.result_input.setText("")

        # Update current input based on mode
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

        # Highlight current input
        self.current_input.setStyleSheet(active_style)
        self.current_input.setFocus(Qt.MouseFocusReason)

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
        amount_style = """
        QLineEdit {
            color: white;
            background-color: #4F4F4F;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
            padding: 5px;
        }
        """

        active_style = """
        QLineEdit {
            color: white;
            background-color: #4F4F4F;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
            padding: 5px;
            border: 2px solid orange;
        }
        """

        if self.height_unit_combo.currentText() == "ft":
            self.height_input.hide()
            self.height_feet_input.show()
            self.height_inches_input.show()
            self.current_input = self.height_feet_input
            self.height_feet_input.setStyleSheet(active_style)
            self.height_inches_input.setStyleSheet(amount_style)
            self.height_feet_input.setFocus()
        else:
            self.height_input.show()
            self.height_feet_input.hide()
            self.height_inches_input.hide()
            self.current_input = self.height_input
            self.height_input.setStyleSheet(active_style)
            self.height_input.setFocus()

        self.weight_input.setStyleSheet(amount_style)

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
