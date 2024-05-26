from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__, static_folder='build', static_url_path='')

def get_db_connection():
    conn = sqlite3.connect('uniguide_student.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Missing username or password'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM StudentLogins WHERE Username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user['Password'], password):
        return jsonify({'status': 'success', 'message': 'Logged in successfully'})
    else:
        return jsonify({'status': 'failure', 'message': 'Invalid username or password'}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not all([first_name, last_name, email, username, password]):
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM StudentLogins WHERE Username = ?", (username,))
    if cursor.fetchone():
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 409
    cursor.execute("SELECT * FROM Students WHERE Email = ?", (email,))
    if cursor.fetchone():
        return jsonify({'status': 'error', 'message': 'Email already in use'}), 409
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO Students (StudentName, Email) VALUES (?, ?)", (f"{first_name} {last_name}", email))
    student_id = cursor.lastrowid
    cursor.execute("INSERT INTO StudentLogins (StudentID, Username, Password) VALUES (?, ?, ?)", (student_id, username, hashed_password))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Signup successful, please log in'}), 201

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
