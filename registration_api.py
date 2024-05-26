from flask import Blueprint, request, jsonify, session
import sqlite3
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from course_data import CourseManager  # Make sure the CourseManager is correctly imported

registration_api = Blueprint('registration_api', __name__)
CORS(registration_api, supports_credentials=True)

DATABASE = 'uniguide_student.db'

def get_db_connection():
    """ Establishes a database connection. """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@registration_api.route('/signup', methods=['POST'])
def signup():
    """ Handles the user signup, including user details and course selection. """
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    major = data.get('major')
    selected_courses = data.get('courses')

    if not all([first_name, last_name, email, username, password]):
        return jsonify({'status': 'error', 'message': 'All required fields must be filled'}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check for existing username
        cur.execute("SELECT * FROM StudentLogins WHERE Username = ?", (username,))
        if cur.fetchone():
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 409

        # Insert the new student
        cur.execute("INSERT INTO Students (StudentName, Major, Email) VALUES (?, ?, ?)",
                    (f"{first_name} {last_name}", major if major else 'Undeclared', email))
        student_id = cur.lastrowid

        # Insert login details
        cur.execute("INSERT INTO StudentLogins (StudentID, Username, Password) VALUES (?, ?, ?)",
                    (student_id, username, hashed_password))

        # Insert selected courses
        for course_id in selected_courses:
            cur.execute("INSERT INTO StudentClasses (StudentID, ClassID) VALUES (?, ?)", (student_id, course_id))

        # Commit the transaction
        conn.commit()

        # Set session
        session['user_id'] = student_id
        session['username'] = username
        session['logged_in'] = True

    except sqlite3.IntegrityError as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': 'Database error: ' + str(e)}), 500
    finally:
        conn.close()

    return jsonify({'status': 'success', 'message': 'Signup successful'})