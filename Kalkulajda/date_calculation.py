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

    def __init__(self, date):
        """
        @brief Initializes the DateCalculation class.
        @param date: The initial date to use for calculations.
        """
        super().__init__()
        self.daysLabel = None
        self.calculateButton = None
        self.resultLabel = None
        self.endDate = None
        self.startDate = None
        self.displayFrame = None
        self.date = date
        self.start_day_combobox = None
        self.start_month_combobox = None
        self.start_year_input = None
        self.end_day_combobox = None
        self.end_month_combobox = None
        self.end_year_input = None

        self.setup_ui()
        self.set_current_date()

    def setup_ui(self):
        """
        @brief Sets up the user interface of the widget.
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.frame_layout()
        layout.addWidget(self.displayFrame)

    def frame_layout(self):
        """
        @brief Creates and sets up the main frame layout of the widget.
        """
        self.displayFrame = QFrame(self)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")
        self.displayFrame.setFixedHeight(405)

        frame_layout = QGridLayout(self.displayFrame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        # Set up start date section
        self.startDate = QLabel("Start date", self.displayFrame)
        self.startDate.setStyleSheet(f"color: white; font-size: 25px; font-weight: bold; margin-top: 3px;")
        self.startDate.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.startDate, 0, 1, Qt.AlignCenter)

        frame_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed), 1, 1)

        start_date_input_layout, self.start_day_combobox, self.start_month_combobox, self.start_year_input = self.create_date_input_layout()
        frame_layout.addLayout(start_date_input_layout, 2, 1, Qt.AlignCenter)

        # Set up end date section
        self.endDate = QLabel("End date", self.displayFrame)
        self.endDate.setStyleSheet(f"color: white; font-size: 25px; font-weight: bold; margin-top: 40px;")
        self.endDate.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.endDate, 3, 1, Qt.AlignCenter)

        frame_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed), 4, 1)

        end_date_input_layout, self.end_day_combobox, self.end_month_combobox, self.end_year_input = self.create_date_input_layout()
        frame_layout.addLayout(end_date_input_layout, 5, 1, Qt.AlignCenter)

        # Set up calculate button
        self.calculateButton = QPushButton("Calculate", self.displayFrame)
        self.calculateButton.setStyleSheet(
            "QPushButton {"
            f"    background-color: {ORANGE}; color: white; font-size: 20px; font-weight: bold; border-radius: 10px; "
            "    margin-top: 15px;"
            "}"
            f"QPushButton:hover {{"
            f"    background-color: {HOVER_OPERATOR};"
            "}}"
        )
        self.calculateButton.setFixedSize(120, 55)
        self.calculateButton.clicked.connect(self.calculate)
        frame_layout.addWidget(self.calculateButton, 6, 1, Qt.AlignCenter)

        # Set up result label
        self.resultLabel = QLabel("", self.displayFrame)
        self.resultLabel.setStyleSheet(f"color: white; font-size: 15px; font-weight: bold; margin-top: 20px;")
        self.resultLabel.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.resultLabel, 7, 1, Qt.AlignCenter)

        self.daysLabel = QLabel("", self.displayFrame)
        self.daysLabel.setStyleSheet(f"color: white; font-size: 25px; font-weight: bold;")
        self.daysLabel.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.daysLabel, 8, 1, Qt.AlignCenter)

        # Add a vertical spacer
        frame_layout.addItem(QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 8, 1)

    def create_date_input_layout(self):
        """
        @brief Creates the layout for date input fields (day, month, year).
        @return: A tuple containing the layout and individual input widgets.
        """
        date_input_layout = QHBoxLayout()
        date_input_layout.setSpacing(10)

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

        # Create day combobox
        day_combobox = QComboBox(self.displayFrame)
        day_combobox.addItems([str(i) for i in range(1, 32)])
        day_combobox.setStyleSheet(combobox_style)
        day_combobox.setFixedSize(120, 40)

        # Create month combobox
        month_combobox = QComboBox(self.displayFrame)
        month_combobox.addItems(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                 'September', 'October', 'November', 'December'])
        month_combobox.setStyleSheet(combobox_style)
        month_combobox.setFixedSize(120, 40)

        # Create year input
        year_input = QLineEdit(self.displayFrame)
        year_input.setStyleSheet("color: white; background-color: #4F4F4F; font-size: 16px; border-radius: 10px; "
                                 "font-weight: bold; padding: 5px;")
        year_input.setFixedSize(120, 40)
        year_input.setPlaceholderText("Year")

        # Add regex validator to year input
        regex = QRegularExpression("^[0-9]{1,4}$")
        validator = QRegularExpressionValidator(regex, year_input)
        year_input.setValidator(validator)

        date_input_layout.addWidget(day_combobox)
        date_input_layout.addWidget(month_combobox)
        date_input_layout.addWidget(year_input)
        return date_input_layout, day_combobox, month_combobox, year_input

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
            # Get values from input widgets
            startDay = int(self.start_day_combobox.currentText())
            startMonth = self.start_month_combobox.currentIndex() + 1
            startYear = int(self.start_year_input.text())
            endDay = int(self.end_day_combobox.currentText())
            endMonth = self.end_month_combobox.currentIndex() + 1
            endYear = int(self.end_year_input.text())

            # Check if the start date is February 29 and not a leap year
            if startMonth == 2 and startDay == 29 and not self.is_leap_year(startYear):
                self.resultLabel.setText(f"Invalid Start date: {startYear} is not a leap year.")
                return

            # Check if the end date is February 29 and not a leap year
            if endMonth == 2 and endDay == 29 and not self.is_leap_year(endYear):
                self.resultLabel.setText(f"Invalid End date: {endYear} is not a leap year.")
                return

            # Check if the year is greater than 0
            if startYear < 1 or endYear < 1:
                raise ValueError("Year must be greater than 0.")

            date1 = date(startYear, startMonth, startDay)
            date2 = date(endYear, endMonth, endDay)
            result = abs((date2 - date1).days)

            # Format the dates with three-letter month abbreviations
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
