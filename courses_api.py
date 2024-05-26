
from flask import Blueprint, jsonify, request
import sqlite3

courses_api = Blueprint('courses_api', __name__)

def get_db_connection():
    conn = sqlite3.connect('uniguide_student.db')
    conn.row_factory = sqlite3.Row
    return conn

@courses_api.route('/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Classes')  # Ensure the table name and database are correct
    courses = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'id': course['ClassID'], 'name': course['ClassName']} for course in courses])

@courses_api.route('/select-courses', methods=['POST'])
def select_courses():
    data = request.get_json()
    student_id = data.get('student_id')
    selected_courses = data.get('selected_courses')
    if not selected_courses:
        return jsonify({'status': 'error', 'message': 'No courses selected'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Validate student_id (optional, but recommended)
    cur.execute('SELECT * FROM Students WHERE StudentID = ?', (student_id,))
    if cur.fetchone() is None:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Invalid student ID'}), 404

    # Transaction handling for production safety
    try:
        cur.execute('DELETE FROM StudentClasses WHERE StudentID = ?', (student_id,))
        for course_id in selected_courses:
            cur.execute('INSERT INTO StudentClasses (StudentID, ClassID) VALUES (?, ?)', (student_id, course_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'status': 'success', 'message': 'Courses updated successfully'})
