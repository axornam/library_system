from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import MySQLdb
import sys

ui, _ = loadUiType("deps\\library.ui")

class MainApp(QMainWindow, ui):
    __Logged_in = False

    def __init__(self):
        # Method number 1
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Method number 2
        # super().__init__()
        # self.setupUi(self)
        # self.ui = Ui_Dialog() // Use this method only when the ui is not inherited; this creates an object of ui

        self.db = MySQLdb.connect(host="localhost", user="root", password="root", db="library")
        self.cur = self.db.cursor()

        self.setWindowIcon(QIcon(QBitmap("icons/nic.png")))

        self.Handle_UI_Changes()
        self.Handle_Buttons()

        self.Show_Authors()
        self.Show_Categorys()
        self.Show_Publishers()

        self.Show_Category_In_ComboBox()
        self.Show_Publishers_In_ComboBox()
        self.Show_Authors_In_ComboBox()

    def Handle_Buttons(self):
        self.themesButton.clicked.connect(self.Show_Themes)
        self.pushButton_21.clicked.connect(self.Hide_Themes)

        # Right Aligned Button Actions when clicked
        self.dayToDayButton.clicked.connect(self.Open_Day_to_Day)
        self.settingsButton.clicked.connect(self.Open_Settings)
        self.usersButton.clicked.connect(self.Open_Users)
        self.booksButton.clicked.connect(self.Open_Books)

        # Books Tab Button Actions
        self.pushButton_2.clicked.connect(self.Add_New_Book)
        self.pushButton_4.clicked.connect(self.Search_Books)
        self.pushButton_3.clicked.connect(self.Edit_Books)
        self.pushButton_5.clicked.connect(self.Delete_Books)

        # Users Tab Button Actions
        self.pushButton_6.clicked.connect(self.Add_New_User)
        self.pushButton_7.clicked.connect(self.Login)
        self.pushButton_8.clicked.connect(self.Edit_User)

        # Settings Tab Button Actions
        self.pushButton_9.clicked.connect(self.Add_Publisher)
        self.pushButton_10.clicked.connect(self.Add_Category)
        self.pushButton_11.clicked.connect(self.Add_Author)

        # Theme Buttons Actions
        self.pushButton_17.clicked.connect(self.dark_theme)
        self.pushButton_18.clicked.connect(self.default_theme)
        self.pushButton_19.clicked.connect(self.dark_gray_theme)
        self.pushButton_20.clicked.connect(self.dark_orange_theme)

    def Handle_UI_Changes(self):
        self.Hide_Themes()
        self.tabWidget.tabBar().setVisible(False)

    def Show_Themes(self):
        if self.groupBox_3.isVisible():
            self.groupBox_3.hide()
        else:
            self.groupBox_3.show()

    def Hide_Themes(self):
        self.groupBox_3.hide()

    ###########################################################################
    ############ BOOKS ########################################################
    ###########################################################################

    ##################################
    # Add a new book to the database #
    ##################################
    def Add_New_Book(self):
        book_title = self.lineEdit_2.text()
        book_code = self.lineEdit_7.text()
        book_price = self.lineEdit_6.text()
        book_description = self.textEdit.toPlainText()
        book_cat = self.comboBox_3.currentIndex()
        book_aut = self.comboBox_7.currentIndex()
        book_pub = self.comboBox_9.currentIndex()

        self.cur.execute(""" INSERT INTO books (book_name, book_code, book_description, book_price, book_author, 
        book_publisher, book_category) VALUES ( %s, %s, %s, %s, %s, %s, %s )
        """, (book_title, book_code, book_description, book_price, book_aut, book_pub, book_cat))
        self.db.commit()
        self.statusBar.showMessage("New Book Added")

        self.lineEdit_2.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_6.setText("")
        self.textEdit.clear()
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.comboBox_9.setCurrentIndex(0)

    ###################################################
    # Search an already existing book in the database #
    ###################################################
    def Search_Books(self):
        book = self.lineEdit_8.text()
        sql = """ SELECT * FROM books WHERE book_name = \"%s\" """ % (book)
        self.cur.execute(sql)
        data = self.cur.fetchone()
        print(data)
        if data:
            self.lineEdit_10.setText(data[1])
            self.lineEdit_4.setText(data[2])
            self.textEdit_2.setText(data[3])
            self.lineEdit_9.setText(str(data[4]))
        else:
            self.statusBar.showMessage("No book found matching that name")

    def Edit_Books(self):
        book_title = self.lineEdit_10.text()
        book_code = self.lineEdit_4.text()
        book_price = self.lineEdit_9.text()
        book_description = self.textEdit_2.toPlainText()
        book_cat = self.comboBox_5.currentIndex()
        book_aut = self.comboBox_10.currentIndex()
        book_pub = self.comboBox_11.currentIndex()

        search_book_title = self.lineEdit_8.text()

        self.cur.execute("""UPDATE books SET book_name=%s, book_code=%s, book_price=%s, book_description=%s, book_category=%s, book_author=%s, book_publisher=%s 
        WHERE book_name=%s;""", (book_title, book_code, book_price, book_description, book_cat, book_aut, book_pub, search_book_title))

        self.db.commit()
        self.statusBar.showMessage("Book Updated successfully")

    def Delete_Books(self):
        book_to_delete = self.lineEdit_8.text()

        warining = QMessageBox.warning(self, "Delete Book", "Are you sure? ", QMessageBox.Yes | QMessageBox.No)
        if warining:
            self.cur.execute("DELETE FROM books WHERE book_name = '%s'" % (book_to_delete))
            self.db.commit()
            self.statusBar.showMessage("Book Deleted Successfully")

            self.lineEdit_10.setText(" ")
            self.lineEdit_4.setText(" ")
            self.lineEdit_9.setText(" ")
            self.textEdit_2.clear()

        else:
            pass

    ################################################################################
    #################### USERS #####################################################
    ################################################################################
    def Add_New_User(self):
        user_name = self.lineEdit_11.text()
        email = self.lineEdit_12.text()

        if self.lineEdit_13.text() == self.lineEdit_14.text():
            password = self.lineEdit_13.text()

            self.cur.execute("""
                INSERT INTO users (user_name, user_password, user_email)
                VALUES (%s, %s, %s)
            """, (user_name, password, email))
            self.db.commit()

            self.lineEdit_12.clear()
            self.lineEdit_11.clear()
            self.lineEdit_13.clear()
            self.lineEdit_14.clear()

            self.statusBar.showMessage("New User Added")
        else:
            self.lineEdit_14.setStyleSheet("border: 1px solid red")
            self.lineEdit_14.clear()
            self.lineEdit_13.setStyleSheet("border: 1px solid red")
            self.lineEdit_13.clear()
            self.statusBar.showMessage("Passwords Do not Match")

    def Login(self):
        name_or_email = self.lineEdit_15.text()
        password = self.lineEdit_16.text()

        self.cur.execute("""
            SELECT * FROM users WHERE user_name = %s OR user_email = %s AND user_password = %s LIMIT 1
        """, (name_or_email, name_or_email, password))

        data = self.cur.fetchone()
        print(data)

        if data:
            self.lineEdit_17.setText(data[1])
            self.lineEdit_18.setText(data[3])
            self.lineEdit_20.setText(data[2])
            self.__Logged_in = True
            self.statusBar.showMessage("You've Been Logged in successfully")
        else:
            self.statusBar.showMessage("Faile Loggin Attempt, Please Try Again with correct Info")

    def Edit_User(self):

        if self.__Logged_in == True:
            user_name = self.lineEdit_17.text()
            user_email = self.lineEdit_18.text()
            if self.lineEdit_20.text() == self.lineEdit_19.text():
                user_password = self.lineEdit_20.text() 
                self.cur.execute("""
                    UPDATE users SET user_name = %s, user_password = %s, user_email = %s WHERE user_name = %s OR user_email = %s;
                """, (user_name, user_password, user_email, self.lineEdit_15.text(), self.lineEdit_15.text()))

                self.db.commit()
                self.statusBar.showMessage("User Credentials Edited Successfully")
                self.lineEdit_20.clear()
                self.lineEdit_18.clear()
                self.lineEdit_17.clear()
                self.lineEdit_19.clear()
                self.lineEdit_15.clear()
                self.lineEdit_16.clear()
            else:
                self.statusBar.showMessage("Mismatched Passwords")
                self.lineEdit_19.clear()
                self.lineEdit_20.clear()

        else:
            self.statusBar.showMessage("You Must Log In")
    ###############################################################################
    ################ SETTINGS #####################################################
    ###############################################################################



    ##########################################
    #######     Change Themes       ##########
    ##########################################

    def dark_theme(self):
        with open("themes\\dark.css", "r") as theme:
            self.setStyleSheet(theme.read())

    def default_theme(self):
        with open("themes\\default.css", "r") as theme:
            self.setStyleSheet(theme.read())

    def dark_orange_theme(self):
        with open("themes\\orange.css", "r") as theme:
            self.setStyleSheet(theme.read())

    def dark_gray_theme(self):
        with open("themes\\gray.css", "r") as theme:
            self.setStyleSheet(theme.read())


    ####################################
    # Category Tab Settings            ##
    ####################################

    # ADD CATEGORY TO THE DATABASE
    def Add_Category(self):
        cat_name = self.lineEdit_22.text()

        self.cur.execute("""
            INSERT INTO category (category_name)
            VALUES (%s) """, (cat_name,))
        self.db.commit()
        self.statusBar.showMessage("New Category Added to Database")
        self.lineEdit_22.setText("")
        self.Show_Categorys()
        self.Show_Category_In_ComboBox()

    # SHOW ALL CATEGORYS FROM THE DATABASE
    def Show_Categorys(self):
        self.cur.execute(""" SELECT category_name FROM category """)
        data = self.cur.fetchall()
        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    ################################
    # Publisher Tab Settings       ##
    ################################
    def Add_Publisher(self):
        pub_name = self.lineEdit_21.text()

        self.cur.execute("""
            INSERT INTO publisher (publisher_name)
            VALUES (%s) """, (pub_name,))
        self.db.commit()
        self.statusBar.showMessage("New Publisher Added to Database")
        self.lineEdit_21.setText("")
        self.Show_Publishers()
        self.Show_Publishers_In_ComboBox()

    def Show_Publishers(self):
        self.cur.execute(""" SELECT publisher_name FROM publisher """)
        data = self.cur.fetchall()
        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    #############################
    # Author tab Settings       ##
    #############################
    def Add_Author(self):
        aut_name = self.lineEdit_23.text()

        self.cur.execute("""
            INSERT INTO author (author_name)
            VALUES (%s) """, (aut_name,))
        self.db.commit()
        self.statusBar.showMessage("New Author Added to Database")
        self.lineEdit_23.setText("")
        self.Show_Authors()
        self.Show_Authors_In_ComboBox()

    def Show_Authors(self):
        self.cur.execute(""" SELECT author_name FROM author """)
        data = self.cur.fetchall()
        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    ###########################################################################
    ####################### SHOW SETTINGS DATA IN THE UI ######################
    ###########################################################################
    def Show_Category_In_ComboBox(self):
        self.cur.execute(""" SELECT category_name FROM category """)
        data = self.cur.fetchall()

        self.comboBox_3.clear()
        for d in data:
            self.comboBox_3.addItems(d)
            self.comboBox_5.addItems(d)

    def Show_Authors_In_ComboBox(self):
        self.cur.execute(""" SELECT author_name FROM author """)
        data = self.cur.fetchall()

        self.comboBox_7.clear()
        for d in data:
            self.comboBox_7.addItems(d)
            self.comboBox_10.addItems(d)

    def Show_Publishers_In_ComboBox(self):
        self.cur.execute(""" SELECT publisher_name FROM publisher """)
        data = self.cur.fetchall()

        self.comboBox_9.clear()
        for d in data:
            self.comboBox_9.addItems(d)
            self.comboBox_11.addItems(d)

    ###########################################################################
    ####################### OPENING TABS ON THE UI ############################
    ###########################################################################

    def Open_Day_to_Day(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Users(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Books(self):
        self.tabWidget.setCurrentIndex(1)


if __name__ == "__main__":
    print("Main Application Module")