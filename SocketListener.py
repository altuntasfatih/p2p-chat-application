import threading
import constants as cn
from dbmanagenment import DbClient
from constants import _onlineList
_log = cn.getlog()

import struct

class Listener(threading.Thread):

    def __init__(self, host,socket,db=None):
        threading.Thread.__init__(self)
        self.host = host[0]
        self.port = host[1]
        self.socket = socket
        if db is None:
            self.db = DbClient("P2PApp", "authentication")


    def run(self):
        while True:
            packet = self.socket.recv(1024)
            if not packet: continue
            result=self.examinePacket(packet)
            if result==-1:
                break
            self.socket.send(result)

        self.socket.close()
        _log.info(" {}  received from {} ".format("Succesfuly Authenticated", self.host))



    def purge(self,message):
        message = message.decode('utf-8')
        index = message.find('\x00')
        if index!=-1:
            return message[0:index]



    def examinePacket(self,packet):


        if len(packet) == 22:
            code, field1, field2, key = struct.unpack('b 10s 10s b', packet)
            field1=self.purge(field1)
            field2 = self.purge(field2)
            _log.info("request ---> type:{} ,field1:{} ,field2:{}    [ {} , {} ] ".format(code, field1, field2, self.host,self.port))

            #todo add validate manner
            response=None

            if code==0:     #register
                response=self.registerUser(field1,field2)
            elif code==1:     #login
                response = self.loginUser(field1,field2)
            elif code== 2:   #search
                response=self.searchUser(field1,field2)
            elif code == 3:  # LOGOUT
                response = self.searchUser(field1)


        return response



    def validate(self):
        return True
    def logOut(self,username):
        response=''
        if username in _onlineList:
            response = struct.pack('b b 15s b', 3, 25, bytes("SuccesfulyExit", 'utf-8'), 15)
            _log.info("response --->type:{} status:{} message:SuccesfulyExit    [ {} , {} ]".format(1, 25, self.host,
                                                                                        self.port))
        else:
            response = struct.pack('b b 15s b', 3, 45, bytes("UserNotfound", 'utf-8'), 15)
            _log.info(
                "response --->type:{} status:{} message:UserNotfound    [ {} , {} ]".format(1, 45, self.host,
                                                                                  self.port))

        return response

    def loginUser(self,username,password):
        result = self.checkAuthentication(username, password)
        response=''
        if result != -1:
            response = struct.pack('b b 15s b', 1, 20, bytes("Ok", 'utf-8'), 15)
            _onlineList[result['_id']] = self.host
            print(_onlineList)
            _log.info("response --->type:{} status:{} message:Ok    [ {} , {} ]".format(1, 20, 'Ok', self.host,
                                                                                        self.port))
        else:
            response = struct.pack('b b 15s b', 1, 41, bytes("Invalid", 'utf-8'), 15)
            _log.info(
                "response --->type:{} status:{} message:Invalid    [ {} , {} ]".format(1, 20, 'Invalid', self.host,
                                                                                      self.port))

        return response
    def searchUser(self,current,search):
        response=''
        if search in _onlineList:
            response = struct.pack('b b 15s b', 2, 22, bytes(_onlineList[search], 'utf-8'), 15)
            _log.info("response --->type:{} status:{} message:Found    [ {} , {} ]".format(1, 23, self.host, self.port))
        else:
            response = struct.pack('b b 15s b', 2, 44, bytes('Notfound', 'utf-8'), 15)
            _log.info("response --->type:{} status:{} message:Notfound    [ {} , {} ]".format(1, 23, self.host, self.port))

        return response

    def registerUser(self,username,password):
        result=self.db.insert({
            "_id": username,
            "name": username,
            "password": password,
            "hostlist": [self.host]

        })
        packet=''
        if result==0:
            _log.info("response ---> type:{} status:{} message:Registered    [ {} , {} ]".format(0,20,self.host, self.port))
            packet = struct.pack('b b 15s b',0, 20, bytes('Registered', 'utf-8'), 15)
        elif result==-1:
            _log.info("response ---> type:{} status:{} message:Duplicate    [ {} , {} ]".format(0,40,self.host, self.port))
            packet = struct.pack('b b 15s b',0, 40, bytes('Duplicate', 'utf-8'), 15)
        else:
            _log.info("response ---> type:{} status:{} message:ErorServer    [ {} , {} ]".format(0,50,self.host, self.port))
            packet = struct.pack('b b 15s b',0, 50, bytes('ErorServer', 'utf-8'), 15)
        return packet

    def checkAuthentication(self,username,password):
        result=self.db.get_documents(filter={
            "_id": username,
            "password":password
        })
        return result
