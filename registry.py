from socket import *
from SocketListener import Listener
from  constants import getlog


"name:ip"
_port=3131
_threadList= []
_log=getlog()


def listJoin():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', _port))
    serverSocket.listen(1)
    _log.info("Server is listing on tcp    [ 0.0.0.0 , {} ]".format(_port))

    while True:
        connectionSocket, addr = serverSocket.accept()
        _log.info("Connection accepted from    [ {} , {} ]".format(addr[0],addr[1]))
        thread = Listener(host=addr, socket=connectionSocket)
        thread.start()
        _threadList.append(thread)


listJoin()