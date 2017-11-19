from socket import *

from  Registryside.SocketListener import  SocketListener

_threadlist_ = []

serverPort=3131

serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("Server is listing")

while True:
    connectionSocket,addr = serverSocket.accept()
    thread = SocketListener(host=addr,socket=connectionSocket)
    thread.start()
    _threadlist_.append(thread)