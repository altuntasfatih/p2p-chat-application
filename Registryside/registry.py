from socket import *

from Registryside.conlistener import Listener
from Registryside.UdpListener import ListenerUdp
from Registryside.inspector import Checker
from  core.constants import getlog,TCP,UDP,CONECTIONS




LOG=getlog()
udpthread=None
checkerthread=None


def initalize():
    global checkerthread
    global udpthread
    udpthread=ListenerUdp(port=UDP)
    udpthread.start()
    checkerthread = Checker()
    checkerthread.start()
    listentPeers()



def listentPeers():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', TCP))
    serverSocket.listen(1)
    LOG.info("Server is listing on tcp    [ 0.0.0.0 , {} ]".format(TCP))

    while True:
        connectionSocket, addr = serverSocket.accept()
        LOG.info("Connection accepted from    [ {} , {} ]".format(addr[0],addr[1]))
        thread = Listener(host=addr, socket=connectionSocket)
        thread.start()
        CONECTIONS.append(thread)


initalize()