import socket
import struct

class Request(socket,struct):

    def __init__(self,type,username,password,sckt,search_name=None):
        self.type = type
        self.username = username
        self.password = password
        self.sckt = sckt
        self.search_name = search_name

    def send_request_toServer(self):
        try:
            packet = None

            if self.type == "register":
                packet = struct.pack('b 10s 15s b', 0, bytes(self.username, 'utf-8'), bytes(self.password, 'utf-8'), 15)
            if self.type == "login":
                packet = struct.pack('b 10s 15s b', 1, bytes(self.username, 'utf-8'), bytes(self.password, 'utf-8'), 15)

            if self.type == "search":
                packet = struct.pack('b 10s 15s b', 2, bytes(self.username, 'utf-8'), bytes(self.search_name, 'utf-8'),15)

            if self.type == "logout":
                packet = struct.pack('b 10s b', 3, bytes(self.username, 'utf-8'),15)

            self.sckt.send(packet)
            recived_packet = self.sckt.recv(1024)
            return recived_packet

        except:
            return -1