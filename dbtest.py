import sqlite3
from werkzeug.security import generate_password_hash

# Establish a database connection
connection = sqlite3.connect('uniguide_student.db')
cursor = connection.cursor()

# Function to add a fictional student
def add_student(cursor, student_name, major, email, username, password):
    # Insert the student into the Students table
    cursor.execute(
        "INSERT INTO Students (StudentName, Major, Email) VALUES (?, ?, ?)",
        (student_name, major, email)
    )
    student_id = cursor.lastrowid  # Retrieve the last inserted ID

    # Hash the password and insert it along with the username into the StudentLogins table
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    cursor.execute(
        "INSERT INTO StudentLogins (StudentID, Username, Password) VALUES (?, ?, ?)",
        (student_id, username, hashed_password)
    )

# Example of adding a student
add_student(cursor, 'Bob Smith', 'Mathematics', 'bob.smith@example.com', 'bob_smith', 'securepassword123')

# Commit the changes and close the database connection
connection.commit()
connection.close()

