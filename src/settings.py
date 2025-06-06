from PySide6.QtCore import QSize, Qt, QRegularExpression, Signal, QEvent
from PySide6.QtGui import QFont, QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFormLayout, QComboBox, QHBoxLayout,
    QSpacerItem, QSizePolicy, QScrollArea)

LIGHT_GRAY = "#979797"
DARK_GRAY = "#3D3D3D"
ORANGE = "#FFA500"
GRAY = "#808080"
COLOR_REST = "#4F4F4F"
LABEL_COLOR = "#25265E"
HOVER_COLOR = "#898989"
HOVER_OPERATOR = "#FF8409"


class Settings(QWidget):
    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.content_layout = None
        self.content_widget = None
        self.theme_combobox = None
        self.font_size_combobox = None
        self.dropdown_visible = False
        self.original_spacing = 20

        self.combo_box_style = """
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
                border: none;
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
                image: url(../Pictures/60995.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                color: white;
                background-color: #4F4F4F;
                border: none;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
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

        self.setWindowTitle("Settings")
        self.setup_ui()
        self.setup_theme_section()
        self.setup_font_size()
        self.setup_event_filters()

    def setup_ui(self):
        self.setFixedSize(400, 405)
        self.setStyleSheet(f"background-color: {DARK_GRAY};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        title_label = QLabel("Settings")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: white; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"background-color: {DARK_GRAY};")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(self.original_spacing)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)

    def setup_theme_section(self):
        theme_container = QFrame()
        theme_container.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {ORANGE};
                border-radius: 10px;
                background-color: {DARK_GRAY};
            }}
        """)

        theme_layout = QHBoxLayout(theme_container)
        theme_layout.setSpacing(70)

        theme_label = QLabel("Theme")
        theme_label.setFont(QFont("Arial", 18, QFont.Bold))
        theme_label.setStyleSheet("color: white; border: none;")
        theme_label.setFixedWidth(100)
        theme_layout.addWidget(theme_label)

        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Light Theme", "Dark Theme", "High Contrast"])
        self.theme_combobox.setCurrentText("Dark Theme")
        self.theme_combobox.setFixedWidth(150)
        self.theme_combobox.setStyleSheet(self.combo_box_style)

        theme_layout.addWidget(self.theme_combobox)
        theme_layout.addStretch()
        self.content_layout.addWidget(theme_container)

    def setup_font_size(self):
        font_option = {
            "Default": True,
            "Small": False,
            "Large": False,
        }

        font_size_container = QFrame()
        font_size_container.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {ORANGE};
                border-radius: 10px;
                background-color: {DARK_GRAY};
            }}
        """)

        font_size_layout = QHBoxLayout(font_size_container)
        font_size_layout.setSpacing(70)

        font_size_label = QLabel("Size")
        font_size_label.setFont(QFont("Arial", 18, QFont.Bold))
        font_size_label.setStyleSheet("color: white; border: none;")
        font_size_label.setFixedWidth(100)
        font_size_layout.addWidget(font_size_label)

        self.font_size_combobox = QComboBox()
        self.font_size_combobox.addItems([key for key in font_option.keys()])
        self.font_size_combobox.setCurrentText(list(font_option.keys())[0])
        self.font_size_combobox.setFixedWidth(150)
        self.font_size_combobox.setStyleSheet(self.combo_box_style)

        font_size_layout.addWidget(self.font_size_combobox)
        font_size_layout.addStretch()
        self.content_layout.addWidget(font_size_container)
        self.content_layout.addStretch()

    def setup_event_filters(self):
        self.theme_combobox.view().installEventFilter(self)
        self.font_size_combobox.view().installEventFilter(self)
        self.theme_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.font_size_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def eventFilter(self, obj, event):
        if obj in [self.theme_combobox.view(), self.font_size_combobox.view()]:
            if event.type() == QEvent.Type.Show:
                dropdown_height = obj.sizeHint().height() * 0.5
                if obj == self.theme_combobox.view():
                    self.content_layout.setSpacing(self.original_spacing + dropdown_height)
                self.dropdown_visible = True
            elif event.type() == QEvent.Type.Hide:
                if obj == self.theme_combobox.view():
                    self.content_layout.setSpacing(self.original_spacing)
                self.dropdown_visible = False
        return super().eventFilter(obj, event)
