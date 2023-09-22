import http.server
import socketserver
import sqlite3
import urllib.parse


# HTML templates
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" href="login.css" />
    <script src="login.js"></script>
  </head>
  <body>
    <div class="background">
    <form
      onsubmit="return validation()"
      
      method="POST"
      name="loginForm"
      action="/login"
    >
      <h3>Login</h3>
      <label for="username">Username</label>
      <input type="text" placeholder="Email" id="email" name="email" />

      <label for="password">Password</label>
      <input
        type="password"
        placeholder="Password"
        id="password"
        name="password"
      />
      <button>Log In</button>
      <div class="forget">
        <a href="/signup">Don't have an account?</a>
      </div>
      </div>
    </form>
  </body>
</html>

"""

SIGNUP_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <link rel="stylesheet" type="text/css" href="signup.css">
    <script src="signup.js"></script>
</head>
<body>
    <div class="signup">
        <form onsubmit="return validation()" method="post" action="/signup">
            <h3 align="center">Sign up</h3>
            <label>First Name: *</label>
            <input type="text" name="firstname" placeholder="Your First Name" size="25" required>
            <label>Last Name: *</label>
            <input type="text" name="lastname" placeholder="Your Last Name" size="25" required>
            <label>Email: *</label>
            <input type="text" name="email" size="25" placeholder="Your Email" required>
            <label>Password: *</label>
            <input type="password" name="password" placeholder="Your Password" size="25" required>
            <div align="center">
                <input type="submit" value="Sign Up">
                <input type="reset" value="Clear" onclick="clear2();">
            </div>
        </form>
    </div>
</body>
</html>
"""

INDEX_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome to the Index Page</h1>
    <p>You are logged in!</p>
</body>
</html>
"""


# Database functions
def create_tables():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def signup(firstname, lastname, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (firstname, lastname, email, password)
            VALUES (?, ?, ?, ?)
        ''', (firstname, lastname, email, password))

        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # User with the same email already exists
        conn.close()
        return False


def login(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users WHERE email = ? AND password = ?
    ''', (email, password))

    user = cursor.fetchone()

    conn.close()
    return user


# Request handler
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the login page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(LOGIN_PAGE.encode())
        elif self.path == '/signup':
            # Serve the signup page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(SIGNUP_PAGE.encode())
        elif self.path == '/signup.css':
            # Serve the signup CSS file
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('signup.css', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/signup.js':
            # Serve the signup JavaScript file
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            with open('signup.js', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/index':
            # Serve the index page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(INDEX_PAGE.encode())
        else:
            # Serve other static files
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)

        if self.path == '/login':
            email = parsed_data['email'][0]
            password = parsed_data['password'][0]

            user = login(email, password)

            if user:
                # Redirect to index page on successful login
                self.send_response(302)
                self.send_header('Location', 'http://localhost:7112/index.html')
                self.end_headers()
            else:
                # Invalid login credentials, redirect back to login page
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
        elif self.path == '/signup':
            firstname = parsed_data['firstname'][0]
            lastname = parsed_data['lastname'][0]
            email = parsed_data['email'][0]
            password = parsed_data['password'][0]

            if signup(firstname, lastname, email, password):
                # Signup successful, redirect to login page
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                # User with the same email already exists, redirect back to signup page
                self.send_response(302)
                self.send_header('Location', '/signup')
                self.end_headers()


def main():
    create_tables()
    server = socketserver.TCPServer(('localhost', 8001), MyRequestHandler)
    print('Server running on http://localhost:8001')
    server.serve_forever()


if __name__ == '__main__':
    main()
