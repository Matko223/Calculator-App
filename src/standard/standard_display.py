"""
@file standard_display.py
@brief: This module provides the standard display for the calculator application.

@author: Martin Valapka
"""

import sys
import os
from decimal import getcontext, Decimal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout
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