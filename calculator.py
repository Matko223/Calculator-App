"""
@file calculator.py
@brief File containing GUI of calculator application.

@author
- Martin Valapka (xvalapm00)

@date - March 19, 2024
"""
import mathlib
import platform
from help_menu import ToplevelWindow
from PIL import Image, ImageTk
from customtkinter import *

LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
LARGE = "Arial 25 bold"
SMALL = "Arial 15"
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


def adjust_button_size(width, height):
    """
    @brief Adjusts the button size based on the platform
    @param width: Original button width
    @param height: Original button height
    @return: Adjusted button width and height
    """
    if platform.system() == 'Linux':
        width += 15
        height += 15
    return width, height


class App(CTk):
    """
    @brief Initialization of the calculator application.

    Attributes:
            buttonFrame: The frame containing the calculator buttons
            displayFrame: The frame containing the calculator display
            toplevel_window: The top-level window for help
            totalExpression: The total expression displayed on the calculator
            currentExpression: The current expression displayed on the calculator
            digits: Dictionary mapping digit keys
            operations: Dictionary mapping operator symbols
    """

    def __init__(self):
        super().__init__()
        self.numbers = None
        self.settingsImagePath = None
        self.currentLabel = None
        self.totalLabel = None
        self.buttonFrame = None
        self.displayFrame = None
        self.toplevel_window = None
        self.title("Calcu-lajda")
        self.resizable(False, False)

        self.iconpath = ImageTk.PhotoImage(file=pictures["logo"])
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        self.totalExpression = ""
        self.currentExpression = "0"
        self.evaluated = False

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

    def center_window(self, width, height, scalefactor=1.0):
        """
        @brief Calculates the position to center a window on the screen
        @param self: Instance of the class
        @param width: The width of the window
        @param height: The height of the window
        @param scalefactor: Optional scale factor to adjust the centering position
        @return: String representing the window geometry
        """
        os_name = platform.system()
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        if os_name == 'Linux':
            x = int(((screenWidth / 2) - (width / 2)) * scalefactor)
            y = int(((screenHeight / 2) - (height / 2)) * scalefactor)
            return f"{width + 75}x{height + 80}+{x}+{y}"

        else:
            x = int(((screenWidth / 2) - (width / 2)) * scalefactor)
            y = int(((screenHeight / 2) - (height / 2)) * scalefactor)
            return f"{width}x{height}+{x}+{y}"

    def create_display_frame(self):
        """
        @brief Create the display frame with total and current expression labels
        @param self: Instance of the class
        """

        self.displayFrame = CTkFrame(self, width=400, height=150, fg_color=DARK_GRAY, border_width=5,
                                     border_color=GRAY, corner_radius=0)
        self.displayFrame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.totalLabel = CTkLabel(self.displayFrame, text=self.totalExpression, anchor="e", padx=15, pady=20,
                                   font=(SMALL, 22), text_color="white")
        self.totalLabel.grid(row=0, column=0, sticky="nsew")

        self.currentLabel = CTkLabel(self.displayFrame, text=self.currentExpression, anchor="e", padx=15, pady=20,
                                     font=(LARGE, 50), text_color="white")
        self.currentLabel.grid(row=1, column=0, sticky="nsew")

        self.displayFrame.grid_rowconfigure(0, weight=1)
        self.displayFrame.grid_rowconfigure(1, weight=1)
        self.displayFrame.grid_columnconfigure(0, weight=1)

    def update_total_label(self):
        """
        @brief Updates the total expression label
        @param self: Instance of the class
        """
        expression = self.totalExpression

        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')
        self.totalLabel.configure(text=expression)
        self.totalLabel.configure(text=expression[:30])

    def update_current_label(self):
        """
        @brief Updates the current expression label by truncating if necessary
        @param self: Instance of the class
        """

        # If 'Error' is in the current expression, change the length to 80 and adjust the font size
        if 'Error' in self.currentExpression:
            if len(self.currentExpression) > 20:
                self.currentExpression = self.currentExpression[:80]
            self.currentLabel.configure(font=("Arial", 15), pady=55)  # Smaller font size for error messages
        else:
            if len(self.currentExpression) > 14:
                self.currentExpression = self.currentExpression[:14]  # Limit the length to 14
            self.currentLabel.configure(font=("Arial", 50), pady=20)  # Larger font size for normal expressions

        # If currentExpression is empty or "0", display "0"
        if not self.currentExpression or self.currentExpression == "0":
            self.currentLabel.configure(text="0")
            self.currentExpression = '0'
        else:
            self.currentLabel.configure(text=self.currentExpression)

    def create_button_frame(self):
        """
        @brief Creates a frame for buttons in the calculator interface
        @param self: Instance of the class
        """

        self.buttonFrame = CTkFrame(self, width=400, height=255, fg_color=GRAY, border_width=0, corner_radius=0)
        self.buttonFrame.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_numbers(self, value):
        """
        @brief Appends the provided value to the current expression and updates the current label.
        @param self: Instance of the class
        @param value: The value to append to the current expression
        """
        # If the current expression is a single minus sign, do not reset it
        if self.currentExpression != "-":
            if (self.currentExpression.startswith("0") and not self.currentExpression.startswith("0.")
                and '^' not in self.currentExpression and '√' not in self.currentExpression):
                self.currentExpression = self.currentExpression[1:]
            # If 'Error' is in the current expression, overwrite it
            if 'Error' in self.currentExpression or 'inf' in self.currentExpression:
                self.currentExpression = str(value)
            elif self.evaluated:
                self.currentExpression = ''
                self.currentExpression += str(value)
                self.evaluated = False
            else:
                self.currentExpression += str(value)
        else:
            self.currentExpression += str(value)
        self.update_current_label()

    def create_digit_buttons(self):
        """
        @brief Creates digit buttons in the calculator interface
        @param self: Instance of the class
        """
        button_width, button_height = adjust_button_size(75, 45)
        for digit, (row, column) in self.digits.items():
            button = CTkButton(self.buttonFrame, text=str(digit), bg_color=GRAY, fg_color=LIGHT_GRAY,
                               border_width=0, corner_radius=10, font=(LARGE, 25),
                               width=button_width, height=button_height, hover_color=GRAY,
                               command=lambda x=digit: self.show_numbers(x))
            button.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
            self.buttonFrame.grid_rowconfigure(row, weight=1)
            self.buttonFrame.grid_columnconfigure(column, weight=1)

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
                self.currentLabel.configure(font=("Arial", 50), pady=20)
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
            if self.currentLabel.cget("text") != '0':
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

    def error(self, message):
        """
        @brief Displays an error message on the calculator's display
        @param self: Instance of the class
        @param message: The error message to display
        """
        self.totalExpression = ""
        self.update_total_label()
        self.currentExpression = "Error: " + message
        self.currentLabel.configure(font=("Arial", 15), pady=55)  # Changed the font size to a smaller value
        self.update_current_label()

    def create_operator_buttons(self):
        """
        @brief Creates operator buttons in the calculator interface
        @param self: Instance of the class
        """

        row = 1
        column = 4
        button_width, button_height = adjust_button_size(75, 45)
        for operator, symbol in self.operations.items():
            button = CTkButton(self.buttonFrame, text=symbol, fg_color=ORANGE,
                               border_width=0, corner_radius=10, font=(LARGE, 25),
                               width=button_width, height=button_height, hover_color=HOVER_OPERATOR,
                               command=lambda op=operator: self.show_operators(op))
            button.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
            self.buttonFrame.grid_rowconfigure(row, weight=1)
            self.buttonFrame.grid_columnconfigure(column, weight=1)
            row += 1

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
        if -1e14 < result < 1e14:
            resultStr = str(result)
            resultIntLength = len(str(int(result)))
            # If the result string is longer than 14 characters, round the result
            if len(resultStr) > 14:
                if resultIntLength == 14:
                    result = round(result)
                else:
                    result = round(result, 14 - resultIntLength)
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

            # If the result is longer than 14 characters, convert it to scientific notation with 5 decimal places
            if len(result) > 14:
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
                self.error("Index must be a non-negative integer and not zero")
                return None
            if float(rootCurrRight) < 0:
                self.error("Cannot take the root of a negative number")
                return None
            result_float = mathlib.root(float(rootCurrRight), int(rootCurrLeft))
            # Check if the result is an integer
            if result_float.is_integer():
                result = str(int(result_float))
            else:
                result = str(result_float)
        return result

    def equals(self):
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
        if -1e14 < result < 1e14:
            resultStr = str(result)
            resultIntLength = len(str(int(result)))
            # If the result string is longer than 14 characters, round the result
            if len(resultStr) > 14:
                if resultIntLength == 14:
                    result = round(result)
                else:
                    result = round(result, 14 - resultIntLength)
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

    def create_equals_button(self):
        """
        @brief Creates equals button in the calculator interface that evaluates the expression
        @param self: Instance of the class
        """
        button_width, button_height = adjust_button_size(75, 45)
        equalsButton = CTkButton(self.buttonFrame, text="=", border_width=0, fg_color=ORANGE,
                                 corner_radius=10, font=(LARGE, 25),
                                 width=button_width, height=button_height, hover_color=HOVER_OPERATOR,
                                 command=self.equals)
        equalsButton.grid(row=4, column=3, sticky="nsew", padx=2, pady=2)
        self.buttonFrame.grid_rowconfigure(4, weight=1)
        self.buttonFrame.grid_columnconfigure(3, weight=1)

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

    def decimal(self):
        """
        @brief Adds a decimal point to the current expression
        @param self: Instance of the class
        """
        if 'Error' not in self.currentExpression or 'inf' not in self.currentExpression:
            if not self.currentExpression or self.currentExpression[-1] != '-':
                if not self.currentExpression:
                    self.currentExpression += '0.'
                elif '.' not in self.currentExpression:
                    self.currentExpression += '.'
        self.update_current_label()

    def create_decimal_button(self):
        """
        @brief Creates decimal point button in the calculator interface
        @param self: Instance of the class
        """
        button_width, button_height = adjust_button_size(75, 45)
        decimalButton = CTkButton(self.buttonFrame, text=".", border_width=0, fg_color=LIGHT_GRAY,
                                  corner_radius=10, font=(LARGE, 25),
                                  width=button_width, height=button_height, hover_color=GRAY,
                                  command=self.decimal)
        decimalButton.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
        self.buttonFrame.grid_rowconfigure(4, weight=1)
        self.buttonFrame.grid_columnconfigure(1, weight=1)

    def clear(self):
        """
        @brief Clears both the current and total expression
        @param self: Instance of the class
        """

        self.currentExpression = "0"
        self.totalExpression = ""
        self.update_total_label()

        if not self.currentExpression:
            self.currentExpression = "0"

        self.update_current_label()

    def create_clean_button(self):
        """
        @brief Creates Clean button in the calculator interface that clears the expression
        @param self: Instance of the class
        """
        button_width, button_height = adjust_button_size(75, 45)
        cleanButton = CTkButton(self.buttonFrame, text="C", border_width=0, fg_color=COLOR_REST,
                                corner_radius=10, font=(LARGE, 25), width=button_width, height=button_height,
                                hover_color=HOVER_COLOR, command=self.clear)
        cleanButton.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=2, pady=2)
        self.buttonFrame.grid_rowconfigure(0, weight=1)
        self.buttonFrame.grid_columnconfigure(3, weight=1)

    def delete(self):
        """
        @brief Deletes the last character from the current expression
        @param self: Instance of the class
        """
        # Only delete if 'Error' is not in the current expression
        if 'Error' not in self.currentExpression or 'inf' not in self.currentExpression:
            if self.currentExpression:
                self.currentExpression = self.currentExpression[:-1]
                self.update_current_label()

            if len(self.currentExpression) == 0:
                self.currentExpression = "0"
                self.update_current_label()

    def create_delete_button(self):
        """
        @brief Creates Delete button in the calculator interface that erases the last character
        @param self: Instance of the class
        """
        button_width, button_height = adjust_button_size(75, 45)
        deleteButton = CTkButton(self.buttonFrame, text="⌫", border_width=0, fg_color=COLOR_REST,
                                 corner_radius=10, font=(LARGE, 25),
                                 width=button_width, height=button_height, hover_color=HOVER_COLOR,
                                 command=self.delete)
        deleteButton.grid(row=0, column=3, columnspan=2, sticky="nsew", padx=2, pady=2)
        self.buttonFrame.grid_rowconfigure(0, weight=1)
        self.buttonFrame.grid_columnconfigure(4, weight=1)

    def exponentiation(self):
        """
        @brief Adds an exponentiation operator to the current expression if it does not already contain one
        @param self: Instance of the class
        @return: True if the operation is located in the expression, False otherwise
        """

        if ('^' not in self.currentExpression and '√' not in self.currentExpression and self.currentExpression[
            -1] != '.' and self.currentExpression[-1] != '-' and 'Error' not in self.currentExpression
            and 'inf' not in self.currentExpression):
            self.currentExpression += '^'
            self.update_current_label()

    def create_exponentiation_button(self):
        """
        @brief Creates exponentiation button in the calculator interface
        @param self: Instance of the class
        """

        button_width, button_height = adjust_button_size(75, 45)
        exponentiationButton = CTkButton(self.buttonFrame, text="x\u207F", border_width=0, fg_color=COLOR_REST,
                                         corner_radius=10, font=(LARGE, 25),
                                         width=button_width, height=button_height, hover_color=HOVER_COLOR,
                                         command=self.exponentiation)
        exponentiationButton.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.buttonFrame.grid_rowconfigure(0, weight=1)
        self.buttonFrame.grid_columnconfigure(0, weight=1)

    def root(self):
        """
        @brief Adds a root operator to the current expression if it does not already contain one
        @param self: Instance of the class
        @return: True if the operation is located in the expression, False otherwise
        """

        if ('√' not in self.currentExpression and '^' not in self.currentExpression and self.currentExpression[
            -1] != '.'
            and self.currentExpression[-1] != '-' and 'Error' not in self.currentExpression
            and 'inf' not in self.currentExpression):
            self.currentExpression += '√'
        self.update_current_label()

    def create_root_button(self):
        """
        @brief Creates root button in the calculator interface
        @param self: Instance of the class
        """

        button_width, button_height = adjust_button_size(75, 45)
        rootButton = CTkButton(self.buttonFrame, text="ⁿ√x", border_width=0, fg_color=COLOR_REST,
                               corner_radius=10, font=(LARGE, 25),
                               width=button_width, height=button_height, hover_color=HOVER_COLOR, command=self.root)
        rootButton.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        self.buttonFrame.grid_rowconfigure(1, weight=1)
        self.buttonFrame.grid_columnconfigure(0, weight=1)

    def factorial(self):
        """
        @brief Computes the factorial of the current expression
        @param self: Instance of the class
        """
        # Check if totalExpression is not empty
        if self.totalExpression:
            self.error("The total expression is not empty. Clear it first!")
            return

        # List of functions to parse
        functions_to_parse = [self.parse_exponentiation, self.parse_root]

        for func in functions_to_parse:
            result = func()
            if result is not None:
                # Check if the result is a decimal or negative
                if '.' in result or int(result) < 0:
                    self.error("Factorial is only defined for non-negative integers")
                    return
                elif int(result) > 100:
                    self.error("Factorial of numbers greater than 100 is too large")
                    return
                else:
                    # If it's not, calculate the factorial of the result
                    result = mathlib.fac(int(result))
                # If the result is an integer, convert it to an integer
                if result.is_integer():
                    result = int(result)
                self.currentExpression = str(result)
                self.update_current_label()
                return

        # If the current expression is a decimal or negative
        if '.' in self.currentExpression or int(self.currentExpression) < 0:
            self.error("Factorial is only defined for non-negative integers")
            return
        elif int(self.currentExpression) > 100:
            self.error("Factorial of numbers greater than 100 is too large")
            return
        else:
            result = mathlib.fac(int(self.currentExpression))

        # If the length of the result is greater than 14
        if len(str(result)) > 14:
            result = "{:.5e}".format(result)
        else:
            result = int(result)
        self.currentExpression = str(result)
        self.update_current_label()

    def create_factorial_button(self):
        """
        @brief Creates factorial button in the calculator interface
        @param self: Instance of the class
        """

        button_width, button_height = adjust_button_size(75, 45)
        factorialButton = CTkButton(self.buttonFrame, text="x!", border_width=0, fg_color=COLOR_REST,
                                    corner_radius=10, font=(LARGE, 25),
                                    width=button_width, height=button_height, hover_color=HOVER_COLOR,
                                    command=self.factorial)
        factorialButton.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        self.buttonFrame.grid_rowconfigure(2, weight=1)
        self.buttonFrame.grid_columnconfigure(0, weight=1)

    def abs(self):
        """
        @brief Computes the absolute value of the current expression
        @param self: Instance of the class
        """
        # Check if totalExpression is not empty
        if self.totalExpression:
            self.error("The total expression is not empty. Clear it first!")
            return

        if not self.totalExpression:
            functions_to_parse = [self.parse_exponentiation, self.parse_root]
            # Loop through the functions to parse
            for func in functions_to_parse:
                result = func()
                if result is not None:
                    # Check if the result is a decimal
                    if '.' in result:
                        result = mathlib.abs(float(result))
                    else:
                        result = mathlib.abs(int(result))
                    self.currentExpression = str(result)
                    self.update_current_label()
                    return

        # If the total expression is not empty, check if the current expression is a decimal
        if '.' in self.currentExpression:
            result = mathlib.abs(float(self.currentExpression))
        else:
            result = mathlib.abs(int(self.currentExpression))

        self.currentExpression = str(result)
        self.update_current_label()

    def create_abs_button(self):
        """
        @brief Creates button in the calculator interface for the absolute value of the expression
        @param self: Instance of the class
        """

        button_width, button_height = adjust_button_size(75, 45)
        absButton = CTkButton(self.buttonFrame, text="|x|", border_width=0, fg_color=COLOR_REST,
                              corner_radius=10, font=(LARGE, 25),
                              width=button_width, height=button_height, hover_color=HOVER_COLOR, command=self.abs)
        absButton.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        self.buttonFrame.grid_rowconfigure(3, weight=1)
        self.buttonFrame.grid_columnconfigure(0, weight=1)

    def place_modulo(self):
        """
        @brief Places the modulo operator in the current expression and updates the labels
        @param self: Instance of the class
        """
        self.show_operators('%')

    def create_modulo_button(self):
        """
        @brief Creates button in the calculator interface for the modulo operation
        @param self: Instance of the class
        """

        button_width, button_height = adjust_button_size(75, 45)
        moduloButton = CTkButton(self.buttonFrame, text="mod", border_width=0, fg_color=COLOR_REST,
                                 corner_radius=10, font=(LARGE, 25),
                                 width=button_width, height=button_height, hover_color=HOVER_COLOR,
                                 command=self.place_modulo)
        moduloButton.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
        self.buttonFrame.grid_rowconfigure(4, weight=1)
        self.buttonFrame.grid_columnconfigure(0, weight=1)

    def create_settings_button(self):
        """
        @brief Creates a settings/help button in the calculator interface
        @param self: Instance of the class
        """
        settings_image = Image.open(pictures['help'])
        settings_image = settings_image.resize((50, 50), Image.Resampling.LANCZOS)

        # Create a CTkImage from the resized image
        ctk_settings_image = CTkImage(settings_image)

        settingsButton = CTkButton(self, image=ctk_settings_image, text="", border_width=0, fg_color=DARK_GRAY,
                                   corner_radius=25, font=(LARGE, 15), width=5, height=5,
                                   bg_color=DARK_GRAY, hover_color=COLOR_REST, command=self.open_settings_window)
        settingsButton.grid(row=0, column=0, sticky="nw", pady=2)

    def open_settings_window(self):
        """
        @brief Opens the settings window.
        If the settings window is not open, it creates a new one and links it to the root window.
        Otherwise, it just focuses on the existing window.
        @param self: Instance of the class
        """

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.wm_transient(self)
        else:
            self.toplevel_window.focus()

    def bind_keys(self):
        """
        @brief Binds keyboard keys to calculator operations and digits
        @param self: Instance of the class
        """

        for key in self.digits:
            self.bind(str(key), lambda event, digit=key: self.show_numbers(digit))

        for key in self.operations:
            self.bind(str(key), lambda event, op=key: self.show_operators(op))

        self.bind("<BackSpace>", lambda event: self.delete())
        self.bind("<c>", lambda event: self.clear())
        self.bind(".", lambda event: self.decimal())
        self.bind("=", lambda event: self.equals())
        self.bind("<Return>", lambda event: self.equals())

    def run(self):
        """
        @brief Runs the application.
        @param self: Instance of the class
        """

        self.geometry(self.center_window(400, 405, self._get_window_scaling()))
        self.create_display_frame()
        self.create_button_frame()
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_equals_button()
        self.create_decimal_button()
        self.create_clean_button()
        self.create_delete_button()
        self.create_exponentiation_button()
        self.create_root_button()
        self.create_factorial_button()
        self.create_abs_button()
        self.create_modulo_button()
        self.create_settings_button()
        self.bind_keys()
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()

# END OF calculator.py file
