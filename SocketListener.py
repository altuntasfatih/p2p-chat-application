import threading
import constants as cn
from dbmanagenment import DbClient
_log = cn.getlog()

import struct

class Listener(threading.Thread):

    def __init__(self, host,socket,port='',db=None):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
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
            code, username, password, key = struct.unpack('b 10s 10s b', packet)
            username=self.purge(username)
            password = self.purge(password)
            _log.info("request ---> type:{} ,username:{} ,password:{}    [ {} , {} ] ".format(code, username, password, self.host[0],self.host[1]))

            #todo add validate manner
            result=None

            if code==0:     #register

                #_log.info("register Request from   {}  {}".format(username, self.host))
                result=self.registerUser(username,password)


            if code==1:     #login
                result=self.checkAuthentication(username,password)
                if result==-1:
                    packet= struct.pack('b b 10s b', 1,20, bytes("Ok", 'utf-8'),15)

                    _log.info("response --->type:{} status:{} message:Ok    [ {} , {} ]".format(1,20,'Ok', self.host[0],self.host[1]))
                elif result==-1:
                    packet = struct.pack('b b 10s b', 1, 41, bytes("Invalid", 'utf-8'), 15)
                    _log.info("response --->type:{} status:{} message:Invalid    [ {} , {} ]".format(1,20,'Invalid', self.host[0],self.host[1]))

            return result

        elif len(packet) == 12:
            code, message, key = struct.unpack('b 10s b', packet)
            _log.info(" {}  {} {} received from {} ".format(code, message, key, self.host))
            if code == -1:  #logout
                return -1
            elif code== 3:   #search
                code, message, key = struct.unpack('b 10s b', packet)
                _log.info(" {}  {} {} received from {} ".format(code, message, key, self.host))



        return bytes("Okey")



    def validate(self):
        return True


    def registerUser(self,username,password):
        result=self.db.insert({
            "_id": username,
            "name": username,
            "password": password,
            "hostlist": [self.host]

        })
        packet=''
        if result==0:
            _log.info("response ---> type:{} status:{} message:Registered    [ {} , {} ]".format(0,20,self.host[0], self.host[1]))
            packet = struct.pack('b b 10s b',0, 20, bytes('Registered', 'utf-8'), 15)
        elif result==-1:
            _log.info("response ---> type:{} status:{} message:Duplicate    [ {} , {} ]".format(0,40,self.host[0], self.host[1]))
            packet = struct.pack('b b 10s b',0, 40, bytes('Duplicate', 'utf-8'), 15)
        else:
            _log.info("response ---> type:{} status:{} message:Erserver    [ {} , {} ]".format(0,50,self.host[0], self.host[1]))
            packet = struct.pack('b b 10s b',0, 50, bytes('Erserver', 'utf-8'), 15)
        return packet

    def checkAuthentication(self,username,password):
        result=self.db.get_documents(filter={
            "_id": username,
            "password":password
        })
