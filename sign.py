import cgi
import sqlite3

# connect to the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# define the function to handle the signup form submission
def signup():
    form = cgi.FieldStorage()
    
    # retrieve the form data
    firstName = form.getvalue('firstName')
    lastName = form.getvalue('lastName')
    email = form.getvalue('email')
    password = form.getvalue('password')
    
    # check if the email is already registered
    cursor.execute('SELECT * FROM users WHERE email=?', (email,))
    user = cursor.fetchone()
    if user:
        return 'Email already registered.'
    
    # insert the new user into the database
    cursor.execute('INSERT INTO users (firstName, lastName, email, password) VALUES (?, ?, ?, ?)',
                   (firstName, lastName, email, password))
    conn.commit()
    
    # redirect to the login page
    print('Content-type: text/html')
    print('Location: login.html')
    print()
    return

# define the function to handle the login form submission
def login():
    form = cgi.FieldStorage()
    
    # retrieve the form data
    email = form.getvalue('email')
    password = form.getvalue('password')
    
    # check if the email and password match a user in the database
    cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
    user = cursor.fetchone()
    if user:
        # redirect to the index page
        print('Content-type: text/html')
        print('Location: index.html')
        print()
        return 'Login successful.'
    else:
        return 'Invalid email or password.'

# handle the form submission and print the result
print('Content-type: text/html')
print()

form = cgi.FieldStorage()
if 'firstName' in form:
    result = signup()
else:
    result = login()

print(result)
