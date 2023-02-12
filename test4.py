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


def getBalance():
    select_user_balance = "SELECT usd_balance FROM users WHERE id = 1"
    # users_balance first element convert it to float
    users_balance = execute_read_query(connection, select_user_balance)

    for u_balance in users_balance:
        temp = u_balance

    get_balance = float(temp[0])
    return get_balance

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

    print(return_message)
    #return(return_message)
            

def shutdown():
    s.close 

message = "LIST" # test inputs here
print(message)
# determine which command
data = message.split()

print(message)
command = data[0]

# BUY
if command == "BUY": 
    # calculate and update
    #return_message = serverBuy(data)
    #send result
    return_message = "200 OK"
    # send OK message

# SELL
elif command == "SELL": 
    # calculate and update
    #return_message = serverSell(data)
    #send result
    return_message = "200 OK"
    # send OK message

# BALANCE
elif command == "BALANCE":
    # Display the balance of user 1
    #return_message = getBalance()
    # send balance
    return_message = "200 OK"
    # send OK message

#LIST
elif command == "LIST":
    #Show balance
    print("here")
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