from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from database import Database
from components import Button, ListWidgetWithTextArea
from chatwindow import ChatWindow
from PyQt5.QtCore import Qt,QTimer

class ChatsPage(QWidget):
    def __init__(self, current_user_id):
        super().__init__()
        self.database = Database()
        self.current_user_id = current_user_id

        self.move(750, 200)
        self.resize(400, 600)
        self.setWindowTitle("Chatlar")
        
        self.newChatBtn = Button(self, 30, "Yangi Chat")
        self.newChatBtn.changeSize()
        self.newChatBtn.setGeometry(30, 30, 150, 50)

        self.refreshBtn = Button(self, 30, "Yangilash")
        self.refreshBtn.changeSize()
        self.refreshBtn.setGeometry(220, 30, 150, 50)

        self.chatsList = ListWidgetWithTextArea(self)
        self.chatsList.setGeometry(30, 100, 340, 450)

        self.loadChats()
        

        self.newChatBtn.clicked.connect(self.createNewChat)

        self.refreshBtn.clicked.connect(self.loadChats)
        
        
        self.chatsList.itemClicked.connect(self.openChatWindow)

    def loadChats(self):
        self.chatsList.clear()

        allChats = self.database.getChatsByUserId(self.current_user_id)
        for chat in allChats:
            user1_id = chat['user1_id']
            user2_id = chat['user2_id']


            other_user_id = user2_id if user1_id == self.current_user_id else user1_id
            other_user = self.database.selectUserById(other_user_id)
            if other_user:
                other_user_name = other_user["fullname"]
                chat_summary = f"{other_user_name}"

                chat_item = self.chatsList.addTextAreaItem(chat_summary)

                if chat_item:
                    chat_item.setData(Qt.UserRole, chat['id'])  
                else:
                    print(f"Xatolik {other_user_name} bilan")
            else:
                print(f"{chat['id']}  Mavjud emas")

    def createNewChat(self):
        username, ok = self.getUserInput()  
        
        if ok and username:
            user = self.database.selectUser(username)
            if user:
                chat_exists = self.database.checkChatExists(self.current_user_id, user['id'])
                if not chat_exists:
                    self.database.createChat(self.current_user_id, user['id'])
                    self.loadChats()  
                else:
                    self.showError("Chat oldindan bor!")  
            else:
                self.showError("Bunaqa foydalanuvchi topilmadi!")

    def openChatWindow(self, item):
        chat_id = item.data(Qt.UserRole)

        self.chat_window = ChatWindow(self.current_user_id, chat_id)
        self.chat_window.show()

        
        self.chat_window.ortgaButton.clicked.connect(self.closechat)
        self.close()
        
    def closechat(self):
        self.chat_window.close()
        self.show()

    def getUserInput(self):
        from PyQt5.QtWidgets import QInputDialog
        username, ok = QInputDialog.getText(self, "Yangi chat yaratish", "Usernameni kiriting:")
        return username, ok

    def showError(self, message):
        from PyQt5.QtWidgets import QMessageBox
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(message)
        msgBox.setWindowTitle("Error")
        msgBox.exec_()

# Uncomment this section if you want to run the code directly
# app = QApplication([])
# oyna = ChatsPage(1)
# oyna.show()
# app.exec_()
