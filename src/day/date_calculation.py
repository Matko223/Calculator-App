"""
@file date_calculation.py
@brief File containing Date calculation mode for the calculator application.

@author Martin Valapka (xvalapm00)
@date 10.09. 2024
"""

from PySide6.QtCore import QSize, Qt, QRegularExpression
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)
from datetime import datetime, date
import os
from utils.img_path import resource_path
from day.date_display import DateDisplay

# Color definitions
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class DateCalculation(QWidget):
    """
    @brief A class that represents a Date Calculation widget.
    """

    def __init__(self, parent=None):
        """
        @brief Initializes the DateCalculation class.
        @param parent: The parent widget.
        """
        super().__init__(parent)
        self.displayFrame = DateDisplay()
        
        self.setup_ui()
        
        self.resultLabel = self.displayFrame.resultLabel
        self.daysLabel = self.displayFrame.daysLabel
        self.calculateButton = self.displayFrame.calculateButton
        self.startDate = self.displayFrame.startDate
        self.endDate = self.displayFrame.endDate
        
        self.start_day_combobox = self.displayFrame.start_day_combobox
        self.start_month_combobox = self.displayFrame.start_month_combobox
        self.start_year_input = self.displayFrame.start_year_input
        self.end_day_combobox = self.displayFrame.end_day_combobox
        self.end_month_combobox = self.displayFrame.end_month_combobox
        self.end_year_input = self.displayFrame.end_year_input
        
        self.set_current_date()
        
        self.calculateButton.clicked.connect(self.calculate)

    def setup_ui(self):
        """
        @brief Sets up the user interface of the widget.
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.displayFrame)

    def set_current_date(self):
        """
        @brief Sets the current date in the input fields.
        """
        current_date = datetime.now()

        self.start_day_combobox.setCurrentText(str(current_date.day))
        self.start_month_combobox.setCurrentIndex(current_date.month - 1)
        self.start_year_input.setText(str(current_date.year))

        self.end_day_combobox.setCurrentText(str(current_date.day))
        self.end_month_combobox.setCurrentIndex(current_date.month - 1)
        self.end_year_input.setText(str(current_date.year))

    def calculate(self):
        """
        @brief Calculates the difference between two dates and displays the result.
        """
        try:
            startDay = int(self.start_day_combobox.currentText())
            startMonth = self.start_month_combobox.currentIndex() + 1
            startYear = int(self.start_year_input.text())
            endDay = int(self.end_day_combobox.currentText())
            endMonth = self.end_month_combobox.currentIndex() + 1
            endYear = int(self.end_year_input.text())

            if startMonth == 2 and startDay == 29 and not self.is_leap_year(startYear):
                self.resultLabel.setText(f"Invalid Start date: {startYear} is not a leap year.")
                return

            if endMonth == 2 and endDay == 29 and not self.is_leap_year(endYear):
                self.resultLabel.setText(f"Invalid End date: {endYear} is not a leap year.")
                return

            if startYear < 1 or endYear < 1:
                raise ValueError("Year must be greater than 0.")

            date1 = date(startYear, startMonth, startDay)
            date2 = date(endYear, endMonth, endDay)
            result = abs((date2 - date1).days)

            date1_str = f"{date1.day} {date1.strftime('%b')}, {date1.year}"
            date2_str = f"{date2.day} {date2.strftime('%b')}, {date2.year}"

            self.resultLabel.setText(f"Difference between {date1_str} and {date2_str} is:")
            self.daysLabel.setText(f"{result} days")

        except ValueError as e:
            self.resultLabel.setText(f"Error: {str(e)}. \nPlease enter valid dates.")

    def is_leap_year(self, year):
        """
        @brief Determines if a given year is a leap year.
        @param year: The year to check.
        @return: True if the year is a leap year, False otherwise.
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
