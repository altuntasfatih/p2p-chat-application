from socket import *




serverPort=3131

serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))

print("Server is listing")
while True:
    message,clientAddress = serverSocket.recvfrom(2048)
    print(" {} received from {} ".format(message,clientAddress))
    message=message.upper()
    serverSocket.sendto(message,clientAddress)
