from core import constants as cn
import struct
from Peerside.ServerChannel import *
from PyQt4 import QtCore, QtGui
from  socket  import  *
import threading
import time
import sys

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

global flagQ


log = cn.getlog()

class PeerOperation():

    def __init__(self,username,ui):
        self.username = username
        self.chat_list =set()
        self.gi=ui
        self.initilaze()

    def initilaze(self):
        listen_thread = threading.Thread(target=self.listen_server, args=('', 5858))
        listen_thread.start()
        get_message_thread = threading.Thread(target=self.get_message, args=('', 1010))
        get_message_thread.start()

    def listen_server(self, ip, port):
        global flagQ

        s = socket(AF_INET, SOCK_STREAM)
        s.bind((ip, port))
        s.listen(1)
        log.info("Server is listening on tcp [ {} , {} ] ".format(ip, port))
        while 1:
            conn, addr = s.accept()

            log.info("Connection excepted from {}".format(addr[0]))
            while 1:
                packet = conn.recv(2048)
                if len(packet) == 0:
                    break
                code, field1, field2 = struct.unpack('b 15s 10s', packet[0:26])
                field1=self.purge(field1)
                field2 = self.purge(field2)
                log.info("Request ---> Type:{} , Field1:{} , Field2:{}    [ {} , {} ] ".format(code, field1, field2, addr[0], addr[1]))
                if code == 0:
                    self.gi.chatR(addr)
                    r=flagQ[1]
                    start_time = 0
                    while r==0:
                        if start_time > 10:
                            self.resetFlag()
                            self.gi.onaytext.setText("Incoming Request")
                            break
                        time.sleep(1)
                        start_time = start_time + 1
                        r = flagQ[1]
                        pass

                    if r==1:
                        r_packet = struct.pack('b b 15s', code, 20 ,"OK".encode('utf-8'))
                        print("Chat Accepted")
                        users=packet[26:].decode('utf-8')
                        print(users)
                        users=str(users)
                        users=users.split('\n')[:-1]
                        self.chat_list.add(addr[0])
                        for item in users:
                            self.chat_list.add(item)

                        print(self.chat_list)
                        conn.send(r_packet)
                        log.info("Response ---> Type:{} Status:{} Message: OK    [ {} , {} ]".format(code,20,addr[0],addr[1]))
                    else:
                        r_packet = struct.pack('b b 15s', code, 40, bytes("Rejected",'utf-8'))
                        conn.send(r_packet)
                        log.info("Response ---> Type:{} Status:{} Message: Rejected  [ {} , {} ]".format(code, 40, addr[0],addr[1]))

                    self.resetFlag()
                elif code==1:
                    self.chat_list.add(field1)

            conn.close()
            log.info(" Connection closed [ {} , {} ]".format(ip, port))
        print("listen_server finished")

    def get_message(self,ip,port):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((ip,port))
        s.listen(1)
        log.info("Server is listening for messages on tcp [ {} , {} ] ".format(ip, port))
        while 1:
            conn, addr = s.accept()
            log.info("Connection excepted from {}".format(addr[0]))
            data = conn.recv(2048)
            code,n_username,mess = struct.unpack('b 10s 100s', data)
            mess=self.purge(mess)
            n_username = self.purge(n_username)
            log.info(
                "Request ---> Type:{} , Field1:{} , Data:{}   [ {} , {} ] ".format(code,n_username,mess, addr[0],addr[1]))
            string=n_username+' >> '+mess
            self.gi.tb_chatscreen.append(string)
            conn.close()
            log.info(" Connection closed [ {} , {} ]".format(ip, port))
        print("get_message finished")

    def send_message(self,ip,port,packet):
        try:
            ss = socket(AF_INET, SOCK_STREAM)
            ss.connect((ip, port))

            log.info("Connected to [ {} , {} ]".format(ip, port))
            ss.send(packet)
            log.info("Response ---> Type:{} Username:{} Message: {}  [ {} , {} ]".format(2,self.username,packet,ip,port))
            ss.close()
            log.info(" Connection closed [ {} , {} ]".format(ip, port))
            return True
        except socket.error as e:
            return False

    def send_messages(self):
        print(self.chat_list)
        mess=self.gi.getMessage()
        ms = "Me >> " + mess
        self.gi.tb_chatscreen.append(ms)
        packet = struct.pack('b 10s 100s', 2, bytes(self.username, 'utf-8'), bytes(mess, 'utf-8'))
        for i in self.chat_list:
            re=self.send_message(i,1010,packet)
            if not re:
                self.chat_list.remove(i)
                print("User {} is removed ".format(i))

    def notifyNewuser(self,ip):
        packet = struct.pack('b 15s 10s', 1, bytes(ip, 'utf-8'), bytes("New User", 'utf-8'))
        print("Chat list komple, ", self.chat_list)
        for i in self.chat_list:
            log.info("Request ---> Type: 1 , IP:{} ,Message: New User    [ Destination : {}  ] ".format(ip, i))
            re = self.send_message(i, 5858, packet)
            print("Notify user sended: ",packet)
            if not re:
                self.chat_list.remove(i)
                log.info("User {} is removed ".format(i))

    def resetFlag(self):
        self.gi.onayB.setVisible(False)
        self.gi.retB.setVisible(False)
        global flagQ
        flagQ = ['name', 0]

    def purge(self, message):
        message = message.decode('utf-8')
        index = message.find('\x00')
        if index != -1:
            return message[0:index]

    def connect_peer(self, ip, port):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((ip, int(port)))
        log.info("Connected to [ {} , {} ]".format(ip, port))
        packet = struct.pack('b 15s 10s', 0, bytes("CHAT REQUEST", 'utf-8'), bytes(self.username, 'utf-8'))
        string = ''
        for value in self.chat_list:
            string = string+ value+'\n'

        packet=packet+bytes(string, 'utf-8')
        s.send(packet)
        log.info(
            "Response ---> Type:{} , Message: CHAT REQUEST , Username:{}   [ {} , {} ] ".format(0, self.username, ip, port))
        recieved = s.recv(2048)
        print(recieved)
        code, status, field2 = struct.unpack('b b 15s', recieved)
        field2=self.purge(field2)
        log.info(
            "Request ---> Type:{} , Status:{} , Field2:{}   [ {} , {} ] ".format(code,status,field2,ip,port))

        s.close()
        log.info(" Connection closed [ {} , {} ]".format(ip, port))
        if status==20 and field2 == "OK":
            self.notifyNewuser(ip)
            self.chat_list.add(ip)
            print(self.chat_list)
        else:
            log.info("Request ---> Connection Rejected [ {} , {} ]".format(ip,port))

    def send_request_to_peer(self):
        ip=self.gi.getIp()
        port=self.gi.getPort()
        self.connect_peer(ip,port)

    def Onay(self):
        global flagQ
        self.gi.onaytext.setText("Incoming Request")
        flagQ = ['name', 1]
        print(flagQ)

    def Ret(self):
        global flagQ
        self.gi.onaytext.setText("Incoming Request")
        flagQ = ['name', -1]

    def refreshOnline(self):
        data = self.gi.channel.send_request(4, self.gi.username, self.gi.password, self.gi.password)
        list=str(data[2], 'utf-8')
        list.replace(' ','')
        self.gi.textBrowser.setText(list)
        print(list)

    def logout(self):

        result = self.gi.channel.send_request(3, self.gi.username, self.gi.password, self.gi.password)
        print(result)
        if result[0] == 25:
            log.info(
                  "Response ---> Type:3 Status:{} Message: {} [ {} ]".format(result[0], result[1], self.gi.username))
            self.gi.onayB.setVisible(False)
            self.gi.retB.setVisible(False)
            self.gi.tb_chatscreen.setVisible(False)
            self.gi.te_message.setVisible(False)
            self.gi.btn_send.setVisible(False)
            self.gi.textBrowser.setVisible(False)
            self.gi.label.setVisible(False)
            self.gi.label.setVisible(False)
            self.gi.te_ip.setVisible(False)
            self.gi.label_2.setVisible(False)
            self.gi.te_port.setVisible(False)
            self.gi.btn_connect.setVisible(False)
            self.gi.btn_refresh.setVisible(False)
            self.gi.btn_logout.setVisible(False)
            self.gi.onaytext.setVisible(False)
            self.gi.onaytext.setVisible(False)
            self.gi.onayB.setVisible(False)

            self.gi.logout_message.setVisible(True)

            return
        else:
            log.info(
                  "Response ---> Type:3 Status:{} Message: {} [ {} ]".format(result[0], result[1], self.gi.username))



class Ui_ChatScreen(QtGui.QDialog):

    def __init__(self,username,password,channel):
        self.username = username
        self.password = password
        self.channel = channel
        self.peer=PeerOperation(username=username,ui=self)


    def chatR(self,name):
        self.onayB.setVisible(True)
        self.retB.setVisible(True)
        global flagQ
        flagQ = [name, 0]
        print("Chat geldi")
        self.onaytext.setText("Chat request: "+str(name[0]))

    def getIp(self):
        return self.te_ip.toPlainText()

    def getPort(self):
        return int(self.te_port.toPlainText())

    def getMessage(self):
        mess=self.te_message.toPlainText()
        self.te_message.setText('')
        return mess

    def setupUi(self, ChatScreen):

        ChatScreen.setObjectName(_fromUtf8("ChatScreen"))
        ChatScreen.resize(1000, 750)
        self.tb_chatscreen = QtGui.QTextBrowser(ChatScreen)
        self.tb_chatscreen.setGeometry(QtCore.QRect(40, 80, 591, 491))
        self.tb_chatscreen.setObjectName(_fromUtf8("tb_chatscreen"))
        self.te_message = QtGui.QTextEdit(ChatScreen)
        self.te_message.setGeometry(QtCore.QRect(40, 580, 471, 31))
        self.te_message.setObjectName(_fromUtf8("te_message"))
        self.btn_send = QtGui.QPushButton(ChatScreen)
        self.btn_send.setGeometry(QtCore.QRect(520, 580, 111, 31))
        self.btn_send.setObjectName(_fromUtf8("btn_send"))
        self.textBrowser = QtGui.QTextBrowser(ChatScreen)
        self.textBrowser.setGeometry(QtCore.QRect(680, 30, 256, 541))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.label = QtGui.QLabel(ChatScreen)
        self.label.setGeometry(QtCore.QRect(40, 36, 31, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.te_ip = QtGui.QTextEdit(ChatScreen)
        self.te_ip.setGeometry(QtCore.QRect(80, 30, 231, 31))
        self.te_ip.setObjectName(_fromUtf8("te_ip"))
        self.label_2 = QtGui.QLabel(ChatScreen)
        self.label_2.setGeometry(QtCore.QRect(320, 36, 51, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.te_port = QtGui.QTextEdit(ChatScreen)
        self.te_port.setGeometry(QtCore.QRect(370, 30, 131, 31))
        self.te_port.setObjectName(_fromUtf8("te_port"))
        self.btn_connect = QtGui.QPushButton(ChatScreen)
        self.btn_connect.setGeometry(QtCore.QRect(520, 30, 111, 31))
        self.btn_connect.setObjectName(_fromUtf8("btn_connect"))
        self.btn_refresh = QtGui.QPushButton(ChatScreen)
        self.btn_refresh.setGeometry(QtCore.QRect(845, 580, 91, 31))
        self.btn_refresh.setObjectName(_fromUtf8("btn_refresh"))

        self.btn_logout = QtGui.QPushButton(ChatScreen)
        self.btn_logout.setGeometry(QtCore.QRect(680,580,91,31))
        self.btn_logout.setObjectName(_fromUtf8("btn_logout"))

        self.logout_message = QtGui.QLabel(ChatScreen)
        self.logout_message.setGeometry(QtCore.QRect(130, 100, 731, 401))
        font2 = QtGui.QFont()
        font2.setPointSize(18)
        font2.setBold(True)
        font2.setWeight(75)
        self.logout_message.setFont(font2)
        self.logout_message.setObjectName(_fromUtf8("logout_message"))
        self.logout_message.setVisible(False)

        self.onaytext = QtGui.QLabel(ChatScreen)
        self.onaytext.setGeometry(QtCore.QRect(420, 640, 350, 31))

        self.onaytext.setFont(font)
        self.onaytext.setText("Incoming Request")

        self.onayB = QtGui.QPushButton(ChatScreen)
        self.onayB.setGeometry(QtCore.QRect(400, 690, 91, 31))
        self.onayB.setText("Onay ver")

        self.retB = QtGui.QPushButton(ChatScreen)
        self.retB.setGeometry(QtCore.QRect(530, 690, 91, 31))
        self.retB.setText("Red et")


        self.btn_logout.clicked.connect(self.peer.logout)
        self.btn_send.clicked.connect(self.peer.send_messages)
        self.btn_connect.clicked.connect(self.peer.send_request_to_peer)

        self.onayB.clicked.connect(self.peer.Onay)
        self.retB.clicked.connect(self.peer.Ret)

        self.btn_refresh.clicked.connect(self.peer.refreshOnline)
        self.peer.refreshOnline()

        self.onayB.setVisible(False)
        self.retB.setVisible(False)

        self.retranslateUi(ChatScreen)
        QtCore.QMetaObject.connectSlotsByName(ChatScreen)

    def retranslateUi(self, ChatScreen):
        ChatScreen.setWindowTitle(_translate("ChatScreen", "P2P Chat Application", None))
        self.btn_send.setText(_translate("ChatScreen", "Send", None))
        self.label.setText(_translate("ChatScreen", "IP :", None))
        self.label_2.setText(_translate("ChatScreen", "PORT : ", None))
        self.btn_connect.setText(_translate("ChatScreen", "Connect", None))
        self.btn_refresh.setText(_translate("ChatScreen", "Refresh", None))
        self.btn_logout.setText(_translate("ChatSecreen", "Logout",None))
        self.logout_message.setText(_translate("ChatScreen", "YOU HAVE BEEN SUCCESSFULLY LOGGED OUT!", None))

    def listen(self):
        while True:
            time.sleep(1)
