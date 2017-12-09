from socket import *
import struct
import threading
import  time

#from core.constants import DES_


class ServerChannel():
    def __init__(self, ip, portTcp,portUDp):
        self.ip = ip
        self.portTcp = portTcp
        self.portUdp = portUDp
        self.sock=None
      #  self.log=getlog()
        self.username=''
        self.password = ''
        self.udpThread = threading.Thread(target=self.sendHello)

    def connect(self):
        s=None
        try:
            s=socket(AF_INET,SOCK_STREAM)
            a=s.connect((self.ip, self.portTcp))
            self.sock=s;
        #   self.log.info("Connection Established with Registery [ {} , {} ]".format(self.ip, self.portTcp))
        except Exception as e:
            print("exception error")
        #  self.log.info("Connection failed to Registery [ {} , {} ]".format(self.ip,self.portTcp))

    def closeChannel(self):
        self.sock.close()

    def e_d_ncrypt(self, packet, flag):
        if flag:
            pass
            #return DES_.encrypt(packet)
        else:
            pass
            #return DES_.decrypt(packet)
        return packet


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

            elif which == 1:#login
                packet = struct.pack('b 10s 15s b', 1, bytes(username, 'utf-8'), bytes(password, 'utf-8'), 15)

            elif which == 2:#search
                packet = struct.pack('b 10s 15s b', 2, bytes(self.username, 'utf-8'), bytes(search_name, 'utf-8'), 15)

            elif which == 3 :#logout
                packet = struct.pack('b 10s 15s b', 3, bytes(self.username, 'utf-8'), bytes('LOGOUT', 'utf-8'), 15)
            elif which == 4:#all online
                packet = struct.pack('b 10s 15s b', 4, bytes(self.username, 'utf-8'), bytes('All', 'utf-8'), 15)


            self.sock.send(self.e_d_ncrypt(packet,flag=True))
            recived_packet = self.e_d_ncrypt(self.sock.recv(1024),flag=False)


            typ, code, message, key = struct.unpack('b b 15s b', recived_packet[0:18])
            message = self.purge(message)
            if typ==4 or code==24:
                print("Online users acknowledgment")
                onlinedata=recived_packet[18:]
                print(onlinedata)
                return [code, message,onlinedata]


            print("Response {} {} {} {}".format(typ, code, message, key))

            return [code,message]
        except Exception as e:
            print(e)
            return -1



    def online_users(self,packet):
        data = str(packet,'utf-8')
        pure_data = data.split(" /t/n")[:-1]
        return pure_data


    def sendHello(self):
        while True:
            serverUdp = socket(AF_INET, SOCK_DGRAM)
            packet = struct.pack('b 10s 10s b', 5, bytes(self.username, 'utf-8'), bytes("HELLO", 'utf-8'), 15)
            a = 2
            while a > 0:
                serverUdp.sendto(packet, (self.ip, self.portUdp))
                a -= 1

            time.sleep(1)



    def send_request(self,opt,name,passs,search_name):

        result=self.operations(which=opt,username=username,password=password,search_name=password)
        self.username = username

        if result[0]==21: #succefuly login
           #self.udpThread.start()
           return result



channel=ServerChannel(ip='localhost',portTcp=3131,portUDp=5151)
channel.connect()
while True:
    options = int(input("\nWhich: "))
    username = input("Username: ")
    password = input("password: ")
    result=channel.send_request(opt=options,name=username,passs=password,search_name=password)
