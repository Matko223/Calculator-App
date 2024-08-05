from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout
)

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
    def __init__(self):
        super().__init__()
        self.result_input = None
        self.displayFrame = None
        self.buttonLayout = None
        self.buttonFrame = None
        self.buttonFrameLayout = None
        self.weight_input = QLineEdit()
        self.height_input = QLineEdit()
        self.height_feet_input = QLineEdit()
        self.height_inches_input = QLineEdit()
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
            "C": (0, 0, 1, 2),
            "⌫": (0, 3, 1, 2),
            ".": (4, 0),
            "CAL": (2, 3, 4, 5),
            "SWITCH": (1, 3, 1, 4)
        }

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
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

    def display_frame(self):
        self.displayFrame = QFrame(self)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")

        layout = QFormLayout(self.displayFrame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(12)

        # Height input
        height_label = QLabel("Height:")
        height_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        self.height_input = QLineEdit()
        self.height_input.setReadOnly(True)
        self.height_input.setStyleSheet(f"""
            background-color: {LIGHT_GRAY};
            border: 2px solid orange;
            border-radius: 5px;
            color: white;
            font-size: 18px;
        """)
        self.height_input.setFixedWidth(200)
        self.height_input.setFixedHeight(30)

        self.height_feet_input = QLineEdit()
        self.height_feet_input.setReadOnly(True)
        self.height_feet_input.setStyleSheet(f"""
            background-color: {LIGHT_GRAY};
            border: 2px solid orange;
            border-radius: 5px;
            color: white;
            font-size: 18px;
        """)
        self.height_feet_input.setFixedWidth(95)
        self.height_feet_input.setFixedHeight(30)

        self.height_inches_input = QLineEdit()
        self.height_inches_input.setReadOnly(True)
        self.height_inches_input.setStyleSheet(f"""
            background-color: {LIGHT_GRAY};
            border: 2px solid orange;
            border-radius: 5px;
            color: white;
            font-size: 18px;
        """)
        self.height_inches_input.setFixedWidth(95)
        self.height_inches_input.setFixedHeight(30)

        self.height_unit_combo = QComboBox()
        self.height_unit_combo.addItems(["cm", "ft"])
        self.height_unit_combo.setStyleSheet(f"""
            background-color: {LIGHT_GRAY};
            border: none;
            border-radius: 5px;
            color: white;
            font-size: 18px;
        """)
        self.height_unit_combo.setFixedWidth(50)
        self.height_unit_combo.currentIndexChanged.connect(self.update_height_inputs)

        # Weight input
        weight_label = QLabel("Weight:")
        weight_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.weight_input = QLineEdit()
        self.weight_input.setReadOnly(True)
        self.weight_input.setStyleSheet(f"""
            background-color: {LIGHT_GRAY};
            border: none;
            border-radius: 5px;
            color: white;
            font-size: 18px;
        """)
        self.weight_input.setFixedWidth(200)
        self.weight_input.setFixedHeight(30)

        self.weight_unit_combo = QComboBox()
        self.weight_unit_combo.addItems(["kg", "lb"])
        self.weight_unit_combo.setStyleSheet(f"""
            background-color: {LIGHT_GRAY};
            border: none;
            border-radius: 5px;
            color: white;
            font-size: 18px;
        """)
        self.weight_unit_combo.setFixedWidth(50)

        # Result label and input
        result_label = QLabel("BMI:")
        result_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)
        self.result_input.setStyleSheet(f"""
            background-color: {LIGHT_GRAY};
            border: none;
            border-radius: 5px;
            color: white;
            font-size: 18px;
        """)
        self.result_input.setFixedWidth(200)
        self.result_input.setFixedHeight(30)

        # Create layouts for height and weight fields
        height_layout = QHBoxLayout()
        height_layout.addWidget(self.height_feet_input)
        height_layout.addWidget(self.height_inches_input)
        height_layout.addWidget(self.height_input)
        height_layout.addWidget(self.height_unit_combo)

        weight_layout = QHBoxLayout()
        weight_layout.addWidget(self.weight_input)
        weight_layout.addWidget(self.weight_unit_combo)

        # Add widgets to the form layout
        layout.addRow(height_label, height_layout)
        layout.addRow(weight_label, weight_layout)
        layout.addRow(result_label, self.result_input)

        self.update_height_inputs()  # Initialize layout based on default unit

        self.current_input = self.height_input

        return self.displayFrame

    def button_frame(self):
        self.buttonFrame = QFrame()
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(1)
        self.buttonFrameLayout.addLayout(self.buttonLayout)

        # Add clear button at the top
        clear_button = self.create_clear_button()
        self.buttonLayout.addWidget(clear_button, *self.special_operations["C"])

        # Add delete button
        delete_button = self.create_delete_button()
        self.buttonLayout.addWidget(delete_button, *self.special_operations["⌫"])

        # Create and add digit buttons
        for digit, (row, col) in self.digits.items():
            button = self.create_digit_button(digit)
            self.buttonLayout.addWidget(button, row, col)

        # Add decimal point button
        decimal_button = self.create_decimal_button()
        self.buttonLayout.addWidget(decimal_button, *self.special_operations["."])

        # Add switch button at the bottom
        switch_button = self.create_switch_button()
        self.buttonLayout.addWidget(switch_button, *self.special_operations["SWITCH"])

        # Add calculate button
        calculate_button = self.create_calculate_button()
        self.buttonLayout.addWidget(calculate_button, *self.special_operations["CAL"])
        return self.buttonFrame

    def create_digit_button(self, digit):
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
        return button

    def create_decimal_button(self):
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
        return button

    def create_clear_button(self):
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
        button.setFixedSize(79 * 3, 55)
        button.clicked.connect(self.clear_input)
        return button

    def create_switch_button(self):
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
        return button

    def create_delete_button(self):
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
        return button

    def create_calculate_button(self):
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
        button.setFixedSize(79 * 2, 55 * 3)
        button.clicked.connect(self.calculate_bmi)
        return button

    def append_digit(self, digit):
        if self.current_input:
            current_text = self.current_input.text()
            if len(current_text) < 3:
                if current_text == "" and digit == "0":
                    return
                if digit == ".":
                    if "." in current_text:
                        return
                    if current_text == "" or current_text.startswith("0"):
                        return
                self.current_input.setText(current_text + digit)

    def clear_input(self):
        self.height_input.clear()
        self.weight_input.clear()
        self.result_input.clear()
        self.height_feet_input.clear()
        self.height_inches_input.clear()

        self.update_height_inputs()

    def delete_digit(self):
        if self.current_input:
            current_text = self.current_input.text()
            self.current_input.setText(current_text[:-1])

    def switch_input(self):
        if self.current_input:
            self.current_input.setStyleSheet(f"background-color: {LIGHT_GRAY}; border: none; border-radius: 5px; "
                                             f"color: white; font-size: 18px;")
        if self.current_input == self.height_input:
            self.current_input = self.weight_input
        else:
            self.current_input = self.height_input
        self.current_input.setStyleSheet(
            f"background-color: {LIGHT_GRAY}; border: 2px solid orange; border-radius: 5px; "
            f"color: white; font-size: 18px;")
        self.current_input.setFocus()

    def switch_input_event(self, event):
        self.switch_input()
        event.accept()

    def update_height_inputs(self):
        if self.height_unit_combo.currentText() == "ft":
            self.height_input.hide()
            self.height_feet_input.show()
            self.height_inches_input.show()
        else:
            self.height_input.show()
            self.height_feet_input.hide()
            self.height_inches_input.hide()

    def calculate_bmi(self):
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
