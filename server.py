import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 5320
s.bind((host, port))
s.listen(5)
socketclient, address = s.accept()
print("Connection recieved from another terminal", address)


while (True):
    message = socketclient.recv(1024)
    message = message.decode("utf-8")
    print(message)