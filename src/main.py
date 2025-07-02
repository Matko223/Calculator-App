"""
@file: main.py
@brief: Main entry point for the Calculator application.

@author: Martin Valapka
"""

import sys
import os
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from standard.calculator import App
from utils.img_path import resource_path


if __name__ == "__main__":
    app = QApplication(sys.argv)

if os.name == "nt":
    icon_path = resource_path(os.path.join('icons', 'real_logo.png'))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(icon_path)

    window = App()
    window.show()
    sys.exit(app.exec())

