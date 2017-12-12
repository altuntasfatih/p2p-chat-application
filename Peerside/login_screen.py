import sys
from PyQt4 import QtCore, QtGui
from core import constants as cn
from Peerside.chat_screen import Ui_ChatScreen
import time

from Peerside.ServerChannel import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

LOG = cn.getlog()
class Ui_LoginScreen(object):

    def __init__(self,mychannel):
        self.mychannel = mychannel
        self.mychannel.connect()

    def register_request(self):
        print()
        uname = self.te_username.toPlainText()
        passw = self.te_password.toPlainText()

        result = self.mychannel.send_request(0,uname,passw,passw)
        print(result)
        if result[0] == 20:
            self.showMessageBox('Succesfully Registered')
            LOG.info("You registered [ {} , {} ]".format(uname, passw))
            result =self.mychannel.send_request(1,uname,passw,passw)
            if result[0] == 21:
                LOG.info("You logined [ {} , {} ]".format(uname, passw))
                self.open_chat()

            else:
                LOG.info("You could not login [ {} , {} ]".format(uname, passw))
                self.showMessageBox('You could not Login')
        else:
            LOG.info("You could not registered [ {} , {} ]".format(uname, passw))
            print(result[0])

    def login_request(self):
        uname = self.te_username.toPlainText()
        passw = self.te_password.toPlainText()

        result = self.mychannel.send_request(1, uname, passw,passw)
        if result[0] == 21:
            LOG.info("You logined [ {} , {} ]".format(uname, passw))
            self.open_chat()
        else:
            LOG.info("You could not  [ {} , {} ]".format(uname, passw))
            self.showMessageBox('You could not Login')

    def showMessageBox(self,message):
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Warning)
        msgBox.setWindowTitle('Message Box')
        msgBox.setText(message)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()


    def open_chat(self):
        self.cwindow = QtGui.QMainWindow()
        self.ui = Ui_ChatScreen(self.te_username.toPlainText(), self.te_password.toPlainText(), self.mychannel)
        self.ui.setupUi(self.cwindow)
        MainWindow.hide()
        self.cwindow.show()

    def setupUi(self, LoginScreen):
        LoginScreen.setObjectName(_fromUtf8("LoginScreen"))
        LoginScreen.resize(1000, 650)
        self.label = QtGui.QLabel(LoginScreen)
        self.label.setGeometry(QtCore.QRect(320, 270, 81, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(LoginScreen)
        self.label_2.setGeometry(QtCore.QRect(320, 320, 81, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.te_username = QtGui.QTextEdit(LoginScreen)
        self.te_username.setGeometry(QtCore.QRect(410, 260, 211, 31))
        self.te_username.setObjectName(_fromUtf8("te_username"))
        self.te_password = QtGui.QTextEdit(LoginScreen)
        self.te_password.setGeometry(QtCore.QRect(410, 310, 211, 31))
        self.te_password.setObjectName(_fromUtf8("te_password"))
        self.label_3 = QtGui.QLabel(LoginScreen)
        self.label_3.setGeometry(QtCore.QRect(280, 140, 401, 71))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.btn_login = QtGui.QPushButton(LoginScreen)
        self.btn_login.setGeometry(QtCore.QRect(410, 350, 93, 28))
        self.btn_login.setObjectName(_fromUtf8("btn_login"))
        self.btn_register = QtGui.QPushButton(LoginScreen)
        self.btn_register.setGeometry(QtCore.QRect(530, 350, 93, 28))
        self.btn_register.setObjectName(_fromUtf8("btn_register"))

        # ----------------------------------------------------------------


        self.btn_login.clicked.connect(self.login_request)
        self.btn_register.clicked.connect(self.register_request)
        # -----------------------------------------------------------------



        self.retranslateUi(LoginScreen)
        QtCore.QMetaObject.connectSlotsByName(LoginScreen)

    def retranslateUi(self, LoginScreen):
        LoginScreen.setWindowTitle(_translate("LoginScreen", "P2P Chat Application", None))
        self.label.setText(_translate("LoginScreen", "Username : ", None))
        self.label_2.setText(_translate("LoginScreen", "Password : ", None))
        self.label_3.setText(_translate("LoginScreen", "P2P CHATT APPLICATION", None))
        self.btn_login.setText(_translate("LoginScreen", "Login", None))
        self.btn_register.setText(_translate("LoginScreen", "Register", None))

    def trigger_chatwindow(self):
        chatwindow = QtGui.QMainWindow()
        ui = Ui_ChatScreen()
        ui.setupUi(chatwindow)
        chatwindow.show()


if __name__ == "__main__":

    main_channel = ServerChannel('192.168.1.41', 3131, 5151)

    LOG.info("Channel connection started [ IP: {} , TCP PORT: {} , UDP PORT: {} ]".format('192.168.43.153',3131,5151))
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_LoginScreen(main_channel)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

