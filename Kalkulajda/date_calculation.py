from PyQt5.QtGui import QRegExpValidator, QRegularExpressionValidator
from PySide6.QtCore import QSize, Qt, QRegularExpression
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)

LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class DateCalculation(QWidget):
    def __init__(self, date):
        super().__init__()
        self.calculateButton = None
        self.resultLabel = None
        self.endDate = None
        self.startDate = None
        self.displayFrame = None
        self.date = date
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # No margins for the main layout
        layout.setSpacing(0)

        self.frame_layout()
        layout.addWidget(self.displayFrame)

    def frame_layout(self):
        self.displayFrame = QFrame(self)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")
        self.displayFrame.setFixedHeight(405)

        # Create a grid layout for the frame with no margins
        frame_layout = QGridLayout(self.displayFrame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        # Adjust the startDate label
        self.startDate = QLabel("Start date", self.displayFrame)
        self.startDate.setStyleSheet(f"color: white; font-size: 20px; font-weight: bold; margin-top: 3px;")
        self.startDate.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.startDate, 0, 1, Qt.AlignCenter)

        # Adjust the endDate label
        self.endDate = QLabel("End date", self.displayFrame)
        self.endDate.setStyleSheet(f"color: white; font-size: 20px; font-weight: bold; margin-top: 100px;")
        self.endDate.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.endDate, 1, 1, Qt.AlignCenter)

        # Add the resultLabel
        self.resultLabel = QLabel("Result", self.displayFrame)
        self.resultLabel.setStyleSheet(f"color: white; font-size: 20px; font-weight: bold; margin-top: 150px;")
        self.resultLabel.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.resultLabel, 3, 1, Qt.AlignCenter)

        # Add the calculateButton, slightly above the resultLabel
        self.calculateButton = QPushButton("Calculate", self.displayFrame)
        self.calculateButton.setStyleSheet(
            f"background-color: {ORANGE}; color: white; font-size: 20px; font-weight: bold; border-radius: 10px;")
        self.calculateButton.setFixedSize(180, 50)
        self.calculateButton.clicked.connect(self.calculate)
        frame_layout.addWidget(self.calculateButton, 3, 1, Qt.AlignCenter)

        # Add a vertical spacer to ensure there is no extra space on the sides
        frame_layout.addItem(QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 3, 1)

    def calculate(self):
        pass
