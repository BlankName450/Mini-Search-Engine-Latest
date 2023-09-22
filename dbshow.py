import sqlite3

# connect to the SQLite database and create a cursor object
mydb = sqlite3.connect('wikipedia.db')
mycursor = mydb.cursor()

# execute the SELECT statement to retrieve all rows from the wikipedia table
mycursor.execute("SELECT title, category, links, snippet FROM wikipedia")

# fetch all the rows and print the values of the title, category, links, and snippet columns
for row in mycursor.fetchall():
    print("Title:", row[0])
    print("Category:", row[1])
    print("Link:", row[2])
    print("Snippet:", row[3])
    print()

# close the database connection
mydb.close()