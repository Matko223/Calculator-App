"""
@file: img_path.py
@brief: This module contains the path to the images used in the calculator app

@author: Martin Valapka
"""

import os
import sys

def resource_path(relative_path):
    """
    @brief Get the absolute path to the resource, works for both development and PyInstaller.
    @param relative_path: The relative path to the resource.
    @return: The absolute path to the resource.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(base_path)
    
    return os.path.join(base_path, relative_path)
