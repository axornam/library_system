from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys, MySQLdb

login,_ = loadUiType("signup.ui")

class SignUp(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Sign Up")
        self.setWindowIcon(QIcon(QBitmap("icons/nic.png")))

        self.conn = MySQLdb.connect("localhost", "root", "root", "library")

        with open("themes\\styles.css", "r+") as styles:
            self.setStyleSheet(styles.read())

        self.handleButtons()

    def handleButtons(self):
        self.cancelButton.clicked.connect(self.close)
        self.loginButton.clicked.connect(self.handleSignUp)
        self.link.clicked.connect(self.goToLogin)

    def goToLogin(self):
        from login import Login
        self.window = Login()
        self.window.show()
        self.close()

    def handleSignUp(self):
        sql = """INSERT INTO users (user_name, user_email, user_password) VALUE (%s, %s, %s)"""
        usrname = self.userNameBox.text()
        usrmail = self.userEmailBox.text()
        usrpass = self.userPasswordBox.text()

        self.cur = self.conn.cursor()
        try:
            self.cur.execute(sql, (usrname, usrmail, usrpass))
            self.conn.commit()
            self.goToLogin()
        except all as e:
            print("Something Happend")
        finally:
            self.conn.close()

        # if self.cur.fetchone():
        #     self.goToLogin()
            # self.w = app.MainApp()
            # self.close()
            # self.w.show()


if __name__ == "__main__":
    print("This is The Sign Up Module")
