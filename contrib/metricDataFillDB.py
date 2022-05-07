from sqlite3 import dbapi2 as sqlite

# Create a connection to the database file "mydb":
con = sqlite.connect("yy.db")

# Get a Cursor object that operates in the context of Connection con:
cur = con.cursor()

fp = open("metricData.sql", "r")

# Execute the SELECT statement:
script = fp.read()
cur.executescript(script)

# Retrieve all rows as a sequence and print that sequence:
#print cur.fetchall() 

cur.close()
con.close()


