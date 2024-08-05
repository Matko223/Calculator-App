from PySide6.QtGui import QKeySequence, QShortcut, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout

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
        self.buttonLayout = None
        self.buttonFrame = None
        self.buttonFrameLayout = None
        self.result_label = QLabel()
        self.weight_input = QLineEdit()
        self.height_input = QLineEdit()
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

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.display_frame())
        input_layout.addWidget(self.button_frame())
        layout.addLayout(input_layout)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def display_frame(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        self.height_input.setPlaceholderText("Height (cm):")
        self.height_input.setReadOnly(True)
        layout.addWidget(self.height_input)

        self.weight_input.setPlaceholderText("Weight (kg):")
        self.weight_input.setReadOnly(True)
        layout.addWidget(self.weight_input)

        return frame

    def button_frame(self):
        self.buttonFrame = QFrame()
        self.buttonFrame.setFixedHeight(280)
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(3, 3, 3, 3)
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
        decimal_button = self.create_digit_button(".")
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
            button.setFixedSize(158, 55)
        else:
            button.setFixedSize(79, 55)
        button.clicked.connect(lambda _, d=digit: self.append_digit(str(d)))
        return button

    def create_clear_button(self):
        button = QPushButton("C")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_GRAY};
            }}
            QPushButton:hover {{
                background-color: {GRAY};
            }}
        """)
        button.setFixedSize(79*3, 55)
        button.clicked.connect(self.clear_input)
        return button

    def create_switch_button(self):
        button = QPushButton("Switch")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_GRAY};
            }}
            QPushButton:hover {{
                background-color: {GRAY};
            }}
        """)
        button.setFixedSize(79*2, 55)
        button.clicked.connect(self.switch_input)
        return button

    def create_delete_button(self):
        button = QPushButton("⌫")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_GRAY};
            }}
            QPushButton:hover {{
                background-color: {GRAY};
            }}
        """)
        button.setFixedSize(79*2, 55)
        button.clicked.connect(self.delete_digit)
        return button

    def create_calculate_button(self):
        button = QPushButton("CAL")
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_GRAY};
            }}
            QPushButton:hover {{
                background-color: {GRAY};
            }}
        """)
        button.setFixedSize(79*2, 55*3)
        button.clicked.connect(self.calculate_bmi)
        return button

    def append_digit(self, digit):
        if self.current_input:
            current_text = self.current_input.text()
            self.current_input.setText(current_text + digit)

    def clear_input(self):
        if self.current_input:
            self.current_input.clear()

    def delete_digit(self):
        if self.current_input:
            current_text = self.current_input.text()
            self.current_input.setText(current_text[:-1])

    def switch_input(self):
        if self.current_input == self.height_input:
            self.current_input = self.weight_input
        else:
            self.current_input = self.height_input
        self.current_input.setFocus()

    def calculate_bmi(self):
        try:
            height = float(self.height_input.text()) / 100
            weight = float(self.weight_input.text())
            bmi = weight / (height * height)
            self.result_label.setText(f"Your BMI is: {bmi:.2f}")
        except ValueError:
            self.result_label.setText("Please enter valid numbers.")
        except ZeroDivisionError:
            self.result_label.setText("Height cannot be 0.")
