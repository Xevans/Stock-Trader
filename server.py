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
connection = create_connection('playground/data.db')


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
  ("MSFT", "MICROSOFT", 100.43, 1),
  ("VLE", "VALVE", 20.40, 2),
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
#data is a list
#BUY
def serverBuy(data):

    get_id = ""
    this_user = 1
    stock_amount = data[2]
    pps = data[3]
    other_user = data[4]
    # data contains list of contents of client request
    # [command, symbol, stock_amount, price per stock, user id of seller]

    #if user does not exist, return a message
    if(get_id <= 0):
        return_message = "User does not exist"

    #if user already owns that stock, return a message
    
    #point cursor to exact data item [id/index 2 under stock_amount]
    select_stock_id = "SELECT user_id FROM stocks WHERE id = 1" # only checking user 1
    stocks_stock_id = execute_read_query(connection, select_stock_id)

    for s_id in stocks_stock_id:
        get_id = s_id
    
    if (get_id == 1):
        return "You already own this stock."

    # calculate cost per stock (stock amount + price per stock)
    # if user cannot afford, return message, otherwise continue
    select_user_balance = "SELECT usd_balance FROM users WHERE id = 1" # only checking user 1
    users_balance = execute_read_query(connection, select_user_balance)

    for u_balance in users_balance:
        get_balance = u_balance
    
    if (u_balance - (pps * stock_amount) < 0):
        return "Insufficient funds"
    
    # deduct calculation from user balance
    difference = (pps * stock_amount)
    new_user_balance = users_balance - difference



    #point cursor to exact data item [id/index 2 under stock_amount]
    select_user_balance = "SELECT usd_balance FROM users WHERE id = 1"


    #now to update the stock amount
    update_user_balance = """
    UPDATE
    users
    SET
    usd_balance = new_user_balance
    WHERE
    id = 1
    """

    execute_query(connection, update_user_balance)

    # read location again #Debug
    select_user_balance = "SELECT usd_balance FROM users WHERE id = 1"

    users_balance = execute_read_query(connection, select_user_balance)

    for u_balance in users_balance:
        print(u_balance) 

    # add difference to user being purchased from
    

    # update id of stock record to purchasing user's record.

    q = 1

def serverSell(data):
    q=1


# establish connections
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 5320
s.bind((host, port))
s.listen(5)
socketclient, address = s.accept()
print("Connection recieved from another terminal", address) #I.E. Client-Server Connection Successful 


#conversation loop
while (True):
    message = socketclient.recv(1024)
    message = message.decode("utf-8")
    print("Recieved: ", message)

    # determine which command
    data = message.split()
    command = data[0]

    # BUY
    if command == "BUY": 
        # calculate and update
        return_message = serverBuy(data)
        #send result
        return_message = "200 OK"
        # send OK message
    
    # SELL
    elif command == "SELL": 
        # calculate and update
        return_message = serverSell(data)
        #send result
        return_message = "200 OK"
        # send OK message

    # BALANCE
    elif command == "BALANCE":
        # Display the balance of user 1
        return_message = getBalance()
        # send balance
        return_message = "200 OK"
        # send OK message

    #LIST
    elif command == "LIST":
        #Show balance
        return_message = getList()
        # send
        return_message = "200 OK"
        # send OK message

    #SHUTDOWN
    elif command == "SHUTDOWN":
        # Shutdown
        return_message = "SHUTDOWN"
        return_message = "200 OK"
        # send OK message

        # shut down server

    #QUIT
    elif command == "QUIT":
        # End Session
        return_message = "QUIT"
        # send message
        return_message = "200 OK"
        # send OK message
        # client does shut down routine