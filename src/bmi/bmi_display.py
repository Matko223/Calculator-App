"""
@file: bmi_display.py
@brief: This module provides a simple display for the BMI calculator.

@author: Martin Valapka
"""

from PySide6.QtCore import QSize, Qt, QRegularExpression, QEvent
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)
from utils.img_path import resource_path
import os

LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"

class BmiDisplay(QWidget):
    """
    @brief A class that represents the BMI display widget.
    """
    def __init__(self, parent=None):
        """
        @brief Initializes the BMI display widget.
        @param parent: The parent widget.
        """
        super().__init__(parent)
        