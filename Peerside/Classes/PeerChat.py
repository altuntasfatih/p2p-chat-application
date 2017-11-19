import socket
import threading


class PeerChat(socket,threading):

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def send_message(self,socket, ip, port):
        socket.connect((ip, port))

        while 1:
            message = input("Caner ->  :")
            socket.send(message.encode('utf-8'))

    def get_message(self,socket, ip, port):
        socket.bind((ip, port))
        socket.listen(1)

        connectionSocket, addr = socket.accept()
        print(addr)

        while 1:
            message = connectionSocket.recv(1024)
            if not message: break
            print("Peer  ->  ")

    def run(self):

        gm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gt = threading.Thread(target=get_message , args=(gm,self.ip,self.port))
        gt.start()

        sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        st = threading.Thread(target=self.send_message,args=(sm,self.ip,self.port))
        st.start()