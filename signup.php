<?php
// Establish a connection to the SQLite database
$db = new SQLite3('users.db');

// Check if the form has been submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Retrieve the form data
    $firstName = $_POST['firstName'];
    $lastName = $_POST['lastName'];
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Hash the password using PHP's built-in password_hash() function
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

    // Insert the user data into the database
    $stmt = $db->prepare('INSERT INTO users (first_name, last_name, email, password) VALUES (:firstName, :lastName, :email, :password)');
    $stmt->bindValue(':firstName', $firstName, SQLITE3_TEXT);
    $stmt->bindValue(':lastName', $lastName, SQLITE3_TEXT);
    $stmt->bindValue(':email', $email, SQLITE3_TEXT);
    $stmt->bindValue(':password', $hashedPassword, SQLITE3_TEXT);
    $result = $stmt->execute();

    // Redirect the user to the login page
    header('Location: login.html');
    exit();
}
?>