from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
CORS(app)  # This allows all domains to access your API

DATABASE = 'uniguide_student.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM StudentLogins WHERE Username = ?", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['Password'], password):
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
