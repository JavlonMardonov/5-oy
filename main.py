#main.py
from PyQt5.QtWidgets import  QApplication,QWidget,QLabel,QMessageBox

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect


from database import Database

from chatspage import ChatsPage

from errors import UsernameAlreadyExists,WrongRepeatedPasswordError

from mainpage import MainPage
from signin import SignInPage
from signup import SignUpPage



class App:
    USER = None
    def __init__(self) -> None:
        
        self.boshSaxifaOyna = MainPage()
        self.tizimgaKirishOyna = SignInPage()
        self.royxatdanOtishOyna = SignUpPage()
        
        self.database = Database()
        
        self.boshSaxifaOyna.signinBtn.clicked.connect(self.showSignInPage)
        self.boshSaxifaOyna.signupBtn.clicked.connect(self.showSignUpPage)

        self.tizimgaKirishOyna.signinBtn.clicked.connect(self.login)
        self.royxatdanOtishOyna.signupBtn.clicked.connect(self.register)

        self.boshSaxifaOyna.show()
        
        
    def showSignInPage(self):
        self.tizimgaKirishOyna.show()
        self.boshSaxifaOyna.close()


    def showSignUpPage(self):
        self.royxatdanOtishOyna.show()
        self.boshSaxifaOyna.close()


    def login(self):
        username = self.tizimgaKirishOyna.usernameInput.text()
        password = self.tizimgaKirishOyna.passwordInput.text()

        foundUser =  self.database.login(username, password)
        if not foundUser:
            return self.alert("User topilmadi!")
        

        self.USER = foundUser
        self.showChatsPage(self.USER["id"])
    

    def register(self):
        try:
            fullname = self.royxatdanOtishOyna.fullnameInput.text()
            username = self.royxatdanOtishOyna.usernameInput.text()
            password = self.royxatdanOtishOyna.passwordInput.text()
            repeat_password = self.royxatdanOtishOyna.repeatPasswordInput.text()

            created_user = self.database.register(fullname, username, password, repeat_password)

            self.USER = created_user
            self.showChatsPage(self.USER["id"])

        except WrongRepeatedPasswordError as message:
            error_message = message.args[0]
            self.alert(error_message)

        except UsernameAlreadyExists as message:
            error_message = message.args[0]
            self.alert(error_message)
            
    def showChatsPage(self,userid):
        self.chatspage=ChatsPage(userid)
        self.chatspage.show()
        self.tizimgaKirishOyna.close()
        self.royxatdanOtishOyna.close()


    
    def alert(self, title: str) -> None:
        msgbox = QMessageBox()
        msgbox.setText(title)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return msgbox.exec()
        
app = QApplication([])
oyna = App()
app.exec_()
