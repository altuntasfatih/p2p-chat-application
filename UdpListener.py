import threading
import constants as cn
from socket import *
_log = cn.getlog()

import struct

class ListenerUdp(threading.Thread):

    def __init__(self,port):
        threading.Thread.__init__(self)
        self.port = port
        self.socket=None;

    def run(self):

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', self.port))

        _log.info("Server is listing on udp   [ 0.0.0.0 , {} ]".format(self.port))
        while True:
            packet, addr = self.socket.recvfrom(2048)
            result=self.examinePacket(packet,addr)
            #_log.info("request ---> type:{} ,message   [ {} , {} ] ".format(code, username, password, self.host[0],self.host[1]))
            #print(" {} received from {} ".format(message, clientAddress))


            self.socket.sendto(result, addr)



        self.socket.close()



    def purge(self,message):
        message = message.decode('utf-8')
        index = message.find('\x00')
        if index!=-1:
            return message[0:index]


    def purge(self,message):
        message = message.decode('utf-8')
        index = message.find('\x00')
        if index!=-1:
            return message[0:index]

    def examinePacket(self,packet):

        typ, username, message, key = struct.unpack('b 10s 10s b', packet)
        _log.info("request ---> type:{} ,username:{} ,message:{}    [ {} , {} ] ".format(typ, username, message,
                                                                                          self.host[0], self.host[1]))

        username=self.purge(username)
        message = self.purge(message)

        packet = struct.pack('b b 10s b', 1, 21, bytes("OkHello", 'utf-8'), 15)

        _log.info("response --->type:{} status:{} message:OkHello    [ {} , {} ]".format(typ,21, self.host[0], self.host[1]))

        return packet



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
            packet = struct.pack('b b 10s b',0, 20, bytes('Ok', 'utf-8'), 15)
        elif result==-1:
            _log.info("Duplicate username  {}   {}".format(username,self.host))
            packet = struct.pack('b b 10s b',0, 40, bytes('Eror', 'utf-8'), 15)
        else:
            _log.info("Unknown eror ocured on server   {} {}".format(username,self.host))
            packet = struct.pack('b b 10s b',0, 50, bytes('Erserver', 'utf-8'), 15)
        return packet


