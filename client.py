import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5320
s.connect((host, port))

message = "Hello, this is the client"
s.send(message.encode("utf-8"))
s.close()