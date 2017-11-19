import threading

from core import constants as cn
from core.constants import _onlineList
from core.dbmanagenment import DbClient

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

        response = None
        if len(packet) == 22:
            code, field1, field2, key = struct.unpack('b 10s 10s b', packet)
            field1=self.purge(field1)
            field2 = self.purge(field2)
            _log.info("request ---> type:{} ,field1:{} ,field2:{}    [ {} , {} ] ".format(code, field1, field2, self.host,self.port))

            #todo add validate manner

            if code==0:     #register
                response=self.registerUser(field1,field2)
            elif code==1:     #login
                response = self.loginUser(field1,field2)
            elif code== 2:   #search
                response=self.searchUser(field1,field2)
            elif code == 3:  # LOGOUT
                response = self.logOut(field1)


        return response

    def validate(self):
        return True
    def logOut(self,username):
        response=''
        if username in _onlineList:
            response = struct.pack('b b 15s b', 3, 25, bytes("succesfulyexit", 'utf-8'), 15)
            self.printLog(23)
            del(_onlineList[username])

        else:
            response = struct.pack('b b 15s b', 3, 45, bytes("usernotfound", 'utf-8'), 15)
            self.printLog(45)
        return response

    def loginUser(self,username,password):
        result = self.checkAuthentication(username, password)
        response=''
        if result != -1:
            response = struct.pack('b b 15s b', 1, 21, bytes("succesfullyogin", 'utf-8'), 15)
            _onlineList[result['_id']] = [self.host,0]
            print(_onlineList)
            self.printLog(21)
        else:
            response = struct.pack('b b 15s b', 1, 41, bytes("invalidcredent", 'utf-8'), 15)
            self.printLog(41)
        return response

    def searchUser(self,current,search):
        if search in _onlineList:
            self.printLog(22)
            return struct.pack('b b 15s b', 2, 22, bytes(_onlineList[search], 'utf-8'), 15)
        else:
            self.printLog(44)
            return struct.pack('b b 15s b', 2, 44, bytes('notfound', 'utf-8'), 15)

    def registerUser(self,username,password):
        result=self.db.insert({
            "_id": username,
            "name": username,
            "password": password,
            "hostlist": [self.host]

        })
        response=''
        if result==0:
            self.printLog(20)
            response = struct.pack('b b 15s b',0, 20, bytes('registered', 'utf-8'), 15)
        elif result==-1:
            self.printLog(40)
            response = struct.pack('b b 15s b',0, 40, bytes('duplicatecredent', 'utf-8'), 15)
        else:
            self.printLog(50)
            response = struct.pack('b b 15s b',0, 50, bytes('erorserver', 'utf-8'), 15)
        return response

    def checkAuthentication(self,username,password):
        result=self.db.get_documents(filter={
            "_id": username,
            "password":password
        })
        return result


    
                     
            
    def printLog(self,code):
        if code==20:
            _log.info("response ---> type:{} status:{} message:registered    [ {} , {} ]".format(0,20,self.host, self.port))
        elif code==21:
            _log.info("response --->type:{} status:{} message:succesfullogin    [ {} , {} ]".format(1, 21, 'succesfullogin', self.host,                                                                                       self.port))
        elif code==22:
            _log.info("response --->type:{} status:{} message:found    [ {} , {} ]".format(2, 22, self.host, self.port))
        elif code==23:
            _log.info("response --->type:{} status:{} message:succesfulyexit    [ {} , {} ]".format(3, 23, self.host,self.port))
        elif code==40:
            _log.info("response ---> type:{} status:{} message:duplicatecredent    [ {} , {} ]".format(0,40,self.host, self.port))
        elif code==41:
            _log.info( "response --->type:{} status:{} message:invalidcredent    [ {} , {} ]".format(1, 41, self.host,self.port))
        elif code==44:
            _log.info("response --->type:{} status:{} message:notfound    [ {} , {} ]".format(2, 44, self.host, self.port))
        elif code==45:
            _log.info(
                "response --->type:{} status:{} message:usernotfound    [ {} , {} ]".format(3, 45, self.host,self.port))
        elif code == 50:
            _log.info("response ---> type:{} status:{} message:erorserver    [ {} , {} ]".format(0,50,self.host, self.port))


