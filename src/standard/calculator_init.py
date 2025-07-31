"""
@file: calculator_init.py
@brief: Initialization methods for the Calculator App class.

@author: Martin Valapka
"""

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from sidebar.mode_menu import Sidebar
from bmi.bmi_calculator import BMICalculator
from expression.photomath_mode import PhotomathMode
from day.date_calculation import DateCalculation
from currency.currency_converter import CurrencyConverter
from settings.settings import Settings
from utils.img_path import resource_path
import os


class CalculatorInit:
    """
    @brief Handles setup of widgets, layouts, and connections for the calculator UI.
    """

    def __init__(self, parent_app):
        """
        @brief Initializes the CalculatorInit class.
        @param parent_app: The main application instance.
        """
        self.parent_app = parent_app
        self.setup_widgets()
        self.setup_layouts()
        self.setup_connections()

    def setup_widgets(self):
        """
        @brief Initializes the main widgets and their properties
        """
        self.parent_app.sidebar = Sidebar(self.parent_app)
        self.default_widget = self.create_default_widget()
        self.parent_app.bmi_widget = BMICalculator()
        self.parent_app.photomath_widget = PhotomathMode()
        self.parent_app.date_widget = DateCalculation(self.parent_app)
        self.parent_app.currency_widget = CurrencyConverter()
        self.parent_app.settings_widget = Settings(self.parent_app)
        self.parent_app.currency_widget.parent_window = self.parent_app

    def setup_layouts(self):
        """
        @brief Sets up the layouts for the calculator UI
        """
        self.parent_app.calculator_layout.addWidget(self.default_widget)
        self.parent_app.calculator_layout.addWidget(self.parent_app.bmi_widget)
        self.parent_app.calculator_layout.addWidget(self.parent_app.photomath_widget)
        self.parent_app.calculator_layout.addWidget(self.parent_app.date_widget)
        self.parent_app.calculator_layout.addWidget(self.parent_app.currency_widget)
        self.parent_app.calculator_layout.addWidget(self.parent_app.settings_widget)

        self.parent_app.main_layout.addWidget(self.parent_app.sidebar)
        self.parent_app.main_layout.addLayout(self.parent_app.calculator_layout)

    def setup_connections(self):
        """
        @brief Connects signals and slots for the calculator UI
        """
        self.parent_app.sidebar.mode_selected.connect(self.switch_mode)
        self.parent_app.sidebar.visibility_changed.connect(
            self.parent_app.currency_widget.handle_sidebar_visibility
        )
        self.parent_app.sidebar.hide()
        self.parent_app.sidebar.select_mode("Standard")
        self.switch_mode("Standard")


    def switch_mode(self, mode):
        """
        @brief Switches between calculator modes
        """
        mode_widgets = {
            "BMI": self.parent_app.bmi_widget,
            "Expression": self.parent_app.photomath_widget,
            "Standard": self.default_widget,
            "Date Calculation": self.parent_app.date_widget,
            "Currency": self.parent_app.currency_widget,
            "Settings": self.parent_app.settings_widget
        }

        if mode == "Standard":
            self.parent_app.handle_clear()
        elif mode == "BMI":
            self.parent_app.bmi_widget.clear_input()
        elif mode == "Currency":
            self.parent_app.currency_widget.clear_input()
        elif mode == "Date Calculation":
            self.parent_app.date_widget.set_current_date()
            self.parent_app.date_widget.resultLabel.setText("")
            self.parent_app.date_widget.daysLabel.setText("")
        elif mode == "Expression":
            self.parent_app.photomath_widget.handle_clear()

        for widget in mode_widgets.values():
            widget.hide()
            self.parent_app.calculator_layout.removeWidget(widget)
        self.parent_app.non_essential_widget.hide()

        selected_widget = mode_widgets.get(mode, self.default_widget)
        selected_widget.show()
        self.parent_app.calculator_layout.addWidget(selected_widget)

        if mode == "Standard":
            self.create_mode_and_help_buttons()
            self.parent_app.non_essential_widget.show()

    def create_default_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(self.parent_app.displayFrame, 1)

        self.parent_app.button_frame()
        layout.addWidget(self.parent_app.buttonFrame)
        
        return widget
    
    def create_mode_and_help_buttons(self):
        """
        @brief Creates the widget and layout for the mode and help menu buttons.
        @return QWidget The mode and help menu buttons widget.
        """
        buttons_widget = QWidget(self.parent_app)
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(5, 5, 5, 5)
        buttons_layout.setSpacing(3)

        self.mode_menu_button = self.parent_app.create_mode_menu_button()
        self.help_menu_button = self.parent_app.create_help_menu_button()

        buttons_layout.addWidget(self.mode_menu_button)
        buttons_layout.addWidget(self.help_menu_button)
        buttons_layout.addStretch()
        return buttons_widget
