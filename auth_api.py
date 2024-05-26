from flask import Blueprint, request, jsonify, session
from flask_cors import CORS
import sqlite3
from werkzeug.security import check_password_hash

auth_api = Blueprint('auth_api', __name__)
CORS(auth_api, supports_credentials=True)


DATABASE = 'uniguide_student.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@auth_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM StudentLogins WHERE Username = ?", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['Password'], password):
        session['logged_in'] = True  # Set session cookie
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

@auth_api.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)  # Clear session on logout
    return jsonify({'message': 'Logged out successfully'}), 200
