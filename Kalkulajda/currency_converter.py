"""
@file currency_converter.py
@brief File containing Currency converter mode for the calculator application.

@author Martin Valapka (xvalapm00)
@date 17.09. 2024
"""

from PySide6.QtCore import QSize, Qt, QRegularExpression
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)
from datetime import datetime, date
import flag

# Color definitions
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.flag2_label = None
        self.flag1_label = None
        self.input_layout = None
        self.currency2 = None
        self.currency1 = None
        self.mainLayout = None
        self.buttonLayout = None
        self.buttonFrameLayout = None
        self.buttonFrame = None
        self.displayFrame = None
        self.amount = None
        self.currency = None
        self.amount1 = None
        self.amount2 = None

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

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {DARK_GRAY}; color: white;")

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.display_frame()
        self.mainLayout.addWidget(self.displayFrame)

        self.button_frame()
        self.mainLayout.addWidget(self.buttonFrame)

    def display_frame(self):
        self.displayFrame = QFrame(self)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")
        self.displayFrame.setFixedHeight(180)

        frame_layout = QGridLayout(self.displayFrame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        input_widget = QWidget()
        self.input_layout, self.currency1, self.currency2, self.amount1, self.amount2 = self.create_input_layout()
        input_widget.setLayout(self.input_layout)
        frame_layout.addWidget(input_widget, 0, 0, Qt.AlignLeft)

    def create_input_layout(self):
        input_layout = QGridLayout()
        input_layout.setSpacing(5)
        input_layout.setAlignment(Qt.AlignTop)
        input_layout.setContentsMargins(10, 40, 10, 10)

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
            image: url(./Pictures/60995.png);
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

        # First row: first currency and amount
        currency1 = QComboBox()
        currency1.setStyleSheet(combobox_style)
        currency1.setFixedSize(120, 40)
        currency1.addItems(["USD", "EUR", "GBP", "JPY"])

        amount1 = QLineEdit()
        amount1.setStyleSheet(amount_style)
        amount1.setFixedSize(180, 40)
        amount1.setPlaceholderText("Amount")

        self.flag1_label = QLabel()
        self.flag1_label.setFixedSize(30, 30)

        # Second row: second currency and amount
        currency2 = QComboBox()
        currency2.setStyleSheet(combobox_style)
        currency2.setFixedSize(120, 40)
        currency2.addItems(["USD", "EUR", "GBP", "JPY"])

        amount2 = QLineEdit()
        amount2.setStyleSheet(amount_style)
        amount2.setFixedSize(180, 40)
        amount2.setPlaceholderText("Converted Amount")
        amount2.setReadOnly(True)

        self.flag2_label = QLabel()
        self.flag2_label.setFixedSize(30, 30)

        # Add widgets to the grid layout
        input_layout.addWidget(currency1, 0, 0)
        input_layout.addWidget(self.flag1_label, 0, 1)
        input_layout.addWidget(amount1, 0, 2)
        input_layout.addWidget(currency2, 1, 0)
        input_layout.addWidget(self.flag2_label, 1, 1)
        input_layout.addWidget(amount2, 1, 2)

        regex = QRegularExpression(r"^\d{1,15}(\.\d*)?$")
        validator = QRegularExpressionValidator(regex, amount1)
        amount1.setValidator(validator)

        currency1.currentTextChanged.connect(lambda: self.update_flag(currency1, self.flag1_label))
        currency2.currentTextChanged.connect(lambda: self.update_flag(currency2, self.flag2_label))
        self.update_flag(currency1, self.flag1_label)
        self.update_flag(currency2, self.flag2_label)
        return input_layout, currency1, currency2, amount1, amount2

    def update_flag(self, currency_combo, flag_label):
        currency = currency_combo.currentText()
        flag_map = {
            "USD": "US",
            "EUR": "EU",
            "GBP": "GB",
            "JPY": "JP"
        }
        country_code = flag_map.get(currency, "")
        flag_emoji = flag.flag(country_code)
        flag_label.setText(flag_emoji)
        flag_label.setFont(QFont("Segoe UI Emoji", 16))

    def button_frame(self):
        """
        @brief Creates the frame for the buttons of the calculator.
        """
        self.buttonFrame = QFrame()
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrame.setFixedHeight(225)

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
        self.create_convert_button()

        return self.buttonFrame

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
        button.setFixedSize(79 * 2, 55)
        button.clicked.connect(self.clear_input)
        self.buttonLayout.addWidget(button, *self.special_operations["C"])

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
        self.buttonLayout.addWidget(button, *self.special_operations["⌫"])

    def create_digit_button(self, digit, row, col):
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

    def create_convert_button(self):
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
        button.setFixedSize(79 * 2, 55 * 2)
        button.clicked.connect(self.convert_currency)
        self.buttonLayout.addWidget(button, *self.special_operations["CONVERT"])

    def clear_input(self):
        pass

    def delete_digit(self):
        pass

    def append_digit(self, param):
        pass

    def convert_currency(self):
        pass
