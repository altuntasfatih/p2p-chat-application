import threading
import socket
import struct
import time

from Peerside.ChannelServer import ServerChannel


ServerChannel
tcp_ip = 'localhost'
tcp_port = 3131
buffer_size = 1024


def udp_check(ip,port):
    MESSAGE = "HELLO"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while 1:
        s.sendto(MESSAGE.encode('utf-8'), (ip, port))
        time.sleep(60)


def request_toServer(type,username,password,sckt,search_name=None):
    try:
        recived_packet = None
        packet = None

        if type == "register":
            packet = struct.pack('b 10s 15s b', 0, bytes(username, 'utf-8'), bytes(password, 'utf-8'), 15)

        if type == "login":
            packet = struct.pack('b 10s 15s b', 1, bytes(username, 'utf-8'), bytes(password, 'utf-8'), 15)

        if type == "search":
            packet = struct.pack('b 10s 15s b', 2, bytes(username, 'utf-8'), bytes(search_name, 'utf-8'),15)

        if type == "logout":
            packet = struct.pack('b 10s b', 3, bytes(username, 'utf-8'),15)

        sckt.send(packet)

        recived_packet = sckt.recv(1024)

        return recived_packet

    except:
        return -1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((tcp_ip,tcp_port))

while 1:
    username= input("Username : ")
    password = input("Password : ")
    search_name = input("Search Name : ")
    choice = input("Request Type : ")

    responsepacket = None

    if choice == "register" or choice == "login" or choice == "logout":
        responsepacket = request_toServer(choice, username, password, s)
    if choice == "search":
        responsepacket = request_toServer(choice,username, password,s,search_name)


    typ, code, message, key = struct.unpack('b b 15s b', responsepacket)
    print("Response {} {} {} {}".format(typ, code, message, key))