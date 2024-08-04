# bmi_calculator.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class BMICalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.result_label = QLabel()
        self.weight_input = QLineEdit()
        self.height_input = QLineEdit()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("BMI Mode")
        layout.addWidget(label)

        self.weight_input.setPlaceholderText("Enter your weight in kg")
        layout.addWidget(self.weight_input)

        self.height_input.setPlaceholderText("Enter your height in cm")
        layout.addWidget(self.height_input)

        calculate_button = QPushButton("Calculate BMI")
        calculate_button.clicked.connect(self.calculate_bmi)
        layout.addWidget(calculate_button)

        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate_bmi(self):
        try:
            height = float(self.height_input.text()) / 100
            weight = float(self.weight_input.text())
            bmi = weight / (height * height)
            self.result_label.setText(f"Your BMI is: {bmi:.2f}")
        except ValueError:
            self.result_label.setText("Please enter valid numbers.")
