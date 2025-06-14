"""
@file: help_content.py
@brief: Help content definitions

@author: Martin Valapka
"""

import os
from ..utils.resource_manager import resource_path

HELP_PICTURES = {
    "Help": resource_path(os.path.join('Pictures', 'help_icon.png')),
    "Clear": resource_path(os.path.join('Pictures', 'Clear.ico')),
    "Del": resource_path(os.path.join('Pictures', 'Del.ico')),
    "Exponentiation": resource_path(os.path.join('Pictures', '^.ico')),
    "Root": resource_path(os.path.join('Pictures', 'Root.ico')),
    "Factorial": resource_path(os.path.join('Pictures', 'Fact.ico')),
    "Absolute value": resource_path(os.path.join('Pictures', 'Abs.ico')),
    "Modulo": resource_path(os.path.join('Pictures', 'Mod.ico')),
    "Addition": resource_path(os.path.join('Pictures', 'add.ico')),
    "Subtraction": resource_path(os.path.join('Pictures', 'sub.ico')),
    "Multiplication": resource_path(os.path.join('Pictures', 'mul.ico')),
    "Division": resource_path(os.path.join('Pictures', 'div.ico')),
    "Equals": resource_path(os.path.join('Pictures', 'equals.ico')),
    "Decimal": resource_path(os.path.join('Pictures', 'decimal.ico'))
}

ABOUT_TEXT = """
Simple Calculator

Developed by:
- Martin Valapka (xvalapm00)

Features:
- Basic arithmetic operations:
  - Addition
  - Subtraction
  - Multiplication
  - Division
- Advanced operations:
  - Exponentiation
  - Root
  - Factorial
  - Absolute value
  - Modulo
- Supports:
  - Decimal numbers
  - Negative numbers

Usage:
- The Calculator is divided into two main sections:
  1. Display Frame: Shows the current expression and the result.
  2. Button Frame: Contains buttons for inputting numbers, operators, and performing various operations.

Evaluation:
- The calculation is performed automatically when you press an operator or the equals button.
- You can also type directly on the keyboard, and the calculator will update accordingly.

Input Handling:
- The calculator accepts a maximum of two operands at a time and performs the specified operation between them.
- If you make a mistake in choosing the operator, you can directly change it by selecting your desired operator.

Character Limit:
- The current expression is limited to 16 characters.
- The total expression can accommodate up to 30 characters.

Enjoy calculating!
"""

BUTTON_DESCRIPTIONS = {
    "Clear": "Clear:\nClears both the current and total expression",
    "Del": "Eraser:\nErases the last digit/operator in the current expression",
    "Exponentiation": "Exponentiation:\nBase^Exponent = Product\n5^2 = 25",
    "Root": "Root:\nⁿ√x = Root\nn - degree, x - radical\n²√25 = 5",
    "Factorial": "Factorial:\nUNARY OPERATOR\nNumber!\n(Num-1)×(Num-2) × ... × 1\n4! = 4 × 3 × 2 × 1",
    "Absolute value": "Absolute value:\nUNARY OPERATOR\n|Number|\nReturns the distance from 0\n|5| = 5\n|-5| = 5",
    "Modulo": "Modulo:\nNum % Num = R\nEvaluates the remainder after division\n7 % 3 = 1",
    "Addition": "Addition:\nNum + Num = Sum\nReturns the sum after addition\n7 + 3 = 10",
    "Subtraction": "Subtraction:\nNum - Num = Difference\nReturns the difference after subtraction\n7 - 3 = 4",
    "Multiplication": "Multiplication:\nNum × Num = Product\nReturns the product after multiplication\n7 × 3 = 21",
    "Division": "Division:\nNum ÷ Num = Quotient\nReturns the quotient after division\nNum ÷ 0 = Division error\n10 ÷ 2 = 5",
    "Equals": "Equals:\nEvaluates the expression:\nFrom the total and current expression\nClears the total expression\nPrints the result to the current expression",
    "Decimal": "Decimal point:\nPlaces decimal point in the current expression\nRounds the number if there are only zeroes behind the decimal point\nRemoves trailing decimal point if no digit follows it"
}

DETAILED_DESCRIPTIONS = {
    "Exponentiation": "How to use Exponentiation:\n1. Choose the base\n2. Select the exponentiation button\n3. Choose the Exponent\n4. Exponent cannot be decimal or negative",
    "Root": "How to use Root:\n1. Choose the degree\n2. Select the root button\n3. Choose the radical\n4. Radical follows mathematical rules + cannot be decimal",
    "Factorial": "How to use Factorial:\n1. Choose the number - not negative or decimal\n2. Select the factorial button '!'",
    "Absolute value": "How to use Absolute value:\n1. Choose the number\n2. Select the Abs. value button",
    "Modulo": "How to use Modulo:\n1. Choose the number\n2. Select the Modulo button\n3. Choose the divisor except 0"
}

class HelpContent:
    """
    @brief: Class to manage help content for the calculator application
    """
    
    @staticmethod
    def get_about_text():
        """@brief: Return the about text for the calculator application"""
        return ABOUT_TEXT.strip()
    
    @staticmethod
    def get_button_description(button_name):
        """brief: Return the description for a specific button"""
        return BUTTON_DESCRIPTIONS.get(button_name, "")
    
    @staticmethod
    def get_detailed_description(button_name):
        """brief: Return the detailed description for a specific button"""
        return DETAILED_DESCRIPTIONS.get(button_name, "")
    
    @staticmethod
    def get_picture_path(button_name):
        """@brief: Return the picture path for a specific button"""
        return HELP_PICTURES.get(button_name, "")
