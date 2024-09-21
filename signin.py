from PyQt5.QtWidgets import QWidget
from components import Input, Button


class SignInPage(QWidget):
    def __init__(self):
        super().__init__()
        self.move(750, 200)
        self.resize(400,600)
        self.setWindowTitle("Tizimga kirish")

        self.usernameInput = Input(self, 100, "Username kiriting...")
        self.passwordInput = Input(self, 180, "Password kiriting...")

        self.signinBtn = Button(self, 300, "Kirish")