
from socket import *
import struct
from  core.constants import getlog
import threading
import  time

class ServerChannel():
    def __init__(self, ip, portTcp,portUDp):
        self.ip = ip
        self.portTcp = portTcp
        self.portUdp = portUDp
        self.sock=None
        self.log=getlog()
        self.username=''
        self.password = ''
        self.udpThread = threading.Thread(target=self.sendHello)

    def connect(self):
        s=None
        try:
            s=socket(AF_INET,SOCK_STREAM)
            a=s.connect((self.ip, self.portTcp))
            self.sock=s;
            self.log.info("Connection Established with Registery [ {} , {} ]".format(self.ip, self.portTcp))
        except Exception as e:
            self.log.info("Connection failed to Registery [ {} , {} ]".format(self.ip,self.portTcp))

    def closeChannel(self):
        self.sock.close()

    def purge(self, message):
        message = message.decode('utf-8')
        index = message.find('\x00')
        if index != -1:
            return message[0:index]
        return message


    def operations(self,which,username='',password='',search_name=''):
        try:
            packet = None

            if which == 0:#register

                packet = struct.pack('b 10s 15s b', 0, bytes(username, 'utf-8'), bytes(password, 'utf-8'), 15)

            elif which == 1:
                packet = struct.pack('b 10s 15s b', 1, bytes(username, 'utf-8'), bytes(password, 'utf-8'), 15)

            elif which == 2:
                packet = struct.pack('b 10s 15s b', 2, bytes(self.username, 'utf-8'), bytes(search_name, 'utf-8'), 15)

            elif which == 3 :
                packet = struct.pack('b 10s 15s b', 3, bytes(self.username, 'utf-8'), bytes('LOGOUT', 'utf-8'), 15)

            self.sock.send(packet)
            recived_packet = self.sock.recv(1024)
            typ, code, message, key = struct.unpack('b b 15s b', recived_packet)
            print("Response {} {} {} {}".format(typ, code, message, key))
            message = self.purge(message)
            return [code,message]
        except Exception as e:
            print(e)
            return -1


    def sendHello(self):
        while True:
            serverUdp = socket(AF_INET, SOCK_DGRAM)
            packet = struct.pack('b 10s 10s b', 5, bytes(self.username, 'utf-8'), bytes("HELLO", 'utf-8'), 15)
            a = 2
            while a > 0:
                serverUdp.sendto(packet, (self.ip, self.portUdp))
                a -= 1

            time.sleep(1)



channel=ServerChannel(ip='localhost',portTcp=3131,portUDp=5151)
channel.connect()
while True:
    options = int(input("\nWhich: "))
    username = input("Username: ")
    password = input("password: ")
    result=channel.operations(which=options,username=username,password=password,search_name=password)
    if result[0]==21: #succefuly login
        channel.udpThread.start()
