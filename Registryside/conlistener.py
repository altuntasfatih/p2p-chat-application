import threading
import time
from core import constants as cn
from core.constants import ONLINEUSERS,DBNAME,COLLECTIONS
from core.dbmanagenment import DbClient
import socket



LOG = cn.getlog()

import struct


class Listener(threading.Thread):
    def __init__(self, host, socket, db=None):
        threading.Thread.__init__(self)
        self.host = host[0]
        self.port = host[1]
        self.socket = socket
        if db is None:
            self.db = DbClient(DBNAME, COLLECTIONS)

    def stop(self):

        self.__stop = True

    def e_d_ncrypt(self,packet,flag):
        if flag:
            pass
            #return DES_.encrypt(packet)
        else:
            pass
            #return DES_.decrypt(packet)
        return packet

    def run(self):
        while True:
            try:

                packet = self.e_d_ncrypt(self.socket.recv(1024),flag=False)
                if not packet: break
                result = self.examinePacket(packet)
                self.socket.send(self.e_d_ncrypt(result,flag=True))
            except socket.error as e:
                break

        LOG.info(" Connection closed [ {} , {} ]".format(self.host, self.port))
        self.socket.close()
        self.stop()

    def purge(self, Message):
        Message = Message.decode('utf-8')
        index = Message.find('\x00')
        if index != -1:
            return Message[0:index]

    def examinePacket(self, packet):

        response = None
        if len(packet) == 27:
            code, field1, field2, key = struct.unpack('b 10s 15s b', packet)
            field1 = self.purge(field1)
            field2 = self.purge(field2)
            LOG.info(
                "Request ---> Type:{} , Field1:{} , Field2:{}    [ {} , {} ] ".format(code, field1, field2, self.host,
                                                                                    self.port))

            # todo add validate manner

            if code == 0:  # register
                response = self.registerUser(field1, field2)
            elif code == 1:  # login
                response = self.loginUser(field1, field2)
            elif code == 2:  # search
                response = self.searchUser(field1, field2)
            elif code == 3:  # LOGOUT
                response = self.logOut(field1)
            elif code == 4:  # All
                response = self.allUser(field1)

        return response

    def validate(self):
        return True

    def logOut(self, username):
        response = ''
        if username in ONLINEUSERS:
            response = struct.pack('b b 15s b', 3, 25, bytes("succesfulyexit", 'utf-8'), 15)
            self.printLog(23)

            del (ONLINEUSERS[username])

        else:
            response = struct.pack('b b 15s b', 3, 45, bytes("usernotfound", 'utf-8'), 15)
            self.printLog(45)

        return response

    def allUser(self, username):

        response = ''
        string = ''
        for key, value in ONLINEUSERS.items():
            string = string + key + '-' + value[0] + ' \t\n '

        if string == '':
            string == "No online User"
            response = struct.pack('b b 15s b', 4, 46, bytes("no online user", 'utf-8'), 15)
            self.printLog(46)
        else:
            response = struct.pack('b b 15s b', 4, 24, bytes("online list", 'utf-8'), 15)
            response = response + bytes(string, 'utf-8')
            self.printLog(24)
        return response

    def loginUser(self, username, password):
        result = self.checkAuthentication(username, password)
        response = ''
        if result != -1:
            response = struct.pack('b b 15s b', 1, 21, bytes("succesfullyogin", 'utf-8'), 15)
            ONLINEUSERS[result['_id']] = [self.host, round(time.time())]
            #print(ONLINEUSERS)
            self.printLog(21)
        else:
            response = struct.pack('b b 15s b', 1, 41, bytes("invalidcredent", 'utf-8'), 15)
            self.printLog(41)
        return response

    def searchUser(self, current, search):
        if search in ONLINEUSERS:
            self.printLog(22)
            return struct.pack('b b 15s b', 2, 22, bytes(ONLINEUSERS[search][0], 'utf-8'), 15)
        else:
            self.printLog(44)
            return struct.pack('b b 15s b', 2, 44, bytes('notfound', 'utf-8'), 15)

    def registerUser(self, username, password):
        result = self.db.insert({
            "_id": username,
            "name": username,
            "password": password,
            "hostlist": [self.host]

        })
        response = ''
        if result == 0:
            self.printLog(20)
            response = struct.pack('b b 15s b', 0, 20, bytes('registered', 'utf-8'), 15)
        elif result == -1:
            self.printLog(40)
            response = struct.pack('b b 15s b', 0, 40, bytes('duplicatecredent', 'utf-8'), 15)
        else:
            self.printLog(50)
            response = struct.pack('b b 15s b', 0, 50, bytes('erorserver', 'utf-8'), 15)
        return response

    def checkAuthentication(self, username, password):
        result = self.db.get_documents(filter={
            "_id": username,
            "password": password
        })
        return result

    def printLog(self, code):
        if code == 20:
            LOG.info(
                "Response ---> Type:{} Status:{} Message: registered    [ {} , {} ]".format(0, 20, self.host, self.port))
        elif code == 21:
            LOG.info(
                "Response ---> Type:{} Status:{} Message: succesfullogin    [ {} , {} ]".format(1, 21, 'succesfullogin',
                                                                                              self.host, self.port))
        elif code == 22:
            LOG.info("Response ---> Type:{} Status:{} Message: found    [ {} , {} ]".format(2, 22, self.host, self.port))
        elif code == 23:
            LOG.info("Response ---> Type:{} Status:{} Message: succesfulyexit    [ {} , {} ]".format(3, 23, self.host,
                                                                                                    self.port))
        elif code == 24:
            LOG.info(
                "Response ---> Type:{} Status:{} Message: online list sended    [ {} , {} ]".format(4, 24, self.host,
                                                                                                  self.port))
        elif code == 40:
            LOG.info("Response ---> Type:{} Status:{} Message: duplicatecredent    [ {} , {} ]".format(0, 40, self.host,
                                                                                                       self.port))
        elif code == 41:
            LOG.info("Response ---> Type:{} Status:{} Message: invalidcredent    [ {} , {} ]".format(1, 41, self.host,
                                                                                                    self.port))
        elif code == 44:
            LOG.info(
                "Response --->Type:{} Status:{} Message: notfound    [ {} , {} ]".format(2, 44, self.host, self.port))
        elif code == 45:
            LOG.info(
                "Response --->Type:{} Status:{} Message: usernotfound    [ {} , {} ]".format(3, 45, self.host,
                                                                                            self.port))
        elif code == 45:
            LOG.info(
                "Response --->Type:{} Status:{} Message: no online user    [ {} , {} ]".format(4, 46, self.host,
                                                                                              self.port))
        elif code == 50:
            LOG.info(
                "Response ---> Type:{} Status:{} Message: erorserver    [ {} , {} ]".format(0, 50, self.host, self.port))


