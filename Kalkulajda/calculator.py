"""
@file calculator.py
@brief File containing GUI of calculator application.

@author Martin Valapka (xvalapm00)
@date 27.07. 2024
"""

import sys
from decimal import getcontext, Decimal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, \
    QLineEdit, QStackedLayout
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QIcon
from PySide6.QtCore import Qt, QSize
import mathlib
from Calculator.Kalkulajda.help_menu import HelpWindow
from Calculator.Kalkulajda.mode_menu import Sidebar
from bmi_calculator import BMICalculator
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

PRODUCTION = True
pictures = {
    "logo": r"Pictures/real_logo.png",
    "help": r"Pictures/help_button.png",
}

if PRODUCTION:
    pictures = {
        "logo": "Kalkulajda/Pictures/real_logo.png",
        "help": "Kalkulajda/Pictures/help_button.png",
    }


class App(QWidget):
    """
    @class App
    @brief Main class for the calculator application GUI.
    """

    def __init__(self):
        """
        @brief Initializes the calculator application.
        """
        super().__init__()
        self.height_input = None
        self.result_label = None
        self.weight_input = None
        self.equals_pressed = False
        self.help_window = None
        self.buttonFrameLayout = None
        self.buttonLayout = None
        self.buttonFrame = None
        self.totalLabel = None
        self.displayLayout = None
        self.displayFrame = None
        self.currentLabel = None
        self.setWindowTitle("Calcu-lajda")
        self.setFixedSize(400, 405)
        self.totalExpression = ""
        self.currentExpression = "0"
        self.evaluated = False
        my_icon = QIcon()
        my_icon.addFile(r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\icons\real_logo.png')
        self.setWindowIcon(my_icon)

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

        # Initialize layouts
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.calculator_layout = QVBoxLayout()

        # Create sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.mode_selected.connect(self.switch_mode)

        # Create widgets
        self.default_widget = self.create_default_widget()
        self.bmi_widget = BMICalculator()

        # Add widgets to calculator layout
        self.calculator_layout.addWidget(self.default_widget)
        self.calculator_layout.addWidget(self.bmi_widget)

        # Add layouts to the main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addLayout(self.calculator_layout)

        # Initialize UI
        self.sidebar.hide()
        self.sidebar.select_mode("Standard")
        self.switch_mode("Standard")

    def create_default_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.display_frame()
        layout.addWidget(self.displayFrame)

        self.button_frame()
        layout.addWidget(self.buttonFrame)
        return widget

    def switch_mode(self, mode):
        if mode == "BMI":
            self.calculator_layout.removeWidget(self.default_widget)
            self.default_widget.hide()
            self.calculator_layout.addWidget(self.bmi_widget)
            self.bmi_widget.show()
        else:
            self.calculator_layout.removeWidget(self.bmi_widget)
            self.bmi_widget.hide()
            self.calculator_layout.addWidget(self.default_widget)
            self.default_widget.show()

        if self.sidebar.is_visible:
            self.toggle_sidebar()

    def display_frame(self):
        """
        @brief Creates and configures the display frame where the calculator's input and results are shown.
        """
        self.displayFrame = QWidget(self)
        self.displayFrame.setFixedHeight(125)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")

        layout = QGridLayout(self.displayFrame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(2)

        help_menu_button = self.create_help_menu_button()
        mode_menu_button = self.create_mode_menu_button()

        button_layout.addWidget(mode_menu_button)
        button_layout.addWidget(help_menu_button)
        button_layout.addStretch()

        layout.addLayout(button_layout, 0, 0, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.totalLabel = QLabel(self.totalExpression, self.displayFrame)
        self.totalLabel.setFont(QFont("Arial bold", 16))
        self.totalLabel.setStyleSheet(f"color: WHITE; padding: 5px;")
        self.totalLabel.setAlignment(Qt.AlignRight)

        layout.addWidget(self.totalLabel, 0, 1, alignment=Qt.AlignRight | Qt.AlignTop)
        self.currentLabel = QLabel(self.currentExpression, self.displayFrame)
        self.currentLabel.setFont(QFont("Arial bold", 32))
        self.currentLabel.setStyleSheet(f"color: WHITE;")
        self.currentLabel.setAlignment(Qt.AlignRight)

        layout.addWidget(self.currentLabel, 1, 0, 1, 2, alignment=Qt.AlignRight | Qt.AlignBottom)
        self.displayFrame.setLayout(layout)

    def create_help_menu_button(self):
        """
        @brief Creates and configures the help menu button.
        @return QPushButton configured help menu button.
        """
        help_menu_button = QPushButton(self.displayFrame)
        help_menu_button.setFixedSize(20, 20)
        icon = QIcon(r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\help_button.png')
        help_menu_button.setIcon(icon)
        help_menu_button.setIconSize(QSize(20, 20))
        help_menu_button.clicked.connect(self.show_help_menu)
        return help_menu_button

    def show_help_menu(self):
        """
        @brief Displays the help menu window.
        """
        self.help_window = HelpWindow(self)
        self.help_window.show()

    def create_mode_menu_button(self):
        """
        @brief Creates and configures the mode menu button.
        @return QPushButton configured mode menu button.
        """
        mode_menu_button = QPushButton(self.displayFrame)
        mode_menu_button.setFixedSize(25, 25)
        icon = QIcon(r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\menu_icon.png')
        mode_menu_button.setIcon(icon)
        mode_menu_button.setIconSize(QSize(25, 25))
        mode_menu_button.setStyleSheet("background-color: transparent; border: none;")
        mode_menu_button.clicked.connect(self.toggle_sidebar)
        return mode_menu_button

    def toggle_sidebar(self):
        """
        @brief Toggles the visibility of the sidebar.
        """
        self.sidebar.toggle()
        if self.sidebar.is_visible:
            self.setFixedSize(600, 405)
            self.sidebar.show()
        else:
            self.setFixedSize(400, 405)
            self.sidebar.hide()

    def button_frame(self):
        """
        @brief Creates and configures the button frame which contains the calculator's buttons.
        """
        self.buttonFrame = QWidget(self)
        self.buttonFrame.setFixedHeight(280)
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(3, 3, 3, 3)

        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonFrameLayout.addLayout(self.buttonLayout)
        self.buttonFrame.setLayout(self.buttonFrameLayout)

        # Create and display the buttons
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

    def error(self, message):
        """
        @brief Displays an error message on the calculator's display.
        @param message The error message to display.
        """
        self.totalExpression = ""
        self.update_total_label()
        self.currentExpression = "Error: " + message
        self.currentLabel.setText(self.currentExpression)
        self.update_current_label()

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
            button.clicked.connect(lambda _, d=digit: self.show_numbers(d))
            self.buttonLayout.addWidget(button, pos[0], pos[1])

            shortcut = QShortcut(QKeySequence(str(digit)), self)
            shortcut.activated.connect(lambda d=digit: self.show_numbers(d))

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
            button.clicked.connect(lambda _, op=operator: self.show_operators(op))
            self.buttonLayout.addWidget(button, pos[0], pos[1])

            shortcut = QShortcut(QKeySequence(operator), self)
            shortcut.activated.connect(lambda op=operator: self.show_operators(op))

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
        button = QPushButton("x\u207F")  # Unicode for superscript
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
        button.clicked.connect(self.handle_exponentiation)
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
        button.clicked.connect(self.handle_clear)
        self.buttonLayout.addWidget(button, pos[0], pos[1], pos[2], pos[3])
        shortcut_clear = QShortcut(QKeySequence("C"), self)
        shortcut_clear.activated.connect(self.handle_clear)

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
        button.clicked.connect(self.handle_delete)
        self.buttonLayout.addWidget(button, pos[0], pos[1], pos[2], pos[3])
        shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), self)
        shortcut.activated.connect(self.handle_delete)

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
        button.clicked.connect(self.handle_root)
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
        button.clicked.connect(self.handle_factorial)
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
        button.clicked.connect(self.handle_absolute_value)
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
        button.clicked.connect(self.handle_modulo)
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
        button.clicked.connect(self.handle_decimal_point)
        self.buttonLayout.addWidget(button, pos[0], pos[1])
        shortcut_decimal = QShortcut(QKeySequence(Qt.Key_Period), self)
        shortcut_decimal.activated.connect(self.handle_decimal_point)

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
        button.clicked.connect(lambda: self.evaluate(equals_button=True))
        self.buttonLayout.addWidget(button, pos[0], pos[1])

        # Bind both Return and Enter keys to handle_equals
        shortcut_enter = QShortcut(QKeySequence(Qt.Key_Enter), self)
        shortcut_enter.activated.connect(lambda: self.evaluate(equals_button=True))
        shortcut_return = QShortcut(QKeySequence(Qt.Key_Return), self)
        shortcut_return.activated.connect(lambda: self.evaluate(equals_button=True))
        shortcut_equals = QShortcut(QKeySequence("="), self)
        shortcut_equals.activated.connect(lambda: self.evaluate(equals_button=True))

    def handle_operator(self, operator):
        """
        @brief Handles the input of an operator.
        @param operator str The operator that was input.
        """
        if self.currentExpression:
            if not self.evaluated:
                self.evaluate()
            self.totalExpression = self.currentExpression + operator
            self.currentExpression = ""
            self.update_total_label()
            self.update_current_label()
        elif self.totalExpression and self.totalExpression[-1] in "+-*/%":
            self.totalExpression = self.totalExpression[:-1] + operator
            self.update_total_label()
        self.equals_pressed = False
        self.evaluated = False

    def show_numbers(self, digit):
        """
        @brief Updates the current expression when a digit is pressed.
        @param digit: The digit to add to the current expression.
        """
        if (self.currentExpression.startswith("0") and not self.currentExpression.startswith("0.")
                and '^' not in self.currentExpression and '√' not in self.currentExpression):
            self.currentExpression = self.currentExpression[1:]
        if 'Error' in self.currentExpression or 'inf' in self.currentExpression:
            self.currentExpression = str(digit)
        elif self.evaluated:
            self.currentExpression = ''
            self.currentExpression += str(digit)
            self.evaluated = False
        else:
            self.currentExpression += str(digit)
        self.update_current_label()

    def show_operators(self, operator):
        """
        @brief Appends the provided operator to the current expression and updates the labels.
        @param operator: The operator to append to the current expression.
        """
        self.update_current_label()

        if '.' in self.currentExpression and not self.currentExpression[-1].isdigit():
            self.currentExpression = self.currentExpression[:-1]

        if '.' in self.currentExpression:
            if all(char == '0' for char in self.currentExpression[self.currentExpression.index('.') + 1:]):
                rounded_num = round(float(self.currentExpression))
                self.currentExpression = str(rounded_num)

        if 'Error' in self.currentExpression or 'inf' in self.currentExpression:
            if operator == '-':
                self.currentLabel.setFont(QFont("Arial", 50))
                self.currentLabel.setContentsMargins(0, 20, 0, 20)
                self.currentExpression = operator
                self.update_current_label()
                return
            else:
                return

        if self.currentExpression.endswith('e+') or self.currentExpression.endswith('e-'):
            self.currentExpression += '0'

        if self.currentExpression == '0':
            if operator == '-':
                self.currentExpression = operator
            elif not self.totalExpression:
                self.totalExpression = self.currentExpression + operator
        self.update_current_label()

        if '-' in self.currentExpression and not self.currentExpression[-1].isdigit():
            return

        if '√' in self.currentExpression and not self.currentExpression[-1].isdigit():
            if operator == '-':
                self.currentExpression += operator
                self.update_current_label()
                return
            else:
                self.currentExpression += '0'

        if '^' in self.currentExpression and not self.currentExpression[-1].isdigit():
            if operator == '-':
                self.currentExpression += operator
                self.update_current_label()
                return
            else:
                self.currentExpression += '0'

        if self.totalExpression and self.totalExpression[-1] in "+-*/%" and self.currentExpression == '0' and len(
                self.totalExpression) != 0:
            if operator == '-' and self.totalExpression[-1] in "+-*/%":
                self.currentExpression = operator
            else:
                self.totalExpression = self.totalExpression[:-1] + operator
        else:
            if self.currentLabel.text() != '0':
                self.totalExpression += self.currentExpression + operator

        self.evaluated = False
        self.currentExpression = ''
        self.update_total_label()
        self.update_current_label()

        if self.signal():
            self.evaluate()
        else:
            pass

    def update_current_label(self):
        """
        @brief Updates the current expression label by truncating if necessary.
        """
        if 'Error' in self.currentExpression:
            if len(self.currentExpression) > 80:
                self.currentExpression = self.currentExpression[:80]
            self.currentLabel.setFont(QFont("Arial", 11))
            self.currentLabel.setAlignment(Qt.AlignCenter)
        else:
            self.currentLabel.setFont(QFont("Arial", 32))
            self.currentLabel.setAlignment(Qt.AlignRight)

            if len(self.currentExpression) > 16:
                self.currentExpression = self.currentExpression[:16]

        if not self.currentExpression or self.currentExpression == "0":
            self.currentLabel.setText("0")
            self.currentExpression = '0'
        else:
            self.currentLabel.setText(self.currentExpression)

    def update_total_label(self):
        """
        @brief Updates the total expression label with formatted operators.
        """
        expression = self.totalExpression

        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')
        self.totalLabel.setText(expression[:30])

    def parse_exponentiation(self):
        """
        @brief Parses the current expression for exponentiation operation (x^y).
        @param self: Instance of the class.
        @return: Result of the exponentiation operation if successful, None otherwise.
        """
        result = None
        if '^' in self.currentExpression and not self.totalExpression:
            expCurrLeft = self.currentExpression.split('^')[0]
            expCurrRight = self.currentExpression.split('^')[1]
            if '.' in expCurrRight or int(expCurrRight) < 0:
                self.error("Exponent must be a non-negative integer")
                return None
            if expCurrLeft == '0' and expCurrRight == '0':
                self.error("0^0 is undefined")
                return None
            if '.' not in expCurrLeft:
                result = str(mathlib.pow(int(expCurrLeft), int(expCurrRight)))
            else:
                result = str(mathlib.pow(float(expCurrLeft), int(expCurrRight)))

            if len(result) > 16:
                result = "{:.5e}".format(float(result))
        return result

    def parse_root(self):
        """
        @brief Parses the current expression for root operation (√x).
        @param self: Instance of the class.
        @return: Result of the root operation if successful, None otherwise.
        """
        result = None
        if '√' in self.currentExpression and not self.totalExpression:
            rootCurrLeft = self.currentExpression.split('√')[0]
            rootCurrRight = self.currentExpression.split('√')[1]
            if '.' in rootCurrLeft or int(rootCurrLeft) < 0 or int(rootCurrLeft) == 0:
                return None
            if float(rootCurrRight) < 0:
                return None
            result_float = mathlib.root(float(rootCurrRight), int(rootCurrLeft))

            epsilon = 1e-10
            if abs(result_float - round(result_float)) < epsilon:
                result = str(int(round(result_float)))
            else:
                result = f"{result_float:.10f}".rstrip('0').rstrip('.')

            if len(result) > 16:
                result = f"{float(result):.5e}"

        return result

    def handle_clear(self):
        """
        @brief Clears the current expression and total expression, resetting the calculator.
        """
        self.currentExpression = "0"
        self.totalExpression = ""
        self.update_total_label()
        self.update_current_label()

    def handle_delete(self):
        """
        @brief Deletes the last character in the current expression or resets it if empty.
        """
        if 'Error' not in self.currentExpression and 'inf' not in self.currentExpression:
            if self.currentExpression:
                self.currentExpression = self.currentExpression[:-1]
                self.update_current_label()

        if len(self.currentExpression) == 0:
            self.currentExpression = "0"
            self.update_current_label()

    def handle_exponentiation(self):
        """
        @brief Appends the exponentiation operator (^) to the current expression if valid.
        """
        if ('^' not in self.currentExpression and '√' not in self.currentExpression
                and self.currentExpression[-1] != '.' and self.currentExpression[-1] != '-'
                and 'Error' not in self.currentExpression and 'inf' not in self.currentExpression):
            self.currentExpression += '^'
            self.update_current_label()

    def handle_root(self):
        """
        @brief Appends the root operator (√) to the current expression if valid.
        """
        if ('√' not in self.currentExpression and '^' not in self.currentExpression
                and self.currentExpression[-1] != '.' and self.currentExpression[-1] != '-'
                and 'Error' not in self.currentExpression and 'inf' not in self.currentExpression):
            self.currentExpression += '√'
        self.update_current_label()

    def handle_factorial(self):
        """
        @brief Calculates the factorial of the current expression if valid and updates it.
        """
        if self.totalExpression:
            self.error("The total expression is not empty. Clear it first!")
            return

        functions_to_parse = [self.parse_exponentiation, self.parse_root]

        for func in functions_to_parse:
            result = func()
            if result is not None:
                if '.' in result or int(result) < 0:
                    self.error("Factorial is only defined for non-negative integers")
                    return
                elif int(result) > 100:
                    self.error("Factorial of numbers greater than 100 is too large")
                    return
                else:
                    result = mathlib.fac(int(result))
                if result.is_integer():
                    result = int(result)
                self.currentExpression = str(result)
                self.update_current_label()
                return

        if '.' in self.currentExpression or int(self.currentExpression) < 0:
            self.error("Factorial is only defined for non-negative integers")
            return
        elif int(self.currentExpression) > 100:
            self.error("Factorial of numbers greater than 100 is too large")
            return
        else:
            result = mathlib.fac(int(self.currentExpression))

        if len(str(result)) > 16:
            result = "{:.5e}".format(result)
        else:
            result = int(result)
        self.currentExpression = str(result)
        self.update_current_label()

    def handle_absolute_value(self):
        """
        @brief Calculates the absolute value of the current expression if valid and updates it.
        """
        if self.totalExpression:
            self.error("The total expression is not empty. Clear it first!")
            return

        if not self.totalExpression:
            functions_to_parse = [self.parse_exponentiation, self.parse_root]
            for func in functions_to_parse:
                result = func()
                if result is not None:
                    if '.' in result:
                        result = mathlib.abs(float(result))
                    else:
                        result = mathlib.abs(int(result))
                    self.currentExpression = str(result)
                    self.update_current_label()
                    return

        if '.' in self.currentExpression:
            result = mathlib.abs(float(self.currentExpression))
        else:
            result = mathlib.abs(int(self.currentExpression))

        self.currentExpression = str(result)
        self.update_current_label()

    def handle_modulo(self):
        """
        @brief Appends the modulo operator (%) to the current expression.
        """
        self.show_operators('%')

    def handle_decimal_point(self):
        """
        @brief Appends a decimal point to the current expression if valid.
        """
        if 'Error' not in self.currentExpression and 'inf' not in self.currentExpression:
            if not self.currentExpression or self.currentExpression[-1] != '-':
                if not self.currentExpression:
                    self.currentExpression += '0.'
                elif '.' not in self.currentExpression:
                    self.currentExpression += '.'
        self.update_current_label()

    def parsing(self):
        """
        @brief Parses the total expression into its components.
        """
        operators = {'+', '-', '*', '/', '%'}
        lastOperator = self.totalExpression[-1] if self.totalExpression else ""
        expression = self.totalExpression[:-1] if lastOperator in operators else self.totalExpression

        # Find the last valid operator
        for i in range(len(expression) - 1, -1, -1):
            if expression[i] in operators and not (
                    (expression[i] == '-' and (i == 0 or expression[i - 1] in operators)) or
                    (i > 0 and expression[i - 1].lower() == 'e')
            ):
                return expression[:i], expression[i], expression[i + 1:], lastOperator

        return expression, "", "", lastOperator

    def evaluate(self, equals_button=False):
        """
        @brief Evaluates the expression by parsing and calculating the result.
        @param equals_button bool True if called from equals button, False otherwise.
        @return bool True if the evaluation was successful, False otherwise.
        """
        self.equals_pressed = equals_button
        leftSide, operator, rightSide, lastOperator = self.parsing()

        if not operator and not rightSide:
            rightSide = self.currentExpression
            operator = lastOperator

        leftSide = self.process_special_operations(leftSide)
        rightSide = self.process_special_operations(rightSide)

        try:
            leftValue = float(leftSide)
            rightValue = float(rightSide)
        except ValueError:
            self.error("Invalid number format")
            return False

        result = self.perform_operation(leftValue, rightValue, operator)
        if result is None:
            return False

        self.update_result(result, lastOperator)
        return True

    def process_special_operations(self, value):
        """
        @brief Processes exponentiation and root operations.
        @param value str The string representation of the value to process.
        @return str The processed value as a string, or None if an error occurred.
        """
        if '^' in value:
            base, exponent = value.split('^')
            return self.calculate_power(float(base), int(exponent))
        elif '√' in value:
            parts = value.split('√')
            if len(parts) == 2:
                index, radicand = parts
                if index:
                    return self.calculate_root(float(radicand), int(index))
                else:
                    return self.calculate_root(float(radicand), 2)
            else:
                self.error("Invalid root format")
                return None
        return value

    def calculate_power(self, base, exponent):
        """
        @brief Calculates the power of a number.
        @param base float The base number.
        @param exponent int The exponent.
        @return str The result as a string, or None if an error occurred.
        """
        if exponent < 0 or '.' in str(exponent):
            self.error("Exponent must be a non-negative integer")
            return None
        if base == 0 and exponent == 0:
            self.error("0^0 is undefined")
            return None
        return str(mathlib.pow(base, exponent))

    def calculate_root(self, radicand, index):
        """
        @brief Calculates the nth root of a number.
        @param radicand float The number under the root.
        @param index int The root index.
        @return str The result as a string, or None if an error occurred.
        """
        if index <= 0 or '.' in str(index):
            self.error("Root index must be a positive integer")
            return None
        if radicand < 0:
            self.error("Cannot take the root of a negative number")
            return None
        result = mathlib.root(radicand, index)
        if abs(result - round(result)) < 1e-5:
            return str(round(result, 5))
        else:
            return str(result)

    def perform_operation(self, left, right, operator):
        """
        @brief Performs the specified arithmetic operation.
        @param left float The left operand.
        @param right float The right operand.
        @param operator str The arithmetic operator.
        @return float The result of the operation, or None if an error occurred.
        """
        getcontext().prec = 28  # Set the precision high enough
        left = Decimal(left)
        right = Decimal(right)

        if operator == '+':
            return float(left + right)
        elif operator == '-':
            return float(left - right)
        elif operator == '*':
            return float(left * right)
        elif operator == '/':
            if right == 0:
                self.error("Cannot divide by zero")
                return None
            return float(left / right)
        elif operator == '%':
            if right == 0:
                self.error("Cannot perform modulo operation with zero")
                return None
            return float(left % right)
        else:
            self.error("Invalid operator")
            return None

    def update_result(self, result, lastOperator):
        """
        @brief Updates the current and total expressions with the calculated result.
        @param result float The calculated result.
        @param lastOperator str The last operator used in the calculation.
        """
        if -1e16 < result < 1e16:
            if abs(result - round(result)) < 1e-10:
                resultStr = str(int(round(result)))
            else:
                resultStr = str(result)

            if len(resultStr) > 16:
                if '.' in resultStr:
                    integer_part = len(str(int(float(resultStr))))
                    result = round(result, 16 - integer_part)
                else:
                    result = round(result)
                resultStr = str(result)
        else:
            resultStr = "{:.10e}".format(result)

        self.currentExpression = resultStr
        if self.equals_pressed:
            self.totalExpression = ""
        else:
            self.totalExpression = resultStr + lastOperator
        self.update_current_label()
        self.update_total_label()
        self.evaluated = True

    def signal(self):
        """
        @brief Handles signal when the total expression has two operators.
        @param self: Instance of the class.
        @return: True if the total expression has exactly two operators, False otherwise.
        """
        # Check if totalExpression is not empty and has at least two characters
        if self.totalExpression and len(self.totalExpression) >= 2:
            operators = ['+', '-', '*', '/', '%']
            operatorCount = 0
            for i, char in enumerate(self.totalExpression):
                if char in operators and i != 0 and self.totalExpression[i - 1] not in ['^', '√']:
                    # Skip the operator if it's a minus sign and the character before it is a digit or another operator
                    if char == '-' and self.totalExpression[i - 1] in operators:
                        continue
                    # Skip if the previous character is 'e'
                    if self.totalExpression[i - 1] == 'e':
                        continue
                    operatorCount += 1
            return operatorCount == 2
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(r'C:\Users\val24\PycharmProjects\pythonProject1'
                                                                  r'\Calculator\icons\real_logo.png')
    window = App()
    window.show()
    sys.exit(app.exec())
