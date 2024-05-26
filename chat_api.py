from flask import Blueprint, request, jsonify, session
import sqlite3
from chatbot import advisor_bot, course_scheduler
from summarizer import setup_conversation_memory, add_messages_to_history
from flask_cors import CORS

chat_api = Blueprint('chat_api', __name__)
CORS(chat_api, supports_credentials=True)

history = []
waiting_for_confirmation = {}  # Dictionary to keep track of user session states

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('uniguide_student.db')
    conn.row_factory = sqlite3.Row
    return conn

@chat_api.route('/')
def index():
    return "Chat Home"

@chat_api.route('/message', methods=['POST'])
def handle_message():
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 401

    data = request.json
    user_message = data['message'].strip().lower()
    response = process_message(user_message)
    return jsonify({'data': response})

def process_message(user_message):
    if user_message == "quit":
        history.clear()  # Clear the history since the session is ending
        return 'Chatbot session ended.'
    elif user_message == "confirm registration":
        return 'Please type "confirm" to proceed with registration, or "cancel" to cancel.'
    else:
        return advisor_bot_answer(user_message)

def advisor_bot_answer(user_message):
    response = advisor_bot.answer(user_message, history)
    full_response = "".join(
        chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""
        for chunk in response
    )
    history.append((user_message, full_response))
    return full_response

@chat_api.route('/save_conversation', methods=['POST'])
def save_conversation():
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 401

    data = request.json
    student_id = data.get('student_id')
    updated_history = add_messages_to_history(history)
    summary = setup_conversation_memory(updated_history).buffer

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Conversations (StudentID, ConversationSummary)
        VALUES (?, ?)
    """, (student_id, summary))
    conn.commit()
    conn.close()

    return jsonify({'data': 'Conversation saved successfully!'})
