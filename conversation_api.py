from flask import Blueprint, request, jsonify, abort, session
import sqlite3

conversation_api = Blueprint('conversation_api', __name__)

DATABASE = 'uniguide_student.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@conversation_api.route('/conversations/<int:student_id>', methods=['GET'])
def get_conversations(student_id):
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 401

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Conversations WHERE StudentID = ?', (student_id,))
    conversations = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(conversation) for conversation in conversations])

@conversation_api.route('/conversations/delete/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 401

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Conversations WHERE ConversationID = ?', (conversation_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Conversation deleted'})

@conversation_api.route('/conversations/toggle_favorite/<int:conversation_id>', methods=['POST'])
def toggle_favorite(conversation_id):
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 401

    # Placeholder for favorite logic
    return jsonify({'status': 'success', 'message': 'Favorite toggled'})
