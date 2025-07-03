"""
@file: date_display.py
@brief: This module provides a simple date display for the calculator application.

@author: Martin Valapka
"""

from PySide6.QtCore import QSize, Qt, QRegularExpression
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)
from datetime import datetime, date
import os
from utils.img_path import resource_path
from day.date_buttons import DateButtons

LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class DateDisplay(QWidget):
    """
    @brief A class that represents a simple date display widget.
    """
    def __init__(self, parent=None):
        """
        @brief Initializes the DateDisplay widget.
        @param parent: The parent widget.
        """
        super().__init__(parent)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.displayFrame = None
        self.startDate = None
        self.endDate = None
        self.start_day_combobox = None
        self.start_month_combobox = None
        self.start_year_input = None
        self.end_day_combobox = None
        self.end_month_combobox = None
        self.end_year_input = None
        self.calculateButton = None
        self.resultLabel = None
        self.daysLabel = None

        self.arrow_icon_path = resource_path(os.path.join('Pictures', '60995.png'))
        self.arrow_icon_path = self.arrow_icon_path.replace('\\', '/')
        
        self.frame_layout()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
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

        self.startDate = QLabel("Start date", self.displayFrame)
        self.startDate.setStyleSheet(f"color: white; font-size: 25px; font-weight: bold; margin-top: 3px;")
        self.startDate.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.startDate, 0, 1, Qt.AlignCenter)

        frame_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed), 1, 1)

        start_date_input_layout, self.start_day_combobox, self.start_month_combobox, self.start_year_input = self.create_date_input_layout()
        frame_layout.addLayout(start_date_input_layout, 2, 1, Qt.AlignCenter)

        self.endDate = QLabel("End date", self.displayFrame)
        self.endDate.setStyleSheet(f"color: white; font-size: 25px; font-weight: bold; margin-top: 40px;")
        self.endDate.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.endDate, 3, 1, Qt.AlignCenter)

        frame_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed), 4, 1)

        end_date_input_layout, self.end_day_combobox, self.end_month_combobox, self.end_year_input = self.create_date_input_layout()
        frame_layout.addLayout(end_date_input_layout, 5, 1, Qt.AlignCenter)

        self.buttonPanel = DateButtons(self, self.displayFrame)
        self.calculateButton = self.buttonPanel.get_calculate_button()
        frame_layout.addWidget(self.calculateButton, 6, 1, Qt.AlignCenter)

        self.resultLabel = QLabel("", self.displayFrame)
        self.resultLabel.setStyleSheet(f"color: white; font-size: 15px; font-weight: bold; margin-top: 20px;")
        self.resultLabel.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.resultLabel, 7, 1, Qt.AlignCenter)

        self.daysLabel = QLabel("", self.displayFrame)
        self.daysLabel.setStyleSheet(f"color: white; font-size: 25px; font-weight: bold;")
        self.daysLabel.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.daysLabel, 8, 1, Qt.AlignCenter)

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
            image: url(""" + self.arrow_icon_path + """);
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

        day_combobox = QComboBox(self.displayFrame)
        day_combobox.addItems([str(i) for i in range(1, 32)])
        day_combobox.setStyleSheet(combobox_style)
        day_combobox.setFixedSize(120, 40)

        month_combobox = QComboBox(self.displayFrame)
        month_combobox.addItems(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                 'September', 'October', 'November', 'December'])
        month_combobox.setStyleSheet(combobox_style)
        month_combobox.setFixedSize(120, 40)

        year_input = QLineEdit(self.displayFrame)
        year_input.setStyleSheet("color: white; background-color: #4F4F4F; font-size: 16px; border-radius: 10px; "
                                 "font-weight: bold; padding: 5px;")
        year_input.setFixedSize(120, 40)
        year_input.setPlaceholderText("Year")

        regex = QRegularExpression("^[0-9]{1,4}$")
        validator = QRegularExpressionValidator(regex, year_input)
        year_input.setValidator(validator)

        date_input_layout.addWidget(day_combobox)
        date_input_layout.addWidget(month_combobox)
        date_input_layout.addWidget(year_input)
        return date_input_layout, day_combobox, month_combobox, year_input
