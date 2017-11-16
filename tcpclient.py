from socket import *
import struct



serverName='localhost'
serverPort=3131
user="Fatih"


clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
a=5;
while a>0:
    username=input("Username: ")
    packet = struct.pack('b 10s 10s b', 0, bytes(username, 'utf-8'), bytes("1234", 'utf-8'), 15)

    clientSocket.send(packet)
    responsepacket = clientSocket.recv(1024)

    typ,code,message,key = struct.unpack('b b 10s b', responsepacket)
    print("Response {} {} {} {}".format(typ,code,message,key))
    a-=1




def sendHello():

    udp = 5151

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    packet = struct.pack('b 10s 10s b', 3, bytes(user, 'utf-8'),bytes("HELLO", 'utf-8'), 15)

    clientSocket.sendto(packet, (serverName, udp))

    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    print("Message: {}  - from {}".format(modifiedMessage, serverAddress))






