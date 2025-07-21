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

AMOUNT_STYLE = """
QLineEdit {
    color: white;
    background-color: #4F4F4F;
    font-size: 16px;
    border-radius: 10px;
    font-weight: bold;
    padding: 5px;
}
"""

ACTIVE_STYLE = """
QLineEdit {
    color: white;
    background-color: #4F4F4F;
    font-size: 16px;
    border-radius: 10px;
    font-weight: bold;
    padding: 5px;
    border: 2px solid orange;
}
"""

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
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.displayFrame = QFrame(self)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")
        self.displayFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.displayFrame)

        layout = QGridLayout(self.displayFrame)
        layout.setContentsMargins(20, 10, 10, 10)
        layout.setHorizontalSpacing(5)
        layout.setVerticalSpacing(8)
        
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer, 0, 0)

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

        # Height input
        height_label = QLabel("Height:")
        height_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(height_label, 0, 1, Qt.AlignRight | Qt.AlignVCenter)

        height_layout = QHBoxLayout()
        height_layout.setSpacing(5)

        self.height_input = QLineEdit()
        self.height_input.setFixedWidth(200)
        self.height_input.setFixedHeight(30)

        self.height_feet_input = QLineEdit()
        self.height_feet_input.setFixedWidth(97)
        self.height_feet_input.setFixedHeight(30)
        self.height_feet_input.setPlaceholderText("Feet")

        self.height_inches_input = QLineEdit()
        self.height_inches_input.setFixedWidth(97)
        self.height_inches_input.setFixedHeight(30)
        self.height_inches_input.setPlaceholderText("Inches")

        self.height_unit_combo = QComboBox()
        self.height_unit_combo.addItems(["cm", "ft"])
        self.height_unit_combo.setFixedWidth(50)
        self.height_unit_combo.currentIndexChanged.connect(self.update_height_inputs)

        height_layout.addWidget(self.height_input)
        height_layout.addWidget(self.height_feet_input)
        height_layout.addWidget(self.height_inches_input)
        height_layout.addWidget(self.height_unit_combo)

        layout.addLayout(height_layout, 0, 2, Qt.AlignLeft | Qt.AlignVCenter)

        # Weight input
        weight_label = QLabel("Weight:")
        weight_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(weight_label, 1, 1, Qt.AlignRight | Qt.AlignVCenter)

        weight_layout = QHBoxLayout()
        weight_layout.setSpacing(5)

        self.weight_input = QLineEdit()
        self.weight_input.setFixedWidth(200)
        self.weight_input.setFixedHeight(30)

        self.weight_unit_combo = QComboBox()
        self.weight_unit_combo.addItems(["kg", "lb"])
        self.weight_unit_combo.setFixedWidth(50)

        weight_layout.addWidget(self.weight_input)
        weight_layout.addWidget(self.weight_unit_combo)

        layout.addLayout(weight_layout, 1, 2, Qt.AlignLeft | Qt.AlignVCenter)

        # Result input
        result_label = QLabel("BMI:")
        result_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(result_label, 2, 1, Qt.AlignRight | Qt.AlignVCenter)

        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)
        self.result_input.setStyleSheet(amount_style)
        self.result_input.setFixedWidth(200)
        self.result_input.setFixedHeight(30)

        layout.addWidget(self.result_input, 2, 2, Qt.AlignLeft | Qt.AlignVCenter)

        self.update_height_inputs()

        if self.height_unit_combo.currentText() == "cm":
            self.current_input = self.height_input
        else:
            self.current_input = self.height_feet_input

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

        self.height_unit_combo.setStyleSheet(combobox_style)
        self.height_unit_combo.setFixedSize(70, 30)

        self.weight_unit_combo.setStyleSheet(combobox_style)
        self.weight_unit_combo.setFixedSize(70, 30)

        self.setup_input_validation(self.height_input)
        self.setup_input_validation(self.weight_input)
        self.setup_input_validation(self.height_feet_input)
        self.setup_input_validation(self.height_inches_input)
    
    def eventFilter(self, obj, event):
        """
        @brief Handles focus events for QLineEdit widgets to add an orange outline.
        @param obj: The object being filtered.
        @param event: The event being processed.
        @return: True if the event is handled, False otherwise.
        """
        if isinstance(obj, QLineEdit):
            if event.type() == QEvent.FocusIn:
                obj.setStyleSheet(ACTIVE_STYLE)
                
                parent = self.parent()
                if parent and hasattr(parent, "current_input") and hasattr(parent, "buttonPanel"):
                    input_fields = [self.height_input, self.weight_input, 
                                    self.height_feet_input, self.height_inches_input]
                    for input_field in input_fields:
                        if input_field != obj:
                            input_field.setStyleSheet(AMOUNT_STYLE)
                    
                    parent.current_input = obj
                    
                    if hasattr(parent.buttonPanel, "current_input"):
                        parent.buttonPanel.current_input = obj
                        
            elif event.type() == QEvent.FocusOut:
                pass
            
        return super().eventFilter(obj, event)
    
    def update_height_inputs(self):
        """
        @brief Updates the visibility of height inputs based on the selected unit.
        """
        is_feet = self.height_unit_combo.currentText() == "ft"
        self.height_input.setVisible(not is_feet)
        self.height_feet_input.setVisible(is_feet)
        self.height_inches_input.setVisible(is_feet)

    def setup_input_validation(self, input_widget):
        """
        @brief Sets up input validation for the given QLineEdit widget.
        @param input_widget: The QLineEdit widget to set up validation for.
        """
        regex = QRegularExpression(r'^\d{0,5}(\.\d{0,2})?$')
        validator = QRegularExpressionValidator(regex)
        input_widget.setValidator(validator)
