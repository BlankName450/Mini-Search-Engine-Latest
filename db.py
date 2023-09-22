import sqlite3

# connect to the SQLite database and create a cursor object
mydb = sqlite3.connect('wikipedia.db')
mycursor = mydb.cursor()

# create the wikipedia table
mycursor.execute("CREATE TABLE wikipedia (id INTEGER PRIMARY KEY, title TEXT, category TEXT, links TEXT, snippet TEXT, tfidf_ranking REAL)")

# commit the changes and close the database connection
mydb.commit()
mydb.close()