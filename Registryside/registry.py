from socket import *

from Registryside.SocketListener import Listener
from Registryside.UdpListener import ListenerUdp
from  core.constants import getlog

"name:ip"
_portTcp=3131
_portUdp=5151
_threadList= []
_log=getlog()



def initalize():
    thread=ListenerUdp(port=_portUdp)
    thread.start()
    listentPeers()


def listentPeers():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', _portTcp))
    serverSocket.listen(1)
    _log.info("Server is listing on tcp    [ 0.0.0.0 , {} ]".format(_portTcp))

    while True:
        connectionSocket, addr = serverSocket.accept()
        _log.info("Connection accepted from    [ {} , {} ]".format(addr[0],addr[1]))
        thread = Listener(host=addr, socket=connectionSocket)
        thread.start()
        _threadList.append(thread)


initalize()