import socket

def showCommands():
    print("Buy - Enter 1\n",
    "Sell - Enter 2\n",
    "Show Balance - Enter 3\n",
    "List Stock Records - Enter 4\n",
    "Shutdown Server - Enter 5\n",
    "End User Session - Enter 6\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5320
s.connect((host, port))

while (True):

    showCommands()
    message = raw_input ("Enter Command: ")
    s.send(message.encode("utf-8"))

    

s.close()