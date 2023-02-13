import socket
import sqlite3
from sqlite3 import Error
#pylance does not recognize errors

#****************************************************************************************
#SQLITE3 setup


# create connection
def create_connection(path):
   connection = None

   try:
      connection = sqlite3.connect(path)
      print("Connection to SQLiteDB successful!")

   except Error as e:
      print(f"The error '{e}' occurred")

   return connection




# execute query
def execute_query(connection, query):
   c = connection.cursor()
   try:
      c.execute(query)
      connection.commit()
      print("Query executed successfully!")
   
   except Error as e:
      print(f"The error '{e}' occurred")




# Execute read query
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except Error as e:
        print(f"The error '{e}' occurred")


# call function to est. connection
connection = create_connection('test3/data.db')
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
INSERT INTO
  users (first_name, last_name, user_name, password, usd_balance)
VALUES
  ("James", "Ed", "james123", "eds23", 500.00),
  ("Todd", "Toodles", "todd123", "todge54", 1000.00),
  ("Mikey","Crown","mikey123","magic321", 50000.00),
  ("Gryffon","Skull","gryffon123","yugioh321", 2000.00),
  ("Ben","Poorards","ben123","pokemon321", 30000.00),
  ("Xavier","Devons","xavier123","rivercitygirls321", 100000.00),
  ("Brandon","Linux","brandon123","toby321", 50000.00);
"""

# add data to user table
execute_query(connection, create_user)  


# define some data to add to stock table
create_stock = """
INSERT INTO
  stocks (stock_symbol, stock_name, stock_balance, user_id)
VALUES
  ("MSFT", "MICROSOFT", 100.3, 1),
  ("VLE", "VALVE", 20.40, 1),
  ("VLE", "VALVE", 10.40, 2),
  ("AZM", "AMAZON", 20.20, 3),
  ("BK", "BURGER_KING", 200.45, 4),
  ("RTG", "RIOT_GAMES", 50, 5),
  ("GOOG", "GOOGLE", 32, 6),
  ("AAPL", "APPLE", 47, 7);
"""

# add data to stock table
execute_query(connection, create_stock)

#SQLITE3 setup end
#****************************************************************************************

#Server.py

#BUY
def serverBuy(data):

    this_user = 1
    symbol = str(data[1])
    stock_amount = float(data[2])
    pps = float(data[3])
    other_user = int(data[4])
    # data contains list of contents of client request
        # [command, symbol, stock_amount, price per stock, user id of seller]


    # get stock name of stock to be purchased
    special_cursor.execute("SELECT stock_name FROM stocks WHERE user_id = ?", (other_user,))
    o_stock_name = special_cursor.fetchall()

    for o_name in o_stock_name:
        temp = o_name

    stock_name = str(temp[0])



    # if the record the client seeks to purchase from does not exist
    special_cursor.execute("SELECT stock_symbol FROM stocks WHERE id = ? AND stock_symbol = ?", (other_user, symbol,))
    exists = special_cursor.fetchall()

    if len(exists) == 0:
        return "Record does not exist"
    


    # if the other user does not have the requested amount of stock
    special_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ? AND stock_symbol = ?", (other_user, symbol))
    other_stock_amount = special_cursor.fetchall()

    for o_amount in other_stock_amount:
        temp = o_amount

    get_o_amount = float(temp[0])
  
    if (get_o_amount - stock_amount < 0):
        return_message = ("Requested user does not have enough stock. Available stock from user ", other_user, ": ", get_o_amount)
        return return_message



    #if client (user) tries to buy stock from their user_id
    special_cursor.execute("SELECT user_id FROM stocks WHERE user_id = ? AND stock_symbol = ?", (other_user, symbol,))
    stocks_stock_id = special_cursor.fetchall()

    for s_id in stocks_stock_id:
        temp = s_id

    get_id = int(temp[0]) # convert from tuple
    #print(get_id) # debug

    if (get_id == 1):
        return "You already own this stock."


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
        stocks (stock_symbol, stock_name, stock_balance, user_id)
        VALUES
        (?, ?, ?, ?);
        """
        #need stock_name
        tuple_items = (symbol, stock_name, stock_amount, 1)
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



    # update usd_balance and stock_balance for user being purchased from.
    # update money (add)
    special_cursor.execute("SELECT usd_balance FROM users WHERE id = ?", (other_user,))
    other_balance = special_cursor.fetchall()

    for o_balance in other_balance:
        temp = o_balance

    get_balance = float(temp[0])
    #print(get_balance)

    new_other_balance = get_balance + difference

    special_cursor.execute("UPDATE users SET usd_balance = ? WHERE id = ?", (new_other_balance, other_user,))

    #update stock amount (reduce)

    special_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ?", (other_user,))
    other_balance = special_cursor.fetchall()

    for o_balance in other_balance:
        temp = o_balance

    get_balance = float(temp[0])
    #print(get_balance)

    new_other_balance = get_balance - stock_amount

    special_cursor.execute("UPDATE stocks SET stock_balance = ? WHERE user_id = ? AND stock_symbol = ?", (new_other_balance, other_user, symbol))

    # commit changes
    #connection.commit() 

    # succeeding return message
    return_message = "BOUGHT: New balance: " + str(new_stock_balance) + " " + symbol + ". USD balance $" + str(new_user_balance)
    return return_message

def serverSell(data):

    this_user = 1
    symbol = str(data[1])
    stock_amount = float(data[2])
    pps = float(data[3])
    other_user = int(data[4])
    # data contains list of contents of client request
        # [command, symbol, stock_amount, price per stock, user id of seller]
    
    # user attempts to sell with themselves
    if other_user == 1:
        return "You cannot sell to yourself."


    # user sells a stock they do not own
    special_cursor.execute("SELECT stock_symbol FROM stocks WHERE user_id = 1 AND stock_symbol = ?", (symbol,))
    exists = special_cursor.fetchall()

    if len(exists) == 0:
        return "You (user1) do not own this stock. \n Use LIST command to see owned stocks"

    # buyer (user being sold to) does not exist
    special_cursor.execute("SELECT user_name FROM users WHERE id = ?", (other_user,))
    exists = special_cursor.fetchall()

    if len(exists) == 0:
        return "The user you are selling to does not exist."


    # user does not have enough stock to sell [less than the amount requested in record]
    special_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ? AND stock_symbol = ?", (this_user, symbol,))
    initial_stock_bal = special_cursor.fetchall()

    for u_stock_bal in initial_stock_bal:
        temp = u_stock_bal

    get_init_stock_bal = float(temp[0])

    if ((get_init_stock_bal - stock_amount) < 0):
        return "You do not have enough stock to complete this transaction."


    # buyer cannot afford the stock
    special_cursor.execute("SELECT usd_balance FROM  users WHERE id = ?", (other_user,))
    initial_other_money = special_cursor.fetchall()

    for o_balance in initial_other_money:
        temp = o_balance

    get_o_balance = float(temp[0])

    difference = stock_amount * pps

    if ((get_o_balance - difference) < 0):
        return "Buyer has insufficient Funds"


    # transaction sequence -----

    # add to client user's usd balance
    special_cursor.execute("SELECT usd_balance FROM users WHERE id = 1")
    user_bal = special_cursor.fetchall()

    for u_bal in user_bal:
        temp = u_bal

    get_u_bal = float(temp[0])

    new_u_bal = get_u_bal + difference

    special_cursor.execute("UPDATE users SET usd_balance = ? WHERE id = ?", (new_u_bal, this_user,))

    # deduct the stock balance from client user's acount
    special_cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ? AND stock_symbol = ?", (this_user, symbol,))
    user_stock_bal = special_cursor.fetchall()

    for u_stock_bal in user_stock_bal:
        temp = u_stock_bal

    get_u_stock_bal = float(temp[0])

    new_u_stock_bal = get_u_stock_bal - stock_amount

    special_cursor.execute("UPDATE stocks SET stock_balance = ? WHERE id = ? AND stock_symbol = ?", (new_u_stock_bal, this_user, symbol,))

    # deduct from the buyer's usd balance

    new_o_bal = get_o_balance - difference

    special_cursor.execute("UPDATE users SET usd_balance = ? WHERE id = ?", (new_o_bal, other_user,))


    # get name of stock
    special_cursor.execute("SELECT stock_name FROM stocks WHERE stock_symbol = ? AND user_id = ?", (symbol, this_user,))
    stock_name = special_cursor.fetchall()

    for s_name in stock_name:
        temp = s_name

    get_stock_name = str(temp[0])


    # see if a record containing the stock symbol exists for the buyer
    special_cursor.execute("SELECT stock_name FROM stocks WHERE stock_symbol = ? AND user_id = ?", (symbol, other_user,))
    exists = special_cursor.fetchall()

    if len(exists) == 0:
        # if buyer has no record to accumulate stock
        #insert a new record
        insertion_query = """
        INSERT INTO
        stocks (stock_symbol, stock_name, stock_balance, user_id)
        VALUES
        (?, ?, ?, ?);
        """
        #need stock_name
        tuple_items = (symbol, get_stock_name, stock_amount, other_user)
        special_cursor.execute(insertion_query, tuple_items)

    else:
        # if buyer has existing record to accumulate stock

        # add to the buyer's stock_amount

        special_cursor.execute("SELECT stock_balance FROM stocks WHERE stock_symbol = ? AND user_id = ?", (symbol, other_user,))
        o_stock_bal = special_cursor.fetchall()

        for o_s_bal in o_stock_bal:
            temp = o_s_bal

        
        get_o_stock_bal = float(temp[0])

        new_o_stock_bal = get_o_stock_bal + stock_amount
        special_cursor.execute("UPDATE stocks SET stock_balance = ? WHERE user_id = ? AND stock_symbol = ?", (new_o_stock_bal, other_user, symbol,))    

        
    # commit

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

#conversation loop




message = "BALANCE" # test inputs here

# determine which command
data = message.split()
command = data[0]

# BUY
if command == "BUY": 
    # calculate and update
    return_message = serverBuy(data)
    print(return_message)
    #send result
    return_message = "200 OK"
    # send OK message

# SELL
elif command == "SELL": 
    # calculate and update
    return_message = serverSell(data)
    print(return_message)
    #send result
    return_message = "200 OK"
    # send OK message

# BALANCE
elif command == "BALANCE":
    # Display the balance of user 1
    # send balance
    return_message = getBalance()
    print(return_message)
    # send OK message
    return_message = "200 OK"
#LIST
elif command == "LIST":
    #Show balance
    return_message = getList()
    print(return_message)
    # send
    return_message = "200 OK"
    # send OK message

#SHUTDOWN
elif command == "SHUTDOWN":
    # Shutdown
    return_message = "SHUTDOWN"
    return_message = "200 OK"
    # send OK message
    #s.close()
    # shut down server

#QUIT
elif command == "QUIT":
    # End Session
    return_message = "QUIT"
    # send message
    return_message = "200 OK"
    # send OK message
    # client does shut down routine