from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt
from database import Database

class ChatWindow(QWidget):
    def __init__(self, current_user_id, chat_id):
        super().__init__()
        self.database = Database()
        self.current_user_id = current_user_id
        self.chat_id = chat_id

        self.setWindowTitle("Chat Window")
        self.resize(600, 800)

        main_layout = QVBoxLayout(self)

        # main_layout.sizeHint

        self.userchatDisplay = QTextEdit(self)
        self.user2chatDisplay = QTextEdit(self)
        self.userchatDisplay.setReadOnly(True)
        self.user2chatDisplay.setReadOnly(True)
        # self.userchatDisplay.setStyleSheet("font-size: 14px;")
        # self.user2chatDisplay.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(self.userchatDisplay)
        main_layout.addWidget(self.user2chatDisplay)

        self.loadMessages()

        input_layout = QHBoxLayout()
        self.refreshBtn = QPushButton("Refresh", self)
        self.refreshBtn.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 8px 12px;
            font-size: 14px;
        """)
        self.refreshBtn.clicked.connect(self.loadMessages)
        input_layout.addWidget(self.refreshBtn)
        
        self.messageInput = QTextEdit(self)
        self.messageInput.setFixedHeight(50)
        # self.messageInput.setFixedWidth(100)
        self.messageInput.setStyleSheet("font-size: 14px;")
        input_layout.addWidget(self.messageInput)


        self.sendButton = QPushButton("Send", self)
        self.sendButton.setStyleSheet("""
            background-color: #28a745;
            color: white;
            padding: 8px 12px;
            font-size: 14px;
        """)
        self.sendButton.clicked.connect(self.sendMessage)
        input_layout.addWidget(self.sendButton)

        main_layout.addLayout(input_layout)

    def loadMessages(self):
        messages = self.database.selectMessages(self.chat_id)
        self.userchatDisplay.clear()
        self.user2chatDisplay.clear()

        for message in messages:
            idd,chat_id,sender_id, message_text, sent_time = message[:5]
            sender = self.database.selectUserById(sender_id)

            
            sender_name = sender["fullname"]
            print(sender_id,'   ',self.current_user_id)
            if sender_id == self.current_user_id:
                formatted_message = f"""
                <div background-color: #e0f7fa; padding: 5px; border-radius: 5px; margin: 5px;">
                    <span><b>{sender_name}</b> ({sent_time}):</span><br>
                    <span>{message_text}</span>
                </div>
                """
                self.userchatDisplay.append(formatted_message)
            else:
                formatted_message = f"""
                <div text-align : right;background-color: #black; padding: 5px; border-radius: 5px; margin: 5px;">
                    <span><b>{sender_name}</b> ({sent_time}):</span><br>
                    <span>{message_text}</span>
                </div>
                """
                self.user2chatDisplay.append(formatted_message)
        self.last_message_count=len(messages) 
            
    def sendMessage(self):

        message_text = self.messageInput.toPlainText().strip()
        if message_text:

            self.database.sendMessage(self.chat_id, self.current_user_id, message_text)
            self.messageInput.clear()
            self.loadMessages()
    

# # Application entry point
if __name__ == "__main__":
    app2 = QApplication([])
    window = ChatWindow(current_user_id=1, chat_id=1)
    window.show()
    app2.exec_()
