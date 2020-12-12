import sqlite3

table = sqlite3.connect("Accounts.db")
UserID=1 #Primary key

cursor = table.cursor()

table.execute("""CREATE TABLE IF NOT EXISTS players(
UserID INT PRIMARY KEY NOT NULL,
Username NOT NULL,Email NOT NULL,
Password NOT NULL,
Level NOT NULL)""") # DDL statement to make table


def add(Username,Email,Password,save_level): # Adds new account
    global UserID
    table.execute("""INSERT or REPLACE INTO players(UserID,Username,Email,Password,Level) VALUES(?,?,?,?,?)""",(UserID,Username,Email,Password,save_level))
    UserID+=1
    table.commit()


cursor.execute("""SELECT * FROM players """)

for row in cursor.fetchall():
    UserID+=1  # Keeps track of how many accounts
    
  
