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
from expression.expression_display import ExpressionDisplay
from expression.expression_buttons import ExpressionButtons


# TODO: Add shortcuts for all buttons, fix the typing, bug fix

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
    """
    @brief This class represents the Photomath mode of the calculator.
    """
    def __init__(self, parent=None):
        """
        @brief Initializes the PhotomathMode with necessary attributes and calls the init_ui method.
        """
        super().__init__(parent)
        self.parent_widget = parent
    
        self.mainLayout = None
        
        self.buttonFrame = ExpressionButtons(self)

        self.operations = self.buttonFrame.operations

        self.displayFrame = ExpressionDisplay(self)
        self.currentInput = self.displayFrame.currentInput
        self.currentExpression = self.displayFrame.currentExpression
        self.evaluated = False

        self.init_ui()

        regex = QRegularExpression(r"^[0-9+\-*/]*$")
        validator = QRegularExpressionValidator(regex, self)
        self.currentInput.setValidator(validator)
        self.currentInput.textChanged.connect(self.on_input_changed)

    def init_ui(self):
        """
        @brief Initializes the user interface of the calculator.
        """
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.mainLayout.addWidget(self.displayFrame, 0)
        self.mainLayout.addWidget(self.buttonFrame, 1)
        self.setLayout(self.mainLayout)

    def error(self, message):
        """
        @brief Displays an error message on the calculator's display.
        @param message The error message to display.
        """
        self.currentExpression = "Error: " + message
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)

    def on_input_changed(self, text):
        """
        @brief Handles the event when the text in the input field changes.
        @param text: The new text in the input field.
        """
        if text != self.currentExpression:
            for i, char in enumerate(text):
                if i >= len(self.currentExpression) or char != self.currentExpression[i]:
                    if char.isdigit():
                        self.show_numbers(char)
                    elif char in "+-*/":
                        self.show_operators(char)

    def show_numbers(self, digit):
        """
        @brief Updates the current expression when a digit is pressed.
        @param digit: The digit to add to the current expression.
        """
        last_char = self.currentExpression[-1] if self.currentExpression else ''
        if self.currentExpression == "0":
            self.currentExpression = str(digit)
        elif 'Error' in self.currentExpression or 'inf' in self.currentExpression or self.evaluated:
            self.currentExpression = str(digit)
            self.evaluated = False
        elif last_char in [')', '|', 'π', '!']:
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

            # Replace the current expression with the new operator
            if self.evaluated and operator == '-':
                self.currentExpression = self.operations[operator]
                self.evaluated = False
            # Replace the last operator if the current expression ends with an operator
            elif last_char in self.operations.values():
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
        self.evaluated = False

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
                self.evaluated = False

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
        if (not self.currentExpression or
                'Error' in self.currentExpression or
                'inf' in self.currentExpression or
                self.currentExpression[-1] in {'π', '.', '!', '(', '^', '|'} or
                self.currentExpression[-1] in self.operations.values()):
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
        """
        @brief Handles the event when the pi button is pressed.
        """
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

    def calculate(self):
        """
        @brief Evaluates the current mathematical expression and updates the display.
        """
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
                # Convert the result to an integer if it's a whole number
                value = float(self.currentExpression)
                if value.is_integer():
                    self.currentExpression = str(int(value))
                else:
                    self.currentExpression = str(value)
            except ValueError:
                # Handle value errors
                self.error("Invalid expression for conversion")

        # Update the display
        self.update_current_input()
        self.currentInput.setText(self.currentExpression)
        self.currentInput.setCursorPosition(0)
        self.evaluated = True

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
