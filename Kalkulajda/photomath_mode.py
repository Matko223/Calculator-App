"""
@file photomath_mod.py
@brief File containing Expression mode for the calculator application.

@author Martin Valapka (xvalapm00)
@date 14.08. 2024
"""
import re

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, \
    QLineEdit, QStackedLayout, QLineEdit
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QIcon, QRegularExpressionValidator
from PySide6.QtCore import Qt, QSize, QRegularExpression
import math

# TODO: Add shortcuts for all buttons, fix the result, calculation with pi, add factorial, fix the typing, bug fix

# Color definitions
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class PhotomathMode(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = None
        self.mainLayout = None
        self.non_essential_widget = None
        self.buttonFrameLayout = None
        self.buttonLayout = None
        self.buttonFrame = None
        self.displayLayout = None
        self.displayFrame = None
        self.currentLabel = None
        self.currentExpression = ""
        self.currentInput = None

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
            "C": (0, 3),
            "⌫": (0, 4),
            "√": (1, 0),
            "!": (2, 0),
            "|x|": (3, 0),
            "π": (4, 0),
            ".": (4, 1),
            "=": (4, 3)
        }

        self.brackets = {
            "(": (0, 1),
            ")": (0, 2)
        }

        self.init_ui()

    def init_ui(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.displayFrame = self.display_frame()
        self.buttonFrame = self.button_frame()

        self.mainLayout.addWidget(self.displayFrame)
        self.mainLayout.addWidget(self.buttonFrame)
        self.setLayout(self.mainLayout)

    def display_frame(self):
        displayFrame = QWidget(self)
        displayFrame.setFixedHeight(125)
        displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")

        layout = QVBoxLayout(displayFrame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addStretch()

        self.non_essential_widget = QWidget(displayFrame)
        non_essential_layout = QVBoxLayout(self.non_essential_widget)
        non_essential_layout.setContentsMargins(0, 0, 0, 0)
        non_essential_layout.setSpacing(0)

        self.currentInput = QLineEdit(self.currentExpression, self.non_essential_widget)
        self.currentInput.setFont(QFont("Arial bold", 32))
        self.currentInput.setStyleSheet("color: WHITE; background-color: transparent; border: none;")
        self.currentInput.setAlignment(Qt.AlignRight)
        self.currentInput.textChanged.connect(self.on_input_changed)

        non_essential_layout.addWidget(self.currentInput)
        layout.addWidget(self.non_essential_widget, alignment=Qt.AlignRight | Qt.AlignBottom)
        displayFrame.setLayout(layout)
        return displayFrame

    def button_frame(self):
        buttonFrame = QWidget(self)
        buttonFrame.setFixedHeight(280)
        buttonFrame.setStyleSheet(f"background-color: {GRAY}; color: white;")
        self.buttonFrameLayout = QVBoxLayout(buttonFrame)
        self.buttonFrameLayout.setContentsMargins(3, 3, 3, 3)

        self.buttonLayout = QGridLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonFrameLayout.addLayout(self.buttonLayout)
        buttonFrame.setLayout(self.buttonFrameLayout)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_bracket_buttons()
        return buttonFrame

    def on_input_changed(self, text):
        # TODO: Implement the logic for the input change(typing)
        self.currentExpression = text
        self.update_current_input()

    def error(self, message):
        """
        @brief Displays an error message on the calculator's display.
        @param message The error message to display.
        """
        self.currentExpression = "Error: " + message
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

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
            elif operation == "π":
                self.create_pi_button(pos)
            elif operation == ".":
                self.create_decimal_button(pos)
            elif operation == "=":
                self.create_equals_button(pos)

    def create_bracket_buttons(self):
        """
        @brief Creates and configures buttons for brackets
        """
        for bracket, pos in self.brackets.items():
            button = QPushButton(bracket)
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
            button.clicked.connect(lambda _, b=bracket: self.show_brackets(b))
            self.buttonLayout.addWidget(button, pos[0], pos[1])

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
        button.setFixedSize(79, 55)
        button.clicked.connect(self.handle_clear)
        self.buttonLayout.addWidget(button, pos[0], pos[1])
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
        button.setFixedSize(79, 55)
        button.clicked.connect(self.handle_delete)
        self.buttonLayout.addWidget(button, pos[0], pos[1])
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

    def create_pi_button(self, pos):
        """
        @brief Creates and configures the button for pi operation (π).
        @param pos: Position of the button in the grid layout as a tuple (row, column).
        """
        button = QPushButton("π")
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
        button.clicked.connect(self.handle_pi)
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
        button.clicked.connect(self.calculate)
        self.buttonLayout.addWidget(button, pos[0], pos[1])

    def show_numbers(self, digit):
        """
        @brief Updates the current expression when a digit is pressed.
        @param digit: The digit to add to the current expression.
        """
        last_char = self.currentExpression[-1] if self.currentExpression else ''
        if self.currentExpression == "0":
            self.currentExpression = str(digit)
        elif 'Error' in self.currentExpression or 'inf' in self.currentExpression:
            self.currentExpression = str(digit)
        elif last_char == ')' or last_char == '|' or last_char == 'π' or last_char == '!':
            return
        else:
            self.currentExpression += str(digit)
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    def show_operators(self, operator):
        """
        @brief Appends the provided operator to the current expression and updates the labels.
        @param operator: The operator to append to the current expression.
        """
        if 'Error' not in self.currentExpression and 'inf' not in self.currentExpression:
            last_char = self.currentExpression[-1] if self.currentExpression else ''

            # Replace the last operator if the current expression ends with an operator
            if last_char in self.operations.values():
                self.currentExpression = self.currentExpression[:-1] + self.operations[operator]
            # Append the operator if the last character is a digit, closing bracket, or percentage
            elif last_char.isdigit() or last_char in [')'] or last_char == '|' or last_char == 'π' or last_char == '!':
                self.currentExpression += self.operations[operator]
            # If the expression is empty or ends with an opening bracket, only allow minus
            elif not self.currentExpression or last_char == '(':
                if operator == '-':
                    self.currentExpression += operator

        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    def update_current_input(self):
        """
        @brief Updates the current expression label by truncating if necessary.
        """
        if 'Error' in self.currentExpression:
            if len(self.currentExpression) > 80:
                self.currentExpression = self.currentExpression[:80]
            self.currentInput.setFont(QFont("Arial", 11))
            self.currentInput.setAlignment(Qt.AlignCenter)
        else:
            self.currentInput.setFont(QFont("Arial", 32))
            self.currentInput.setAlignment(Qt.AlignRight)

        if not self.currentExpression:
            self.currentInput.setText("")
        else:
            if len(self.currentExpression) > 30:
                self.currentExpression = self.currentExpression[:30]
                self.currentInput.setText(self.currentExpression)

    def handle_clear(self):
        """
        @brief Clears the current expression, resetting the calculator.
        """
        self.currentExpression = ""
        self.update_current_input()

    def handle_delete(self):
        """
        @brief Deletes the last character in the current expression or resets it if empty.
        """
        if 'Error' not in self.currentExpression and 'inf' not in self.currentExpression:
            if self.currentExpression:
                self.currentExpression = self.currentExpression[:-1]
                self.update_current_input()
                self.currentInput.setText(self.currentExpression)

        if len(self.currentExpression) == 0:
            self.currentExpression = ""
            self.update_current_input()
            self.currentInput.setText(self.currentExpression)

    def handle_decimal_point(self):
        """
        @brief Appends a decimal point to the current expression if valid.
        """
        if 'Error' in self.currentExpression or 'inf' in self.currentExpression:
            return

        # If the expression is empty or ends with an operator, do not allow a decimal point
        if not self.currentExpression or self.currentExpression[-1] in ['+', '-', '×', '÷', '(', '^', '√', 'π', '!']:
            return
        else:
            # Find the last number in the expression
            last_number = ''
            for char in reversed(self.currentExpression):
                if char.isdigit() or char == '.':
                    last_number = char + last_number
                else:
                    break

            # If the last number doesn't contain a decimal point, add one
            if '.' not in last_number:
                self.currentExpression += '.'
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    def handle_exponentiation(self):
        """
        @brief Appends the exponentiation operator to the current expression.
        """
        if ('Error' in self.currentExpression or 'inf' in self.currentExpression or
                (self.currentExpression and
                 (self.currentExpression[-1] == 'π'
                  or self.currentExpression[-1] == '.'
                  or self.currentExpression[-1] == '!'
                  or self.currentExpression[-1] == '('
                  or self.currentExpression[-1] in self.operations.values()
                  or self.currentExpression[-1] == '|'))):
            return
        self.currentExpression += '^'
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    def handle_root(self):
        """
        @brief Appends the root operator to the current expression.
        """
        if ('Error' in self.currentExpression or 'inf' in self.currentExpression or
                (self.currentExpression and
                 (self.currentExpression[-1] == 'π'
                  or self.currentExpression[-1] == '.'
                  or self.currentExpression[-1] == '!'))):
            return
        self.currentExpression += '√('
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    def handle_factorial(self):
        """
        @brief Appends the factorial operator to the current expression.
        """
        if ('Error' not in self.currentExpression and 'inf' not in self.currentExpression and
                self.currentExpression and
                self.currentExpression[-1] not in ['+', '-', '*', '/', '^', '√', '(', 'π', '!']):
            self.currentExpression += '!'
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    def handle_pi(self):
        if (not self.currentExpression or
                self.currentExpression[-1].isdigit() or
                self.currentExpression[-1] in self.operations.values()):
            self.currentExpression += 'π'
        else:
            return
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    def handle_absolute_value(self):
        """
        @brief Appends the absolute value placeholder to the current expression.
        """
        if ('Error' in self.currentExpression or 'inf' in self.currentExpression or
                (self.currentExpression and
                 (self.currentExpression[-1] == 'π'
                  or self.currentExpression[-1] == '.'
                  or self.currentExpression[-1] == '!'
                  or self.currentExpression[-1] == '('
                  or self.currentExpression[-1] in self.operations.values()
                  or self.currentExpression[-1] == '|'))):
            return
        self.currentExpression += '|0|'
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    import math
    import re

    def calculate(self):
        pi_value = math.pi

        try:
            # Replace π with its numeric value, ensuring multiplication where necessary
            expression = self.currentExpression.replace("π", f"({pi_value})")
            expression = re.sub(r'(\d)\(', r'\1*(', expression)
            expression = re.sub(r'\)(\d)', r')*\1', expression)

            # Replace other custom operators with Python-compatible operators
            expression = expression.replace("\u00F7", "/").replace("\u00D7", "*").replace("^", "**")

            # Handle factorial
            while '!' in expression:
                factorial_index = expression.index('!')

                # Find the start of the number or expression before the factorial
                start = factorial_index - 1
                while start >= 0 and (expression[start].isdigit() or expression[start] == '.'):
                    start -= 1
                start += 1

                # Extract the number or expression
                factorial_expr = expression[start:factorial_index]

                # Replace the factorial with math.factorial
                expression = expression[:start] + f"math.factorial({factorial_expr})" + expression[factorial_index + 1:]

            # Custom handling for root operations
            while '√' in expression:
                root_index = expression.index('√')
                degree_start = root_index - 1
                while degree_start >= 0 and (expression[degree_start].isdigit() or expression[degree_start] == '.'):
                    degree_start -= 1
                degree_start += 1

                if degree_start < root_index:
                    root_degree = expression[degree_start:root_index]
                    expression = expression[:degree_start] + expression[root_index:]
                    root_index -= (root_index - degree_start)
                else:
                    root_degree = "2"

                if expression[root_index + 1] == '(':
                    paren_count = 1
                    end = root_index + 2
                    while paren_count > 0:
                        if expression[end] == '(':
                            paren_count += 1
                        elif expression[end] == ')':
                            paren_count -= 1
                        end += 1
                    root_expr = expression[root_index + 2:end - 1]
                    expression = (expression[:root_index] +
                                  f"math.pow({root_expr}, 1/{root_degree})" +
                                  expression[end:])
                else:
                    end = root_index + 1
                    while end < len(expression) and (expression[end].isdigit() or expression[end] == '.'):
                        end += 1
                    root_expr = expression[root_index + 1:end]
                    expression = (expression[:root_index] +
                                  f"math.pow({root_expr}, 1/{root_degree})" +
                                  expression[end:])

            # Handle absolute value
            while '|' in expression:
                start = expression.index('|')
                end = expression.index('|', start + 1)
                abs_expr = expression[start + 1:end]
                expression = expression[:start] + f"abs({abs_expr})" + expression[end + 1:]

            # Replace other custom functions
            expression = expression.replace("mod", "%")

            # Safe built-in functions that can be used in eval
            safe_dict = {
                "math": math,
                "abs": abs,
                "factorial": math.factorial,
            }

            # Evaluate the expression
            result = eval(expression, safe_dict)
            self.currentExpression = str(result)

        except ZeroDivisionError:
            self.error("Cannot divide by zero")
        except (SyntaxError, NameError):
            self.error("Invalid input")
        except Exception as e:
            self.error(str(e))

        if isinstance(self.currentExpression, str) and self.currentExpression.endswith('0'):
            try:
                value = float(self.currentExpression)
                if value.is_integer():
                    self.currentExpression = str(int(value))
                else:
                    self.currentExpression = str(value)
            except ValueError:
                self.error("Invalid expression for conversion")
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    def show_brackets(self, bracket):
        """
        @brief Appends the provided bracket to the current expression and updates the labels.
        @param bracket: The bracket to append to the current expression.
        """
        open_brackets = self.currentExpression.count('(')
        close_brackets = self.currentExpression.count(')')

        # Handle opening bracket
        if bracket == '(':
            if (not self.currentExpression or self.currentExpression[-1] in self.operations.values() or
                    self.currentExpression[-1] in '('):
                self.currentExpression += bracket

        # Handle closing bracket
        elif bracket == ')':
            if (open_brackets > close_brackets and self.currentExpression and
                    self.currentExpression[-1] not in self.operations.values() and self.currentExpression[-1] != '('):
                self.currentExpression += bracket

        # Update display
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)
