import sqlite3
from sqlite3 import Error


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
  stocks (stock_symbol, stock_name, stock_amount, stock_balance, user_id)
VALUES
  ("MSFT", "MICROSOFT", 12.3, 100.43, 1),
  ("VLE", "VALVE", 14, 20.40, 2),
  ("AZM", "AMAZON", 20, 20.20, 2),
  ("BK", "BURGER_KING", 15.5, 200.45, 4),
  ("RTG", "RIOT_GAMES", 21.5, 50, 5),
  ("GOOG", "GOOGLE", 25.3, 32, 6),
  ("AAPL", "APPLE", 26.7, 47, 7);
"""

# add data to stock table
execute_query(connection, create_stock) 


# point cursor to users table
select_users = "SELECT * FROM users"
# retrieve and store in users var
users = execute_read_query(connection, select_users)

# read and print list
for user in users:
    print(user)


#print all stock records
select_stocks = "SELECT * FROM stocks"
stocks = execute_read_query(connection, select_stocks)

for stock in stocks:
    print(stock)


#REF 03
#special_cursor.execute("SELECT stock_amount FROM stocks WHERE user_id = ? AND stock_symbol = ?", (3, "AZM",))
#stocks_stock_amount = special_cursor.fetchall()

#if len(stocks_stock_amount) == 0:
#   print("Record not found")

#REF: 02 point special cursor to specific row given two rows with same user id
#special_cursor.execute("SELECT stock_amount FROM stocks WHERE user_id = ? AND stock_symbol = ?", (2, "AZM",))
#stocks_stock_amount = special_cursor.fetchall()

#REF: 01
#select_stock_amount = "SELECT stock_amount FROM stocks WHERE user_id = 7"

#stocks_stock_amount = execute_read_query(connection, select_stock_amount)

for s_amount in stocks_stock_amount:
   print("retrieved: ", s_amount) # outputs valve's current stock amount

#now to update the stock amount
update_stock_amount = """
UPDATE
   stocks
SET
   stock_amount = 16.5
WHERE
   id = 2
"""

execute_query(connection, update_stock_amount)

# read location again
select_stock_amount = "SELECT stock_amount FROM stocks WHERE id = 2"

stocks_stock_amount = execute_read_query(connection, select_stock_amount)

#for s_amount in stocks_stock_amount:
 #  print(s_amount) 
