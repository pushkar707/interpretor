# loading in modules
import sqlite3



# creating file path
dbfile = 'db.sqlite3'
# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()

# reading all table names
table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
# Be sure to close the connection
con.close()
print(table_list)