#mainpage.py
from PyQt5.QtWidgets import QWidget, QLabel
from components import Label, Button 

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.move(750, 200)
        self.setFixedSize(600, 800)  
        self.setWindowTitle("Bosh sahifa")

        pixmap = QPixmap("icons/Telegram.png")
        
        scaled_pixmap = pixmap.scaled(200, 200) 

        label_width = scaled_pixmap.width()
        center_x = (self.width() - label_width) // 2 
            
        self.image_label = QLabel(self)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setGeometry(center_x, 50, label_width, scaled_pixmap.height())  


        self.signinBtn = Button(self, 350, "Tizimga kirish")  
        self.signupBtn = Button(self, 430, "Ro'yxatdan o'tish")  

       
        self.signinBtn.changeSize() 
        self.signupBtn.changeSize() 
