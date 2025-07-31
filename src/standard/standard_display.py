"""
@file standard_display.py
@brief: This module provides the standard display for the calculator application.

@author: Martin Valapka
"""

import sys
import os
from decimal import getcontext, Decimal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QIcon
from PySide6.QtCore import Qt, QSize
from standard import mathlib
from currency.currency_converter import CurrencyConverter
from day.date_calculation import DateCalculation
from help.help_menu import HelpWindow
from sidebar.mode_menu import Sidebar
from bmi.bmi_calculator import BMICalculator
from expression.photomath_mode import PhotomathMode
from settings.settings import Settings
from utils.img_path import resource_path
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


class StandardDisplay(QWidget):
    """
    @brief A class that represents the standard display for the calculator application.
    """
    def __init__(self, parent=None):
        """
        @brief Initializes the StandardDisplay class.
        @param parent: The parent widget.
        """
        super().__init__(parent)
        self.totalExpression = ""
        self.currentExpression = "0"
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.displayFrame = QWidget(self)
        self.displayFrame.setFixedHeight(125)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.displayFrame)
        
        layout = QVBoxLayout(self.displayFrame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.totalLabel = QLabel(self.totalExpression, self.displayFrame)
        self.totalLabel.setFont(QFont("Arial bold", 16))
        self.totalLabel.setStyleSheet(f"color: WHITE; padding: 5px;")
        self.totalLabel.setAlignment(Qt.AlignRight)
        layout.addWidget(self.totalLabel)

        layout.addStretch()

        self.non_essential_widget = QWidget(self.displayFrame)
        non_essential_layout = QVBoxLayout(self.non_essential_widget)
        non_essential_layout.setContentsMargins(0, 0, 0, 0)
        non_essential_layout.setSpacing(0)

        self.currentLabel = QLabel(self.currentExpression, self.non_essential_widget)
        self.currentLabel.setFont(QFont("Arial bold", 32))
        self.currentLabel.setStyleSheet(f"color: WHITE;")
        self.currentLabel.setAlignment(Qt.AlignRight)

        non_essential_layout.addWidget(self.currentLabel)

        layout.addWidget(self.non_essential_widget, alignment=Qt.AlignRight | Qt.AlignBottom)
        self.displayFrame.setLayout(layout)
