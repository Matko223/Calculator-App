"""
@file: help_content_manager.py
@brief: This module manages the help content for the calculator application.

@author: Martin Valapka
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QFrame
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from utils.img_path import resource_path
from help.help_content_standard import HELP_PICTURES_STANDARD, ABOUT_TEXT_STANDARD

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


class HelpContentManager(QMainWindow):
    def __init__(self):
        """
        @brief Initialize the help content manager
        """
        pass

    def get_help_content(self, mode):
        """
        @brief Get help content based on calculator mode
        @param mode: Calculator mode (standard, bmi, currency, etc.)
        @return: Dictionary containing help content for the specified mode
        """
        if mode == "Standard":
            from help.help_content_standard import HELP_CONTENT_STANDARD, HELP_PICTURES_STANDARD, ABOUT_TEXT_STANDARD
            return {
                "content": HELP_CONTENT_STANDARD,
                "pictures": HELP_PICTURES_STANDARD
            }
        else:
            from help.help_content_standard import HELP_CONTENT_STANDARD, HELP_PICTURES_STANDARD, ABOUT_TEXT_STANDARD
            return {
                "content": HELP_CONTENT_STANDARD,
                "pictures": HELP_PICTURES_STANDARD
            }

    def render_help_content(self, help_window, mode):
        """
        @brief Render help content in the help window
        @param help_window: The help window to render content in
        @param mode: The calculator mode to render content for
        """
        for i in reversed(range(help_window.scroll_layout.count())): 
            help_window.scroll_layout.itemAt(i).widget().setParent(None)
        
        help_data = self.get_help_content(mode)
        content = help_data["content"]
        pictures = help_data["pictures"]
        
        for section in content["sections"]:
            alignment = Qt.AlignCenter if section["align"] == "center" else Qt.AlignLeft
            help_window.add_section_label(section["title"], 25, ORANGE, alignment)
            
            for item in section["content"]:
                if item["type"] == "text":
                    help_window.add_text_label(item["text"].strip(), 10, "white")
                elif item["type"] == "image_label":
                    help_window.add_image_and_label(
                        help_window.scroll_layout,
                        pictures[item["image"]],
                        item["text"]
                    )
