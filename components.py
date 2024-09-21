from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QTextEdit, QLabel, QListWidget, QVBoxLayout, QListWidgetItem
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QSize


BUTTON_MAX_WIDTH = 0


class Input(QLineEdit):
    def __init__(self, oyna: QWidget, y: int, placeHolderText: str = 'kiriting...'):
        super().__init__(oyna)
        self.setPlaceholderText(placeHolderText)
        self.setGeometry(50, y, 300, 50)
        self.setStyleSheet("font-size: 22px;")

    def warning(self):
        old_style = self.styleSheet()
        self.setStyleSheet(old_style + "border: 4px solid red;")

    def correct(self):
        old_style = self.styleSheet()
        self.setStyleSheet(old_style + "border: 4px solid green;")


class TextArea(QTextEdit):
    def __init__(self, oyna: QWidget, y: int):
        super().__init__(oyna)
        self.setPlaceholderText("Malumot kiriting...")
        self.setGeometry(50, y, 300, 250)
        self.setStyleSheet("font-size: 22px;")

class Button(QPushButton):
    def __init__(self, oyna: QWidget, y: int, text: str):
        global BUTTON_MAX_WIDTH

        self.oyna = oyna
        self.y = y

        super().__init__(oyna)
        self.setText(text)
        self.setStyleSheet("""
            QPushButton {
                font-size: 22px;
                font-weight: bold;
                border-radius: 20px;
                border: none;
                background-color: black;
                color: white;
            }
                
            QPushButton::hover {
                background-color: #2e2e2e;
                color: white;
            }
                           
            QPushButton::pressed {
                background-color: white;
                color: black;
                border: 1px solid black;
            }             
        """)
        self.adjustSize()
        button_width = self.width() + 60

        if button_width > BUTTON_MAX_WIDTH:
            BUTTON_MAX_WIDTH = button_width

        self.setGeometry((oyna.width() - button_width) // 2, y, button_width, 50)


    def changeSize(self):
        self.setGeometry((self.oyna.width() - BUTTON_MAX_WIDTH) // 2, self.y, BUTTON_MAX_WIDTH, 50)


class Label(QLabel):
    def __init__(self, text: str, oyna: QWidget, y: int):
        super().__init__(oyna)
        self.setText(text)
        self.setStyleSheet("font-size: 36px;")
        self.adjustSize()
        self.move((oyna.width() - self.width()) // 2, y)


class ListWidgetWithTextArea(QListWidget):
    def __init__(self, oyna: QWidget):
        super().__init__(oyna)
        self.setGeometry(50, 120, oyna.width() - 100, 450)
        self.setStyleSheet("color: black; font-size : 24px;")

    def addTextAreaItem(self, text: str):

        widget = QWidget()
        
        layout = QVBoxLayout(widget)
        
        text_edit = QTextEdit()
        text_edit.setText(text)
        text_edit.setEnabled(False)
        
        layout.addWidget(text_edit)
        
        item = QListWidgetItem()
        
        icon = QIcon("icons/user.svg")
        item.setIcon(icon)
        
        item.setSizeHint(QSize(300, 100))
        
        self.addItem(item)
        
        self.setItemWidget(item, widget)
        
        self.setIconSize(QSize(40, 40))