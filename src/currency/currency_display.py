"""
@file: currency_display.py
@brief: This module provides a simple currency display for the calculator application.

@author: Martin Valapka
"""

from PySide6.QtCore import QSize, Qt, QRegularExpression
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator, QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)
from .currency_api import get_exchange_rate, get_supported_currencies, get_currency_name, get_flag_image
from utils.img_path import resource_path
import os
import sys

# Color definitions
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class CurrencyDisplay(QWidget):
    """
    @brief A class that represents a simple currency display widget.
    """
    def __init__(self, parent=None):
        """
        @brief Initializes the CurrencyDisplay widget.
        @param parent: The parent widget.
        """
        super().__init__(parent)
        self.parent = parent
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.currency_names = get_currency_name()
        self.eu_flag_path = resource_path(os.path.join('Pictures', 'european-union.png'))

        self.displayFrame = QFrame(self)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")
        self.displayFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.displayFrame)
        
        frame_layout = QGridLayout(self.displayFrame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        
        input_widget = QWidget()
        input_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.input_layout, self.currency1, self.currency2, self.amount1, self.amount2 = self.create_input_layout()
        input_widget.setLayout(self.input_layout)
        
        frame_layout.addWidget(input_widget, 0, 0)

    def create_input_layout(self):
        """
        @brief Creates the layout for the input fields
        """
        input_layout = QGridLayout()
        input_layout.setSpacing(3)
        input_layout.setColumnStretch(0, 1)
        input_layout.setContentsMargins(5, 35, 5, 7)

        vertical_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        input_layout.addItem(vertical_spacer, 2, 0)

        self.spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        arrow_icon_path = resource_path(os.path.join('Pictures', '60995.png'))
        arrow_icon_path = arrow_icon_path.replace('\\', '/')

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
            font-family: 'Consolas';
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
            image: url(""" + arrow_icon_path + """);
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

        amount_style = """
        QLineEdit {
            color: white;
            background-color: #4F4F4F;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
            padding: 5px;
        }
        """

        currency1 = QComboBox()
        currency1.setStyleSheet(combobox_style)
        currency1.setMinimumSize(320, 40)
        currency1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        currency1.addItems([f"{code} | {name}" for code, name in self.currency_names])

        amount1 = QLineEdit()
        amount1.setStyleSheet(amount_style)
        amount1.setMinimumSize(320, 40)
        amount1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        amount1.setPlaceholderText("Amount")

        shuffle_button = QPushButton()
        shuffle_button.setFont(QFont("Arial", 20))
        shuffle_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #4F4F4F;
                border-radius: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {DARK_GRAY};
            }}
        """)
        icon = QIcon(resource_path(os.path.join('Pictures', 'shuffle.png')))
        shuffle_button.setIcon(icon)
        shuffle_button.setIconSize(QSize(30, 30))
        shuffle_button.setFixedSize(40, 40)
        
        if self.parent:
            shuffle_button.clicked.connect(self.parent.shuffle_currencies)

        currency2 = QComboBox()
        currency2.setStyleSheet(combobox_style)
        currency2.setMinimumSize(320, 40)
        currency2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        currency2.addItems([f"{code} | {name}" for code, name in self.currency_names])

        amount2 = QLineEdit()
        amount2.setStyleSheet(amount_style)
        amount2.setMinimumSize(320, 40)
        amount2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        amount2.setPlaceholderText("Converted Amount")
        amount2.setReadOnly(True)

        self.flag1_label = QLabel()
        self.flag1_label.setFixedSize(50, 35)
        self.flag2_label = QLabel()
        self.flag2_label.setFixedSize(50, 35)

        currency1_layout = QHBoxLayout()
        currency1_layout.addWidget(self.flag1_label)
        currency1_layout.addSpacing(5)
        currency1_layout.addWidget(currency1)
        currency1_layout.setAlignment(Qt.AlignLeft)

        amount1_layout = QHBoxLayout()
        amount1_layout.addWidget(amount1)
        amount1_layout.addWidget(shuffle_button)
        amount1_layout.setSpacing(5)
        amount1_layout.setAlignment(Qt.AlignLeft)

        currency2_layout = QHBoxLayout()
        currency2_layout.addWidget(self.flag2_label)
        currency2_layout.addSpacing(5)
        currency2_layout.addWidget(currency2)
        currency2_layout.setAlignment(Qt.AlignLeft)

        input_layout.addLayout(currency1_layout, 0, 0)
        input_layout.addLayout(amount1_layout, 1, 0)

        vertical_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        input_layout.addItem(vertical_spacer, 2, 0)

        input_layout.addLayout(currency2_layout, 3, 0)
        input_layout.addWidget(amount2, 4, 0)

        currency1.currentIndexChanged.connect(lambda: self.update_flag(currency1, self.flag1_label))
        currency2.currentIndexChanged.connect(lambda: self.update_flag(currency2, self.flag2_label))

        if self.parent:
            currency2.currentIndexChanged.connect(self.parent.clear_input)

        self.update_flag(currency1, self.flag1_label)
        self.update_flag(currency2, self.flag2_label)

        regex = QRegularExpression(r"^\d{1,15}(\.\d*)?$")
        validator = QRegularExpressionValidator(regex, amount1)
        amount1.setValidator(validator)
        
        return input_layout, currency1, currency2, amount1, amount2

    def update_flag(self, combo_box, flag_label):
        """
        @brief Updates the flag image based on the selected currency
        @param combo_box: The QComboBox containing the currency selection
        @param flag_label: The QLabel where the flag image will be displayed
        """
        currency_code = combo_box.currentText().split(' | ')[0]
        flag_width = 70
        flag_height = 45
        eu_flag_width = 50
        eu_flag_height = 35

        if currency_code == "EUR":
            pixmap = QPixmap(self.eu_flag_path)
            if not pixmap.isNull():
                flag_label.setPixmap(
                    pixmap.scaled(eu_flag_width, eu_flag_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            flag_data = get_flag_image(currency_code[:2])
            if flag_data:
                pixmap = QPixmap()
                pixmap.loadFromData(flag_data)
                flag_label.setPixmap(
                    pixmap.scaled(flag_width, flag_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                flag_label.clear()
