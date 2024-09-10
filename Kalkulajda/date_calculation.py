from PySide6.QtCore import QSize, Qt, QRegularExpression
from PySide6.QtGui import QFont, QIcon, Qt, QShortcut, QKeySequence, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy)
from datetime import datetime, date

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
        self.start_day_combobox = None
        self.start_month_combobox = None
        self.start_year_input = None
        self.end_day_combobox = None
        self.end_month_combobox = None
        self.end_year_input = None

        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.frame_layout()
        layout.addWidget(self.displayFrame)

    def frame_layout(self):
        self.displayFrame = QFrame(self)
        self.displayFrame.setStyleSheet(f"background-color: {DARK_GRAY};")
        self.displayFrame.setFixedHeight(405)

        frame_layout = QGridLayout(self.displayFrame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        # Adjust the startDate label
        self.startDate = QLabel("Start date", self.displayFrame)
        self.startDate.setStyleSheet(f"color: white; font-size: 25px; font-weight: bold; margin-top: 3px;")
        self.startDate.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.startDate, 0, 1, Qt.AlignCenter)

        frame_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed), 1, 1)

        # Add comboboxes for day and month, and text field for year
        start_date_input_layout, self.start_day_combobox, self.start_month_combobox, self.start_year_input = self.create_date_input_layout()
        frame_layout.addLayout(start_date_input_layout, 2, 1, Qt.AlignCenter)

        # Adjust the endDate label
        self.endDate = QLabel("End date", self.displayFrame)
        self.endDate.setStyleSheet(f"color: white; font-size: 25px; font-weight: bold; margin-top: 40px;")
        self.endDate.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.endDate, 3, 1, Qt.AlignCenter)

        frame_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed), 4, 1)

        # Add comboboxes for end date
        end_date_input_layout, self.end_day_combobox, self.end_month_combobox, self.end_year_input = self.create_date_input_layout()
        frame_layout.addLayout(end_date_input_layout, 5, 1, Qt.AlignCenter)

        # Add the calculateButton, slightly above the resultLabel
        self.calculateButton = QPushButton("Calculate", self.displayFrame)
        self.calculateButton.setStyleSheet(
            "QPushButton {"
            f"    background-color: {ORANGE}; color: white; font-size: 20px; font-weight: bold; border-radius: 10px; "
            "    margin-top: 15px;"
            "}"
            f"QPushButton:hover {{"
            f"    background-color: {HOVER_OPERATOR};"
            "}}"
        )
        self.calculateButton.setFixedSize(120, 55)
        self.calculateButton.clicked.connect(self.calculate)
        frame_layout.addWidget(self.calculateButton, 6, 1, Qt.AlignCenter)

        # Add the resultLabel
        self.resultLabel = QLabel("", self.displayFrame)
        self.resultLabel.setStyleSheet(f"color: white; font-size: 15px; font-weight: bold; margin-top: 20px;")
        self.resultLabel.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.resultLabel, 7, 1, Qt.AlignCenter)

        # Add a vertical spacer to ensure there is no extra space on the sides
        frame_layout.addItem(QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 8, 1)

    def create_date_input_layout(self):
        date_input_layout = QHBoxLayout()
        date_input_layout.setSpacing(10)

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
            padding-right: 20px;
        }
        QComboBox:on {
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 0px;
            border-top-right-radius: 10px;
        }
        QComboBox::down-arrow {
            image: url(./Pictures/60995.png);
            width: 12px;
            height: 12px;
        }
        QComboBox QAbstractItemView {
            color: white;
            background-color: #4F4F4F;
            selection-background-color: #666666;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }
        QComboBox::item {
            padding: 4px;
        }
        QComboBox::item:selected {
            background-color: #666666;
        }
        """

        day_combobox = QComboBox(self.displayFrame)
        day_combobox.addItems([str(i) for i in range(1, 32)])
        day_combobox.setStyleSheet(combobox_style)
        day_combobox.setFixedSize(120, 40)

        month_combobox = QComboBox(self.displayFrame)
        month_combobox.addItems(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                 'September', 'October', 'November', 'December'])
        month_combobox.setStyleSheet(combobox_style)
        month_combobox.setFixedSize(120, 40)

        year_input = QLineEdit(self.displayFrame)
        year_input.setStyleSheet("color: white; background-color: #4F4F4F; font-size: 16px; border-radius: 10px; "
                                 "font-weight: bold; padding: 5px;")
        year_input.setFixedSize(120, 40)
        year_input.setPlaceholderText("Year")

        # Add regex validator to year input
        regex = QRegularExpression("^[0-9]{1,4}$")
        validator = QRegularExpressionValidator(regex, year_input)
        year_input.setValidator(validator)

        date_input_layout.addWidget(day_combobox)
        date_input_layout.addWidget(month_combobox)
        date_input_layout.addWidget(year_input)
        return date_input_layout, day_combobox, month_combobox, year_input

    def calculate(self):
        try:
            # Get values from input widgets
            startDay = int(self.start_day_combobox.currentText())
            startMonth = self.start_month_combobox.currentIndex() + 1
            startYear = int(self.start_year_input.text())
            endDay = int(self.end_day_combobox.currentText())
            endMonth = self.end_month_combobox.currentIndex() + 1
            endYear = int(self.end_year_input.text())

            date1 = date(startYear, startMonth, startDay)
            date2 = date(endYear, endMonth, endDay)
            result = abs((date2 - date1).days)

            # Format the dates with three-letter month abbreviations
            date1_str = f"{date1.day} {date1.strftime('%b')}, {date1.year}"
            date2_str = f"{date2.day} {date2.strftime('%b')}, {date2.year}"

            self.resultLabel.setText(f"Difference between {date1_str} and {date2_str} is:\n{result} days")
        except ValueError as e:
            self.resultLabel.setText(f"Error: {str(e)}. \nPlease enter valid dates.")