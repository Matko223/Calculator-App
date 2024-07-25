import os
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QFrame
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
import platform
import sys

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

help_pictures = {
    "Help": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\help_icon.png',
    "Clear": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\Clear.ico',
    "Del": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\Del.ico',
    "Exponentiation": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\^.ico',
    "Root": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\Root.ico',
    "Factorial": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\Fact.ico',
    "Absolute value": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\Abs.ico',
    "Modulo": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\Mod.ico',
    "Addition": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\add.ico',
    "Subtraction": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\sub.ico',
    "Multiplication": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\mul.ico',
    "Division": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\div.ico',
    "Equals": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\equals.ico',
    "Decimal": r'C:\Users\val24\PycharmProjects\pythonProject1\Calculator\Kalkulajda\Pictures\decimal.ico'
}


class HelpWindow(QMainWindow):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root

        if platform.system() == 'Linux':
            self.setGeometry(root.geometry().x() + 40, root.geometry().y() + 65, 450, 400)
        else:
            self.setGeometry(root.geometry().x() + 65, root.geometry().y() + 80, 350, 350)

        self.setWindowTitle("Help")
        self.setWindowIcon(QPixmap(help_pictures["Help"]))
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
        self.create_help_content()

    def create_help_content(self):
        self.add_section_label("About", 25, ORANGE, Qt.AlignCenter)
        about_text = """Simple calculator developed by:
xcsirim00, xgajduv00, xlajdat00, and xvalapm00\n
It supports basic arithmetic operations:
Addition, subtraction, multiplication, and division.
Additionally, it provides features like:
Exponentiation, root, factorial, absolute value, and modulo.
It also supports decimal numbers and negative numbers.\n
Enjoy calculating!\n
The Calculator is divided into 2 frames - display and buttons.
The display frame shows the current expression and the result.
While the button frame contains buttons for inputting numbers, operators, and performing various operations.\n
The evaluation works automatically when you press the operator or when you press the equals button.
You can also perform calculations by typing directly on the keyboard, and the calculator will update accordingly.\n
The calculator takes maximum two operands at the same time and performs the specified operation between them.
When you make a mistake with choosing the operator, you can directly change it by selecting your desired operator.\n
The current expression is limited to 16 characters, while the total expression can accommodate up to 30 characters.\n"""
        self.add_text_label(about_text, 10, "white")

        self.add_section_label("Usage", 25, ORANGE, Qt.AlignLeft)

        self.add_image_and_label(self.scroll_layout, help_pictures["Clear"],
                                 "Clear:\nClears both the current and total expression")
        self.add_image_and_label(self.scroll_layout, help_pictures["Del"],
                                 "Erasor:\nErases the last digit/operator in the current expression")
        self.add_image_and_label(self.scroll_layout, help_pictures["Exponentiation"],
                                 "Exponentiation:\nBase^Exponent = Product\n\n5^2 = 25")
        self.add_image_and_label(self.scroll_layout, help_pictures["Root"],
                                 "Root:\nⁿ√x = Root\n\nn - degree, x - radical\n\n²√25 = 5")
        self.add_image_and_label(self.scroll_layout, help_pictures["Factorial"],
                                 "Factorial:\nUNARY OPERATOR\n\nNumber!\n\n(Num-1)×(Num-2) × ... × 1\n\n4! = 4 × 3 × 2 × 1")
        self.add_image_and_label(self.scroll_layout, help_pictures["Absolute value"],
                                 "Absolute value:\nUNARY OPERATOR\n\n|Number|\n\nReturns the distance from 0\n\n|5| = 5\n\n|-5| = 5")
        self.add_image_and_label(self.scroll_layout, help_pictures["Modulo"],
                                 "Modulo:\nNum % Num = R\n\nEvaluates the remainder after division\n\n7 % 3 = 1")
        self.add_image_and_label(self.scroll_layout, help_pictures["Addition"],
                                 "Addition:\nNum + Num = Sum\n\nReturns the sum after addition\n\n7 + 3 = 10")
        self.add_image_and_label(self.scroll_layout, help_pictures["Subtraction"],
                                 "Subtraction:\nNum - Num = Difference\n\nReturns the difference after subtraction\n\n7 - 3 = 4")
        self.add_image_and_label(self.scroll_layout, help_pictures["Multiplication"],
                                 "Multiplication:\nNum × Num = Product\n\nReturns the product after multiplication\n\n7 × 3 = 21")
        self.add_image_and_label(self.scroll_layout, help_pictures["Division"],
                                 "Division:\nNum ÷ Num = Quotient\n\nReturns the quotient after division\n\nNum ÷ 0 = Division error\n\n10 ÷ 2 = 5")
        self.add_image_and_label(self.scroll_layout, help_pictures["Equals"],
                                 "Equals:\nEvaluates the expression:\n\nFrom the total and current expression\n\nClears the total expression\n\nPrints the result to the current expression")
        self.add_image_and_label(self.scroll_layout, help_pictures["Decimal"],
                                 "Decimal point:\nPlaces decimal point in the current expression\n\nRounds the number if there are only zeroes behind the decimal point\n\nRemoves trailing decimal point if no digit follows it")

        self.add_section_label("Specific usage", 25, ORANGE, Qt.AlignLeft)
        self.add_text_label("More detailed usage of specific buttons\n", 10, "white")

        self.add_image_and_label(self.scroll_layout, help_pictures["Exponentiation"],
                                 "How to use Exponentiation:\n1. Choose the base\n2. Select the exponentiation button\n3. Choose the Exponent\n4. Exponent cannot be decimal or negative")
        self.add_image_and_label(self.scroll_layout, help_pictures["Root"],
                                 "How to use Root:\n1. Choose the degree\n2. Select the root button\n3. Choose the radical\n4. Radical follows mathematical rules + cannot be decimal")
        self.add_image_and_label(self.scroll_layout, help_pictures["Factorial"],
                                 "How to use Factorial:\n1. Choose the number - not negative or decimal\n2. Select the factorial button '!'")
        self.add_image_and_label(self.scroll_layout, help_pictures["Absolute value"],
                                 "How to use Absolute value:\n1. Choose the number\n2. Select the Abs. value button")
        self.add_image_and_label(self.scroll_layout, help_pictures["Modulo"],
                                 "How to use Modulo:\n1. Choose the number\n2. Select the Modulo button\n3. Choose the divisor except 0")

    def add_section_label(self, text, font_size, color, alignment):
        label = QLabel(text)
        label.setFont(QFont("Arial", font_size))
        label.setStyleSheet(f"color: {color}; background-color: {DARK_GRAY}; font-weight: bold;")
        label.setAlignment(alignment)
        label.setContentsMargins(0, 10, 0, 10)  # Adding top and bottom margins
        self.scroll_layout.addWidget(label)

    def add_text_label(self, text, font_size, color):
        label = QLabel(text)
        label.setFont(QFont("Arial", font_size))
        label.setStyleSheet(f"color: {color}; background-color: {DARK_GRAY}; font-weight: bold")
        label.setWordWrap(True)
        label.setContentsMargins(0, 10, 0, 10)  # Adding top and bottom margins
        self.scroll_layout.addWidget(label)

    def add_image_and_label(self, layout, image_path, text):
        container = QFrame()
        container.setStyleSheet(f"background-color: {GRAY}; border-radius: 10px;")
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(5, 15, 5, 15)  # Adding top and bottom margins
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
            description_label.setWordWrap(True)
            description_label.setFixedWidth(event.size().width() - image.sizeHint().width() - 40)

        container.resizeEvent = resize_wraplength


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    help_window = HelpWindow(main_window)
    help_window.show()
    sys.exit(app.exec())
