from socket import *
import struct
import sys

def tcp():

    serverName='127.0.0.1'
    serverPort=3131

    clientSocket=socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    while True:
        options=input("Which: ")
        username = input("Username: ")
        packet=''

        if options == "0":

            password = input("password: ")
            packet = struct.pack('b 10s 10s b', 0, bytes(username, 'utf-8'), bytes(password, 'utf-8'), 15)

        if options == "1":

            password = input("password: ")
            packet = struct.pack('b 10s 10s b', 1, bytes(username, 'utf-8'), bytes(password, 'utf-8'), 15)

        if options == "2":

            search = input("Search :")
            packet = struct.pack('b 10s 10s b', 2, bytes(username, 'utf-8'), bytes(search, 'utf-8'), 15)

        if options == "3":  #LOGOUT
            packet = struct.pack('b 10s 10s b', 3, bytes(username, 'utf-8'),bytes('LOGOUT', 'utf-8'), 15)

        if options == "4":  # LOGOUT
            sendHello(username)


        clientSocket.send(packet)
        responsepacket = clientSocket.recv(1024)

        typ,code,message,key = struct.unpack('b b 15s b', responsepacket)
        print("Response {} {} {} {}".format(typ,code,message,key))





def sendHello(user):
    serverName = '127.0.0.1'

    udp = 5151

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    packet = struct.pack('b 10s 10s b', 5, bytes(user, 'utf-8'),bytes("HELLO", 'utf-8'), 15)
    a=10
    while a>0:
        clientSocket.sendto(packet, (serverName, udp))
        a-=1

    #modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    #print("Message: {}  - from {}".format(modifiedMessage, serverAddress))



tcp()