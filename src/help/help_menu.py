"""
@file help_menu.py
@brief File containing help menu of the Standard Calculator.

@author Martin Valapka (xvalapm00)
@date 27.07. 2024
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QFrame
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from utils.img_path import resource_path
from help.help_content_standard import HELP_PICTURES_STANDARD, ABOUT_TEXT_STANDARD
from help.help_content_manager import HelpContentManager
import os

# Define constants
LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
LARGE = "Arial 25 bold"
SMALL = "Arial 15"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class HelpWindow(QMainWindow):
    """
    @brief Help window for the calculator application.
    """
    def __init__(self, root, *args, **kwargs):
        """
        @brief Constructor for HelpWindow.
        @param root: Parent window.
        @param args: Additional arguments.
        @param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.root = root
        self.setGeometry(root.geometry().x() + 65, root.geometry().y() + 80, 350, 350)
        self.setWindowTitle("Help")
        self.setWindowIcon(QPixmap(resource_path(os.path.join('Pictures', 'help_icon.png'))))
        self.setStyleSheet(f"background-color: {DARK_GRAY};")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.scroll_content.setStyleSheet(f"background-color: {DARK_GRAY};")
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll_area)
        
        self.content_manager = HelpContentManager()
        
        current_mode = getattr(root, "current_mode", "Standard") 
        
        self.create_help_content(current_mode)

    def create_help_content(self, mode="Standard"):
        """
        @brief Creates the help content for the specified mode.
        @param mode: Calculator mode to show help for
        """
        self.content_manager.render_help_content(self, mode)

    def add_section_label(self, text, font_size, color, alignment):
        """
        @brief Adds a section label to the help content.
        @param text: The text for the label.
        @param font_size: The font size for the label.
        @param color: The color for the label.
        @param alignment: The alignment for the label.
        """
        label = QLabel(text)
        label.setFont(QFont("Arial", font_size))
        label.setStyleSheet(f"color: {color}; background-color: {DARK_GRAY}; font-weight: bold;")
        label.setAlignment(alignment)
        self.scroll_layout.addWidget(label)

    def add_text_label(self, text, font_size, color):
        """
        @brief Adds a text label to the help content.
        @param text: The text for the label.
        @param font_size: The font size for the label.
        @param color: The color for the label.
        """
        label = QLabel(text)
        label.setFont(QFont("Arial", font_size))
        label.setStyleSheet(f"color: {color}; background-color: {DARK_GRAY}; font-weight: bold;")
        label.setWordWrap(True)
        self.scroll_layout.addWidget(label)

    def add_image_and_label(self, layout, image_path, text):
        """
        @brief Adds an image and a label to the help content.
        @param layout: The layout to add the image and label to.
        @param image_path: The path to the image.
        @param text: The text for the label.
        """
        container = QFrame()
        container.setStyleSheet(f"background-color: {GRAY}; border-radius: 10px;")
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.setSpacing(10)

        image = QLabel()
        pixmap = QPixmap(image_path)
        image.setPixmap(pixmap.scaled(45, 35, Qt.KeepAspectRatio))
        image.setFixedSize(45, 35)
        container_layout.addWidget(image)

        label_container = QVBoxLayout()
        title, description = text.split(':', 1)
        title_label = QLabel(title + ':')
        title_label.setFont(QFont("Arial", 10))
        title_label.setStyleSheet(f"color: white; background-color: {GRAY}; font-weight: bold;")
        label_container.addWidget(title_label)

        description_label = QLabel(description.strip())
        description_label.setFont(QFont("Arial", 10))
        description_label.setStyleSheet(f"color: white; background-color: {GRAY}; font-weight: bold;")
        description_label.setWordWrap(True)
        label_container.addWidget(description_label)

        container_layout.addLayout(label_container)

        container_layout.setStretchFactor(image, 0)
        container_layout.setStretchFactor(label_container, 1)

        layout.addWidget(container)

        def resize_wraplength(event):
            """
            @brief Adjusts the width of the description label to ensure proper word wrapping.
            @param event: The resize event that triggers this function.
            """
            description_label.setWordWrap(True)
            description_label.setFixedWidth(event.size().width() - image.sizeHint().width() - 40)

        container.resizeEvent = resize_wraplength
