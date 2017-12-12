from socket import *

from  Registryside.conlistener import Listener

_threadlist_ = []

serverPort=3131

serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("Server is listing")

while True:
    connectionSocket,addr = serverSocket.accept()
    print("Connection accepted from    [ {} , {} ]".format(addr[0], addr[1]))
    thread = Listener(host=addr,socket=connectionSocket)
    thread.start()
    _threadlist_.append(thread)