"""
@file currency_converter.py
@brief File containing Currency converter mode for the calculator application.

@author Martin Valapka (xvalapm00)
@date 17.09. 2024
"""

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QSizePolicy)
from .currency_api import get_exchange_rate
from utils.img_path import resource_path
from .currency_display import CurrencyDisplay
from .currency_buttons import CurrencyButtons
import os

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
        self.setStyleSheet(f"background-color: {DARK_GRAY}; color: white;")
        
        self.displayFrame = CurrencyDisplay(self)
        
        self.flag1_label = self.displayFrame.flag1_label
        self.flag2_label = self.displayFrame.flag2_label
        self.eu_flag_path = resource_path(os.path.join('Pictures', 'european-union.png'))
        self.input_layout = self.displayFrame.input_layout
        self.currency1 = self.displayFrame.currency1
        self.currency2 = self.displayFrame.currency2
        self.amount1 = self.displayFrame.amount1
        self.amount2 = self.displayFrame.amount2
        self.spacer = self.displayFrame.spacer
        
        self.buttonWidget = CurrencyButtons(self)
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.displayFrame)
        self.mainLayout.addWidget(self.buttonWidget)

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

        if len(current_text) > 15:
            return

        if param == '.' and not current_text:
            return

        if param == '.' and '.' in current_text:
            return

        new_text = current_text + param
        self.amount1.setText(new_text)

    def shuffle_currencies(self):
        """
        @brief Swaps the selected currencies
        """
        base_currency = self.currency1.currentIndex()
        target_currency = self.currency2.currentIndex()
        self.currency1.setCurrentIndex(target_currency)
        self.currency2.setCurrentIndex(base_currency)
        self.amount1.clear()
        self.amount2.clear()

    def convert_currency(self):
        """
        @brief Converts the amount from one currency to another
        """
        if not self.amount1.text():
            return
            
        try:
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
        except (ValueError, ZeroDivisionError):
            self.amount2.setText("Error")

    def handle_sidebar_visibility(self, visible):
        """
        @brief Handles the sidebar visibility change
        @param visible: Boolean indicating if sidebar should be visible
        """
        if visible:
            self.input_layout.setContentsMargins(5, 10, 5, 7)
            if self.spacer:
                self.spacer.changeSize(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        else:
            self.input_layout.setContentsMargins(5, 35, 5, 7)
            if self.spacer:
                self.spacer.changeSize(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.input_layout.invalidate()
        self.input_layout.activate()
        self.displayFrame.updateGeometry()
        self.update()
