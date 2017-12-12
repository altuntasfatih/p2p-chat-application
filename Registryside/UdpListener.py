import threading
from socket import *
import time
from core import constants as cn
from core.constants import ONLINEUSERS

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

            #self.socket.sendto(result, addr)

        self.socket.close()



    def purge(self,message):
        message = message.decode('utf-8')
        index = message.find('\x00')
        if index!=-1:
            return message[0:index]

    def examinePacket(self,packet,addr):

        typ, username, message, key = struct.unpack('b 10s 10s b', packet)
        username = self.purge(username)
        message = self.purge(message)

        _log.info("Request ---> Type:{} ,Username:{} ,Message:{}    [ {} , {} ] ".format(typ, username, message,
                                                                                         addr[0], addr[1]))
        if username in ONLINEUSERS:
            _log.info("Type:{} Status:{} message:OkHello    [ {} , {} ]".format(typ, 24, addr[0], addr[1]))
            ONLINEUSERS[username]=[ONLINEUSERS[username][0],round(time.time())]
        else:
            _log.info("Type:{} Status:{} message:UserNotFound    [ {} , {} ]".format(typ, 46, addr[0], addr[1]))

        print(ONLINEUSERS)
    def validate(self):
        return True



