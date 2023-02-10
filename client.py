import socket

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
    stock_amount = raw_input ("How much stock to buy: ")
    price_per_stock = raw_input ("How much the stock costs to buy per stock: ")
    userID = 1

    message = ("BUY " + symbol + " " + stock_amount + " " + price_per_stock + " " + str(userID))
    return message

    
def userSell():
    symbol = raw_input ("Enter Stock Symbol: ")
    stock_amount = raw_input ("How much stock to buy: ")
    price_per_stock = raw_input ("How much the stock costs to buy per stock: ")
    userID = 1

    message = ("SELL " + symbol + " " + stock_amount + " " + price_per_stock + " " + userID)
    return message


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5320
s.connect((host, port))

while (True):

    showCommands() # show user commands

    message = raw_input ("Enter Command: ")

    if message == "1":
        # BUY
        message = userBuy()
        print("1")
    
    elif message == "2":
        # SELL
        message = userSell()
        print("2")

    elif message == "3":
        #Show balance
        message = "LIST"
        print("3")
    
    elif message == "4":
        # List stocks
        message = "BALANCE"
        print("4")

    elif message == "5":
        # Shutdown
        message = "SHUTDOWN"
        print("5")

    elif message == "6":
        # End Session
        message = "QUIT"
        print("6")


    # Wait for reply from server
    
    #reply = s.recv(1024)
    #reply = reply.decode("utf-8")
    #print(reply)








    s.send(message.encode("utf-8"))

    

s.close()