import socket
import sqlite3
from sqlite3 import Error
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE, SIG_DFL)
#pylance does not recognize errors

#****************************************************************************************
#SQLITE3 setup


# create connection
def create_connection(path):
    connection = None
    connection = sqlite3.connect(path)
    print("Connection to SQLiteDB successful!")

    return connection




# execute query
def execute_query(connection, query):
    c = connection.cursor()

    c.execute(query)
    connection.commit()
    print("Query executed successfully!")
   




# Execute read query
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None

    cursor.execute(query)
    result = cursor.fetchall()
    return result


# call function to est. connection
connection = create_connection('data2.db')
special_cursor = connection.cursor() # for handing special requests


# users table definition 
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   first_name TEXT,
   last_name TEXT,
   user_name TEXT NOT NULL,
   password TEXT,
   usd_balance REAL NOT NULL
);
"""

# stocks table definition 
create_stocks_table = """
CREATE TABLE IF NOT EXISTS stocks (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   stock_symbol TEXT NOT NULL,
   stock_name TEXT,
   stock_amount REAL,
   stock_balance REAL,
   user_id INTEGER,
   FOREIGN KEY (user_id) REFERENCES users (id)
);
"""


# create user and stock tables (if they dont exist)
execute_query(connection, create_users_table)
execute_query(connection, create_stocks_table)


# define some data to add to user table
create_user = """
INSERT OR IGNORE INTO
  users (first_name, last_name, user_name, password, usd_balance)
VALUES
  ("James", "Ed", "james123", "eds23", 500.00);
"""

# add data to user table
execute_query(connection, create_user)  


# define some data to add to stock table
#create_stock = """
#INSERT OR IGNORE INTO
#  stocks (stock_symbol, stock_name, stock_balance, user_id)
#VALUES
#  ("MSFT", "MICROSOFT", 100.43, 1);
#"""

# add data to stock table
#execute_query(connection, create_stock)

#SQLITE3 setup end
#****************************************************************************************

#Server.py
#data is a list
#BUY
#BUY
def serverBuy(data):

    this_user = 1
    symbol = str(data[1])
    stock_amount = float(data[2])
    pps = float(data[3])
    other_user = 1
    # data contains list of contents of client request
        # [command, symbol, stock_amount, price per stock, user id of seller]


    #Safe to attempt transaction. Begin transaction.

    # calculate cost per stock (stock amount + price per stock)
    # if user cannot afford, return message, otherwise continue
    select_user_balance = "SELECT usd_balance FROM users WHERE id = 1" # only checking user 1
    users_balance = execute_read_query(connection, select_user_balance)

    for u_balance in users_balance:
        temp = u_balance

    get_balance = float(temp[0])
    
    if (get_balance - (pps * stock_amount) < 0):
        return "Insufficient funds"

    
    # user can afford transaction
    # deduct calculation from user balance
    difference = (pps * stock_amount)
    new_user_balance = get_balance - difference

    special_cursor.execute("UPDATE users SET usd_balance = ? WHERE id = 1", (new_user_balance,))


    select_user_balance = "SELECT usd_balance FROM users WHERE id = 1" # only checking user 1
    users_balance = execute_read_query(connection, select_user_balance)

    for u_balance in users_balance:
        temp = u_balance

    get_balance = float(temp[0])
    

    new_stock_balance = 0.0
    # if user has no record for stock accumulated [no matching record] [does not exist for client user], add record
    special_cursor.execute("SELECT stock_symbol FROM stocks WHERE user_id = 1 AND stock_symbol = ?", (symbol,))
    exists = special_cursor.fetchall()
    if len(exists) == 0:
        new_stock_balance = stock_amount

        #insert a new record
        insertion_query = """
        INSERT INTO
        stocks (stock_symbol, stock_balance, user_id)
        VALUES
        (?, ?, ?);
        """
        #need stock_name
        tuple_items = (symbol, stock_amount, 1)
        special_cursor.execute(insertion_query, tuple_items)

    else:
        
        #calculate additional stock
        special_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = 1 AND stock_symbol = ?", (symbol,))
        current_stock_amount = special_cursor.fetchall()

        for u_amounts in current_stock_amount:
            temp = u_amounts

        get_current_stock_amount = float(temp[0])

        new_stock_balance = get_current_stock_amount + stock_amount

        # add stock to existing record
        special_cursor.execute("UPDATE stocks SET stock_balance = ? WHERE user_id = 1", (new_stock_balance,))

    connection.commit() 

    # succeeding return message
    return_message = "BOUGHT: New balance: " + str(new_stock_balance) + " " + symbol + ". USD balance $" + str(new_user_balance)
    return return_message







def serverSell(data):

    this_user = 1
    symbol = str(data[1])
    stock_amount = float(data[2])
    pps = float(data[3])
    other_user = 1
    # data contains list of contents of client request
        # [command, symbol, stock_amount, price per stock, user id of seller]
    



    # user sells a stock they do not own
    special_cursor.execute("SELECT stock_symbol FROM stocks WHERE user_id = 1 AND stock_symbol = ?", (symbol,))
    exists = special_cursor.fetchall()

    if len(exists) == 0:
        return "You (user1) do not own this stock. \n Use LIST command to see owned stocks"



    # user does not have enough stock to sell [less than the amount requested in record]
    special_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ? AND stock_symbol = ?", (this_user, symbol,))
    initial_stock_bal = special_cursor.fetchall()

    for u_stock_bal in initial_stock_bal:
        temp = u_stock_bal

    get_init_stock_bal = float(temp[0])

    if ((get_init_stock_bal - stock_amount) < 0):
        return "You do not have enough stock to complete this transaction."




    # transaction sequence -----

    # add to client user's usd balance
    special_cursor.execute("SELECT usd_balance FROM users WHERE id = 1")
    user_bal = special_cursor.fetchall()

    for u_bal in user_bal:
        temp = u_bal

    get_u_bal = float(temp[0])

    new_u_bal = get_u_bal + (stock_amount * pps)

    special_cursor.execute("UPDATE users SET usd_balance = ? WHERE id = ?", (new_u_bal, this_user,))

    # deduct the stock balance from client user's acount
    special_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ? AND stock_symbol = ?", (this_user, symbol,))
    user_stock_bal = special_cursor.fetchall()

    for u_stock_bal in user_stock_bal:
        temp = u_stock_bal

    get_u_stock_bal = float(temp[0])

    new_u_stock_bal = get_u_stock_bal - stock_amount

    special_cursor.execute("UPDATE stocks SET stock_balance = ? WHERE user_id = ? AND stock_symbol = ?", (new_u_stock_bal, this_user, symbol,))


    # commit
    connection.commit()

    # succeeding message
    return_message = "SOLD: New balance: " + str(new_u_stock_bal) + " " + symbol + ". USD $" + str(new_u_bal)
    return return_message





def getBalance():

    special_cursor.execute("SELECT first_name FROM users WHERE id = 1")
    fetch_first_name = special_cursor.fetchall()

    for f_name in fetch_first_name:
        temp = f_name

    get_first_name = str(temp[0])

    special_cursor.execute("SELECT last_name FROM users WHERE id = 1")
    fetch_last_name = special_cursor.fetchall()

    for l_name in fetch_last_name:
        temp = l_name

    get_last_name = str(temp[0])

    select_user_balance = "SELECT usd_balance FROM users WHERE id = 1"
    # users_balance first element convert it to float
    users_balance = execute_read_query(connection, select_user_balance)

    for u_balance in users_balance:
        temp = u_balance

    get_balance = float(temp[0])

    return_message = "Balance for user, " + get_first_name + " " + get_last_name + ": $" + str(get_balance) + "\n"
    return return_message




def getList():
    select_stocks = "SELECT id, stock_symbol, stock_balance, user_id FROM stocks"
    records = execute_read_query(connection, select_stocks)
    
    return_message = ""
    for tuple in records:
        return_message += "\n"
        for item in tuple:
            #print(item)
            return_message += str(item)
            return_message += " "


    return(return_message)
















# establish connections
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 5310
s.bind((host, port))
s.listen(5)
socketclient, address = s.accept()
print("Connection recieved from another terminal", address) #I.E. Client-Server Connection Successful 

#conversation loop
while (True):
    
    

    message = socketclient.recv(1024)
    if not message:
        print ("No message recieved...\n")
        break
    message = message.decode("utf-8")
    print("Recieved: " + str(message))

    # determine which command
    data = message.split()
    command = data[0]

    # BUY
    if command == "BUY": 
        # calculate and update
        return_message = serverBuy(data)
        return_message += "\n200 OK"
        #send result
        socketclient.send(return_message.encode("utf-8"))
    
    # SELL
    elif command == "SELL": 
        # calculate and update
        return_message = serverSell(data)
        return_message += "\n200 OK"
        # send result
        socketclient.send(return_message.encode("utf-8"))

    # BALANCE
    elif command == "BALANCE":
        # Display the balance of user 1
        return_message = getBalance()
        # send balance
        return_message += "\n200 OK"
        print(return_message)
        socketclient.send(return_message.encode("utf-8"))

    #LIST
    elif command == "LIST":
        #Show balance
        return_message = getList()
        return_message += "\n200 OK"
        # send
        socketclient.sendall(return_message.encode("utf-8"))

    #SHUTDOWN
    elif command == "SHUTDOWN":
        # Shutdown
        return_message = "SHUTDOWN"
        # send
        return_message += "\n200 OK"
        socketclient.send(return_message.encode("utf-8"))
        print("Shutting down.\n")
        # shut down server
        s.shutdown(1)
        break

    #QUIT
    elif command == "QUIT":
        # End Session
        return_message = "QUIT"
        # send message
        return_message += "\n200 OK"
        socketclient.send(return_message.encode("utf-8"))
        # client does shut down routine

        #listen for another client
        socketclient, address = s.accept()
        print("\nConnection recieved from another terminal", address) #I.E. Client-Server Connection Successful 

connection.close()
s.close()