import socket
import time
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE, SIG_DFL)

def showCommands():
    print(
    "Enter 1    | Buy\n" +
    "Enter 2    | Sell\n" +
    "Enter 3    | Show Balance\n" +
    "Enter 4    | List Stock Records\n" +
    "Enter 5    | Shutdown Server\n" +
    "Enter 6    | End User Session\n")

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
            stock_amount = raw_input ("How much stock to sell: ")
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
        
    while True:
        try:
            userID = raw_input ("Which user would you like to buy from: ")
            int(userID)
        except:
            print("Invalid input. Enter Number only.")
        else:
            break

    message = ("SELL " + symbol + " " + str(stock_amount) + " " + str(price_per_stock) + " " + str(userID))
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
        message = userBuy()
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")
    
    elif message == "2":
        # SELL
        message = userSell()
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "3":
        # List stocks
        message = "BALANCE"
        print(message + "\n")
        s.send(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")

    elif message == "4":
        #Show balance
        message = "LIST"
        print(message + "\n")
        s.sendall(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")


    elif message == "5":
        # Shutdown
        message = "SHUTDOWN"
        print(message + "\n")
        s.sendall(message.encode("utf-8"))
        #send(message)
        reply = s.recv(1024) #reply from server
        print("\n" + reply + "\n")
        break

    elif message == "6":
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
        showCommands()

s.close()
    
    
    
    