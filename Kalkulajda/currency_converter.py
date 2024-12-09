"""
@file currency_converter.py
@brief File containing Currency converter mode for the calculator application.

@author Martin Valapka (xvalapm00)
@date 17.09. 2024
"""

from PySide6.QtCore import QSize, Qt, QRegularExpression
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator, QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)
from currency_api import get_exchange_rate, get_supported_currencies, get_currency_name, get_flag_image

# TODO: DIFFERENT LAYOUT

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
    """
    @brief Class representing the currency converter mode of the calculator
    """

    def __init__(self):
        """
        @brief Initializes the currency converter class
        """
        super().__init__()
        self.flag1_label = None
        self.flag2_label = None
        self.eu_flag_path = (r"C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\european"
                             r"-union.png")
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
        self.currency_list = get_supported_currencies()
        self.currency_names = get_currency_name()

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
        """
        @brief Sets up the UI of the currency converter
        """
        self.setStyleSheet(f"background-color: {DARK_GRAY}; color: white;")

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.display_frame()
        self.mainLayout.addWidget(self.displayFrame)

        self.button_frame()
        self.mainLayout.addWidget(self.buttonFrame)

    def display_frame(self):
        """
        @brief Creates the frame for the display of the calculator.
        """
        self.displayFrame = QFrame(self)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")
        self.displayFrame.setFixedHeight(225)

        frame_layout = QGridLayout(self.displayFrame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        input_widget = QWidget()
        self.input_layout, self.currency1, self.currency2, self.amount1, self.amount2 = self.create_input_layout()
        input_widget.setLayout(self.input_layout)
        frame_layout.addWidget(input_widget, 0, 0, Qt.AlignLeft)

    def create_input_layout(self):
        """
        @brief Creates the layout for the input fields
        """
        input_layout = QGridLayout()
        input_layout.setSpacing(3)
        input_layout.setAlignment(Qt.AlignTop)
        input_layout.setContentsMargins(5, 35, 5, 7)

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
            font-family: 'Consolas';
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
        currency1.setFixedSize(320, 40)
        currency1.addItems([f"{code} | {name}" for code, name in self.currency_names])

        amount1 = QLineEdit()
        amount1.setStyleSheet(amount_style)
        amount1.setFixedSize(320, 40)
        amount1.setPlaceholderText("Amount")

        shuffle_button = QPushButton()
        shuffle_button.setFont(QFont("Arial", 20))
        shuffle_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #4F4F4F;
                border-radius: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {DARK_GRAY};
            }}
        """)
        icon = QIcon("./Pictures/shuffle.png")
        shuffle_button.setIcon(icon)
        shuffle_button.setIconSize(QSize(30, 30))
        shuffle_button.setFixedSize(40, 40)
        # shuffle_button.clicked.connect(self.shuffle_currencies)

        # Second row: second currency and amount
        currency2 = QComboBox()
        currency2.setStyleSheet(combobox_style)
        currency2.setFixedSize(320, 40)
        currency2.addItems([f"{code} | {name}" for code, name in self.currency_names])

        amount2 = QLineEdit()
        amount2.setStyleSheet(amount_style)
        amount2.setFixedSize(320, 40)
        amount2.setPlaceholderText("Converted Amount")
        amount2.setReadOnly(True)

        # Create flag labels
        self.flag1_label = QLabel()
        self.flag1_label.setFixedSize(50, 35)
        self.flag2_label = QLabel()
        self.flag2_label.setFixedSize(50, 35)

        # Create horizontal layouts for currency+flag combinations
        currency1_layout = QHBoxLayout()
        currency1_layout.addWidget(self.flag1_label)
        currency1_layout.addSpacing(5)
        currency1_layout.addWidget(currency1)
        currency1_layout.setAlignment(Qt.AlignLeft)

        # Create horizontal layout for amount1 and shuffle button
        amount1_layout = QHBoxLayout()
        amount1_layout.addWidget(amount1)
        amount1_layout.addWidget(shuffle_button)
        amount1_layout.setSpacing(5)
        amount1_layout.setAlignment(Qt.AlignLeft)

        currency2_layout = QHBoxLayout()
        currency2_layout.addWidget(self.flag2_label)
        currency2_layout.addSpacing(5)
        currency2_layout.addWidget(currency2)
        currency2_layout.setAlignment(Qt.AlignLeft)

        # Add layouts to the grid
        input_layout.addLayout(currency1_layout, 0, 0)
        input_layout.addLayout(amount1_layout, 1, 0)

        # Add vertical spacer
        spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        input_layout.addItem(spacer, 2, 0)

        input_layout.addLayout(currency2_layout, 3, 0)
        input_layout.addWidget(amount2, 4, 0)

        currency1.currentIndexChanged.connect(lambda: self.update_flag(currency1, self.flag1_label))
        currency2.currentIndexChanged.connect(lambda: self.update_flag(currency2, self.flag2_label))

        self.update_flag(currency1, self.flag1_label)
        self.update_flag(currency2, self.flag2_label)

        regex = QRegularExpression(r"^\d{1,15}(\.\d*)?$")
        validator = QRegularExpressionValidator(regex, amount1)
        amount1.setValidator(validator)

        return input_layout, currency1, currency2, amount1, amount2

    def update_flag(self, combo_box, flag_label):
        """
        @brief Updates the flag image based on the selected currency
        @param combo_box: The QComboBox containing the currency selection
        @param flag_label: The QLabel where the flag image will be displayed
        """
        currency_code = combo_box.currentText().split(' | ')[0]
        flag_width = 70
        flag_height = 45
        eu_flag_width = 50
        eu_flag_height = 35

        if currency_code == "EUR":
            pixmap = QPixmap(self.eu_flag_path)
            if not pixmap.isNull():
                flag_label.setPixmap(
                    pixmap.scaled(eu_flag_width, eu_flag_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            flag_data = get_flag_image(currency_code[:2])
            if flag_data:
                pixmap = QPixmap()
                pixmap.loadFromData(flag_data)
                flag_label.setPixmap(
                    pixmap.scaled(flag_width, flag_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                flag_label.clear()

    def button_frame(self):
        """
        @brief Creates the frame for the buttons of the calculator.
        """
        self.buttonFrame = QFrame()
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrame.setFixedHeight(180)

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
        button.clicked.connect(self.clear_input)
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
        button.clicked.connect(self.delete_digit)
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
        button.clicked.connect(lambda _, d=digit: self.append_digit(str(d)))
        self.buttonLayout.addWidget(button, row, col)

        shortcut = QShortcut(QKeySequence(str(digit)), self)
        shortcut.activated.connect(lambda d=digit: self.append_digit(d))

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
        button.clicked.connect(lambda: self.append_digit("."))
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
        button.clicked.connect(self.convert_currency)
        self.buttonLayout.addWidget(button, *self.special_operations["CONVERT"])

    def clear_input(self):
        """
        @brief Clears the input fields
        """
        self.amount1.clear()
        self.amount2.clear()

    def delete_digit(self):
        """
        @brief Deletes the last digit from the current amount
        """
        current_text = self.amount1.text()
        if current_text:
            new_text = current_text[:-1]
            self.amount1.setText(new_text)

    def append_digit(self, param):
        """
        @brief Appends a digit to the current amount
        @param param: digit to append
        """
        current_text = self.amount1.text()
        new_text = current_text + param
        self.amount1.setText(new_text)

    def convert_currency(self):
        """
        @brief Converts the amount from one currency to another
        """
        base_currency = self.currency1.currentText()
        base_currency = base_currency.split(' | ')[0]
        target_currency = self.currency2.currentText()
        target_currency = target_currency.split(' | ')[0]
        amount = float(self.amount1.text())
        exchange_rate = get_exchange_rate(base_currency, target_currency)

        if exchange_rate is not None:
            converted_amount = amount * exchange_rate[1] / exchange_rate[0]
            self.amount2.setText(f"{converted_amount:.2f}")
        else:
            self.amount2.setText("Error")
