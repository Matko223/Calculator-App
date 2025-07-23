"""
@file: expression_display.py
@brief: This module provides a display for mathematical expressions in the calculator application.

@author: Martin Valapka
"""

import re
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, \
    QLineEdit, QStackedLayout, QLineEdit, QSizePolicy
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QIcon, QRegularExpressionValidator
from PySide6.QtCore import Qt, QSize, QRegularExpression
import math

# Color definitions
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class ExpressionDisplay(QWidget):
    """
    @brief A class that represents a display for mathematical expressions.
    """
    def __init__(self, parent=None):
        """
        @brief Initializes the ExpressionDisplay widget.
        @param parent: The parent widget.
        """
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.currentInput = None
        self.currentExpression = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        displayFrame = QWidget()
        displayFrame.setFixedHeight(125)
        displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")
        displayFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        main_layout.addWidget(displayFrame)

        layout = QVBoxLayout(displayFrame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addStretch()

        self.non_essential_widget = QWidget(displayFrame)
        self.non_essential_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        non_essential_layout = QVBoxLayout(self.non_essential_widget)
        non_essential_layout.setContentsMargins(0, 0, 0, 0)
        non_essential_layout.setSpacing(0)

        self.currentInput = QLineEdit(self.currentExpression, self.non_essential_widget)
        self.currentInput.setFont(QFont("Arial bold", 32))
        self.currentInput.setStyleSheet("color: WHITE; background-color: transparent; border: none;")
        self.currentInput.setAlignment(Qt.AlignRight)
        self.currentInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        non_essential_layout.addWidget(self.currentInput)
        
        layout.addWidget(self.non_essential_widget)
        displayFrame.setLayout(layout)
