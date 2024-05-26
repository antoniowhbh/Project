from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from course_data import CourseManager  # Adjust import as necessary

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24).hex()  # Change this to a proper secret in production

DATABASE = 'uniguide_student.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/courses', methods=['GET'])
def get_courses():
    course_manager = CourseManager('course_descriptions.txt')
    courses = course_manager.get_course_names_and_titles()
    return jsonify(courses)

@app.route('/select-courses', methods=['POST'])
def select_courses():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    user_id = session['user_id']
    selected_courses = request.json.get('selected_courses', [])

    if len(selected_courses) > 30:
        return jsonify({'error': 'You cannot select more than 30 courses'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Clear existing selections if any
        cur.execute("DELETE FROM StudentCourses WHERE StudentID = ?", (user_id,))

        # Insert new selections
        for course_id in selected_courses:
            cur.execute("INSERT INTO StudentCourses (StudentID, CourseID) VALUES (?, ?)", (user_id, course_id))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'success': 'Courses successfully updated'})

if __name__ == '__main__':
    app.run(debug=True)
