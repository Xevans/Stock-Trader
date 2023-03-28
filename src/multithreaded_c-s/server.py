import socket
import sqlite3
from sqlite3 import Error
import threading
from threading import Thread

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
connection = create_connection('data.db')
special_cursor = connection.cursor() # for handing special requests


# users table definition 
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   first_name TEXT,
   last_name TEXT,
   user_name TEXT NOT NULL,
   password TEXT,
   root_status INTEGER,
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
   user_name TEXT,
   user_id INTEGER,
   FOREIGN KEY (user_id) REFERENCES users (id)
);
"""


# create user and stock tables (if they dont exist)
execute_query(connection, create_users_table)
execute_query(connection, create_stocks_table)


# if table is empty insert the following users
special_cursor.execute("SELECT * FROM users")
if (len(special_cursor.fetchall()) < 1):
    # define some data to add to user table
    create_user = """
    INSERT OR IGNORE INTO
    users (first_name, last_name, user_name, password, usd_balance, root_status)
    VALUES
    ("James", "Ed", "james123", "eds23", 500.00, 0),
    ("Mary", "Toodles", "Mary", "Mary01", 1000.00, 0),
    ("John","Johnson","John","John01", 50000.00, 0),
    ("Moe","Skull","Moe","Moe01", 2000.00, 0),
    ("Ben","Poorards","ben123","pokemon321", 30000.00, 0),
    ("Xavier","Devons","xavier123","rivercitygirls321", 100000.00, 0),
    ("Root", "Roots", "Root", "Root01", 30000.00, 1),
    ("Brandon","Linux","brandon123","toby321", 50000.00, 0);

    """

    # add data to user table
    execute_query(connection, create_user)  

# if table is empty insert the following users
special_cursor.execute("SELECT * FROM users")
if (len(special_cursor.fetchall()) < 1):
    # define some data to add to stock table
    create_stock = """
    INSERT OR IGNORE INTO
    stocks (stock_symbol, stock_name, stock_balance, user_name, user_id)
    VALUES
    ("MSFT", "MICROSOFT", 100.43, "james123",  1),
    ("VLE", "VALVE", 20.40, "Mary", 2),
    ("AZM", "AMAZON", 20.20, "John", 3),
    ("BK", "BURGER_KING", 200.45, "Moe", 4),
    ("RTG", "RIOT_GAMES", 50, "ben123", 5),
    ("GOOG", "GOOGLE", 32, "xavier123", 6),
    ("AAPL", "APPLE", 47, "brandon123", 8);
    """

    # add data to stock table
    execute_query(connection, create_stock)

#SQLITE3 DATABASE setup end
#****************************************************************************************

#Server.py

#globals
p_lock = threading.Lock()
shut_down_status = False
busy_count = 0

#data is a list
#BUY
def serverBuy(this_user, client_payload):

    p_lock.acquire()

    thread_connection = create_connection('data.db')
    thread_cursor = thread_connection.cursor()

    #client_payload contains: BUY SYMBOL AMOUNT PPS
    symbol = str(client_payload[1])
    stock_amount = float(client_payload[2])
    pps = float(client_payload[3])

    # user_data contains list of contents of client request
        # [command, symbol, stock_amount, price per stock, user id of seller]


    #Safe to attempt transaction. Begin transaction.

    # calculate cost per stock (stock amount + price per stock)
    # if user cannot afford, return message, otherwise continue
    thread_cursor.execute("SELECT usd_balance FROM users WHERE id = ?", (this_user,)) # fix to check current user id
    users_balance = thread_cursor.fetchall()

    for u_balance in users_balance:
        temp = u_balance

    get_balance = float(temp[0])
    
    if (get_balance - (pps * stock_amount) < 0):
        return "Insufficient funds"

    
    # user can afford transaction
    # deduct calculation from user balance
    difference = (pps * stock_amount)
    new_user_balance = round((get_balance - difference), 2)

    thread_cursor.execute("UPDATE users SET usd_balance = ? WHERE id = ?", (new_user_balance, this_user,))


    thread_cursor.execute("SELECT usd_balance FROM users WHERE id = ?", (this_user,)) # only checking user 1
    users_balance = thread_cursor.fetchall()

    for u_balance in users_balance:
        temp = u_balance

    get_balance = float(temp[0])
    

    new_stock_balance = 0.0
    # if user has no record for stock accumulated [no matching record] [does not exist for client user], add record
    thread_cursor.execute("SELECT stock_symbol FROM stocks WHERE user_id = ? AND stock_symbol = ?", (this_user, symbol,))
    exists = thread_cursor.fetchall()
    if len(exists) == 0:
        new_stock_balance = round(stock_amount, 2)

        #insert a new record
        insertion_query = """
        INSERT INTO
        stocks (stock_symbol, stock_balance, user_id)
        VALUES
        (?, ?, ?);
        """
        #no stock_name
        tuple_items = (symbol, stock_amount, this_user)
        thread_cursor.execute(insertion_query, tuple_items)

    else:
        
        #calculate additional stock
        thread_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ? AND stock_symbol = ?", (this_user, symbol,))
        current_stock_amount = thread_cursor.fetchall()

        for u_amounts in current_stock_amount:
            temp = u_amounts

        get_current_stock_amount = float(temp[0])

        new_stock_balance = round((get_current_stock_amount + stock_amount), 2)

        # add stock to existing record
        thread_cursor.execute("UPDATE stocks SET stock_balance = ? WHERE user_id = ?", (new_stock_balance, this_user,))

    thread_connection.commit() 
    thread_connection.close()

    # succeeding return message
    return_message = "BOUGHT: New balance: " + str(new_stock_balance) + " " + symbol + ". USD balance $" + str(new_user_balance)

    p_lock.release()
    return return_message






#SELL
def serverSell(this_user, client_payload):

    p_lock.acquire()

    thread_connection = create_connection('data.db')
    thread_cursor = thread_connection.cursor()

    #client_payload contains: BUY SYMBOL AMOUNT PPS
    symbol = str(client_payload[1])
    stock_amount = float(client_payload[2])
    pps = float(client_payload[3])
  
    # data contains list of contents of client request
        # [command, symbol, stock_amount, price per stock, user id of seller]
    



    # user sells a stock they do not own
    thread_cursor.execute("SELECT stock_symbol FROM stocks WHERE user_id = ? AND stock_symbol = ?", (this_user, symbol,))
    exists = thread_cursor.fetchall()

    if len(exists) == 0:
        return "You (user1) do not own this stock. \n Use LIST command to see owned stocks"



    # user does not have enough stock to sell [less than the amount requested in record]
    thread_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ? AND stock_symbol = ?", (this_user, symbol,))
    initial_stock_bal = thread_cursor.fetchall()

    for u_stock_bal in initial_stock_bal:
        temp = u_stock_bal

    get_init_stock_bal = float(temp[0])

    if ((get_init_stock_bal - stock_amount) < 0):
        return "You do not have enough stock to complete this transaction."

    # transaction sequence -----

    # add to client user's usd balance
    thread_cursor.execute("SELECT usd_balance FROM users WHERE id = ?", (this_user,))
    user_bal = thread_cursor.fetchall()

    for u_bal in user_bal:
        temp = u_bal

    get_u_bal = float(temp[0])

    new_u_bal = round((get_u_bal + (stock_amount * pps)), 2)

    thread_cursor.execute("UPDATE users SET usd_balance = ? WHERE id = ?", (new_u_bal, this_user,))

    # deduct the stock balance from client user's acount
    thread_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ? AND stock_symbol = ?", (this_user, symbol,))
    user_stock_bal = thread_cursor.fetchall()

    for u_stock_bal in user_stock_bal:
        temp = u_stock_bal

    get_u_stock_bal = float(temp[0])

    new_u_stock_bal = round((get_u_stock_bal - stock_amount), 2)

    thread_cursor.execute("UPDATE stocks SET stock_balance = ? WHERE user_id = ? AND stock_symbol = ?", (new_u_stock_bal, this_user, symbol,))


    # commit
    thread_connection.commit()
    thread_connection.close()

    # succeeding message
    return_message = "SOLD: New balance: " + str(new_u_stock_bal) + " " + symbol + ". USD $" + str(new_u_bal)

    p_lock.release()
    return return_message




# BALANCE
def getBalance(this_user):

    p_lock.acquire()

    thread_connection = create_connection('data.db')
    thread_cursor = thread_connection.cursor()

    thread_cursor.execute("SELECT first_name FROM users WHERE id = ?", (this_user,))
    fetch_first_name = thread_cursor.fetchall()

    for f_name in fetch_first_name:
        temp = f_name

    get_first_name = str(temp[0])

    thread_cursor.execute("SELECT last_name FROM users WHERE id = ?", (this_user,))
    fetch_last_name = thread_cursor.fetchall()

    for l_name in fetch_last_name:
        temp = l_name

    get_last_name = str(temp[0])

    thread_cursor.execute("SELECT usd_balance FROM users WHERE id = ?", (this_user,))
    # users_balance first element convert it to float
    users_balance = thread_cursor.fetchall()

    for u_balance in users_balance:
        temp = u_balance

    get_balance = float(temp[0])

    return_message = "Balance for user, " + get_first_name + " " + get_last_name + ": $" + str(get_balance) + "\n"

    p_lock.release()
    return return_message




#DEPOSIT
def deposit(amount, user_id):
    # retrieve balance
    # update value
    # store new balance
    # return new balance value

    p_lock.acquire()

    thread_connection = create_connection('data.db')
    thread_cursor = thread_connection.cursor()

    thread_cursor.execute("SELECT usd_balance FROM users WHERE id = ?", (user_id,))
    # users_balance first element convert it to float
    balance_record = thread_cursor.fetchall()

    for u_balance in balance_record:
        temp = u_balance

    get_balance = float(temp[0])

    new_balance = round((get_balance + amount), 2)

    thread_cursor.execute("UPDATE users SET usd_balance = ? WHERE id = ?", (new_balance, user_id,))

    #commit
    thread_connection.commit()
    thread_connection.close()

    p_lock.release()

    return new_balance

    #test print # passed
    #special_cursor.execute("SELECT usd_balance FROM users WHERE id = ?", (user_id,))
    # users_balance first element convert it to float
    #balance_record = special_cursor.fetchall()

    #for u_balance in balance_record:
    #    print(u_balance)




#need to check if root user to "use" getList()
#LIST - LIST ALL RECORDS
def getList():

    p_lock.acquire()
    thread_connection = create_connection('data.db')

    select_stocks = "SELECT id, stock_symbol, stock_balance, user_id FROM stocks"
    records = execute_read_query(thread_connection, select_stocks)
    
    return_message = ""
    for tuple in records:
        return_message += "\n"
        for item in tuple:
            print(item)#debug func
            return_message += str(item)
            return_message += " "

    thread_connection.close()

    p_lock.release()
    return(return_message)




#USERLIST - LIST ONLY USER'S RECORDS
def getUserList(user_id):

    p_lock.acquire()

    thread_connection = create_connection('data.db')
    thread_cursor = thread_connection.cursor()

    thread_cursor.execute("SELECT id, stock_symbol, stock_balance FROM stocks WHERE user_id = ?", (user_id,))
    records = thread_cursor.fetchall()
    
    return_message = ""

    for tuple in records:
        return_message += "\n"
        for item in tuple:
            #print(item)
            return_message += str(item)
            return_message += " "

    thread_connection.close()

    p_lock.release()
    return(return_message)




#WHO
def getActiveUsers():
    return_message = ""

    for name in active_user_first_names:
        for ip in active_user_ip_addresses:
            return_message += name + "  " + ip + "\n"
    return return_message 




#LOOKUP
def lookup(symbol, id):

    p_lock.acquire()

    #special_cursor.execute("SELECT stock_symbol, user_id FROM stocks WHERE stock_symbol = ? AND user_id = ?", (symbol, payload[3]))
    #results = special_cursor.fetchall()

    thread_connection = create_connection('data.db')
    thread_cursor = thread_connection.cursor()

    partial_symbol = "%" + symbol + "%"

    thread_cursor.execute("SELECT stock_symbol, user_id FROM stocks WHERE stock_symbol LIKE ?", (partial_symbol,))
    results = thread_cursor.fetchall()

    return_message = ""

    # go through all records pulled from selection
    # only return the records that contain user id of the current user
    for tuples in results:
        print(tuples)
        if tuples[1] == id:
            return_message += "\n"
            for items in tuples:
                #print(items)
                return_message += str(items) + " "

    thread_connection.close()

    p_lock.release()
    return return_message




#LOGIN
def userLogin(user_name, password):

    p_lock.acquire()

    #following two lines must exist in each server function with db operations above
    #special cursor must be replaced with thread cursor.
    thread_connection = create_connection('data.db')
    thread_cursor = thread_connection.cursor()
    
    return_data = []
    login_staus = False
    root_status = False

    # user sells a stock they do not own
    thread_cursor.execute("SELECT first_name, last_name, usd_balance, id, root_status FROM users WHERE user_name = ? AND password = ?", (user_name, password,))
    exists = thread_cursor.fetchall()

    if len(exists) == 0:
        return -1

    # extract data from tuple and return
    for tuple in exists:
        for item in tuple:
            print(item) #debug
            return_data.append(item)

    login_staus = True

    #if the user is root
    if int(return_data[4]) == 1:
        root_status = True
    
    thread_connection.close()

    p_lock.release()
    return login_staus, root_status, return_data

def updateShutdown():

    p_lock.acquire()
    global shut_down_status
    shut_down_status = True
    p_lock.release()

def checkShutdownStatus():

    p_lock.acquire()
    return shut_down_status
    p_lock.release()

def incBusyCount():
    global busy_count
    busy_count += 1

def decBusyCount():
    global busy_count
    busy_count -= 1

def getBusyCount():
    global busy_count
    return busy_count

active_user_first_names = []
active_user_ip_addresses = []


def operations(socketclient, ip):

    login_status = False 
    root_status = False
    shut_down_status = False
    debug_lock = 0
    user_data = [] # first name, last name, balance, id

    #conversation loop
    while (True): 

        message = socketclient.recv(1024)
        if not message:
            print ("No message recieved...\n")
            break
        message = message.decode("utf-8")
        print("Recieved: " + str(message))

        # check if the busy thread count is zero and shutdown status is true
            # if both these conditions are true, do not finish request. return message that server is down. then close connection

        # otherwise call function to update global counter of busy threads.
        global busy_count

        if (busy_count == 0 and shut_down_status == True):
            return_message = "Error Server shutting down"
            socketclient.send(return_message.encode("utf-8"))

            socketclient.close()

        else:
            incBusyCount()


        # need calls in each block to decrement busy count

        # determine which command
        payload = message.split()
        command = payload[0]


        if command == "LOGIN":

            user_name = payload[1]
            password = payload[2]

            if login_status == True:
                return_message = "Error: You are already logged in."
                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()
                break
            
            login_status, root_status, user_data = userLogin(user_name, password)

            try:
                login_status, root_status, user_data = userLogin(user_name, password)
            except:
                # could not log in. let client know
                return_message = "Error: User record not found or not available."
                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()
            else:
                # login successful, let client know
                active_user_first_names.append(user_data[0])
                active_user_ip_addresses.append(ip)
                return_message = "200 OK"
                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()
            
            continue
        

        #QUIT
        elif command == "QUIT":
            # End Session
            return_message = "QUIT"
            return_message += "\n200 OK"
            socketclient.send(return_message.encode("utf-8"))

            #log out user if logged in
            if login_status == True:
                login_status = False
                root_status = False
                active_user_first_names.remove(user_data[0])
                active_user_ip_addresses.remove(ip)
                user_data.clear() # not necessary since each thread has its own instance.
            
            decBusyCount()
            break
            
        if login_status == True:
            
            #LOGOUT
            if command == "LOGOUT":
                login_status = False
                root_status = False
                active_user_first_names.remove(user_data[0])
                active_user_ip_addresses.remove(ip)
                user_data.clear() # not necessary since each thread has its own instance.
                
                # send message
                return_message += "\n200 OK"
                socketclient.send(return_message.encode("utf-8"))

                decBusyCount()
            
            #WHO
            elif command == "WHO":
                if root_status == True:
                    return_message = getActiveUsers()
                    return_message += "\n200 OK"
                    socketclient.send(return_message.encode("utf-8"))
                else:
                    return_message = "Not a root user."
                    return_message += "\n200 OK"
                    socketclient.send(return_message.encode("utf-8"))

                decBusyCount()

                # call function to decrement busy thread count

                
            
            #LOOKUP
            elif command == "LOOKUP":
                symbol = payload[1] #changed from data[1] > payload[1]
                this_user_id = user_data[3]
                return_message = lookup(symbol, this_user_id)

                if (len(return_message) < 1):
                    return_message = "Error 404: Your search did not match any records."
                else:
                    return_message += "\n200 OK"

                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()
                

            # BUY
            elif command == "BUY": 
                # calculate and update
                this_user_id = user_data[3]
                return_message = serverBuy(this_user_id, payload)
                return_message += "\n200 OK"
                #send result
                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()
            
            #DEPOSIT
            elif command == "DEPOSIT":
                # call deposit
                amount = float(payload[1]) #changed from data[1] > payload[1]
                this_user_id = user_data[3]
                new_balance = deposit(amount, this_user_id)
                return_message = "New balance: " + str(new_balance)
                return_message += "\n200 OK"
                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()

            # SELL
            elif command == "SELL": 
                # calculate and update
                return_message = serverSell(user_data, payload)
                return_message += "\n200 OK"
                # send result
                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()

            # BALANCE
            elif command == "BALANCE":
                # Display the balance of user 1
                this_user_id = user_data[3]
                return_message = getBalance(this_user_id)
                # send balance
                return_message += "\n200 OK"
                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()


            #LIST
            elif command == "LIST":
                #Show list
                if root_status == True:
                    return_message = getList()
                else:
                    #return_message = getList()
                    this_user_id = user_data[3]
                    return_message = getUserList(this_user_id)
                    #call func that lists stocks owned by user

                return_message += "\n200 OK"
                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()

            #SHUTDOWN
            elif command == "SHUTDOWN":
                if root_status == True:
                    # Shutdown
                    return_message = "SHUTDOWN"
                    # sendfff
                    return_message += "\n200 OK"
                    socketclient.send(return_message.encode("utf-8"))
                   
                    # shut down server
                    # when returning to main thread. Server will shut down when it sees the status change
                    updateShutdown()

                else:
                    print("not a root user")
                    # send err message to client
                    return_message = "You don't have access to that command!"
                    socketclient.send(return_message.encode("utf-8"))

                decBusyCount()

            else:
                # not valid command
                return_message = "\nError, you input an invalid command!\n"
                socketclient.send(return_message.encode("utf-8"))
                decBusyCount()

    socketclient.close()  # leaving operations  



############ MAIN ############
# establish connections
def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = socket.gethostname()
    print("server IP address: " + str(host))
    port = 5310
    s.bind((host, port))
    s.listen(10) #10 user support 


    while True:
        print("Waiting for connection...")
        socketclient, address = s.accept()
        #p_lock.acquire()
        print("Connection recieved from another terminal") #I.E. Client-Server Connection Successful
        print("Currently connected to: ", address[0], ": ", address[1])

        thread = Thread(target = operations, args = (socketclient, address[0], ))
        thread.start()
        thread.join()
        


###Start
main()