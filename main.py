from PyQt5.QtWidgets import QApplication
import sys
import login, signup, app

if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = login.Login()
    w.show()
    sys.exit(a.exec_())
