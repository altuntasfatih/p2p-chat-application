import time
import socket
import threading

class UDP_Check(time,socket,threading):

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def send_hello(self):
        MESSAGE = "HELLO"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while 1:
            s.sendto(MESSAGE.encode('utf-8'), (self.ip, self.port))
            time.sleep(60)

    def run(self):

        check_thread = threading.Thread(target=self.send_hello, args=(self.ip,self.port))
        check_thread.start()