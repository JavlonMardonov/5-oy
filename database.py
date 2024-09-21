import mysql.connector
from errors import WrongRepeatedPasswordError, UsernameAlreadyExists

class Database:
    def __init__(self):
        self.__db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2008"
        )
        self.__cursor = self.__db.cursor()

        self.__setup()

    def __setup(self):
        self.__cursor.execute("CREATE DATABASE IF NOT EXISTS TELEGRAM;")
        self.__cursor.execute("USE TELEGRAM;")

        # Users Table
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            FULLNAME VARCHAR(128),
            USERNAME VARCHAR(128) UNIQUE,
            PASSWORD VARCHAR(64),
            SIGN_DATETIME TIMESTAMP DEFAULT NOW()
            );
        """)

        # Chats Table
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS CHATS (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            USER1_ID INT,
            USER2_ID INT,
            FOREIGN KEY (USER1_ID) REFERENCES USERS(ID),
            FOREIGN KEY (USER2_ID) REFERENCES USERS(ID),
            CHAT_DATETIME TIMESTAMP DEFAULT NOW()
            );
        """)

        # Messages Table
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS MESSAGES (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            CHAT_ID INT,
            SENDER_ID INT,
            MESSAGE_TEXT TEXT,
            SENT_DATETIME TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (CHAT_ID) REFERENCES CHATS(ID),
            FOREIGN KEY (SENDER_ID) REFERENCES USERS(ID)
            );
        """)

    def selectUsers(self) -> list:
        query = "SELECT * FROM USERS"
        self.__cursor.execute(query)
        users = self.__cursor.fetchall()
        return users

    def selectUser(self, username: str) -> dict | None:
        query = "SELECT * FROM USERS WHERE USERNAME = %s"
        self.__cursor.execute(query, (username,))
        user = self.__cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "fullname": user[1],
                "username": user[2],
                "password": user[3],
                "sign_datetime": user[4]
            }
        else:
            return None

    def login(self, username: str, password: str) -> dict | None:
        query = "SELECT * FROM USERS WHERE USERNAME = %s AND PASSWORD = %s"
        self.__cursor.execute(query, (username, password))
        user = self.__cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "fullname": user[1],
                "username": user[2],
                "password": user[3],
                "sign_datetime": user[4]
            }
        else:
            return None

    def register(self, fullname: str, username: str, password: str, repeat_password: str):
        if password != repeat_password:
            raise WrongRepeatedPasswordError("Passwords do not match!")

        foundUser = self.selectUser(username)
        if foundUser:
            raise UsernameAlreadyExists("Username already taken.")

        try:
            query = "INSERT INTO USERS (FULLNAME, USERNAME, PASSWORD) VALUES (%s, %s, %s)"
            self.__cursor.execute(query, (fullname, username, password))
            self.__db.commit()
            return "Registration successful!"
        except mysql.connector.Error as err:
            return f"Error: {err}"

    def createChat(self, user1_id: int, user2_id: int):
        query = "INSERT INTO CHATS (USER1_ID, USER2_ID) VALUES (%s, %s)"
        self.__cursor.execute(query, (user1_id, user2_id))
        self.__db.commit()
        return "Chat created!"

    def selectChats(self) -> list:
        query = "SELECT * FROM CHATS"
        self.__cursor.execute(query)
        chats = self.__cursor.fetchall()
        return chats

    def selectChat(self, chat_id: int) -> dict | None:
        query = "SELECT * FROM CHATS WHERE ID = %s"
        self.__cursor.execute(query, (chat_id,))
        chat = self.__cursor.fetchone()
        if chat:
            return {
                "id": chat[0],
                "user1_id": chat[1],
                "user2_id": chat[2],
                "chat_datetime": chat[3]
            }
        else:
            return None
    def sendMessage(self, chat_id: int, sender_id: int, message_text: str):
        query = "INSERT INTO MESSAGES (CHAT_ID, SENDER_ID, MESSAGE_TEXT) VALUES (%s, %s, %s)"
        self.__cursor.execute(query, (chat_id, sender_id, message_text))
        self.__db.commit()
        return "Message sent!"

    def selectMessages(self, chat_id: int) -> list:
        query = "SELECT * FROM MESSAGES WHERE CHAT_ID = %s"
        self.__cursor.execute(query, (chat_id,))
        messages = self.__cursor.fetchall()
        return messages

    def selectMessage(self, message_id: int) -> dict | None:
        query = "SELECT * FROM MESSAGES WHERE ID = %s"
        self.__cursor.execute(query, (message_id,))
        message = self.__cursor.fetchone()
        if message:
            return {
                "id": message[0],
                "chat_id": message[1],
                "sender_id": message[2],
                "message_text": message[3],
                "sent_datetime": message[4]
            }
        else:
            return None
    def getChatsByUserId(self, user_id: int) -> list:
        query = """
        SELECT * FROM CHATS WHERE USER1_ID = %s OR USER2_ID = %s
        """
        self.__cursor.execute(query, (user_id, user_id))
        chats = self.__cursor.fetchall()
        return [
            {
                "id": chat[0],
                "user1_id": chat[1],
                "user2_id": chat[2],
                "chat_datetime": chat[3]
            }
            for chat in chats
        ]

    def selectUserById(self, user_id: int) -> dict | None:
        query = "SELECT * FROM USERS WHERE ID = %s"
        self.__cursor.execute(query, (user_id,))
        user = self.__cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "fullname": user[1],
                "username": user[2],
                "password": user[3],
                "sign_datetime": user[4]
            }
        else:
            return None

    def checkChatExists(self, user1_id: int, user2_id: int) -> bool:
        query = """
        SELECT * FROM CHATS WHERE (USER1_ID = %s AND USER2_ID = %s)
        OR (USER1_ID = %s AND USER2_ID = %s)
        """
        self.__cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
        chat = self.__cursor.fetchone()
        return chat is not None