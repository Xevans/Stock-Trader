import socket
import time
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE, SIG_DFL)
#root user only access 
def showCommands():
    print(
    "Enter 1    | Log in\n" +
    "Enter 2    | Log out\n" +
    "Enter 3    | Buy\n" +
    "Enter 4    | Sell\n" +
    "Enter 5    | Show Balance\n" +
    "Enter 6    | Make Deposit\n" +    
    "Enter 7    | List Stock Records\n" +
    "Enter 8    | Look up a stock record\n" +
    "Enter 9    | Active Users List*\n" +
    "Enter 10   | Shutdown Server*\n" +
    "Enter 11   | End User Session\n")

def login():
    username = raw_input ("Enter username: ")
    password = raw_input ("Enter password: ")

    message = ("LOGIN " + username + " " + password)
    return message




def userBuy():
    symbol = raw_input ("Enter Stock Symbol: ")

    while True:
        try:
            stock_amount = raw_input ("How much stock to buy: ")
            float(stock_amount)
        except:
            print("Invalid input. Enter Number only.")
        else:
            break
    
    while True:
        try:
            price_per_stock = raw_input ("How much the stock costs to buy per stock: ")
            float(price_per_stock)
        except:
            print("Invalid input. Enter Number only.")
        else:
            break
        

    message = ("BUY " + symbol + " " + str(stock_amount) + " " + str(price_per_stock))
    return message

    
def userSell():
    symbol = raw_input ("Enter Stock Symbol: ")
    
    while True:
        try:
            stock_amount = raw_input ("Enter amount of stock to sell: ")
            float(stock_amount)
        except:
            print("Invalid input. Enter Number only.")
        else:
            break
    
    while True:
        try:
            price_per_stock = raw_input ("Enter price per stock: ")
            float(price_per_stock)
        except:
            print("Invalid input. Enter Numbers only.")
        else:
            break
        

    message = ("SELL " + symbol + " " + str(stock_amount) + " " + str(price_per_stock))
    return message

def userDeposit():
    while True:
        try:
            deposit_amount = raw_input ("Enter how much you would like to deposit: ")
            float(deposit_amount)
        except:
            print("Invalid input. Enter Numbers only.")
        else:
            break

    message = ("DEPOSIT " + str(deposit_amount))
    return message


def userLookup():

    while True:
        search_query = raw_input ("Enter the stock you wish to look up: ")

        if (len(search_query) > 0):
            break
    
    message = ("LOOKUP " + str(search_query))
    return message
            







s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5310
s.connect((host, port))
#s.sendall("Hello!".encode("utf-8"))

while (True):

    showCommands() # show user commands

    message = raw_input("Enter Command: ")

    if message == "1":
        # BUY
        message = login()
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "2":
        # BUY
        message = "LOGOUT"
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "3":
        # BUY
        message = userBuy()
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")
    
    elif message == "4":
        # SELL
        message = userSell()
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "5":
        # List stocks
        message = "BALANCE"
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "6":
        # DEPOSIT
        message = userDeposit()
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "7":
        #Show balance
        message = "LIST"
        print(message + "\n")
        s.sendall(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "8":
        # LOOKUP # look up a stock 
        message = userLookup()
        print(message + "\n")
        s.sendall(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")
    
    elif message == "9":
        # WHO # show users that are logged in
        message = "WHO"
        print(message + "\n")
        s.sendall(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "10":
        # Shutdown
        message = "SHUTDOWN"
        print(message + "\n")
        s.sendall(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "11":
        # End Session
        message = "QUIT"
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")
        s.shutdown(1)
        break

    else:
        print("Invalid Input, Try Again\n")

s.close()
    
    
    
    