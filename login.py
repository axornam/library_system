from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys, MySQLdb

login,_ = loadUiType("login.ui")

class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon(QBitmap("icons/nic.png")))
        
        with open("themes\\styles.css", "r+") as styles:
            self.setStyleSheet(styles.read())

        self.conn = MySQLdb.connect("localhost", "root", "root", "library")
        if(self.conn != None):
            print("Database Connected Successfully")

        self.handleButtons()

    def handleButtons(self):
        self.cancelButton.clicked.connect(self.close)
        self.loginButton.clicked.connect(self.handleLogin)
        self.link.clicked.connect(self.goToLogin)

    def goToLogin(self):
        from signup import SignUp
        self.window = SignUp()
        self.window.show()
        self.close()

    def handleLogin(self):
        sql = "SELECT user_name, user_email, user_password FROM users WHERE user_name = %s OR user_email = %s AND user_password = %s LIMIT 1;"
        usrname = self.userNameBox.text()
        usrpass = self.passwordBox.text()
        print("Name:", usrname)
        print("Pass:", usrpass)

        self.cur = self.conn.cursor()
        self.cur.execute(sql, (usrname, usrname, usrpass))
        print(self.cur.fetchone())
        
        if self.cur.fetchone() != ():
            from app import MainApp
            self.w = MainApp()
            self.w.show()
            self.close()
        else:
            print("\a Username does not exists")

if __name__ == "__main__":
    print("This is the Login Module")
