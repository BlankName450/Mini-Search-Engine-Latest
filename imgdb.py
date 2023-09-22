import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('image_search.db')
cursor = conn.cursor()

# Create the images table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        url TEXT,
        tags TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
