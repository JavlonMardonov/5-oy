from PyQt5.QtWidgets import QWidget
from components import Input, Button


class SignUpPage(QWidget):
    def __init__(self):
        super().__init__()
        self.move(750, 200)
        self.resize(400,600)
        self.setWindowTitle("Ro'yxatdan o'tish")

        self.fullnameInput = Input(self, 100, "Fullname kiriting...")
        self.usernameInput = Input(self, 170, "Username(Nickname) kiriting...")
        self.passwordInput = Input(self, 240, "Password kiriting...")
        self.repeatPasswordInput = Input(self, 310, "Parolni takrorlang...")

        self.signupBtn = Button(self, 450, "Ro'yhatdan o'tish")