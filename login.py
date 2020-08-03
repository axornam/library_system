from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from main import MainApp
import sys, MySQLdb

login,_ = loadUiType("login.ui")

class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon(QBitmap("icons/nic.png")))

        self.handleButtons()

    def handleButtons(self):
        self.cancelButton.clicked.connect(self.close)
        self.loginButton.clicked.connect(self.handleLogin)

    def handleLogin(self):
        self.conn = MySQLdb.connect("localhost", "root", "sysadmin", "library")
        self.cur = self.conn.cursor()

        sql = "SELECT user_name FROM users WHERE user_name = %s AND user_password = %s LIMIT 1;"

        self.cur.execute(sql, (self.userNameBox.text(), self.passwordBox.text()))
        if self.cur.fetchone():
            self.w = MainApp()
            self.close()
            self.w.show()