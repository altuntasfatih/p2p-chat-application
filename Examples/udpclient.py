from socket import *



serverName='localhost'
serverPort=3131

clientSocket=socket(AF_INET,SOCK_DGRAM)
#clientSocket.bind(('',19157))use this port for my machine
message=input("Input: ")

clientSocket.sendto(bytes(message,'utf-8'),(serverName,serverPort))

modifiedMessage,serverAddress = clientSocket.recvfrom(2048)

print("Message: {}  - from {}".format(modifiedMessage,serverAddress))