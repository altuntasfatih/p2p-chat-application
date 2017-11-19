import socket
import threading

from Peerside.Classes.PeerChat import PeerChat


def chat_request(socket,ip,port):
    request = "CHAT REQUEST"
    comeback = ""
    try:
        socket.connect((ip,port))
        socket.send(request.encode('utf-8'))

        comeback = socket.recv(1024)
        print(comeback)
        if comeback == "OK":
            peer = PeerChat(ip,port)
            peer.run()
            return True
        if comeback == "REJECT":
            return False
    except:
        print("hata")
        pass

def request_handler():

    handler_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    handler_socket.bind(('',5858))
    handler_socket.listen(1)

    comeback_msg1 = "OK"
    comeback_msg2 = "REJECT"

    connectionSocket, addr = handler_socket.accept()
    print(addr)
    while 1:

        packet = connectionSocket.recv(1024)
        print(packet)
        if not packet: break

        if packet.decode('utf-8') == "CHAT REQUEST":
            requested = 1
            ip_addresses.append(addr[0])
            connectionSocket.send(comeback_msg1.encode('utf-8'))
            peer = PeerChat(addr[0],5000)
            peer.run()

    connectionSocket.close()

def main():

    rh = threading.Thread(target=request_handler) #REQUEST LISTENER
    rh.start()


main()