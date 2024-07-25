import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QIcon
from PySide6.QtCore import Qt, QSize
import mathlib
from Calculator.Kalkulajda.help_menu import HelpWindow
from Calculator.Kalkulajda.mode_menu import ModeWindow


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
    def __init__(self):
        super().__init__()
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
            "C": (0, 1, 1, 2),
            "⌫": (0, 3, 1, 2),
            "√": (1, 0),
            "!": (2, 0),
            "|x|": (3, 0),
            "%": (4, 0),
            ".": (4, 1),
            "=": (4, 3)
        }

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.display_frame()
        self.button_frame()
        main_layout.addWidget(self.displayFrame)
        main_layout.addWidget(self.buttonFrame)
        main_layout.addStretch()
        self.setLayout(main_layout)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

    def display_frame(self):
        self.displayFrame = QWidget(self)
        self.displayFrame.setFixedHeight(125)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")

        # Create a QGridLayout for the displayFrame
        layout = QGridLayout(self.displayFrame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        help_menu_button = self.create_help_menu_button()
        layout.addWidget(help_menu_button, 0, 0, alignment=Qt.AlignLeft | Qt.AlignTop)

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
        help_menu_button = QPushButton(self.displayFrame)
        help_menu_button.setFixedSize(20, 20)
        icon = QIcon(r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\help_button.png')
        help_menu_button.setIcon(icon)
        help_menu_button.setIconSize(QSize(20, 20))
        help_menu_button.clicked.connect(self.show_help_menu)
        return help_menu_button

    def show_help_menu(self):
        # Create an instance of HelpWindow and show it
        self.help_window = HelpWindow(self)
        self.help_window.show()

    def show_mode_menu(self):
        # Create an instance of ModeWindow and show it
        self.mode_window = ModeWindow(self)
        self.mode_window.show

    def button_frame(self):
        self.buttonFrame = QWidget(self)
        self.buttonFrame.setFixedHeight(280)
        self.buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(3, 3, 3, 3)

        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonFrameLayout.addLayout(self.buttonLayout)
        self.buttonFrame.setLayout(self.buttonFrameLayout)

    def error(self, message):
        """
        @brief Displays an error message on the calculator's display
        @param self: Instance of the class
        @param message: The error message to display
        """
        self.totalExpression = ""
        self.update_total_label()
        self.currentExpression = "Error: " + message
        self.currentLabel.setText(self.currentExpression)
        self.update_current_label()

    def create_digit_buttons(self):
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
        button.clicked.connect(lambda _, op="x\u207F": self.handle_exponentiation())
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_clear_button(self, pos):
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
        button.clicked.connect(lambda _, op="C": self.handle_clear())
        self.buttonLayout.addWidget(button, pos[0], pos[1], pos[2], pos[3])

    def create_delete_button(self, pos):
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
        button.clicked.connect(lambda _, op="⌫": self.handle_delete())
        self.buttonLayout.addWidget(button, pos[0], pos[1], pos[2], pos[3])

        shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), self)
        shortcut.activated.connect(self.handle_delete)

    def create_square_root_button(self, pos):
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
        button.clicked.connect(lambda _, op="ⁿ√x": self.handle_root())
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_factorial_button(self, pos):
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
        button.clicked.connect(lambda _, op="!": self.handle_factorial())
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_absolute_value_button(self, pos):
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
        button.clicked.connect(lambda _, op="|x|": self.handle_absolute_value())
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_modulo_button(self, pos):
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
        button.clicked.connect(lambda _, op="%": self.handle_modulo())
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_decimal_button(self, pos):
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
        button.clicked.connect(lambda _, op=".": self.handle_decimal_point())
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def create_equals_button(self, pos):
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
        button.clicked.connect(self.handle_equals)
        self.buttonLayout.addWidget(button, pos[0], pos[1])

        # Bind both Return and Enter keys to handle_equals
        shortcut_enter = QShortcut(QKeySequence(Qt.Key_Enter), self)
        shortcut_enter.activated.connect(self.handle_equals)
        shortcut_equals = QShortcut(QKeySequence("="), self)
        shortcut_equals.activated.connect(self.handle_equals)

    def show_numbers(self, digit):
        if (self.currentExpression.startswith("0") and not self.currentExpression.startswith("0.")
                and '^' not in self.currentExpression and '√' not in self.currentExpression):
            self.currentExpression = self.currentExpression[1:]
        # If 'Error' is in the current expression, overwrite it
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
        @param self: Instance of the class
        @param operator: The operator to append to the current expression
        """
        self.update_current_label()

        # If the current expression ends with a decimal point, remove it
        if '.' in self.currentExpression and not self.currentExpression[-1].isdigit():
            self.currentExpression = self.currentExpression[:-1]

        # If the current expression has a decimal point followed only by zeros, round it to an integer
        if '.' in self.currentExpression:
            if all(char == '0' for char in self.currentExpression[self.currentExpression.index('.') + 1:]):
                rounded_num = round(float(self.currentExpression))
                self.currentExpression = str(rounded_num)

        # If the current expression is an error message or 'inf', only allow '-' to overwrite it
        if 'Error' in self.currentExpression or 'inf' in self.currentExpression:
            if operator == '-':
                # Reset the font size when not displaying an error
                self.currentLabel.setFont(QFont("Arial", 50))
                self.currentLabel.setContentsMargins(0, 20, 0, 20)
                self.currentExpression = operator
                self.update_current_label()
                return
            else:
                return

        if self.currentExpression.endswith('e+') or self.currentExpression.endswith('e-'):
            self.currentExpression += '0'

        # If the current expression is empty, only allow '-' as the first character
        if self.currentExpression == '0':
            if operator == '-':
                self.currentExpression = operator
            elif not self.totalExpression:
                self.totalExpression = self.currentExpression + operator
        self.update_current_label()

        # If the current expression ends with '-', do not append another operator
        if '-' in self.currentExpression and not self.currentExpression[-1].isdigit():
            return

        # If the current expression ends with '√' and not a digit, append '-' or '0' based on the operator
        if '√' in self.currentExpression and not self.currentExpression[-1].isdigit():
            if operator == '-':
                self.currentExpression += operator
                self.update_current_label()
                return
            else:
                self.currentExpression += '0'

        # If the current expression ends with '^' and not a digit, append '-' or '0' based on the operator
        if '^' in self.currentExpression and not self.currentExpression[-1].isdigit():
            if operator == '-':
                self.currentExpression += operator
                self.update_current_label()
                return
            else:
                self.currentExpression += '0'

        # If the total expression ends with an operator and the current expression is empty, handle '-' differently
        if self.totalExpression and self.totalExpression[-1] in "+-*/%" and self.currentExpression == '0' and len(
                self.totalExpression) != 0:
            if operator == '-' and self.totalExpression[-1] in "+-*/%":
                self.currentExpression = operator
            else:
                # Replace the last operator in totalExpression with the new operator
                self.totalExpression = self.totalExpression[:-1] + operator
        else:
            # Check if the current label text is '0' before appending the operator to the total expression
            if self.currentLabel.text() != '0':
                self.totalExpression += self.currentExpression + operator

        self.evaluated = False
        self.currentExpression = ''
        self.update_total_label()
        self.update_current_label()

        # If the signal function returns True, perform an evaluation
        if self.signal():
            self.evaluate()
        else:
            pass

    def update_current_label(self):
        """
        @brief Updates the current expression label by truncating if necessary
        @param self: Instance of the class
        """
        if 'Error' in self.currentExpression:
            if len(self.currentExpression) > 80:
                self.currentExpression = self.currentExpression[:80]
            self.currentLabel.setFont(QFont("Arial", 11))
            self.currentLabel.setAlignment(Qt.AlignCenter)
        else:
            self.currentLabel.setFont(QFont("Arial", 30))
            self.currentLabel.setAlignment(Qt.AlignRight)

            if len(self.currentExpression) > 16:
                self.currentExpression = self.currentExpression[:16]

        if not self.currentExpression or self.currentExpression == "0":
            self.currentLabel.setText("0")
            self.currentExpression = '0'
        else:
            self.currentLabel.setText(self.currentExpression)

    def update_total_label(self):
        expression = self.totalExpression

        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')
        self.totalLabel.setText(expression)
        self.totalLabel.setText(expression[:30])

    def parse_exponentiation(self):
        """
        @brief Parses the current expression for exponentiation operation
        @param self: Instance of the class
        @return: Result of the exponentiation operation if successful, None otherwise
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
        @brief Parses the current expression for root operation
        @param self: Instance of the class
        @return: Result of the root operation if successful, None otherwise
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
        self.currentExpression = "0"
        self.totalExpression = ""
        self.update_total_label()
        self.update_current_label()

    def handle_delete(self):
        if 'Error' not in self.currentExpression or 'inf' not in self.currentExpression:
            if self.currentExpression:
                self.currentExpression = self.currentExpression[:-1]
                self.update_current_label()

        if len(self.currentExpression) == 0:
            self.currentExpression = "0"
            self.update_current_label()

    def handle_exponentiation(self):
        if ('^' not in self.currentExpression and '√' not in self.currentExpression and self.currentExpression[
            -1] != '.' and self.currentExpression[-1] != '-' and 'Error' not in self.currentExpression
                and 'inf' not in self.currentExpression):
            self.currentExpression += '^'
            self.update_current_label()

    def handle_root(self):
        if ('√' not in self.currentExpression and '^' not in self.currentExpression and self.currentExpression[
            -1] != '.'
                and self.currentExpression[-1] != '-' and 'Error' not in self.currentExpression
                and 'inf' not in self.currentExpression):
            self.currentExpression += '√'
        self.update_current_label()

    def handle_factorial(self):
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
        self.show_operators('%')

    def handle_decimal_point(self):
        if 'Error' not in self.currentExpression or 'inf' not in self.currentExpression:
            if not self.currentExpression or self.currentExpression[-1] != '-':
                if not self.currentExpression:
                    self.currentExpression += '0.'
                elif '.' not in self.currentExpression:
                    self.currentExpression += '.'
        self.update_current_label()

    def parsing(self):
        """
        @brief Parses the total expression into its components
        @param self: Instance of the class
        @return: Tuple containing the left side, operator, right side, last operator
        """

        lastOperator = ""
        if len(self.totalExpression) >= 3:
            lastOperator = self.totalExpression[-1]

        self.totalExpression = self.totalExpression[:-1]
        operators = {'+', '-', '*', '/', '%'}

        # Find the indices of the operators
        separatorIndices = [i for i, char in enumerate(self.totalExpression) if char in operators]

        # Ignore minus sign if it's part of a negative number or if it's part of scientific notation
        separatorIndices = [i for i in separatorIndices if not (
                (self.totalExpression[i] == '-' and (i == 0 or self.totalExpression[i - 1] in operators)) or
                (i > 0 and self.totalExpression[i - 1].lower() == 'e'))]

        # If there's only one operator or none, split the expression normally
        if len(separatorIndices) == 1:
            separatorIndex = separatorIndices[0]
            leftSide = self.totalExpression[:separatorIndex]
            rightSide = self.totalExpression[separatorIndex + 1:]
            separator = self.totalExpression[separatorIndex]
            return leftSide, separator, rightSide, lastOperator
        else:
            # If there are no operators or more than one, return an error
            self.error("Invalid number of operators")

    def evaluate(self):
        """
        @brief Evaluate the expression
        @param self: Instance of the class
        @return: True if the result is successfully evaluated and cleaned, False otherwise
        """
        components = self.parsing()
        leftSide, separator, rightSide, lastOperator = components
        result = 0

        if '^' in leftSide:
            expLeft = leftSide.split('^')[0]
            expRight = leftSide.split('^')[1]
            if '.' in expRight or int(expRight) < 0:
                self.error("Exponent must be a non-negative integer")
                return None
            if expLeft == '0' and expRight == '0':
                self.error("0^0 is undefined")
                return None
            if '.' not in expLeft:
                leftSide = str(mathlib.pow(int(expLeft), int(expRight)))
            else:
                leftSide = str(mathlib.pow(float(expLeft), int(expRight)))

        if '^' in rightSide:
            expLeft = rightSide.split('^')[0]
            expRight = rightSide.split('^')[1]
            if '.' in expRight or int(expRight) < 0:
                self.error("Exponent must be a non-negative integer")
                return None
            if expLeft == '0' and expRight == '0':
                self.error("0^0 is undefined")
                return None
            if '.' not in expLeft:
                rightSide = str(mathlib.pow(int(expLeft), int(expRight)))
            else:
                rightSide = str(mathlib.pow(float(expLeft), int(expRight)))

        # Then handle square root
        if '√' in leftSide:
            rootRight = leftSide.split('√')[0]
            rootLeft = leftSide.split('√')[1]
            if '.' in rootRight or int(rootRight) <= 0:
                self.error("Root index must be a non-negative integer")
                return None
            if float(rootLeft) < 0:
                self.error("Cannot take the root of a negative number")
                return None
            leftSide = str(mathlib.root(float(rootLeft), int(rootRight)))
            if '.' in leftSide:
                leftSideFloat = float(leftSide)
                if round(leftSideFloat * 10 ** 5) % 10 == 0:
                    leftSide = str(round(leftSideFloat))

        if '√' in rightSide:
            rootRight = rightSide.split('√')[0]
            rootLeft = rightSide.split('√')[1]
            if '.' in rootRight or int(rootRight) <= 0:
                self.error("Root index must be a non-negative integer")
                return None
            if float(rootLeft) < 0:
                self.error("Cannot take the root of a negative number")
                return None
            rightSide = str(mathlib.root(float(rootLeft), int(rootRight)))
            if '.' in rightSide:
                rightSide_float = float(rightSide)
                if round(rightSide_float * 10 ** 5) % 10 == 0:
                    rightSide = str(round(rightSide_float))

        # Convert to float or int as necessary
        if '.' in leftSide or 'e' in leftSide:
            leftSideFloat = float(leftSide)
        else:
            leftSideFloat = int(leftSide)
        if '.' in rightSide or 'e' in rightSide:
            rightSide_float = float(rightSide)
        else:
            rightSide_float = int(rightSide)

        # Perform the remaining operations
        if separator == '+':
            result += mathlib.add(leftSideFloat, rightSide_float)
        elif separator == '-':
            result += mathlib.sub(leftSideFloat, rightSide_float)
        elif separator == '*':
            result += mathlib.mul(leftSideFloat, rightSide_float)
        elif separator == '/':
            if rightSide_float == 0:
                self.error("Cannot divide by zero")
                return False
            elif leftSideFloat % rightSide_float == 0:
                result = mathlib.div(leftSideFloat, rightSide_float)
                result = int(result)
            else:
                result += mathlib.div(leftSideFloat, rightSide_float)
        elif separator == '%':
            if rightSide_float == 0:
                self.error("Cannot perform modulo operation with zero")
                return False
            result += mathlib.mod(leftSideFloat, rightSide_float)
        else:
            return False

        # Check if the result is within a certain range to avoid scientific notation
        if -1e16 < result < 1e16:
            resultStr = str(result)
            resultIntLength = len(str(int(result)))
            # If the result string is longer than 16 characters, round the result
            if len(resultStr) > 16:
                if resultIntLength == 16:
                    result = round(result)
                else:
                    result = round(result, 16 - resultIntLength)
                resultStr = str(result)
        else:
            resultStr = "{:.5e}".format(result)

        # Update the current expression with the result
        self.currentExpression = resultStr
        self.update_current_label()

        # Update the total expression with the new result and the operator
        self.totalExpression = str(resultStr) + lastOperator
        self.update_total_label()
        self.evaluated = True
        return self.evaluated

    def handle_equals(self):
        """
                @brief Calculates the result of the expression when the equals button is pressed
                @param self: Instance of the class
                @return True if the calculation is successful, False otherwise.
                """
        # Parse exponentiation
        exponentiation_result = self.parse_exponentiation()
        if exponentiation_result is not None:
            self.currentExpression = exponentiation_result
            self.update_current_label()
            return True  # Return if exponentiation was performed

        # Parse root
        root_result = self.parse_root()
        if root_result is not None:
            self.currentExpression = root_result
            self.update_current_label()
            return True  # Return if root was performed

        # Check if totalExpression is not empty before accessing its last character
        if self.totalExpression:
            leftSide = self.totalExpression[:-1]
            operator = self.totalExpression[-1]
        else:
            return False  # Return False if totalExpression is empty

        rightSide = self.currentExpression

        # Check and handle exponentiation in leftSide
        if '^' in leftSide:
            expLeft = leftSide.split('^')[0]
            expRight = leftSide.split('^')[1]
            if '.' in expRight or int(expRight) < 0:
                self.error("Exponent must be a non-negative integer")
                return None
            if expLeft == '0' and expRight == '0':
                self.error("0^0 is undefined")
                return None
            if '.' not in expLeft:
                leftSide = str(mathlib.pow(int(expLeft), int(expRight)))
            else:
                leftSide = str(mathlib.pow(float(expLeft), int(expRight)))

        if '^' in rightSide:
            expLeft = rightSide.split('^')[0]
            expRight = rightSide.split('^')[1]
            if '.' in expRight or int(expRight) < 0:
                self.error("Exponent must be a non-negative integer")
                return None
            if expLeft == '0' and expRight == '0':
                self.error("0^0 is undefined")
                return None
            if '.' not in expLeft:
                rightSide = str(mathlib.pow(int(expLeft), int(expRight)))
            else:
                rightSide = str(mathlib.pow(float(expLeft), int(expRight)))

        # Check and handle root in leftSide
        if '√' in leftSide:
            rootLeft = leftSide.split('√')[0]
            rootRight = leftSide.split('√')[1]
            if '.' in rootLeft or int(rootLeft) <= 0:
                self.error("Root index must be a non-negative integer")
                return None
            if float(rootRight) < 0:
                self.error("Cannot take the root of a negative number")
                return None
            leftSide = str(mathlib.root(float(rootRight), int(rootLeft)))
            if '.' in leftSide:
                leftSideFloat = float(leftSide)
                if round(leftSideFloat * 10 ** 5) % 10 == 0:
                    leftSide = str(round(leftSideFloat))

        # Check and handle root in rightSide
        if '√' in rightSide:
            rootLeft = rightSide.split('√')[0]
            rootRight = rightSide.split('√')[1]
            if '.' in rootLeft or int(rootLeft) <= 0:
                self.error("Root index must be a non-negative integer")
                return None
            if float(rootRight) < 0:
                self.error("Cannot take the root of a negative number")
                return None
            rightSide = str(mathlib.root(float(rootRight), int(rootLeft)))
            if '.' in rightSide:
                rightSideFloat = float(rightSide)
                if round(rightSideFloat * 10 ** 5) % 10 == 0:
                    rightSide = str(round(rightSideFloat))

        if '.' in leftSide or 'e' in leftSide:
            leftSideFloat = float(leftSide)
        else:
            leftSideFloat = int(leftSide)

        if '.' in rightSide or 'e' in rightSide:
            rightSideFloat = float(rightSide)
        else:
            rightSideFloat = int(rightSide)

        if operator == '+':
            result = mathlib.add(leftSideFloat, rightSideFloat)
        elif operator == '-':
            result = mathlib.sub(leftSideFloat, rightSideFloat)
        elif operator == '*':
            result = mathlib.mul(leftSideFloat, rightSideFloat)
        elif operator == '/':
            if rightSideFloat == 0:
                self.error("Cannot divide by zero")
                return None
            if leftSideFloat % rightSideFloat == 0:
                result = mathlib.div(leftSideFloat, rightSideFloat)
                result = int(result)
            else:
                result = mathlib.div(leftSideFloat, rightSideFloat)
        elif operator == '%':
            if rightSideFloat == 0:
                self.error("Cannot perform modulo operation by zero")
                return None
            result = mathlib.mod(leftSideFloat, rightSideFloat)
        else:
            return False

        # Check if the result is within a certain range to avoid scientific notation
        if -1e16 < result < 1e16:
            resultStr = str(result)
            resultIntLength = len(str(int(result)))
            # If the result string is longer than 16 characters, round the result
            if len(resultStr) > 16:
                if resultIntLength == 16:
                    result = round(result)
                else:
                    result = round(result, 16 - resultIntLength)
                resultStr = str(result)
        else:
            resultStr = "{:.5e}".format(result)

        # Update the current expression with the result
        self.currentExpression = resultStr
        self.update_current_label()

        # Update the total expression with the new result and the operator
        self.totalExpression = ""
        self.update_total_label()
        self.evaluated = True
        return self.evaluated

    def signal(self):
        """
        @brief Handles signal when the total expression has two operators
        @param self: Instance of the class
        @return: True if the total expression has two operators, False otherwise
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
                    # Skip if previous character is 'e'
                    if self.totalExpression[i - 1] == 'e':
                        continue
                    operatorCount += 1
            return operatorCount == 2
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
