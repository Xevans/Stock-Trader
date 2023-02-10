import socket
import sqlite3
from sqlite3 import Error
#pylance does not recognize errors

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 5320
s.bind((host, port))
s.listen(5)
socketclient, address = s.accept()
print("Connection recieved from another terminal", address) #I.E. Client-Server Connection Successful 


while (True):
    message = socketclient.recv(1024)
    message = message.decode("utf-8")
    print(message)