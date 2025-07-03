"""
@file: date_buttons.py
@brief: This module provides the buttons for the date calculation mode in the calculator application.

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

LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"

class DateButtons(QWidget):
    """
    @brief A class that represents the buttons for the date calculation mode.
    """
    
    def __init__(self, parent=None, frame=None):
        """
        @brief Initializes the DateButtons class.
        @param parent: The parent widget.
        @param frame: The frame to add the buttons to.
        """
        super().__init__(parent)
        if frame:
            self.displayFrame = frame
        else:
            self.displayFrame = QFrame(self)
            
        if not frame:
            self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")

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

    def get_calculate_button(self):
        """
        @brief Returns the calculate button.
        @return: The calculate button.
        """
        return self.calculateButton