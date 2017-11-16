import threading
import constants as cn
from dbmanagenment import DbClient
_log = cn.getlog()
import struct

class ClientListener(threading.Thread):
    def __init__(self,name,host,socket,port='',db=None):
        threading.Thread.__init__(self)
        self.name=name
        self.host = host
        self.port = port
        self.socket = socket



    def run(self):
        while True:
            packet = self.socket.recv(1024)
            if not packet: continue
            result=self.examinePacket(packet)
            if result==-1:
                break
            self.socket.send(self.examinePacket(packet))

        self.socket.close()
        _log.info(" {}  received from {} ".format("Succesfuly Authenticated", self.host))



    def examinePacket(self,packet):
        if len(packet) == 22:
            code, username, password, key = struct.unpack('b 10s 10s b', packet)

            #todo add validate manner
            result=None

            if code==0:     #register
                result=self.registerUser(username,password)
                _log.info(" Register Request from   {}  {}".format( username,self.host))
                _log.info(" {} {} {} {} received from {} ".format(code, username, password, key, self.host))

            if code==1:     #login
                result=self.registerUser(username,password)
                _log.info(" Register Request from   {}  {}".format( username,self.host))
                _log.info(" {} {} {} {} received from {} ".format(code, username, password, key, self.host))
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
            _log.info("Succesfuly registered  {}   {}".format(username,self.host))
            packet = struct.pack('b 10s  b', 200, bytes('Succesfuly registered', 'utf-8'), 15)
        elif result==-1:
            _log.info("Duplicate username  {}   {}".format(username,self.host))
            packet = struct.pack('b 10s  b', 400, bytes('Duplicate username', 'utf-8'), 15)
        else:
            _log.info("Unknown eror ocured on server   {} {}".format(username,self.host))
            packet = struct.pack('b 10s  b', 500, bytes('Unknown eror ocured on server', 'utf-8'), 15)
        return packet

    def checkAuthentication(self,username,password):
        result=self.db.get_documents(filter={
            "_id": username,
            "password":password
        })
